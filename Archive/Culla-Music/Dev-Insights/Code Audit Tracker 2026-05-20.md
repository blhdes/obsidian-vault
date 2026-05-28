---
title: Code Audit Tracker — post-VM-extraction window
date: 2026-05-20
tags: [culla-music, audit, tracker]
---

# Code Audit Tracker — 2026-05-20

Tracker for the in-progress code audit covering everything merged **after the ViewModel coordinator-extraction refactor** finished on 2026-05-16. Acts as the source of truth so the audit survives across chat sessions.

## Audit window

- **Baseline commit:** `c95c341` — *refactor: tighten actor isolation in persistence caches* (2026-05-18, last of the refactor block)
- **Head at audit start:** `e21b801` — *fix: show full vinyl in dark and tinted app icons* (2026-05-20)
- **Range:** `c95c341..HEAD`
- **Volume:** ~28 commits, 24 files, +1960 / −188 lines.

Why this baseline: the four VM extractions (`UndoCoordinator`, `MembershipIndex`, `LovedPlaylistResolver`, `DismissedDateStore`) plus the actor-isolation pass were the last "architectural" moment. Everything since is feature + polish work that has not been independently reviewed.

## Themes (commits grouped)

### 1. Artist hub (new surface)
- `3577d6e` feat: artist hub sheet from the swipe card
- `15500a1` feat: play/pause top songs in artist hub and add Apple Music link
- `719105b` feat: official "Listen on Apple Music" badge
- `6d34ef2` feat: brand the Google CTA with the official "G" mark

### 2. Source picker overhaul
- `1815392`(pre-window context) → replaced by `SourceScopePickerSheet`
- `cd1d597` feat: polish source-playlist picker UX
- `b7f9086` feat: source-playlist deck shows the full collection
- `514edb2` feat: track counts for artist rows in source picker
- `042c7e0` feat: search and sort for the source picker
- `5972cda` fix: paginate library artists and drop misleading zero counts
- `737ed70` refactor: collapse source-picker sort UI into an inline chip
- `00b7e2b` feat: scope swipe sessions by library artist
- `53993d6` feat: initials fallback for artists without catalog artwork
- `d775bb9` feat: show track count next to each playlist row

### 3. App icon
- `28c1875` feat: add app icon with light, dark, and tinted variants
- `e21b801` fix: show full vinyl in dark and tinted app icons

### 4. Hero morph + home flow
- `8ba54b4` feat: hero morph transition from Home to Swipe deck
- `35f3d68` feat: warm membership snapshot on Home so source counts work on first launch
- `d1f8a71` fix: tighten Home count flows — source-aware, race-safe, flicker-free
- `43c72d0` fix: correct unsorted exclusion and dismissed loading state

