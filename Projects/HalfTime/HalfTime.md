---
title: HalfTime
date: 2026-06-01
tags: [project, ios, swift, dj, halftime]
---

# ⏱️ HalfTime

Index note for the **HalfTime** iOS app — a minimalist BPM half-time / double-time
tool for DJs. Source code lives at `/Users/agomezu/Claude/halftime-app/`.

## What it does

- Swipe up/down anywhere to set your track's BPM (fractional, 0.1 steps).
- Big number shows **half** of that BPM by default.
- Single tap flips to **double** (for the drop). Tap again to go back.
- Haptic detent on every whole BPM while swiping; firmer thud on the flip.
- Remembers the last BPM and mode between launches.

## Sections

- **[[Ideas]]** — product ideas, feature sketches, UX experiments not yet decided.
- **Dev-Insights** — lessons learned while coding (create when the first one comes up).
- **Phases** — milestones / releases (create when there's a first milestone).

## Quick links

- Repo: `/Users/agomezu/Claude/halftime-app/`
- Open it: `cd halftime-app && xcodegen generate && open HalfTime.xcodeproj`
- Bundle id: `agu.halftime` · iOS 18+ · portrait-only

## Status

Scaffolded and building (2026-06-01). SwiftUI + `@Observable` view model,
UserDefaults persistence, primed haptics. Next: real app icon, decide whether to
show half *and* double simultaneously (see the idea note).

Related: [[Projects/Culla/Culla|Culla]] · DJ work in [[Areas/Mixing-DJing/]]
