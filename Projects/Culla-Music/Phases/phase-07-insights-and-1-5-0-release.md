---
title: Phase 7 — Insights, Swipe Refinements & the 1.5.0 Release
date: 2026-09-14
tags: [culla-music, phase, insights, charts, history, app-store, implemented]
status: implemented (1.5.0/build 2 prepared for App Store submission; on-device QA not re-verified since Phase 6)
---

# Phase 7 — Insights, Swipe Refinements & the 1.5.0 Release

> **Status (2026-09-14):** Merged on `main`. 36 commits, `5f5bb03` (2026-06-17) → `809fd54` (2026-09-14) — though the real work stops at `cda1020` (2026-07-27); the last commit is a lone `Localizable.xcstrings` reformat with no functional change, and the repo has been dormant since. This note is filling the gap the project index left undocumented since Phase 6 (2026-06-15).

This audit note was written retroactively (2026-09-14) by reading `git log` and the current source — it wasn't authored phase-by-phase like 1–6, so it's schematic rather than a full narrative.

---

## 1. Insights screen — ships the [[Archive/Culla-Music/Ideas/stats-activity-view|Stats / activity view]] idea

A new full-screen stats surface (`Views/InsightsView.swift`, `ViewModels/InsightsModel.swift`), opened from Settings, superset of the original idea:

- Hero sort count with a library-coverage gauge, current/best streaks, a per-playlist breakdown (`3642c91`, tap "+ N more" to expand — `8ae9a8f`).
- **Top Artists** with portraits that tap through to the artist hub (`71e40c3`), shimmering while portraits resolve instead of popping in (`bb75c0a`).
- **Round two** (`c7cc848`): taste profile, all-time genre mix, release-decade (Eras) histogram, localization.
- Everything except Top Artists portraits is computed live from the durable `SortedSong` / `DismissedSong` SwiftData rows — no counters, works retroactively over the whole sorting history.

Went beyond the original sketch (which asked for a 30-day bar chart + top-3 playlists + streak) — no Duolingo-style guilt mechanics, calm tone preserved.

## 2. Session entry/exit choreography — hero morph retired

The Home → Swipe **matched-geometry hero morph** from [[Phases/phase-05-liquid-glass-and-restraint|Phase 5]] was replaced with a quieter "tile recede/settle" choreography:

- Double-tap-to-skip gets a recede animation on just the artwork tile (`d7a3af3`, `890ef62`), settled to a quick in-place crossfade rather than a geometry move (`fa78247`).
- **`2c75c39` "session entry/exit joins the quiet tile choreography, hero morph retired"** — session entry/exit now uses the same recede/settle language as the skip, and the old `matchedGeometryEffect` hero-morph transition is gone.
- **Vault impact:** [[Phases/phase-05-liquid-glass-and-restraint|Phase 5]] §2 and the `qa-testing-tracker` "Home ↔ Swipe matched-geometry hero morph" section both describe a transition that **no longer exists** in the app. Annotated in both places rather than rewritten (see below).

## 3. Down-swipe share — arming disc

Phase 6 shipped down-swipe-to-share as a basic gesture (`31353ba`). Phase 7 gives it a dedicated visual language:

- **Arm swipes inside the play disc**, previewing the down-swipe share before release (`91aa0ad`).
- Disc animations scoped so the arming glyph tracks the drag 1:1 (`6791bf6`).

## 4. Playlist tracklist sheet (new: `Views/PlaylistDetailSheet.swift`)

Tapping a membership pill on the swipe card now opens a tracklist sheet for that playlist — cover hero, monospaced rows with durations, tap-to-preview, artist under each title (`a4efc88`). Same sleeve language as the Phase-6 `AlbumDetailSheet`. Membership pills were flattened to plain material/tint so Liquid Glass can't bleed or glitch mid-drag (`2aad31c`, `e17b5f6`). A marquee for the sheet's artist sub-line shipped and was reverted same-day (`95e627b` → `4bb9078`).

## 5. Dismissed / catalog data-integrity fixes

Follow-on hardening of the Phase-6 catalog-auditioning + sort-reconciliation work:

