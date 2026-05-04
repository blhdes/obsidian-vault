---
title: Phase 2 — Home Screen
date: 2026-05-04
tags: [culla-music, phase, ux, design, home-screen, implemented]
status: implemented (compiles; on-device testing pending)
---

# Phase 2 — Home Screen

> **Status (2026-05-04):** Built and compiling cleanly. Behavioural testing on device still pending — verify mode switching, the dismissed-deck un-dismiss-on-right-swipe, and the unsorted count cache.

## Why

The app currently skips straight from auth into the swipe deck — no choice, no context. This phase adds a calm entry point where the user picks *what* to sort and *in which order*, mirroring the role `DatePickerView` plays in [[Projects/Culla/Culla|Culla]].

---

## Three review modes

| Mode | What it shows | Exclusion logic |
|---|---|---|
| **Library** | Full library, unseen by the app | Excludes `SortedSong` + `DismissedSong` records |
| **Unsorted** | Songs not in any *personal* playlist | Excludes editable-playlist members + `SortedSong` |
| **Dismissed** | The rejected stack | Loads from `DismissedSong`, resolves via MusicKit |

> **Library ≠ Unsorted.** Library = "Culla Music hasn't touched this". Unsorted = "not in any user-owned playlist". A song already in a playlist but never seen by our app appears in Library but NOT in Unsorted.

### Dismissed mode swipe behaviour change
- Right swipe → adds to playlist **+ deletes the `DismissedSong` record** (un-dismisses)
- Left swipe → re-dismisses (refreshes `dismissedAt` timestamp)

---

## Shared sort order

A single "Order" 2-segment control — **Newest first / Oldest first** — sits below the mode cards and applies to whichever mode is selected. Persisted via `@AppStorage`.

---

## Editable vs non-editable playlists

Users often have playlists they saved but don't own (Apple editorial, algorithmic mixes, friends' shares). `MusicKit.Playlist.kind` distinguishes them:

- `.personal` → user-created, **editable** ✅
- `.editorial`, `.personalMix`, `.external` → **read-only** ❌

**Impact:**
- **Unsorted mode** only excludes songs in `.personal` playlists. Songs only in editorial/algorithmic playlists count as unsorted (user never actively filed them).
- **Sidebar** only allows `.personal` playlists as targets. Read-only playlists appear in Manage but are disabled with a "Read-only" label.
- **`Playlist` model** gains `isEditable: Bool = true`, written from `kind == .personal` during sync.

---

## Screen layout

```
[App wordmark — small, top]

[ ◉  Library          2,847 ]   ← async count
[ ○  Unsorted            —  ]   ← bg fetch, shows — until ready; cached daily
[ ○  Dismissed          142 ]   ← cheap SwiftData count

─────────────────────────────
Order   [Newest first] [Oldest]

[      Start Cullaing  →     ]
```

No tab bar. Navigation is a state-machine swap: `HomeView ↔ MusicSwipeView` (same pattern as Culla's `DatePickerView ↔ SwipeView`).

---

## Count performance (5k library)

| Mode | Time | Strategy |
|---|---|---|
| Library | ~100ms | One MusicKit count query |
| Unsorted | 2–4s | Cross-ref editable playlists only; cache daily in `@AppStorage` |
| Dismissed | <5ms | SwiftData `fetchCount` |

---

## New files

- `Models/SwipeConfig.swift` — `SwipeConfig`, `ReviewMode`, `SortOrder`
- `Views/HomeView.swift` + `HomeViewModel`

## Edited files

- `Models/Playlist.swift` — add `isEditable: Bool`
- `Views/RootView.swift` — `activeConfig: SwipeConfig?` state machine
- `Views/ManagePlaylistsSheet.swift` — disable non-editable rows
- `ViewModels/MusicSwipeViewModel.swift` — accept `SwipeConfig`, route by mode
- `Services/MusicLibraryService.swift` — `ascending` param, `fetchEditablePlaylistSongIDs()`, `resolveSongs(ids:)`

---

## Implementation notes (deviations from plan)

A few small adjustments were needed to get the build green:

- **`@MainActor` moved off the class** in `MusicSwipeViewModel`. Combining `@Observable` and `@MainActor` at class level produced a macro/isolation conflict; the annotation now sits on the `init` instead. Behaviour is the same (all mutation happens on the main actor) but the macro is happy.
- **No default value for `config`** in the view model's init. A nonisolated default expression evaluating `SwipeConfig()` clashed with the main-actor init; callers always pass one explicitly now.
- **`MusicKit.Playlist.kind` comparison via string interpolation.** `kind == .personal` wouldn't resolve directly because of (a) the local `Playlist` model's name colliding with `MusicKit.Playlist`, and (b) SDK-version variation on the static member. Using `playlist.kind.map { "\($0)" } == "personal"` sidesteps both.
- **Explicit type annotation on `playlist.with([.tracks])`** — `let populated: MusicKit.Playlist = …` — for the same name-collision reason, so the compiler resolves `.tracks` as `PartialMusicAsyncProperty<MusicKit.Playlist>`.
- **`sortedFromDismissed` undo case added.** Right-swiping in dismissed mode does two things (delete the `DismissedSong`, insert a `SortedSong`); undo had to mirror both, restoring the original `dismissedAt` timestamp so chronological order in dismissed mode survives undo.
- **Back button in `MusicSwipeView`.** An optional `onBack: (() -> Void)?` overlay (top-leading chevron, blurred material disc) so the user can return from the deck to the Home screen. Fades with the rest of the chrome on drag.
- **Session exclusion set.** `MusicSwipeViewModel` now keeps a `sessionExclusionSet` that grows as songs are acted on, instead of re-querying SwiftData on every refill. Cheaper and avoids races between the background refill and the latest swipe.

---

*Implementation plan → `/Users/agomezu/.claude/plans/let-s-start-working-on-optimized-orbit.md`*
