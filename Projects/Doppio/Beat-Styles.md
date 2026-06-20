---
title: Doppio — Beat Styles (the five orb modes)
date: 2026-06-21
updated: 2026-06-21
tags: [project, doppio, ios, ui]
---

# 🟠 Beat Styles

The orb's five looks, cycled with a **two-finger tap** (choice is remembered).
All but *Bare* keep the steady centre number and the **inner = result (bold) /
outer = source (faint)** twin-rhythm idea — they only differ in *how* the rhythm
is drawn. Lives in `Doppio/Views/PulseOrb.swift` (`BeatStyle` enum).

| Style | What it draws | Pace |
|---|---|---|
| **Orbit** | A glowing dot travels around each ring; its glow ticks brighter on each beat. | once per **bar** |
| **Ripple** | A ring born at the centre, expanding to the edge — a slow swell of light. | once per **bar** |
| **Sweep** | A bright comet arc sweeps the ring, leaving a radar tail. | once per **beat** |
| **Pulse** *(default)* | Two concentric rings breathe in/out; the inner one glows on the beat. | once per **beat** |
| **Bare** | Nothing but the number — animation loop fully off. | — |

## Why Orbit & Ripple are per-bar (2026-06-21)

They originally ran per-beat like the others, so at club tempos they blurred into
fast motion that read too much like their neighbours (Ripple ≈ Pulse, Orbit ≈
Sweep). Slowing them to **one gesture per 4/4 bar** (4× slower) makes them read as
*paused* and distinct. Orbit keeps a per-beat **glow tick** so the tempo stays
legible even though the dot moves slowly; Ripple's slow expansion carries the
motion on its own. Implemented via a `barPhase()` helper (`phase / beatsPerBar`).

Related: [[Doppio]] · [[Dev-Insights]]
