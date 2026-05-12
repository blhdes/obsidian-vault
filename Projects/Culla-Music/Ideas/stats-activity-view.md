---
title: Stats / activity view
date: 2026-05-12
tags: [culla-music, idea, feature, stats, charts, ux]
---

# Stats / activity view

A lightweight activity dashboard so the user can see what they've actually done in Culla. Surfaces effort and patterns without being pushy.

## Why

- Validates the work the user has put in — Culla rewards consistency but currently shows zero visibility on it.
- Surfaces patterns ("you almost always sort to *Chill* on Sunday nights") that could later feed into smart suggestions ([[smart-playlist-suggestion]]).

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
