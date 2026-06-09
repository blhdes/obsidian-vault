---
title: Culla-Music — deferred fixes for next version (post-ASC)
date: 2026-06-09
tags: [culla-music, dev-insights, swift-refine, backlog]
---

# Next-version fixes (deferred from the pre-ASC /swift-refine audit)

Surfaced during the 5-file `/swift-refine` sanity pass before the first ASC listing.
The 5 audited files all shipped (2 real bugs fixed). These 4 were deliberately
deferred. **Do #1 and #2 next version; #3 and #4 are optional gold-plating.**

## ✅ Worth doing

### 1. `.unsorted` cold-open exclusion gap
On a cold, not-yet-synced library the unsorted deck briefly surfaces songs that
already have a playlist home (because `fetchPlaylistSongIDs` returns
empty-but-successful before the library mirror syncs). Transient, self-heals on
the next fetch, no data corruption — but it's a bad first impression for a brand
new user. Fix needs a **readiness signal** (non-empty / hasSynced) before the
exclusion set is trusted, so "not ready yet" isn't treated as "no playlists."

- **File:** `Services/MusicLibraryService.swift` (`deckExclusionSet` `.unsorted` branch) + `ViewModels/MusicSwipeViewModel.swift` (`loadInitial` unsorted path)
- **Run:** `/swift-refine CullaMusic/CullaMusic/Services/MusicLibraryService.swift`

### 2. Refill `try?` early-exhaustion
A transient network blip during a background refill makes the fetch return nil,
the queue never tops up, and continued swiping latches `isEmpty = true`
permanently — looks like the library ran out when it didn't. Fix is a **bounded
retry** on the refill path.
⚠️ Cap the retry — an unbounded retry is the infinite-skeleton trap.

- **File:** `ViewModels/MusicSwipeViewModel.swift` (the `advance()` refill `Task`)
- **Run:** `/swift-refine CullaMusic/CullaMusic/ViewModels/MusicSwipeViewModel.swift`

## ⛔ Skip unless already in that code

### 3. Extract the ~320-line playback engine
`MusicLibraryService` playback section → its own `PreviewPlaybackController`.
Pure architecture, zero user-facing benefit, and **cascades into every view that
reads `service.isPlayingPreview` / `nowPlayingSongID` / `playbackPosition`**.
Only worth it next time playback is being touched anyway.

### 4. `DeckState` enum
Collapse `isLoading` / `isEmpty` / `currentSong == nil` into one enum in the VM.
Low value, also cascades into `MusicSwipeView`.

---
Related: [[Projects/Culla-Music/Culla-Music|Culla-Music]] — move this note there
(Dev-Insights) once it's actioned.
