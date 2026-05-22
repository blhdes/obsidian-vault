---
title: Culla Music — Project Index
date: 2026-05-04
tags: [culla-music, ios, swiftui, musickit, active]
---

# Culla Music

Apple Music swipe-sorter. One song at a time — swipe right to add to a playlist, left to dismiss. A standalone SwiftUI app, built to eventually merge back into [[Projects/Culla/Culla|Culla]] as a feature once it reaches v1.

**Repo:** https://github.com/blhdes/culla-music (private)  
**Started:** 2026-05-03 | **Status (2026-05-16):** Phase 4 shipped — Dismissed-mode tooling (stale-dismissal resurfacing, age chip, long-press cleanup menu with per-playlist removal sheet + Forget dismissal + inline-snackbar undo). Followed by a four-step VM split that shrunk `MusicSwipeViewModel` from 1218 → 940 LOC (-23%) with no behavior change. On-device validation ongoing — see [[qa-dismissed-cleanup-menu|QA — Dismissed-mode cleanup menu]].

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
│   ├── MusicSwipeViewModel.swift  — deck queue (batch=50, refill@10), sidebar filter,
│   │                                 playlist sync, session-scoped exclusion set,
│   │                                 mode-specific load/dismiss/assign. Orchestrates
│   │                                 the four coordinators below.
│   ├── UndoCoordinator.swift      — owns SwipeAction, PlaylistRemovalSnapshot, and the
│   │                                 actionHistory stack (record/popLast/remove/clear).
│   ├── MembershipIndex.swift      — per-song membership dict + memoized playlist-
│   │                                 resolution cache (reset/invalidateCache/add/
│   │                                 remove/memberships/rebuild).
│   ├── LovedPlaylistResolver.swift — @MainActor coordinator: eventual-consistency
│   │                                 resolve-or-create flow, session-created tracker,
│   │                                 read-only self-heal, upsert helper.
│   └── DismissedDateStore.swift   — @Observable store of dismissedDates + SwiftData
│                                     fetch helpers (loadAll/recentSongIDs/record(for:))
│                                     + the 30-day resurface constant.
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
- **Post-Phase-3 polish** (2026-05-12 → 2026-05-13):
  - Lazy library count on Home (`476b806`) — folded into the existing unsorted walk; separate cache fingerprints. Loader spinner replaced with a hairline `LinearLoader` (`08b9d78`).
  - Long-press to fully reveal the playlist sidebar (`12a5a49`).
  - Dynamic accent gradient sampled from song artwork (`2210913`) — primary + hue-distant secondary, HSL-clamped, cross-faded into the sidebar glow + a faint panel wash.
  - Up-swipe = Loved (`128e9d5`) — vertical-dominant up-drag adds the song to a *Loved* playlist; auto-creates "Culla Loves" on first use. Pink heart overlay mirrors the trash overlay; Loved chip gets a ♥ glyph.
  - Settings picker for the Loved target (`be56d03`) — `LovedPlaylistPickerSheet` with an "Auto (Culla Loves)" reset row; storage keyed by Apple Music playlist ID.
  - Rollback on remote-write failure (`1c45fd6`) — system-managed playlists like Apple Music's *Smart Favorites* silently reject `MusicLibrary.shared.add()`; the new `rollbackLoved` helper undoes the local exclusion + membership entries so songs don't vanish from the deck.
  - "Smart Favorites" hidden + Sort From opened to read-only sources (`bbca8a8`).
