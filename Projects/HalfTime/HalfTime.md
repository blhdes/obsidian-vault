---
title: Doppio (formerly beatmch / HalfTime)
date: 2026-06-01
updated: 2026-06-10
tags: [project, ios, swift, dj, doppio, halftime, beatmch]
---

# ⏱️ Doppio

> Renamed from **HalfTime** → **beatmch** → **Doppio** (decided 2026-06-10, see
> [[Inbox/beatmch-app-naming|the naming note]] — *doppio movimento* = "twice as
> fast"). The vault folder stays `HalfTime/` so existing `[[wikilinks]]` keep
> working; everything else was renamed on 2026-06-10 — codebase (folder `Doppio/`,
> `Doppio.xcodeproj`, bundle id `agu.doppio`), the local repo folder
> (`Claude/doppio/`), and the GitHub repo (`blhdes/doppio`).

Index note for the **Doppio** iOS app — a minimalist BPM half-time / double-time
tool for DJs, built as a *living metronome*, not a calculator. Source code lives at
`/Users/agomezu/Claude/doppio/`.

## What it does

- **Swipe up/down** anywhere to set your track's BPM (fractional, 0.1 steps, 20–300).
  A faint scale on the right edge shows where you are — and you can grab that bar to
  jump to an absolute BPM.
- **Hold a second finger** for fine mode: the swipe slows ~10× so you nudge a decimal.
- Big number shows **half** of the source BPM; a **single tap** flips to **double**
  (for the drop). The motion shows both rhythms at once — result (bold) + source (faint).
- **Two-finger tap** cycles the beat style: Orbit · Ripple · Sweep · Pulse · Bare.
- **12 themes**, each a cross-hue mesh-gradient journey; **shake** the phone for a random one.
- Haptic detent per whole BPM (per 0.1 in fine mode), firmer thud on the flip.
- Remembers last BPM, mode, beat style, and theme between launches.
- Respects **Reduce Motion** (backgrounds freeze, rings hold still, dots blink on the beat).

## Sections

- **[[Ideas]]** — product ideas, feature sketches, UX experiments not yet decided.
- **[[Dev-Insights]]** — lessons learned while coding.
- **Phases** — milestones / releases (create when there's a first milestone).

## Quick links

- Repo: `/Users/agomezu/Claude/doppio/` · GitHub: `blhdes/doppio`
- Open it: `cd doppio && xcodegen generate && open Doppio.xcodeproj`
- Xcode 26+ · iOS 18+ (Liquid Glass on iOS 26, frosted-material fallback below) · portrait-only

## Status

Well past scaffold (updated 2026-06-04). Has 5 beat styles, 12 cross-hue themes,
mesh-gradient backgrounds, shake-to-theme, fine mode, and an honest half/double
twin-rhythm display. SwiftUI + `@Observable` view model, UserDefaults persistence,
primed haptics. See [[Dev-Insights]] for the latest polish pass.

Related: [[Projects/Culla/Culla|Culla]] · DJ work in [[Areas/Mixing-DJing/]]
