---
title: Stats / activity view
date: 2026-05-12
tags: [culla-music, idea, feature, stats, charts, ux, shipped]
---

> **✅ Shipped — Phase 7 (first pass `3642c91`, 2026-07-13; round two `c7cc848`, 2026-07-14).** Landed as the full-screen **Insights** screen (`Views/InsightsView.swift` + `ViewModels/InsightsModel.swift`), opened from Settings. Went beyond this sketch: hero sort count with a library-coverage gauge, current/best streaks, a per-playlist breakdown, Top Artists with tap-through portraits, an all-time genre mix, a release-decade (Eras) histogram, and a taste profile — all computed live from the local SwiftData rows, no counters. See [[Projects/Culla-Music/Phases/phase-07-insights-and-1-5-0-release|Phase 7]]. Original sketch kept below.

# Stats / activity view

A lightweight activity dashboard so the user can see what they've actually done in Culla. Surfaces effort and patterns without being pushy.

## Why

- Validates the work the user has put in — Culla rewards consistency but currently shows zero visibility on it.
- Surfaces patterns ("you almost always sort to *Chill* on Sunday nights") that could later feed into smart suggestions ([[Projects/Culla-Music/Ideas/smart-playlist-suggestion|smart-playlist-suggestion]]).

## Behavior

- Entry point: a chart icon on the Home screen, or a button in Settings.
- Content (all read from local SwiftData — no network):
  - **Songs sorted per day**, last 30 days, as a bar chart via SwiftUI `Charts`.
  - **Top 3 playlists by sort volume** (last 30 days).
  - **Dismissed count** total + last-7-days delta.
  - **Current streak** — consecutive days with at least one sort action. Lightweight; not a Duolingo guilt-trip.

## Notes

- Stays local-only. No screenshots of the user's library leaving the device.
- "Streak" as a soft signal (small number + colored dot), not a forced notification.
- Empty state: a one-liner ("Sort a few songs to see your activity here.") with no fake placeholder data.

## Open questions

- **Persistence.** `SortedSong` and `DismissedSong` already have `sortedAt` / `dismissedAt`. Confirm they're indexed-friendly for daily-bucket queries.
- **Replay tie-in.** Worth a *"Compare your sorts vs. your Replay listens"* secondary chart? Probably out of scope for v1 of this view — keep it lean first.

## Size / risk

Medium. Risk: making it feel like Duolingo. Keep the visual tone calm and the streak optional / dismissible.
