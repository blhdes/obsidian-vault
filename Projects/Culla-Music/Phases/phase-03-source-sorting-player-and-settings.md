---
title: Phase 3 — Source Sorting, Player Polish & Settings
date: 2026-05-12
tags: [culla-music, phase, sorting, player, settings, hot-clip, chips, implemented]
status: implemented (compiles; on-device testing in progress)
---

# Phase 3 — Source Sorting, Player Polish & Settings

> **Status (2026-05-12):** All features merged on `main`. Builds clean against iOS 26 SDK. On-device validation in progress on the iPhone 17 Pro simulator and on the physical *Alejandro* device.

Phase 2 left the app with a Home screen and three review modes ([[Phases/phase-02-home-screen|Phase 2]]). Phase 3 turns it into something usable for real triage: sort *from* a specific playlist, hear the most recognizable part of a song, see where the song already lives, and customize the chrome.

Covers commits `24f7cff` (2026-05-07) → `a7d9b57` (2026-05-12).

---

## 1. Sort from any playlist (was [[Ideas/sort-from-any-playlist|idea]])

The deck can now be sourced from any editable playlist, not just the general library. When the source is a playlist, a **COPY / MOVE** segmented control appears on the Home screen.

- **COPY** (default): right-swipe only adds the song to the target playlist. The source playlist is untouched.
- **MOVE**: right-swipe adds to target *and* removes from source — useful for breaking a generic dumping-ground playlist into curated buckets.

The source picker is a pill button styled after photo Culla's `albumFilterButton` — icon + name + clear-X, glass-effect on iOS 26+, quaternary fallback below. Tapping it opens a `SourcePlaylistPickerSheet` (mirrors `ManagePlaylistsSheet`'s look — cover thumbnails, checkmark on the active source).

**Persisted as:** `SwipeConfig.sourcePlaylistID` + `sourcePlaylistName` + `sourceTransferMode`. The transfer mode is also stored in `@AppStorage("music.sourceTransferMode")` so the user's preference survives mode switches.

**Files touched:** `Models/SwipeConfig.swift`, `Services/MusicLibraryService.swift`, `Views/HomeView.swift`, `Views/SourcePlaylistPickerSheet.swift` (new), `ViewModels/MusicSwipeViewModel.swift`.

---

## 2. Settings screen (was [[Ideas/settings-screen|idea]])

A dedicated Settings sheet, presented from a gear button on `HomeView`. Single grouped `Form`, mirroring the look from photo Culla. Surfaces every preference in one place instead of scattering them across menus.

### Sections

| Section | Contents |
|---|---|
| **Appearance** | Theme (System/Light/Dark) + sidebar accent palette swatches (`AccentPalette`) |
| **Behavior** | Haptics master toggle + "Start at song highlight" (hot-clip preview, see §3) |
| **Playlist scope** | "Include read-only playlists" — drives chip scope *and* unsorted scope (see §6) |
| **Playlists** | `authorDisplayName` text field — overrides the credit Apple Music stamps on Culla-created playlists |

`@AppStorage` keys: `appColorScheme`, `appAccentPalette`, `hapticsEnabled`, `useHotPreview`, `membershipIncludeCurated`, `authorDisplayName`. `RootView` reads `appColorScheme` and applies `.preferredColorScheme`.

**Files touched:** `Helpers/AccentPalette.swift` (new), `Views/SettingsView.swift` (new), `Views/RootView.swift`, `Views/HomeView.swift`, `Views/PlaylistSidebarView.swift`, `Services/MusicLibraryService.swift` (reads `authorDisplayName` during playlist creation).

---

## 3. Hot-clip preview during swiping (was [[Ideas/swipe-and-player-enhancements|idea #2]])

Optional Settings toggle: **"Start at song highlight"**. When on, the swipe player plays Apple Music's curated ~30s preview clip via `AVPlayer` instead of streaming the full song from 0:00 via `ApplicationMusicPlayer`. Falls back to the full song when no preview asset exists for a track.

The preview is curated to be the most recognizable part of a song — better for fast triage than 10–20s of intro.

### Implementation gotchas

