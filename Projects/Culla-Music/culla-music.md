---
title: Culla Music — Project Index
date: 2026-05-04
tags: [culla-music, ios, swiftui, musickit, active]
---

# Culla Music

Apple Music swipe-sorter. One song at a time — swipe right to add to a playlist, left to dismiss. A standalone SwiftUI app, built to eventually merge back into [[Projects/Culla/Culla|Culla]] as a feature once it reaches v1.

**Repo:** https://github.com/blhdes/culla-music (private)  
**Started:** 2026-05-03 | **Status (2026-05-14):** Phase 3 + polish pass shipped. Latest: up-swipe = Loved (auto-created *Culla Loves* + Settings picker + rollback on remote-write failure), dynamic accent gradient sampled from artwork, lazy library count on Home, long-press to fully reveal sidebar, hairline `LinearLoader`. On-device validation ongoing.

---

## Architecture

Mirrors [[Projects/Culla/Culla|Culla]] 1:1 — same `@Observable` + SwiftData stack, no TCA or MVVM overhead. Intentional: the eventual merge is a folder graft, not a rewrite.

| Culla | Culla Music |
|---|---|
| `Gallery` | `Playlist` |
| `SortedPhoto` | `SortedSong` |
| `DismissedPhoto` | `DismissedSong` |
| `PhotoLibraryService` | `MusicLibraryService` |
| `SwipeView` | `MusicSwipeView` |
| `GallerySidebarView` | `PlaylistSidebarView` |

**Stack:** SwiftUI + SwiftData + MusicKit + ApplicationMusicPlayer. iOS 17+ minimum.

---

## File structure

```
CullaMusic/
├── CullaMusicApp.swift
├── Models/
│   ├── Playlist.swift         — @Model, mirrors Gallery. isInSidebar + isEditable
│   ├── SortedSong.swift       — @Model, FK → Playlist
│   ├── DismissedSong.swift    — @Model, persists swipe-left decisions
│   └── SwipeConfig.swift      — value type: ReviewMode + SortOrder, drives a session
├── Services/
│   └── MusicLibraryService.swift  — @Observable singleton. Auth, paged library
│                                     fetch (asc/desc), playlist CRUD, ID resolver,
│                                     editable-playlist song IDs, AM player
├── ViewModels/
│   └── MusicSwipeViewModel.swift  — deck queue (batch=50, refill@10), undo history,
│                                     sidebar filter, playlist sync, session-scoped
│                                     exclusion set, mode-specific load/dismiss/assign
└── Views/
    ├── RootView.swift             — state machine: auth → HomeView → MusicSwipeView
    ├── HomeView.swift             — entry point: 3 mode cards + sort picker + start.
    │                                 HomeViewModel computes counts (cached daily for
    │                                 unsorted via @AppStorage)
    ├── MusicSwipeView.swift       — drag/snap/fly-off, sidebar reveal, Manage btn,
    │                                 optional back chevron to return to Home
    ├── SongCardView.swift         — AsyncImage artwork + play button overlay
    ├── PlaylistSidebarView.swift  — neutral material panels, accent highlight on drop
    ├── ManagePlaylistsSheet.swift — sidebar toggle per playlist + artwork covers,
    │                                 read-only rows disabled with caption
    ├── NewPlaylistSheet.swift     — TextField → create AM playlist + local row
    ├── AuthGateView.swift         — MusicKit auth prompt + Settings deep-link fallback
    └── EmptyStateView.swift       — "All caught up" + Refresh
```

---

## Key decisions

**Three review modes, picked from a Home screen** ([[Phases/phase-02-home-screen|Phase 2]]). Library / Unsorted / Dismissed. The Home screen replaces the old "auth → straight into deck" flow and mirrors Culla's `DatePickerView`.

**"Unsorted" = not in any user-owned playlist** — refined in Phase 2. Songs that live only in Apple editorial mixes, algorithmic playlists, or playlists shared by others still count as unsorted, since the user never actively filed them. Earlier definition ("not yet acted on in our app") was simpler but ignored playlists Apple Music already gave the user — too many obvious "you literally put this here" songs.

**Editable vs read-only playlists** — `Playlist.isEditable: Bool`, written from `MusicKit.Playlist.kind` during sync (editorial / personalMix / replay → read-only; everything else → editable). The earlier `curatorName == nil` heuristic was abandoned because Apple stamps the creating app's bundle name into `curatorName` for third-party-created playlists, which incorrectly downgraded Culla-made playlists to read-only on relaunch. Sync also preserves `isEditable=true` once set, so any wrongly-downgraded record auto-repairs on next sync.

**Sidebar cap raised to 13 playlists** (was 5 in MVP) — `Playlist.isInSidebar: Bool` flag. User selects via a Manage button (bottom-left, fades on drag). First sync auto-selects the first N *editable* playlists so it's usable immediately without a Manage detour.

