---
title: Themes & motion polish pass
date: 2026-06-04
tags: [beatmch, dev-insight, swift, swiftui, themes, motion]
---

# Themes & motion polish pass — 2026-06-04

A batch of refinements to [[Projects/Doppio/Doppio|beatmch]], all shipped and
pushed to `blhdes/beatmch`. Mostly about making the look calmer and the motion
*honest* to the actual tempo.

## What changed

- **Themes: 20 → 12 cross-hue journeys.** Cut the near-duplicate themes down to a
  curated 12, one strong identity per "lane." Each theme's background mesh now
  **sweeps diagonally through three real hues** (e.g. indigo → blue → teal) instead
  of just dimming a single colour into a vignette, lit by a **jewel accent**. The
  ×2 / ×½ flip always does something deliberate to the colour (warm↔cool swap,
  brightness lift, or a hue clash), noted per-theme in the code.
- **Ripple & Sweep kept honest to BPM.** The two animated beat styles now track the
  real tempo instead of drifting, and stay **readable via motion blur** so a fast
  beat still looks intentional rather than smeared.
- **Orb number centred under Reduce Motion.** With Reduce Motion on, the big number
  now stays properly centred on the rings (it was off before).
- **Post-shake theme name = plain quiet text.** After a shake-to-random-theme, the
  theme's name surfaces as understated plain text — no loud styling.
- **Shake-to-theme no longer bounces back.** Shaking to a new theme used to snap back
  to the previous one; that bug is fixed, so the new theme sticks.

## Why it matters

The throughline: a DJ glances at this in a dark booth mid-set. Fewer, more distinct
themes = quicker recognition; honest motion = you can *trust* what the beat animation
is telling you; quieter text = nothing shouting for attention while you're mixing.

## Where it lives

- Themes: `beatmch/Theme/Theme.swift` (the 12 themes + `Palette.sweep(...)` helper).
- Beat-style motion + Reduce-Motion centring: `beatmch/Views/PulseOrb.swift`.
- Shake handling + theme-name text: `beatmch/Views/ContentView.swift`.

Related: [[Projects/Doppio/Doppio|beatmch index]]
