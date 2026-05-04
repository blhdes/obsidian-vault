---
title: Culla Music — Project Index
date: 2026-05-04
tags: [culla-music, ios, swiftui, musickit, active]
---

# Culla Music

Apple Music swipe-sorter. One song at a time — swipe right to add to a playlist, left to dismiss. A standalone SwiftUI app, built to eventually merge back into [[Projects/Culla/Culla|Culla]] as a feature once it reaches v1.

**Repo:** https://github.com/blhdes/culla-music (private)  
**Started:** 2026-05-03 | **Status:** MVP built and running on device

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
│   ├── Playlist.swift         — @Model, mirrors Gallery. Has isInSidebar: Bool
│   ├── SortedSong.swift       — @Model, FK → Playlist
│   └── DismissedSong.swift    — @Model, persists swipe-left decisions
├── Services/
│   └── MusicLibraryService.swift  — @Observable singleton. Auth, paged library
│                                     fetch, playlist CRUD, ApplicationMusicPlayer
├── ViewModels/
│   └── MusicSwipeViewModel.swift  — deck queue (batch=50, refill@10), undo history,
│                                     sidebar filter, playlist sync
└── Views/
    ├── RootView.swift             — state machine: loading → needsAuth → ready
    ├── MusicSwipeView.swift       — drag/snap/fly-off, sidebar reveal, Manage btn
    ├── SongCardView.swift         — AsyncImage artwork + play button overlay
    ├── PlaylistSidebarView.swift  — neutral material panels, accent highlight on drop
    ├── ManagePlaylistsSheet.swift — sidebar toggle per playlist + artwork covers
    ├── NewPlaylistSheet.swift     — TextField → create AM playlist + local row
    ├── AuthGateView.swift         — MusicKit auth prompt + Settings deep-link fallback
    └── EmptyStateView.swift       — "All caught up" + Refresh
```

---

## Key decisions

**"Unsorted" = not yet acted on in our app** — not "not in any Apple Music playlist". Cheaper (SwiftData query only), mirrors Culla's exclusion pattern, and avoids the complex cross-playlist membership check.

**Sidebar capped at 5 playlists** — `Playlist.isInSidebar: Bool` flag. User selects via a Manage button (bottom-left, fades on drag). First sync auto-selects first 5 so it's usable immediately without a Manage detour.

**Tap-to-play, not autoplay** — simpler for MVP; no audio session edge cases mid-drag.

**`ApplicationMusicPlayer` for playback** — `AVPlayer + previewAssets` silently fails for library tracks (CDN timeout). ApplicationMusicPlayer is the canonical path: full track for subscribers, 30s preview for non-subscribers, works for all library content.

**Neutral sidebar aesthetic** — dropped neon palette (works for photos, feels off for music). Material + soft accentColor highlight on active drop target only.

**No date/calendar entry point** — opens straight to the swipe deck. Keeps it minimalist.

**Up/down swipes disabled in MVP** — reserved for favorite/share in a later version.

---

## MVP scope

- Auth → fetch library songs (paged, most-recently-added first)
- Swipe right → drop on sidebar playlist → adds song to AM playlist (async)
- Swipe left → dismiss (persisted, never reappears)
- Tap card → play/pause via ApplicationMusicPlayer
- Manage button → sheet with sidebar toggles + artwork covers + "+ New playlist"
- Undo (up to full history, auto-fades after 2.5s)
- Empty state with Refresh

## Out of scope

Up/down gestures, autoplay, favorites, share, stats, paywall, duplicate scanning, calendar entry, multi-platform (Spotify/YouTube), iPad/macOS layouts.

---

## Known issues / next steps

- MusicKit has no public single-song-removal-from-playlist API (iOS 17/18). Undo reverts the local `SortedSong` row but can't remove from Apple Music — surfaces a "Removed locally" toast.
- `MusicLibraryRequest.offset` pagination: verify behavior on edge cases (libraries with < 100 songs, libraries > 10k).
- No settings screen yet (haptics toggle, etc.).
- Eventually: merge into Culla as a tab or modal flow. Name collision audit done — all Culla Music types are uniquely prefixed.

---

*Original brainstorm → [[Inbox/apple-music-swipe-sorter-idea]]*