- **Two players, one card.** `MusicLibraryService` keeps both `ApplicationMusicPlayer.shared` (for full songs) and an `AVPlayer` instance (for hot clips). The `playPreview(for:)` entry point reads the toggle and routes accordingly. Position observers run on whichever player is active; scrub routes the same way.
- **Audio session category.** Hot clips need `AVAudioSession.setCategory(.playback)` set before `play()` or the OS sometimes routes them to the silent-switch path.
- **Library tracks have preview assets too.** Initially the hot-clip path only worked for catalog `Song` instances. Fixed in `ad92b0f` by resolving the preview URL via the catalog lookup before falling back to "no preview" — library songs proxy through their catalog match.
- **Boundary clicks.** The 30s preview is a finite AVPlayer item — the first/last frames clipped audibly. Fixed in `dc5349f` with a 0.6s `AVMutableAudioMix` volume ramp on both ends. Applied before `play()` so the very first frames ramp from 0.

**Files touched:** `Services/MusicLibraryService.swift` (heavy), `Views/SettingsView.swift`.

---

## 4. Scrubbable progress bar (was [[Ideas/swipe-and-player-enhancements|idea #3]])

A hairline progress bar at the bottom of the artwork, with tiny elapsed/-remaining labels below. Fades in only while a track is playing, cross-fades on track change so it feels like part of the artwork rather than UI chrome.

- **Scrub:** drag the bar to seek. Wider invisible hit-target than the visual line (the finger needs more than a hairline).
- **Haptic ticks** while scrubbing, gated by the existing `hapticsEnabled` setting.
- **Hidden during hot-clip preview** (`ee5953c`): scrubbing a 30s clip felt wrong — the bar would hit the end every few seconds and the user lost a sense of "did I scrub the song or the clip?" Toggle-aware: bar only appears in full-song mode. The artwork scrim also got `.clipShape(RoundedRectangle)` so it doesn't leak past the rounded corners while the bar is hidden.

**Files touched:** `Views/MusicSwipeView.swift`, `Views/SongCardView.swift`, `Services/MusicLibraryService.swift` (exposes `playbackPosition` / `playbackDuration`).

---

## 5. Playlist membership chips (was [[Ideas/swipe-and-player-enhancements|idea #1]])

Small pill chips under the artist name on the swipe card show which playlist(s) the current song already belongs to. Avoids re-sorting a song into a playlist it's already in.

- Membership index is built **once per session** from Apple Music (`fetchPlaylistMembershipIndex`) and stored on the view model as `[songID: [MusicItemID]]`.
- **Optimistically updated** on sort/undo so chips reflect the user's just-applied decision without a refetch.
- Chip count is capped on the card; overflow shows a `+N` chip.

---

## 6. Read-only playlist scope toggle

The chip-scope toggle (`membershipIncludeCurated` in `@AppStorage`) was first added for the chips in §5. Phase 3 also wired it through to the **Unsorted** mode:

- **OFF** (default): editorial / replay / personalMix / **external** playlists are ignored everywhere. Songs that live *only* in those playlists are treated as unsorted and surfaced for triage.
- **ON**: those playlists are included in chips and in the unsorted exclusion set — useful if the user actually curates from inside Apple-curated playlists.

The "external" kind (publicly shared playlists from another user / web URL) was originally treated as user-controlled. Corrected in `a7d9b57`: external playlists are read-only for the receiving user, so they now follow the same rule as editorial/replay/personalMix in all three switch sites (`MusicLibraryService.isUserControlled`, `HomeView` editability sync, `MusicSwipeViewModel` editability sync).

The home screen also now **recomputes the unsorted count instantly** when the toggle flips. Extracted `HomeViewModel.recomputeUnsortedCount()` from `loadCounts()` and wired it to an `@AppStorage` observer + `.onChange`. The cache-fingerprint includes the toggle state, so flipping reliably invalidates and shows a loader while the new count computes.

**Settings copy tightened:** label became "Include read-only playlists", footer collapsed from a paragraph to one line.

---

## 7. MusicKit reliability fixes

The cluster of fixes that kept Phase 3 actually working day-to-day:

- **`5bdb843` Library artwork via `ArtworkImage`.** iOS 19 started returning `musicKit://artwork/library/...` URLs from `Artwork.url(width:height:)` for library items instead of public `https://mzstatic.com/...` URLs. `AsyncImage` silently fails on `musicKit://`. Swapped to MusicKit's first-party `ArtworkImage` view in `SongCardView` and `ManagePlaylistsSheet`. Full incident write-up in `Dev-Insights/MusicKit Catalog API Cert Setup 2026-05-11.md`.
- **`48b6a72` Retry `addSong` after Apple Music index errors.** Apple Music's playlist index is eventually consistent — re-adding a song right after a remove sometimes fails even though the backend would accept it a moment later. Retry once after a short delay; the dedupe check catches the case where the original add actually went through.
- **`2c76460` Invalidate unsorted-count cache on sort/dismiss.** Cache fingerprint now includes the local `SortedSong` and `DismissedSong` counts. Previously the user could sort 50 songs and the home count would only refresh on the next calendar-day rollover.
- **`08adb12` Bundle ID bump to `agu.CullaMusic2`.** Side effect of the catalog-API cert diagnosis — the new ID is what's currently provisioned on test devices, so keep it for now. Also gitignored `*.mobileprovision`.