### 5. Visual polish on swipe surfaces
- `4c83085` feat: tint monochrome artwork instead of dropping to palette
- `9583912` perf: cache playlist memberships so chips render instantly
- `b951e18` style: soften Manage button so it recedes into the chrome
- `ac233f8` fix: dynamic sidebar accent broken on library songs (musicKit:// URLs)
- `a393565` refactor: drop color wash from swipe overlays, keep only the icon
- `ee714d1` fix: home UX, dismissed-menu lift cropping, portrait lock, stale playlists
- `bf40cc2` fix: surface freshly-loved songs when sorting from their playlist

### 6. Docs / chore
- `cee5eb5` docs: README — list PlaylistTracksCache and real Helpers files
- `7e15320` docs: note why dismissed-menu lift can't shrink to just the cover
- `05559e8` chore: track shared Xcode scheme, ignore Claude Code local state

## File surfaces touched

| File | Change |
| --- | --- |
| `Views/SourceScopePickerSheet.swift` | **+655 (new file)** — replaces `SourcePlaylistPickerSheet` |
| `Views/SourcePlaylistPickerSheet.swift` | **−105 (deleted)** |
| `Views/ArtistDetailSheet.swift` | **+409 (new)** — artist hub UI |
| `Views/HomeView.swift` | +226 — counts, warming, hero source, initials |
| `Services/MusicLibraryService.swift` | +228 — artist scoping, pagination, counts |
| `ViewModels/MembershipIndex.swift` | +104 — warm snapshot, count surfaces |
| `Views/SongCardView.swift` | +46 — artist hub entry, hero morph anchor |
| `Models/SwipeConfig.swift` | +38 — library-artist scope |
| `Helpers/Transitions.swift` | **+39 (new)** — hero morph plumbing |
| `ViewModels/MusicSwipeViewModel.swift` | +48 — full-collection source-playlist deck, artist scope |
| `Views/RootView.swift` | +32 — hero transition wiring |
| `Helpers/SafariView.swift` | **+17 (new)** — embedded Safari for artist links |
| `Views/MusicSwipeView.swift` | +17 — hero morph + artist hub sheet |
| `Views/ManagePlaylistsSheet.swift` | +9 — track counts |
| `Assets.xcassets/AppIcon.appiconset/*` | new — 3 PNG variants + Contents.json |
| `Assets.xcassets/apple-music-badge.imageset/*` | new — badge SVG |
| `Assets.xcassets/google-g.imageset/*` | new — Google G SVG |
| `design/app-icon.svg` | new — design source |
| `README.md` | +7 — Helpers + cache docs |

## What the audit needs to look for

- **`SourceScopePickerSheet` (+655 in one shot)** — by far the largest single-file delta. Likely candidate for sub-component extraction; needs concurrency / cancellation review for the search/sort/pagination work.
- **`ArtistDetailSheet` (+409)** — new external-network surface (Apple Music link, Safari, Google CTA). Audit for: link safety, fallbacks when artist not found, playback ownership conflicts with the swipe deck.
- **`HomeView` (+226)** — count flows touched by 4 separate commits including race fixes. Verify the race-safe path actually holds, no leftover stale-flicker conditions.
- **`MusicLibraryService` (+228)** — pagination + artist scope additions. Check actor isolation matches the post-`c95c341` model and that count queries don't trigger N+1.
- **`MembershipIndex` warming** — confirm the warm snapshot doesn't fight the actor-isolated cache from the baseline refactor.
- **Hero morph transition** — `matchedGeometryEffect` ownership across `Home → Root → Swipe → SongCard`. Risk: namespace mismatch, lingering layers on cancel.
- **App icon assets** — verify the iOS 19 icon manifest still references all three variants after the dark/tinted vinyl fix.

## Status — CLOSED ✅

Audit complete (2026-05-20), **archived 2026-05-28**. All severity-tagged findings resolved; see [[Code Audit Findings 2026-05-20]] for the per-finding fixes (B1–B4, M1–M7, P1–P3 across 11 commits, P4 audited-and-skipped). Refactors R1–R6 were logged as a non-blocking backlog and are **not** part of this closed audit.

- [x] Window defined
- [x] Themes grouped
- [x] File surfaces enumerated
- [x] Tracker saved to vault
- [x] Audit pass on `SourceScopePickerSheet` → P1, R1
- [x] Audit pass on `ArtistDetailSheet` → M6
- [x] Audit pass on `HomeView` count flows → B2, M2, P2
- [x] Audit pass on `MusicLibraryService` pagination + scope → B1, M1, M5, M7, P4
- [x] Audit pass on hero morph transition → covered in QA tracker, no code finding
- [x] Findings rolled up into [[Code Audit Findings 2026-05-20]]

## Related

- [[Projects/Culla-Music/culla-music|Culla Music project index]]
- [[Projects/Culla-Music/Phases/phase-03-source-sorting-player-and-settings|Phase 03 — source sorting]]
- [[Projects/Culla-Music/Phases/phase-04-dismissed-mode-tooling|Phase 04 — dismissed-mode tooling]]
- [[Projects/Culla-Music/Phases/phase-app-icon-design|Phase — app icon design]]
