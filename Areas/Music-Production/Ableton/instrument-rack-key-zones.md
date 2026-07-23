---
title: Instrument Rack Key Zones
date: 2026-07-23
tags: [ableton, instrument-rack, key-zones, workflow, live-lite]
---

# Instrument Rack Key Zones

A **Drum Rack is actually a specialized Instrument Rack** — one built from empty and pre-configured so every pad shows its own nested instrument on its own MIDI key. A plain **Instrument Rack** is the same underlying container, but built with regular melodic instruments (Drift, Simpler...) as its chains — and each chain gets its own **Key Range**, exactly like a Drum Rack pad, via the same **I/O** toggle in the Chain List already known from [[drum-rack-anatomy|Drum Rack Anatomy]].

## Why this matters for a track-budget squeeze

Live Lite's 8-track cap means a project can't always give every distinct sound its own track. An Instrument Rack solves this the same way Drum Rack solved it for percussion: **one MIDI track, several genuinely different instrument chains, split so only one plays at a time** — here, split by note range instead of by pad.

## Building one

- Select an instrument (+ any effects already on it) on a track, `Cmd+G` (Group) — this wraps them into a Rack, becoming **Chain 1**.
- Add a second chain: drag another instrument into the Chain List panel, or right-click → new chain.
- Open the **I/O** toggle on each chain to reveal its **Key Range** editor (same mechanic as a Drum Rack pad's key zone) and set non-overlapping ranges — e.g. Chain 1 low, Chain 2 high.
- Each chain can carry its own effects *after* its own instrument, inside the chain — separate from any effects on the other chain.

## Applied: STAB/LEAD sharing one track ([[../Track-Sketches/hardgroove-134|Hardgroove 134]])

Track 5 was budgeted for **STAB/LEAD** together from the project's kickoff. Solution: one Instrument Rack —
- **Chain 1 (STAB):** existing Drift → Auto Filter → Chorus-Ensemble, key-zoned to cover the STAB chord's existing register (roughly C1–B4).
- **Chain 2 (LEAD):** a new Drift patch → Phaser-Flanger, key-zoned above it (C5 and up) — matching the already-known "lead sits on top" register-lane rule from [[bleep-lead-motif|Bleep Lead & Motif Writing]].

Both chains live on the same track, in the same clip if wanted (notes in each register automatically route to their own chain) — no extra track spent.
