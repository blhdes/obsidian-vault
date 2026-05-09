---
title: CullaMusic MusicKit Playback Regression 2026-05-07
date: 2026-05-09
tags: [culla, dev-insight, musickit, ios19, post-mortem]
---

## Resolution (2026-05-09) — actual root cause

**Root cause:** `MusicKit.Artwork.url(width:height:)` returned `musicKit://artwork/library/...` scheme URLs for library items at the time of the regression. SwiftUI's `AsyncImage` cannot resolve the `musicKit://` scheme — it silently falls into its `failure` branch and renders the placeholder. All song and playlist covers went gray even though the underlying data was intact.

**Why it suddenly broke on 2026-05-07** is *not fully known*. Git blame shows the `AsyncImage(url: song.artwork?.url(...))` code has been in `SongCardView` unchanged since the initial scaffolding (`1a112ea`, 2026-05-03). The playlist version was added in `5cffded` on 2026-05-05. Between "working on 2026-05-06" and "broken on 2026-05-07", only `24f7cff` (source-playlist sorting) landed and it doesn't touch artwork or playback setup. The trigger was therefore *external*, most likely:

1. An iOS point-release update applied automatically overnight that changed `Artwork.url()` to return `musicKit://` for library items.
2. A change in *which* songs the user was swiping — catalog-matched library songs return `https://` URLs while iCloud-Music-Library-only uploads may always have returned `musicKit://`. The pre-2026-05-07 sessions may have happened to land on catalog-matched songs.
3. An Apple backend change in the URL scheme returned by their library API.

Either way, `AsyncImage` was *never* going to work for `musicKit://` URLs — earlier conditions just happened to return HTTPS. The `ArtworkImage` switch is the right permanent fix regardless of which external trigger flipped it.

The *playback* failure that appeared simultaneously was a separate, intermittent daemon flakiness in `applicationQueuePlayer`'s XPC channel. It cleared on its own after the device-side cycles we did during diagnosis and has been stable since. No code change was needed for it.

**The fix (one line per artwork view):**

```swift
// Before
if let url = song.artwork?.url(width: 600, height: 600) {
    AsyncImage(url: url) { phase in ... }
}

// After
if let artwork = song.artwork {
    ArtworkImage(artwork, width: size, height: size)
}
```

`ArtworkImage` is MusicKit's first-party view (iOS 16+). It knows how to authenticate and load `musicKit://` scheme URLs via the framework's internal loader.

Commit: `5bdb843 fix: render library artwork via MusicKit ArtworkImage`.

## How we missed it (anti-playbook)

The console was flooded with very loud, very official-looking errors that looked like authentication / entitlement / account problems:

```
ICError Code=-7013 "Client is not entitled to access account store"
activeAccountDSID = nil, activeLockerAccountDSID = nil
applicationQueuePlayer _establishConnectionIfNeeded timeout [ping did not pong]
ACAccountStore: Failed to fetch the iTunes accounts. error = ... Code=9
AMSAcknowledgePrivacyTask: Privacy acknowledgement is needed
```

We chased these for hours: re-signed the app, re-issued provisioning profiles, toggled the MusicKit App Service flag in the Apple Developer portal, signed out and back into Media & Purchases (with T&C accept), full device reboots, even renamed the bundle ID to `agu.CullaMusic2` to escape what we thought was poisoned per-app `accountsd` state. Every time the device dance temporarily "fixed" things, we declared victory; every fresh install brought the same symptoms back, reinforcing the wrong hypothesis.

The actual bug — `musicKit://` in the artwork URL — was visible the second we printed `song.artwork?.url(...).absoluteString`. AsyncImage failures don't log to the console; they just render the fallback. So the silent failure of the real bug let the loud-but-unrelated daemon errors run the investigation.

## Playbook for next time MusicKit covers/playback breaks

In this exact order. **Do not skip steps 1–2 to chase 3.**

