
## Resolution (2026-05-09)

**Root cause:** Device-side iTunes/Media account state, not app code. Triggered by changing the Apple Music profile handle (`agomezurrea` → `alegurrea`) and display name (`Ale` → `@`). This put `accountsd` / `itunescloudd` into a state where they refused to expose the iTunes account to third-party MusicKit clients, while Music.app kept working because it has private entitlements that bypass the same gate.

**What fixed it:**
1. Settings → [Name] → Media & Purchases → Sign Out, then Sign In, **and accept the "Apple Media Services Terms" screen that appears**.
2. **Full device reboot** (power off, wait, power on). Sign-in alone did not work — `accountsd` was caching the failed state.

**Diagnostic that confirmed the diagnosis:** A one-shot launch log of `MusicSubscription.subscriptionUpdates` showed `canBecomeSubscriber = false` — that flag should never be false on a healthy device, so it proved the account daemon was unreachable from this app, not that the user lacked a subscription. After reboot it flipped to `true`.

**What did NOT help (do not retry):**
- Rolling back app code (source-playlist feature etc.) — the bug is environmental, not in commits.
- Switching wildcard ↔ explicit provisioning profile.
- Adding a `CullaMusic.entitlements` file with `com.apple.developer.musickit = true` — that key is for **macOS / MusicKit JS only**, not iOS. Adding it to an iOS project produces *"Entitlement com.apple.developer.musickit not found and could not be included in profile"* at build time. Native iOS MusicKit needs only `NSAppleMusicUsageDescription` in Info.plist (already set as `INFOPLIST_KEY_NSAppleMusicUsageDescription`).
- "+ Capability → MusicKit" in Xcode is not even an option in this account/Xcode version.

**Playbook for next time MusicKit playback breaks suddenly:**
1. Look for `ICError -7013`, `activeAccountDSID = nil`, `accounts Code=9`, "Privacy acknowledgement is needed" in logs → environmental, not code.
2. Sign out / in of Media & Purchases, accept any T&C.
3. Reboot the device.
4. Only after both above fail should you consider code-level changes.

---

## Context

CullaMusic stopped loading song artwork and stopped playing songs through `ApplicationMusicPlayer`. The user reports this worked on previous commits/yesterday. Native Apple Music can still stream normally on the same device.

Primary recurring logs:

```text
applicationQueuePlayer _establishConnectionIfNeeded timeout [ping did not pong]
activeAccountDSID = nil, activeLockerAccountDSID = nil
ICError Code=-7013 "Client is not entitled to access account store"
AMSAcknowledgePrivacyTask: Privacy acknowledgement is needed because we failed to get an account
ICMusicSubscriptionStatusRequestOperation: Aborted fetching subscription status because privacy link needs to be displayed first
```

## Important Interpretation

Do not treat the current local rollback as the desired product direction. We are removing layers only to isolate the regression. The desired feature direction still includes playlist-source sorting; this note tracks what was temporarily backed out and what did not fix the issue.

## Backshifts Already Tried

1. Apple Developer / signing investigation

- Confirmed original build had been using wildcard provisioning profile: `iOS Team Provisioning Profile: *`.
- Created/selected explicit development profile for bundle ID `agu.CullaMusic`: `CullaMusic Development`.
- Verified command-line build used `CullaMusic Development` at one point.
- Result: issue persisted.

2. Bundle ID correction

- A wrong temporary change to `agu.culla` was made during signing diagnosis because a local explicit profile existed for that old app ID.
- User clarified this is a new app and must remain `agu.CullaMusic`.
- Bundle ID was restored to `agu.CullaMusic`.

3. Apple Music account/display-name hypothesis

- User had changed Apple Music profile/display name from `Ale` to `@` around the same time.
- User changed/rechecked account state, rebooted, confirmed native Apple Music streaming works.
- Result: CullaMusic still fails.

4. Source-playlist feature rollback

The source-playlist feature commit was backed out locally from app code to remove recent MusicKit-heavy changes while testing:

- `CullaMusic/CullaMusic/Models/SwipeConfig.swift`
- `CullaMusic/CullaMusic/Services/MusicLibraryService.swift`
- `CullaMusic/CullaMusic/ViewModels/MusicSwipeViewModel.swift`
- `CullaMusic/CullaMusic/Views/HomeView.swift`

Removed layers included:

- source playlist selection UI on Home
- source transfer mode (`copy` / `move`)
- playlist-source paging through `fetchNextPlaylistSongs`
- source playlist remove/restore behavior during sort/undo
- serialized playlist mutation helper added in the feature

Result: issue persisted.

5. Signing project setting rollback

Manual signing changes and the temporary MusicKit `SystemCapabilities` marker in the Xcode project were reverted back to the repo's original automatic signing setup.

Result expected/current: still reported as failing.

## Current Local Repo State At Time Of Note

The working tree has local modifications that are diagnostic, not final product work:

- Source-playlist app code is currently backed out relative to commit `24f7cff feat: sort songs from source playlists`.
- Xcode project signing settings were restored to automatic signing.
- `CullaMusic_Development.mobileprovision` is untracked and should not be committed.

## Working Hypotheses Remaining

1. The issue may not be caused by the source-playlist feature code, because backing out those app-code changes did not fix playback/artwork.
2. The issue may be tied to Apple Media Services account/privacy state despite native Music streaming working, because logs repeatedly show account DSID resolution failure and privacy acknowledgement paths.
3. The issue may be tied to generated/local provisioning or device install state, but both wildcard and explicit profile paths have been tested and failed.
4. Need a true last-known-good commit test on the same device to distinguish repo regression from external Apple account/runtime state.

## Next Useful Diagnostic

Checkout and run the exact last-known-good commit from before `24f7cff`, without preserving current working-tree edits. Do this only after saving or stashing current diagnostic changes.

Candidate command sequence:

```bash
git stash push -u -m "diagnostic: musickit regression rollback state"
git checkout 91c5d02
xcodebuild -project CullaMusic/CullaMusic.xcodeproj -scheme CullaMusic -configuration Debug build
```

Then run on physical device from Xcode.

Expected interpretation:

- If last-known-good commit works: regression is in commits after it; bisect forward.
- If last-known-good commit fails: likely external Apple account / provisioning / device runtime state, not current app code.
