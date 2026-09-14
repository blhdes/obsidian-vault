---
title: "Phase 7 — Insights, Screenshot Tooling & App Store Submission"
date: 2026-06-14
tags: [culla-music, phase, insights, charts, app-store, done]
status: shipped
---

# Phase 7 — Insights, Screenshot Tooling & App Store Submission

Schematic record — reconstructed retroactively from git history (no phase note existed for this cluster). ~40 commits, **2026-06-14 → 2026-07-27** (the bulk landed by mid-July; late commits were metadata sync). Picks up right after [[phase-06-surfaces-onboarding-and-release|Phase 6]].

## 1. Insights screen (ships the [[Archive/Culla-Music/Ideas/stats-activity-view|Stats / activity view]] idea)

The music sibling of Culla's photo-app Insights — full-screen, opened from Settings, computed live from SwiftData (`SortedSong`/`DismissedSong`), no separate daily-stats model.

- **First pass** (`3642c91`) — sorting stats, streaks, top artists.
- **Artist portraits** (`71e40c3`) in the Top Artists rows.
- **Round two** (`c7cc848`) — taste profile, genre/playlist coverage, tap-through into the artist hub, localized.
- Polish: expandable "+ X more" playlist breakdown (`8ae9a8f`), playlist-chip accent no longer trails by a step (`cb49bef`), artwork accents warmed ahead of display (`c692387`), toasts hug their text instead of a fixed width (`14130b6`).

Went **beyond** the original idea sketch (taste profile + coverage + artist tap-through weren't in the original spec) but delivers all four core asks: per-day activity chart, top-playlists breakdown, dismissed count, and streak.

## 2. Screenshot tooling & App Store submission assets

- Flag-gated `cullaScreenshotMode` portfolio sidebar (`eef441a`), demo images dropped in favor of neutral iconographic hero covers (`5f5bb03`), then glass (`42f5467`) and brand-mark (`418c045`) cover variants with depth fade.
- Rights-safe screenshot plan documented (`47eb120`); Apple Music editorial-notes HTML rendered as rich text so album/artist "About" copy reads correctly in captures (`e98209e`).
- App Store submission kit for 1.5.0/build 2 (`613c521`), version bump + encryption-exempt flag (`2bf7ded`, 2026-07-11).
- **Submitted**: store metadata synced to the actual submitted 1.5.0 listing — new name ("Culla Music: Swipe Your Songs"), subtitle, keywords, What's New (`cda1020`, 2026-07-27).

## 3. Interaction choreography

- Double-tap skip reworked into a quick recede/crossfade instead of a geometry move (`d7a3af3`, `fa78247`).
- Session entry/exit joins the same quiet-tile choreography; the old hero-morph transition retired (`890ef62`, `2c75c39`).
- Play disc rework: swipes arm from inside the disc with a live down-swipe share preview (`91aa0ad`), membership pills flattened to a plain tint so Liquid Glass drag transforms can't glitch them (`2aad31c`, `e17b5f6`), disc animation scoping so the arming glyph tracks the drag 1:1 (`6791bf6`).
- Playlist tracklist sheet opens from the card's membership pills (`a4efc88`); a marquee treatment for the sheet's artist sub-line shipped then reverted same day (`95e627b` / `4bb9078`).

## 4. Reliability & correctness fixes

- Dismissed-count/catalog-absence reconciliation: read Apple's 404 as authoritative catalog-absence (`d18d315`), judge catalog-flagged dismissals on dual evidence with a forced fresh count walk (`d995d64`), heal misflagged dismissed rows (`62380ac`), prune dismissed songs deleted from the AM library (`f7fca8f`).
- Stale autoplay cancellation on session exit (`e0330b1`); Top Artists avatars shimmer instead of pop-in (`bb75c0a`); History keeps deleted tracks as greyed tombstones (`72b5e4d`); Settings toggles get localized subtitles (`54774a6`); status bar hide-by-default with a Look toggle (`bc03c23`).

## Known gap

**QA is now badly behind** — [[qa-testing-tracker|QA Testing Tracker]]'s last logged pass is still 2026-05-22, so all of Phase 6 *and* this phase (~110+ commits: Insights, screenshot tooling, the submitted 1.5.0 build, choreography rework, reconciliation fixes) are unverified on device. Biggest pre-next-release risk — see [[Projects/Culla-Music/culla-music|project index → Known issues]].

## Related

- [[Projects/Culla-Music/Phases/phase-06-surfaces-onboarding-and-release|Phase 6 — New Surfaces, Onboarding & Release Readiness]] — the phase this builds on
- [[Archive/Culla-Music/Ideas/stats-activity-view|Stats / activity view]] — the idea this phase shipped
- [[Projects/Culla-Music/culla-music|Culla Music — Project Index]]