1. **Print `song.artwork?.url(width: X, height: Y)?.absoluteString` for one song.** If it's `musicKit://...`, the issue is the rendering view — switch any `AsyncImage`-based artwork rendering to MusicKit's `ArtworkImage(artwork, width:, height:)`. Five-minute fix.
2. **Print `MusicAuthorization.currentStatus` and one snapshot of `MusicSubscription.subscriptionUpdates`.** If `canPlayCatalogContent = true` after auth, the framework-level account state is fine; stop chasing entitlements and account daemons.
3. Only if both above are clean and playback still fails, *then* look at device-side state (Settings → Apple Account → Media & Purchases sign-out/in, accept any T&C, full device reboot). And even then expect this to be transient daemon flakiness, not your problem to "solve" — just clear it.
4. Things that are wrong turns and we should stop suggesting:
   - Adding `com.apple.developer.musickit` to an iOS `.entitlements` file (it's a macOS / MusicKit JS key — fails to build on iOS).
   - Looking for "MusicKit" under Xcode's "+ Capability" picker (not listed there for this account/Xcode version).
   - Regenerating the provisioning profile to "include MusicKit entitlements" — native iOS MusicKit doesn't use a per-profile entitlement, the four-key minimal profile is correct.
   - Bisecting commits when the root cause is an OS-level API behavior change between iOS versions.

## Diagnosis pattern worth keeping

When a feature visibly fails but the console errors don't quite line up with it, *instrument the visible symptom directly* before chasing the loud logs. A `print` next to the gray placeholder revealed the truth in 30 seconds; without it we had nothing to disprove the daemon-state hypothesis with.

## Original incident notes (preserved for reference)

The sections below are what we wrote *during* the incident, before we knew the real cause. Kept here so the wrong-turn reasoning is visible — useful to recognize the same pattern next time.

### Context (as observed at the time)

CullaMusic stopped loading song artwork and stopped playing songs through `ApplicationMusicPlayer`. Worked on previous commits/yesterday. Native Apple Music can still stream normally on the same device.

Recurring system errors:

```text
applicationQueuePlayer _establishConnectionIfNeeded timeout [ping did not pong]
activeAccountDSID = nil, activeLockerAccountDSID = nil
ICError Code=-7013 "Client is not entitled to access account store"
AMSAcknowledgePrivacyTask: Privacy acknowledgement is needed because we failed to get an account
ICMusicSubscriptionStatusRequestOperation: Aborted fetching subscription status because privacy link needs to be displayed first
```

### Things tried that did not fix it

1. Apple Developer / signing investigation — switched between wildcard and explicit `CullaMusic Development` profiles. Issue persisted on both.
2. Bundle ID corrections — accidentally changed to `agu.culla` then back to `agu.CullaMusic`, then later renamed to `agu.CullaMusic2` to escape "poisoned" per-app state. None of these were the bug.
3. Apple Music account/display-name hypothesis — user changed display name from `Ale` to `@` and handle from `agomezurrea` → `alegurrea` around the same time. We thought this triggered the regression but it was coincidence.
4. Source-playlist feature rollback — backed out `24f7cff` locally to test whether the new feature code caused the regression. It did not.
5. Signing project setting rollback — reverted manual signing changes and the temporary MusicKit `SystemCapabilities` marker. No effect.
6. Device-side dance — sign out / in Media & Purchases with T&C accept, full device reboot. Temporarily appeared to work but didn't survive the next reinstall (because it was never the real fix).
7. Adding a `.entitlements` file with `com.apple.developer.musickit = true` — failed to build with *"Entitlement com.apple.developer.musickit not found and could not be included in profile"*. That key is macOS / MusicKit JS only.
8. Regenerating the `CullaMusic Development` provisioning profile after re-saving the App Service flag — new profile had the same minimal four entitlements as the old one (because native iOS MusicKit doesn't use a profile entitlement at all).
