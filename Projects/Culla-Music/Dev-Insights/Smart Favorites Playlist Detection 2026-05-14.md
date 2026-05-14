---
title: Detecting Apple Music's smart Favorites playlist
date: 2026-05-14
tags: [culla-music, dev-insight, musickit, playlist, detection, read-only, up-swipe]
---

# Detecting Apple Music's smart Favorites playlist

How Culla Music decides whether a playlist accepts `MusicLibrary.shared.add(...)`. Driven by a real user bug: the Spanish *Canciones favoritas* system playlist kept showing up in the Loved-target picker and silently failing every write.

Centralized in `MusicLibraryService.swift` as the top-level helper `computeEditability(for: amPlaylist) -> Bool`. Both syncs (`HomeView.syncPlaylistsFromAppleMusic` and `MusicSwipeViewModel.syncPlaylistsFromAppleMusic`) call it; the up-swipe Loved path falls back to a third layer when both miss.

## The three layers

### 1. `Playlist.Kind` — Apple's own read-only tag

MusicKit's `Playlist.kind` enum covers the obvious cases:

```swift
case .editorial, .external, .personalMix, .replay:
    return false  // Apple-managed, programmatic writes will fail
```

- `.editorial` — Apple-curated playlists.
- `.external` — playlists shared by another user / via a public web URL. Read-only for the *receiving* user.
- `.personalMix` — algorithmic mixes ("New Music Mix", "Chill Mix", etc).
- `.replay` — yearly Replay playlists.

**What this layer misses:** the smart Favorites playlist returns `kind = nil`. Its metadata is indistinguishable from a user-made playlist — same `curatorName = nil`, same `kind`, same write API shape. No native fingerprint exists.

### 2. Localized name set — best-effort heuristic

A hardcoded `Set<String>` of names Apple uses for the Favorites playlist across locales:

```swift
let smartFavoritesNames: Set<String> = [
    "Favorite Songs",      // en
    "Favorites",           // en (alt / older)
    "Favourites",          // en-GB
    "Canciones favoritas", // es
    "Favoritos",           // es (alt / iOS 18+)
    "Morceaux favoris",    // fr
    "Lieblingstitel",      // de
    // ... ~16 entries total, see source
]
```

`computeEditability` returns `false` when the playlist's name appears in this set.

**Why this works:** the system playlist's name is stable per locale.

**Why it's fragile:** depends on us knowing every locale variant Apple ships, and Apple can rename it (iOS 18 added new variants like *Favoritos* / *Favoris*). Add new entries as users in unsupported locales report failures.

### 3. Self-heal on write failure — the safety net

If both layers miss and the user up-swipes a song with the bad playlist as their Loved target, `MusicLibrary.shared.add(...)` throws. The `catch` block in `MusicSwipeViewModel.loveCurrent`:

```swift
} catch {
    rollbackLoved(...)                                 // un-do the optimistic local write
    playlist.isEditable = false                        // mark read-only locally
    if playlist.isInSidebar { playlist.isInSidebar = false }
    try? modelContext.save()
    if defaults.string(forKey: lovedPlaylistDefaultsKey) == amIDString {
        defaults.removeObject(forKey: lovedPlaylistDefaultsKey)  // clear stale Loved target
    }
    playlists = fetchLocalPlaylists()                  // republish so UI updates
    toastMessage = "Couldn't add to \(displayName)"
}
```

The user sees one toast, then the playlist is gone from the picker, sidebar, and Loved-target storage forever.

### Sticky-downgrade glues the three layers together

Before this work, both syncs were *overwriting* `existing.isEditable` with the freshly-computed value on every run. A playlist marked read-only by layer 3 would be re-upgraded to editable on the next Home appearance if layer 2's name list didn't catch it. The fix:

```swift
// In both syncs:
existing.isEditable = existing.isEditable && computeEditability(for: amPlaylist)
```

`A && B` means: sync can downgrade an editable playlist to read-only when the heuristic now says so, but **never re-upgrades a read-only one**. Once any layer flags a playlist read-only, it sticks.

## Why HomeView had its own (broken) sync

Historical artifact: `HomeView.HomeViewModel.syncPlaylistsFromAppleMusic` predated `MusicSwipeViewModel.syncPlaylistsFromAppleMusic` and had only the `Playlist.Kind` switch — no name filter. Every Home appearance ran it, re-upgrading the smart Favorites back to `isEditable = true` and undoing whatever the swipe view's sync had decided. The dedupe / consolidation (single `computeEditability` helper) was as important as the new detection layers.

A natural follow-up: collapse the two syncs entirely. They share enough logic that one of them should call into the other (probably HomeView's `HomeViewModel` calling `MusicSwipeViewModel`'s, since the latter has the richer downgrade-transition logic that clears `lovedPlaylistID`).

## One more safety net: `resolveOrCreateLovedPlaylist`

Before the write would even be attempted, the stored Loved target is now re-validated:

```swift
if let stored = defaults.string(forKey: lovedPlaylistDefaultsKey),
   !stored.isEmpty,
   let match = playlists.first(where: { $0.appleMusicPlaylistID == stored }),
   match.isEditable {            // <-- the new guard
    return match
}
// fall through to auto-create "Culla Loves"
```

If sync has since flagged the stored target read-only, this falls through to auto-creating *Culla Loves* instead of repeating the failed write. The user doesn't even taste a single failure if they happen to open the app after a sync that downgraded their target.

## Trade-offs (the design tension)

- **Layers 1 and 2** are pre-emptive — no failed write, no user-visible toast. But fragile: they only catch what we've encoded.
- **Layer 3** is robust — it learns from reality and can't be wrong, because the failure *is* the signal. But the user sees one failure before the system heals.
- **Sticky-downgrade** is the multiplier — it makes each of the above permanent. Without it, layers 1/2 are restored every sync and layer 3 lasts a single session.

## Files touched (commit `f69e51c`)

- `Services/MusicLibraryService.swift` — top-level `computeEditability(for:)` + `smartFavoritesNames`.
- `ViewModels/MusicSwipeViewModel.swift` — sync uses helper + sticky-downgrade; `loveCurrent` self-heals on write failure; `resolveOrCreateLovedPlaylist` requires `isEditable`.
- `Views/HomeView.swift` — sync uses the same helper + sticky-downgrade.

## Lessons

- **Centralize behavior-bearing constants.** Two sync sites holding their own copies of "what's read-only?" is a bug waiting to happen — and it was. The `private let` constant should have been file-internal or module-internal from the start, with a single caller.
- **Heuristic + observed failure beats heuristic alone.** If the system has a way to tell you it can't do the thing, listen to it and persist the answer.
- **Sticky state across syncs.** Anytime sync is computing a flag that other code paths *also* write to, default to OR-only / AND-only updates so the two paths don't fight.

## Related

- [[culla-music]] — project index, Post-Phase-3 polish entry.
- [[Ideas/up-swipe-heart-loved]] — the feature this work was hardening.
- Commits: `1c45fd6` (initial rollback on remote write fails), `bbca8a8` (hide smart Favorites + open Sort From to read-only sources), `f69e51c` (this work).