- Prune dismissed songs deleted from the Apple Music library so the Dismissed count matches the deck (`f7fca8f`).
- **History tombstones** (`72b5e4d`, new `ViewModels/HistoryStore.swift` logic) — a History row for a since-deleted song becomes a greyed tombstone (saved title/artist/cover, swipe actions blocked, no dead Undo) instead of disappearing or erroring.
- Heal dismissed rows misflagged as catalog tracks (`62380ac`); judge catalog-flagged dismissals on dual evidence, one fresh count walk per reconcile version (`d995d64`); treat Apple's 404 as an authoritative catalog-absence verdict so dead dismissals finally void (`d18d315`).

## 6. Settings / Look

- **Hide the status bar by default**, with a "Show status bar" toggle in a new Look section (`bc03c23`).
- Settings toggles get localized explanatory subtitles (`54774a6`).

## 7. Misc polish

- Cancel stale autoplay so it can't start after leaving the swipe session (`e0330b1`).
- Playlist chips no longer trail the card's accent by one step (`cb49bef`); artwork accents warmed ahead of display so card tints stop switching (`c692387`).
- Swipe toasts hug their text instead of a fixed 280pt width (`14130b6`).
- Apple Music editorial notes render as rich HTML text instead of raw markup (`e98209e`).

## 8. Dev tooling — screenshot mode refinements

Follow-on to Phase 6's `cullaScreenshotMode`: neutral iconographic hero covers (`5f5bb03`), glass covers with a single track glyph (`42f5467`), brand-mark covers with depth fade (`418c045`), rights-safe screenshot plan (`47eb120`) — all in service of App Store screenshots that don't expose real library data.

## 9. App Store — 1.5.0 (build 2) release readiness

- **Version bumped to 1.5.0 (build 2)**, marked encryption-exempt (`2bf7ded`).
- **App Store submission kit added** for 1.5.0 build 2 (`613c521`), store metadata later synced to reflect **"a submitted 1.5.0 listing"** (`cda1020`, 2026-07-27).
- Per `store/CHECKLIST.md` in the repo: **the app already has a live App Store record** — this is described throughout as *"an update to an app that's already live (version 1.0, build 1)"*, App Store ID `6778348600`, listing at `apps.apple.com/us/app/cullamusic/id6778348600`. **The vault had never recorded that Culla Music shipped to the App Store at all** — the index only ever described "App Store prep" as future work. Corrected in [[Projects/Culla-Music/culla-music|the project index]].
- 1.5.0's What's New (per `store/METADATA.md`): Insights, tappable playlist chips → tracklist sheet, swipe-down share with the arming disc, History tombstones, hidden-status-bar Look option, and fixes — i.e. everything in §1–§6 above.
- Some checklist steps in `store/CHECKLIST.md` (screenshots, archive/upload, final submit) are still marked 👉 (user-driven, outside git) as of the last docs sync — **actual current App Store Connect status wasn't independently verified by this audit** and should be checked directly.

---

## Files touched (non-exhaustive)

- New: `Views/InsightsView.swift`, `ViewModels/InsightsModel.swift`, `Views/PlaylistDetailSheet.swift`.
- Heaviest churn: `Views/MusicSwipeView.swift` (recede choreography, arming disc), `ViewModels/HistoryStore.swift` (tombstones), `Services/MusicLibraryService.swift` (catalog-absence / dismissed reconciliation — now 1589 lines, up from 935 at the last count in the project index's refactor backlog).

## Outstanding / next steps

- **On-device QA gap is now large** — [[qa-testing-tracker|QA Testing Tracker]]'s last logged pass is still 2026-05-22 (146 commits / ~3.75 months behind, spanning all of Phase 6 and this phase).
- **Refactor backlog (R1–R6, from the 2026-05-20 code audit) still open and has grown** — `MusicLibraryService.swift` is now 1589 lines (was 935), `HomeView.swift` 1244 lines, `SourceScopePickerSheet.swift` 524 lines.
- **Still-open ideas:** [[Ideas/smart-playlist-suggestion|Smart playlist suggestion chip]], [[Ideas/artist-count-name-fallback|Name-based artist-count fallback]] — neither shows any implementation in the codebase as of this audit.
- **Repo has been dormant since 2026-07-27** (aside from a trivial 2026-09-14 reformat commit) — likely paused pending the 1.5.0 App Store review/release cycle.

---

*Phase 6 → [[Phases/phase-06-surfaces-onboarding-and-release|Phase 6 — New Surfaces, Onboarding & Release Readiness]]*
*Project index → [[Projects/Culla-Music/culla-music|Culla Music]]*
