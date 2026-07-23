---
title: Auto Filter Movement
date: 2026-07-22
tags: [ableton, effects, auto-filter, sound-design, stab]
---

# Auto Filter Movement

An **effects-chain filter** — a separate device from a synth's own internal filter, placed after the instrument in the chain. Where a synth's built-in filter (e.g. Drift's Low Pass) sets a *static* tone, Auto Filter's own **LFO section** can add rhythmic *movement* on top, without touching the instrument's patch at all.

## Why add it if the instrument already has a filter

Drift's internal Low Pass (Type I, ~900Hz) already shapes [[../Track-Sketches/hardgroove-134|Hardgroove 134]]'s STAB into a dark, filtered chord — but that cutoff sits still. Auto Filter, dropped into the STAB's device chain right after Drift, reopens the question of *movement*: does the cutoff wobble, breathe, or stay put? It's a separate creative decision from the instrument's own tone, layered on afterward.

## The device, briefly

| Section | What it does |
|---|---|
| **Filter** | Type (Low/Band/High/Notch/Morph), Frequency, Resonance — same concept as any filter already known (acid lead, Drift, Simpler's hat filter) |
| **LFO** | Rate (Hz, free-running — or **Sync**, locked to a tempo note-division like 1/16, 1/8), Amount (how far the LFO swings the cutoff), Waveform (Sine = smooth wobble, Square = choppier on/off) |
| **Envelope Follower** | Tracks the *input signal's own* volume/transient to move the filter — a different movement source than the LFO; not used in this pass, flagged for later |

**Sync vs. free Hz reapplies the same lesson from Drift's own LFO** ([[drift-kick-from-scratch|Building a Kick From Scratch in Drift]] §7): a synced Rate locks the wobble to the beat grid; a free Hz rate can drift out of phase with the tempo. The same **~20Hz audio-rate threshold** applies here too — a slow synced rate (e.g. 1/16) reads as shaped movement, cranking Rate high enough turns it into the filter's own buzz/texture instead of felt motion.

## Starter recipe — STAB (Hardgroove 134)

- Add **Auto Filter** after Drift in the STAB chain (chain order: Drift → Auto Filter).
- Filter Type: **Low Pass** (matches the STAB's existing dark, filtered character rather than fighting it).
- Frequency: set close to where Drift's own cutoff already sits (~900Hz) as the LFO's center point.
- LFO: **Sync** on, Rate **1/16** or **1/8** (try both by ear), Amount moderate, Waveform **Sine** to start (smoothest wobble).
- A/B against LFO Amount at 0 to hear exactly what the movement adds versus the static filtered tone alone.

## Other movement options flagged for this same pass

Not yet built — options to compare once Auto Filter's been tried:
- **Chorus-Ensemble** — thickens/widens via short modulated delay lines, a different flavor of movement (width, not filter sweep).
- **Phaser-Flanger** — a sweeping comb-filter effect, a more pronounced "swirl" than Auto Filter's plain cutoff wobble.
