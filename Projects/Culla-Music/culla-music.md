---
title: Culla Music — Project Index
date: 2026-05-04
tags: [culla-music, ios, swiftui, musickit, active]
---

# Culla Music

Apple Music swipe-sorter. One song at a time — swipe right to add to a playlist, left to dismiss. A standalone SwiftUI app, built to eventually merge back into [[Projects/Culla/Culla|Culla]] as a feature once it reaches v1.

**Repo:** https://github.com/blhdes/culla-music (private)  
**Web:** [culla.app/music](https://culla.app/music) — landing + privacy (`#privacy`) + support (`#support`), in the `culla-web` repo. App Store submission guide → [[Areas/Xcode/app-store-submission|App Store submission]].  
**Started:** 2026-05-03 | **Status (2026-05-28):** Phase 5 shipped — a **design-language** phase: a Liquid Glass vocabulary rolled out app-wide, then a deliberate **restraint pass** back toward minimalism (scoped accent to critical surfaces, calm Settings tier, neutral cover shadows, flush artist hub). A new **artist hub** surface landed and was redesigned twice (badges → "About" bio → flush layout). → [[Phases/phase-05-liquid-glass-and-restraint|Phase 5]]. Since then a **post-Phase-5 polish** pass (2026-05-26 → 28): a richer swipe card (album + year, accent-tinted chips), a scrubbable progress bar, a per-playlist **library queue filter**, read-only / "Move out" correctness fixes, and a batch of iOS 26 Liquid Glass / mesh / live-theme fixes.

**QA:** All manual testing lives in a single tracker → [[qa-testing-tracker|QA Testing Tracker]].

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
│   ├── Playlist.swift          — @Model, mirrors Gallery. isInSidebar + isEditable
│   ├── SortedSong.swift        — @Model, FK → Playlist
│   ├── DismissedSong.swift     — @Model, persists swipe-left decisions
│   ├── SwipeConfig.swift       — value type: ReviewMode + SortOrder (+ library-artist/playlist scope)
│   └── QueueFilterStore.swift  — @AppStorage set of playlist AM IDs hidden from .library sessions
│                                  (lenient: hide a song only if ALL its playlists are filtered)
├── Services/
│   ├── MusicLibraryService.swift  — @Observable singleton. Auth, paged library fetch,
│   │                                 playlist CRUD, ID resolver, artist scoping/counts,
│   │                                 AM player + hot-clip preview, deckExclusionSet
│   ├── PlaylistTracksCache.swift   — cached per-playlist track IDs (membership chips + counts)
│   ├── CarouselSongFeed.swift      — supplies covers for the Home art carousel
│   ├── ArtistBioService.swift      — chained MusicBrainz → Wikipedia "About" lookup
│   ├── ArtistBioCache.swift        — on-disk cache for resolved bios
│   └── MusicBrainzClient.swift     — MusicBrainz id + disambiguation client
├── ViewModels/
│   ├── MusicSwipeViewModel.swift  — deck queue (batch=50, refill@10), sidebar filter, playlist
│   │                                 sync, session exclusion set; orchestrates the 4 below
│   ├── UndoCoordinator.swift      — SwipeAction + PlaylistRemovalSnapshot + actionHistory stack
│   ├── MembershipIndex.swift      — per-song membership dict + memoized resolution cache
│   ├── LovedPlaylistResolver.swift — resolve-or-create Loved flow + read-only self-heal
│   └── DismissedDateStore.swift   — dismissedDates + SwiftData helpers + 30-day resurface
├── Views/
│   ├── RootView.swift             — state machine: auth → HomeView → MusicSwipeView (hero morph)
│   ├── HomeView.swift             — entry: mode cards + sort picker + source filter + start;
│   │                                 HomeViewModel computes counts (daily @AppStorage cache)
│   ├── HomeHeroArtStack / HomeArtCarouselView / CarouselIdentityStrip.swift
│   │                                 — Home hero stack, drag-to-scrub peek carousel + labels
│   ├── MusicSwipeView.swift       — drag/snap/fly-off, sidebar reveal, Manage btn, back chevron
│   ├── SongCardView.swift         — ArtworkImage artwork + centred play/progress-ring ZStack
│   │                                 (frame-pinned), album+year, accent-tinted chips
│   ├── ProgressBarView.swift      — scrubbable progress bar with a playhead dot
│   ├── PlaylistSidebarView.swift  — neutral material panels, accent highlight on drop
│   ├── PlaylistMembershipChips.swift — "already in X" chips on the card
│   ├── ArtistDetailSheet.swift    — artist hub: photo, genres, top songs, About bio, AM/Google links
│   ├── SourceScopePickerSheet.swift — pick a source: Playlists / Artists tabs, search + sort
│   ├── ManagePlaylistsSheet.swift — Sidebar / Filter segments: sidebar toggles + queue-filter toggles
│   ├── RemoveFromPlaylistsSheet.swift — per-playlist removal + Forget dismissal
│   ├── NewPlaylistSheet.swift     — TextField → create AM playlist + local row
│   ├── SettingsView.swift         — calm utility tier: theme / accent / haptics / playback / author
│   ├── AccentPalettePickerSheet / LovedPlaylistPickerSheet.swift — Settings sub-sheets
│   ├── AuthGateView.swift         — MusicKit auth prompt + Settings deep-link fallback
│   └── EmptyStateView.swift       — "All caught up" + Refresh
└── Helpers/
    ├── GlassPanel / GlassSurface / SettingsCard.swift — glass + calm-tier card primitives
    ├── LivingMeshBackground / HomeAmbientBackground.swift — animated mesh + artwork-keyed glow
    ├── AccentEnvironment / AccentExtractor / AccentPalette / Color+Contrast.swift — dynamic accent
    ├── Transitions.swift          — hero-morph matchedGeometry plumbing
    ├── GradientCapsuleButton / HeroIconTile / LinearLoader / CullaLogo.swift — UI bits
    └── Haptics / SafariView / HTTP.swift — system glue
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
- **Phase 5** — [[Phases/phase-05-liquid-glass-and-restraint|Liquid Glass & the Restraint Pass]]. A design-language phase. Glass vocabulary rollout (`glassSurface` helper + `GlassPanel`; HomeView `7932595`, Settings/sheets `b366dda`), Home art carousel + scrub deck + hero morph (`ac61938`, `8ba54b4`), then a **restraint pass** back to minimalism — accent scoped to critical surfaces (`f60704d`), Settings quieted to a calm tier (`50513e3`), accent halos restrained to the CTA + selection borders (`901aefc`). New **artist hub** surface (`3577d6e`) with official Google/Apple Music badges, "About" bio (`74bdfe7`), and a flush redesign + always-on AM link (`3d3d507`). Brand logo wordmark (`93c0698`) + app icon (`28c1875`). 2026-05-18 → 2026-05-25. Parallel feature/perf work (source picker, artist-scoped sessions) tracked separately.
- **Post-Phase-5 polish** (2026-05-26 → 2026-05-28):
  - **Swipe card metadata** — optional album + release year on the card (`b131c1c`), long album labels wrap instead of truncating (`0210973`), playlist chips tinted with the song accent (`5fa1699`) and kept legible on dark album accents (`7d5e2c1`).
  - **Player polish** — scrubbable progress bar with a playhead dot + pause/resume position (`5fe3ae3`); progress fill no longer retracts when the preview is paused (`b1c5861`); playback settings renamed to "Auto play" / "Hot Preview" (`c38449f`).
  - **Play-button drift RESOLVED** (`d530f7c`, `92638aa`, `829eeaa`) — the centre play disc shared an *unsized* ZStack with the hot-preview ring; removing the ring on pause shrank the box and re-resolved the disc. Fix = pin the ZStack to 86×86. ~9 blind attempts failed; 3 cheap observations cracked it. → [[Dev-Insights/Swipe Play Button Drift On Pause RESOLVED 2026-05-27|drift write-up]].
  - **Per-playlist library queue filter** (`3e9d841`) — new `QueueFilterStore`; a Filter segment in `ManagePlaylistsSheet` lets the user hide a playlist's songs from `.library` swipe sessions (lenient: hidden only when *every* playlist a song belongs to is filtered).
  - **Read-only / "Move out" correctness** — recover playlists stuck read-only from the retired editability latch (`71840a4`; editability is re-derived each sync, never latched); gate "Move out" to app-created playlists, killing a false move + oversized toast (`0339162`); stop user playlists being mislabeled read-only with a zero count (`d54e551`).
  - **Misc** — solid accent fill + contrast-aware text on the selected mode tile (`4c115c2`); artist sheet collapsed into one loading state then reveal (`de8ff5a`); scoped playlist/artist source now persists across Home ⇄ Swipe (`b7ab445`).
  - **iOS 26 fixes** (2026-05-28) — Manage Playlists slab no longer renders transparent over the animated mesh (`c515bc8`, a compositor quirk → [[Dev-Insights/Liquid Glass Transparent Over Animated Mesh 2026-05-28|write-up]]); Settings sheet reacts to theme changes live (`9ee8c3b`); mesh side-middle points anchored at the screen edges (`3ce79c2`).

## Ideas

**Shipped (archived in [[Archive/Culla-Music/Ideas/|Archive/Culla-Music/Ideas]]):**
- ✅ [[Archive/Culla-Music/Ideas/settings-screen|Settings screen]] — Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/sort-from-any-playlist|Sort from any playlist]] — Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/swipe-and-player-enhancements|Swipe & player enhancements]] — all three (chips, hot-clip preview, progress bar) in Phase 3.
- ✅ [[Archive/Culla-Music/Ideas/lazy-library-count|Lazy library count on Home]] — post-Phase-3 polish, 2026-05-12.
- ✅ [[Archive/Culla-Music/Ideas/dynamic-accent-from-artwork|Dynamic accent color from artwork]] — post-Phase-3 polish, 2026-05-12. Shipped as a 2-color gradient.
- ✅ [[Archive/Culla-Music/Ideas/up-swipe-heart-loved|Up-swipe = Heart / Loved]] — post-Phase-3 polish, 2026-05-13.
- ✅ [[Archive/Culla-Music/Ideas/sort-songs-from-this-artist|Sort songs from this artist]] — shipped 2026-05-19 via `00b7e2b feat: scope swipe sessions by library artist`. Surfaced through the source picker's Artists tab rather than the artist hub.
- ✅ [[Archive/Culla-Music/Ideas/artist-bio-from-musicbrainz-wikipedia|Artist bio from MusicBrainz + Wikipedia]] — shipped 2026-05-25 via `74bdfe7`; "About" card in the artist hub (chained MusicBrainz → Wikipedia + disk cache). [[Phases/phase-05-liquid-glass-and-restraint|Phase 5]].