- **Phase 4** — [[Phases/phase-04-dismissed-mode-tooling|Dismissed Mode Tooling]]. Resurface stale dismissals in Unsorted (`2414cda`), rework Dismissed gestures + dismissed-age chip (`d48a75f`), long-press cleanup menu (`9a3d607`), per-playlist removal sheet + Forget dismissal + inline-snackbar undo (`fb9d6f1`). 2026-05-14 → 2026-05-15.
- **Post-Phase-4 cleanup** (2026-05-16) — `MusicSwipeViewModel` split into four `@Observable` / `@MainActor` coordinators, 1218 → 940 LOC (-23%), no behavior change. Order: UndoCoordinator (`83936d9`, owns `SwipeAction` + `PlaylistRemovalSnapshot` + action stack), MembershipIndex (`f3c326d`, per-song dict + memoized playlist cache; `playlistsProvider` wired post-init), LovedPlaylistResolver (`c4b888f`, resolve-or-create + read-only self-heal; shrinks the `loveCurrent` catch from 18 → 7 lines), DismissedDateStore (`d47ba64`, dismissedDates map + 3 SwiftData helpers + 30-day resurface constant). Also: silenced `[hotpreview]` flow-trace prints (`4b849c8`) — catch-block error prints kept.

## Ideas

**Shipped (archived in [[Archive/Culla-Music/Ideas/|Archive/Culla-Music/Ideas]]):**
- ✅ [[Archive/Culla-Music/Ideas/settings-screen|Settings screen]] — Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/sort-from-any-playlist|Sort from any playlist]] — Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/swipe-and-player-enhancements|Swipe & player enhancements]] — all three (chips, hot-clip preview, progress bar) in Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/lazy-library-count|Lazy library count on Home]] — post-Phase-3 polish, 2026-05-12.
- ✅ [[Archive/Culla-Music/Ideas/dynamic-accent-from-artwork|Dynamic accent color from artwork]] — post-Phase-3 polish, 2026-05-12. Shipped as a 2-color gradient.
- ✅ [[Archive/Culla-Music/Ideas/up-swipe-heart-loved|Up-swipe = Heart / Loved]] — post-Phase-3 polish, 2026-05-13.
- ✅ [[Archive/Culla-Music/Ideas/sort-songs-from-this-artist|Sort songs from this artist]] — shipped 2026-05-19 via `00b7e2b feat: scope swipe sessions by library artist`. Surfaced through the source picker's Artists tab rather than the artist hub.

**Still open:**
- [[Ideas/stats-activity-view|Stats / activity view]] — local-only Charts dashboard (sorts per day, top playlists, streak).
- [[Ideas/smart-playlist-suggestion|Smart playlist suggestion chip]] — uses the membership index to hint a likely target.
- [[Ideas/onboarding-flow|First-launch onboarding]] — 3 screens, skippable, mirrors photo Culla's pattern. Eligible for a 4th screen now that up-swipe = Loved has shipped.
- [[Ideas/artist-bio-from-musicbrainz-wikipedia|Artist bio from MusicBrainz + Wikipedia]] — adds an "About" section to the artist hub via chained MusicBrainz → Wikipedia lookups, with on-disk caching.
- [[Ideas/artist-count-name-fallback|Name-based fallback for missing artist counts]] — name-based catalog lookup for the small subset of artists where MusicKit's `\.artists, contains:` filter returns 0.

## Known issues / next steps

- Playlists created via `MusicLibrary.shared.createPlaylist(...)` get stamped with `curatorName = "CullaMusic"` (Apple's third-party-app attribution policy). Sidestepped via kind-based detection, but the "CullaMusic" label still shows up in Apple Music's UI as a created-via attribution. No public way to suppress.
- `MusicLibraryRequest.offset` pagination: verify behavior on edge cases (libraries with < 100 songs, libraries > 10k).
- Phase 2 still needs hands-on coverage: mode switching, dismissed-mode right-swipe (un-dismiss + sort), unsorted count cache invalidation, back chevron behaviour.
- `MusicLibraryService.startClipPositionObserver` concurrency warning (see memory `project_avplayer_concurrency_warnings`) — small follow-up next time that file is touched.
- Eventually: merge into Culla as a tab or modal flow. Name collision audit done — all Culla Music types are uniquely prefixed.

---

*Original brainstorm → [[Inbox/apple-music-swipe-sorter-idea]]*