**Tap-to-play, not autoplay** — simpler for MVP; no audio session edge cases mid-drag.

**`ApplicationMusicPlayer` for playback** — `AVPlayer + previewAssets` silently fails for library tracks (CDN timeout). ApplicationMusicPlayer is the canonical path: full track for subscribers, 30s preview for non-subscribers, works for all library content.

**Neutral sidebar aesthetic** — dropped neon palette (works for photos, feels off for music). Material + soft accentColor highlight on active drop target only.

**Up-swipe = Loved (down still reserved)** — up-swipe now files the current song into a configurable *Loved* playlist (default: auto-created "Culla Loves"). Down-swipe stays unbound for a future "Share" action.

**Session-scoped exclusion set** — `MusicSwipeViewModel.sessionExclusionSet` grows as songs are acted on. Cheaper than re-querying SwiftData on every refill and avoids races between background refills and the latest swipe.

---

## MVP scope

- Auth → Home screen → pick mode (Library / Unsorted / Dismissed) + order → deck
- Swipe right → drop on sidebar playlist → adds song to AM playlist (async)
- Swipe left → dismiss (persisted, never reappears) — except in Dismissed mode, where left = skip
- In Dismissed mode, swipe right also un-dismisses (deletes the `DismissedSong`)
- Tap card → play/pause via ApplicationMusicPlayer
- Manage button → sheet with sidebar toggles + artwork covers + "+ New playlist", read-only playlists disabled
- Undo (up to full history, auto-fades after 2.5s) — restores `dismissedAt` for the dismissed→sorted case
- Empty state with Refresh
- Back chevron from deck returns to Home

## Out of scope

Up/down gestures, autoplay, favorites, share, stats, paywall, duplicate scanning, multi-platform (Spotify/YouTube), iPad/macOS layouts.

---

## Phases

- **Phase 1** — MVP scaffolding (auth, deck, sidebar, manage, undo). Done 2026-05-03.
- **Phase 2** — [[Phases/phase-02-home-screen|Home screen + 3 review modes + sort order]]. Built 2026-05-04.
- **Polish pass** — Soft card transitions, real Apple Music playlist removal on undo (via `MusicLibrary.edit(_:items:)` filter+replace), wider sidebar (50% → 80%) with playlist artwork covers, deadzoned + opacity-gated sidebar reveal, kind-based editability detection, sidebar cap 5 → 13. 2026-05-06.
- **Phase 3** — [[Phases/phase-03-source-sorting-player-and-settings|Source sorting + player polish + settings]]. Sort from any playlist (COPY/MOVE), settings sheet (theme/accent/haptics/author), hot-clip preview, scrubbable progress bar, playlist membership chips, read-only scope toggle, MusicKit reliability fixes. 2026-05-07 → 2026-05-12.

## Ideas

**Implemented:**
- ✅ [[Ideas/settings-screen|Settings screen]] — Phase 3.
- ✅ [[Ideas/sort-from-any-playlist|Sort from any playlist]] — Phase 3.
- ✅ [[Ideas/swipe-and-player-enhancements|Swipe & player enhancements]] — all three (chips, hot-clip preview, progress bar) in Phase 3.

**Open (2026-05-12 batch):**
- [[Ideas/up-swipe-heart-loved|Up-swipe = Heart / Loved]] — uses the reserved vertical gesture from MVP.
- [[Ideas/dynamic-accent-from-artwork|Dynamic accent color from artwork]] — extract dominant color per song; mirrors photo Culla.
- [[Ideas/stats-activity-view|Stats / activity view]] — local-only Charts dashboard (sorts per day, top playlists, streak).
- [[Ideas/smart-playlist-suggestion|Smart playlist suggestion chip]] — uses the membership index to hint a likely target.
- [[Ideas/onboarding-flow|First-launch onboarding]] — 3 screens, skippable, mirrors photo Culla's pattern.
- [[Ideas/lazy-library-count|Lazy library count on Home]] — fills the `—` slot from Phase 3's outstanding list.

## Known issues / next steps

- Playlists created via `MusicLibrary.shared.createPlaylist(...)` get stamped with `curatorName = "CullaMusic"` (Apple's third-party-app attribution policy). Sidestepped via kind-based detection, but the "CullaMusic" label still shows up in Apple Music's UI as a created-via attribution. No public way to suppress.
- `MusicLibraryRequest.offset` pagination: verify behavior on edge cases (libraries with < 100 songs, libraries > 10k).
- Phase 2 still needs hands-on coverage: mode switching, dismissed-mode right-swipe (un-dismiss + sort), unsorted count cache invalidation, back chevron behaviour.
- No settings screen yet (see [[Ideas/settings-screen|idea]]).
- Eventually: merge into Culla as a tab or modal flow. Name collision audit done — all Culla Music types are uniquely prefixed.

---

*Original brainstorm → [[Inbox/apple-music-swipe-sorter-idea]]*