**Still open:**
- [[Ideas/stats-activity-view|Stats / activity view]] — local-only Charts dashboard (sorts per day, top playlists, streak).
- [[Ideas/smart-playlist-suggestion|Smart playlist suggestion chip]] — uses the membership index to hint a likely target.
- [[Ideas/onboarding-flow|First-launch onboarding]] — 3 screens, skippable, mirrors photo Culla's pattern. Eligible for a 4th screen now that up-swipe = Loved has shipped.
- [[Ideas/album-about-editorial-notes|Album "About" from Apple editorial notes]] — sibling to the shipped artist bio, but uses MusicKit `Album.editorialNotes` (no Wikipedia, no disambiguation). Needs an album surface — MVP is a "From the album X" card on the hub.
- [[Ideas/artist-count-name-fallback|Name-based fallback for missing artist counts]] — name-based catalog lookup for the small subset of artists where MusicKit's `\.artists, contains:` filter returns 0.

## Dev-Insights

Debugging write-ups kept as live reference (consult before touching the related code):

- [[Dev-Insights/Liquid Glass Transparent Over Animated Mesh 2026-05-28|iOS 26 glass over animated mesh]] — `.glassSurface` over a 30 fps `MeshGradient` can render transparent; the bug is **invisible to screenshots/ReplayKit**. Use `.thinMaterial` for large surfaces over the living mesh.
- [[Dev-Insights/Swipe Play Button Drift On Pause RESOLVED 2026-05-27|Play-button drift on pause]] — an unsized ZStack shared by the play disc + hot-preview ring; pin its frame.
- [[Dev-Insights/Smart Favorites Playlist Detection 2026-05-14|Smart Favorites detection]] — system-managed playlists silently reject remote writes; detect + roll back.
- [[Dev-Insights/MusicKit Catalog API Cert Setup 2026-05-11|MusicKit catalog API cert setup]] — the developer-token / cert path for catalog calls.
- [[Dev-Insights/CullaMusic MusicKit Playback Regression 2026-05-07|MusicKit playback regression]] — `ApplicationMusicPlayer` vs `AVPlayer` for library tracks.

