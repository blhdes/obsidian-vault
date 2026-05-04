---
title: Culla Music — Project Index
date: 2026-05-04
tags: [culla-music, ios, swiftui, musickit, active]
---

# Culla Music

Apple Music swipe-sorter. One song at a time — swipe right to add to a playlist, left to dismiss. A standalone SwiftUI app, built to eventually merge back into [[Projects/Culla/Culla|Culla]] as a feature once it reaches v1.

**Repo:** https://github.com/blhdes/culla-music (private)  
**Started:** 2026-05-03 | **Status:** Phase 2 home screen implemented (2026-05-04, compiles; on-device testing pending)

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

**Editable vs read-only playlists** — `Playlist.isEditable: Bool`, written from `MusicKit.Playlist.kind == .personal` during sync. Only editable playlists can target the sidebar; read-only ones show in Manage but are disabled with a "Read-only" caption.

**Sidebar capped at 5 playlists** — `Playlist.isInSidebar: Bool` flag. User selects via a Manage button (bottom-left, fades on drag). First sync auto-selects the first 5 *editable* playlists so it's usable immediately without a Manage detour.

**Tap-to-play, not autoplay** — simpler for MVP; no audio session edge cases mid-drag.

**`ApplicationMusicPlayer` for playback** — `AVPlayer + previewAssets` silently fails for library tracks (CDN timeout). ApplicationMusicPlayer is the canonical path: full track for subscribers, 30s preview for non-subscribers, works for all library content.

**Neutral sidebar aesthetic** — dropped neon palette (works for photos, feels off for music). Material + soft accentColor highlight on active drop target only.

**Up/down swipes disabled in MVP** — reserved for favorite/share in a later version.

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
- **Phase 2** — [[Phases/phase-02-home-screen|Home screen + 3 review modes + sort order]]. Built 2026-05-04, on-device testing pending.

## Known issues / next steps

- MusicKit has no public single-song-removal-from-playlist API (iOS 17/18). Undo reverts the local `SortedSong` row but can't remove from Apple Music — surfaces a "Removed locally" toast.
- `MusicLibraryRequest.offset` pagination: verify behavior on edge cases (libraries with < 100 songs, libraries > 10k).
- Phase 2 needs hands-on testing: mode switching, dismissed-mode right-swipe (un-dismiss + sort), unsorted count cache invalidation, back chevron behaviour.
- No settings screen yet (haptics toggle, etc.).
- Eventually: merge into Culla as a tab or modal flow. Name collision audit done — all Culla Music types are uniquely prefixed.

---

*Original brainstorm → [[Inbox/apple-music-swipe-sorter-idea]]*