---

## New files

- `Models/SwipeConfig.swift` — added `sourcePlaylistID`, `sourcePlaylistName`, `sourceTransferMode`
- `Helpers/AccentPalette.swift` — accent palette enum
- `Views/SettingsView.swift` — the new settings sheet
- `Views/SourcePlaylistPickerSheet.swift` — source playlist picker

## Edited files

- `Services/MusicLibraryService.swift` — heaviest churn. Source-playlist song fetching, hot-clip AVPlayer + fade envelope, position observers, playlist removal, `isUserControlled` (extended to `.external`), `authorDisplayName` read, retry-on-add, `fetchPlaylistMembershipIndex`.
- `Views/HomeView.swift` — source picker pill, transfer-mode segmented control, gear button → Settings, `@AppStorage` observer for instant unsorted-count refresh, `recomputeUnsortedCount()` extracted.
- `Views/MusicSwipeView.swift` — progress bar, scrub, chip rendering, `@AppStorage` observer for chip/unsorted refresh.
- `Views/SongCardView.swift` — `ArtworkImage` swap, progress bar slot, chips.
- `Views/ManagePlaylistsSheet.swift` — `ArtworkImage` swap.
- `Views/RootView.swift` — `.preferredColorScheme` from `appColorScheme`.
- `Views/PlaylistSidebarView.swift` — reads `appAccentPalette`.
- `ViewModels/MusicSwipeViewModel.swift` — source-playlist routing, transfer-mode handling, membership index build + optimistic updates, `rebuildMembershipIndex()`, `refreshUnsortedExclusion()`, `.external` added to the editability switch.

---

## Implementation notes

- **`Playlist.Kind.external` is read-only.** The original `kind`-based editability detection (`b43edd2`, Polish pass) excluded `.editorial`, `.personalMix`, `.replay`. Phase 3 corrected this to also exclude `.external` (shared playlists from another user / public web URL — they're read-only for the receiving user). Three switch sites updated in lockstep so the scope is consistent everywhere.
- **Two players, two position observers.** `MusicLibraryService` runs separate `addPeriodicTimeObserver` blocks for `ApplicationMusicPlayer` and `AVPlayer`. The `AVPlayer` callback is `@Sendable`, so the closure body wraps in `MainActor.assumeIsolated` to satisfy strict concurrency without an actor hop. Same trick will be needed when the `MusicLibraryService.startPositionObserver` warnings (see memory: `project_avplayer_concurrency_warnings`) get fixed.
- **Membership index lifecycle.** Built on `loadInitial` and `reload`. Rebuilds when `membershipIncludeCurated` flips (the scope changes). Updated optimistically on each swipe so the chips don't lag.
- **Source-playlist song fetch.** `MusicLibraryService.fetchPlaylistSongs(id:ascending:)` resolves the playlist by ID, calls `.with([.tracks])`, then sorts by `dateAdded`. The deck excludes already-sorted and already-dismissed songs via the session exclusion set, same as Library mode.

---

## Outstanding / next steps

- On-device pass needed for: COPY/MOVE round-trip with undo, hot-clip preview on slow networks, scrubbing in both player modes, chip-toggle UX during an active swipe session.
- `MusicLibraryService.startClipPositionObserver` still has the same concurrency warning pattern as `startPositionObserver` (see memory). Worth a small follow-up pass.
- "Library" count on the Home screen still shows `—` because the library-count query is intentionally skipped (would be a 5k-song scan on first launch). Decide whether to surface it lazily or drop the slot.
- Eventually: merge into [[Projects/Culla/Culla|Culla]] as a tab/modal. Name-collision audit still clean.

---

*Phase 2 → [[Phases/phase-02-home-screen|Phase 2 — Home Screen]]*
*Source ideas → [[Ideas/sort-from-any-playlist]] · [[Ideas/settings-screen]] · [[Ideas/swipe-and-player-enhancements]]*