*Closed work archived → [[Archive/Culla-Music/Dev-Insights/_index|Archived Dev-Insights]] (the 2026-05-20 code audit).*

## Known issues / next steps

- Playlists created via `MusicLibrary.shared.createPlaylist(...)` get stamped with `curatorName = "CullaMusic"` (Apple's third-party-app attribution policy). Sidestepped via kind-based detection, but the "CullaMusic" label still shows up in Apple Music's UI as a created-via attribution. No public way to suppress.
- `MusicLibraryRequest.offset` pagination: verify behavior on edge cases (libraries with < 100 songs, libraries > 10k).
- **Hands-on QA gap** — [[qa-testing-tracker|QA Testing Tracker]] is the live source of truth, but its last logged pass is 2026-05-22. The post-Phase-5 polish (swipe-card metadata, scrubbable bar, queue filter, iOS 26 fixes; 2026-05-24 → 28) still wants an on-device pass logged.
- `MusicLibraryService.startClipPositionObserver` concurrency warning (see memory `project_avplayer_concurrency_warnings`) — still present; small follow-up next time that file is touched.
- **Refactor backlog R1–R6** (from the now-closed [[Archive/Culla-Music/Dev-Insights/Code Audit Findings 2026-05-20|code audit]]) — non-blocking: split `SourceScopePickerSheet`, decompose `HomeView.body`, extract `ArtistLibraryService` + `MusicPreviewPlayer` from `MusicLibraryService` (935 lines), `CountCache`, `ToastCoordinator`.
- Eventually: merge into Culla as a tab or modal flow. Name collision audit done — all Culla Music types are uniquely prefixed.

---

*Original brainstorm → [[Inbox/apple-music-swipe-sorter-idea]]*
