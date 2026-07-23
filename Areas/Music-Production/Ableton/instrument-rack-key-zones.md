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

- **`Cmd+G` is context-sensitive — a real gotcha.** Selecting a *track header* and pressing `Cmd+G` creates a **Track Group** (a folder for organizing/collapsing tracks in the track list) — a completely different feature, no device fusion, no space saved. To build a Rack, the *devices themselves* (inside the track's Device View) must be selected first.
- In the Device View, click the instrument's title bar (+ shift-click any effects after it already on the track) to select them, **then** `Cmd+G` — this wraps the selection into a Rack, becoming **Chain 1**, still on the same track.
- Add a second chain: open the Rack's **Chain List** view, drag another instrument in and drop it below Chain 1 to create Chain 2.
- **Confirmed on Live 12 Lite: a plain Instrument Rack's Chain List exposes Key Range directly** — unlike Drum Rack, where it hides behind the I/O toggle. Click the **Key** button (alongside Vel / Chain / Hide at the top of the Chain List) to reveal a Key Zone editor bar above the chain rows, and drag each chain's range boundaries directly in that bar — non-overlapping, e.g. Chain 1 low, Chain 2 high.
- Each chain can carry its own effects *after* its own instrument, inside the chain — separate from any effects on the other chain.

## Applied: STAB/LEAD sharing one track ([[../Track-Sketches/hardgroove-134|Hardgroove 134]])

Track 5 was budgeted for **STAB/LEAD** together from the project's kickoff. Solution: one Instrument Rack —
- **Chain 1 (STAB):** existing Drift → Auto Filter → Chorus-Ensemble, key-zoned to cover the STAB chord's existing register (roughly C1–B4).
- **Chain 2 (LEAD):** a new Drift patch → Phaser-Flanger, key-zoned above it (C5 and up) — matching the already-known "lead sits on top" register-lane rule from [[bleep-lead-motif|Bleep Lead & Motif Writing]].

Both chains live on the same track, in the same clip if wanted (notes in each register automatically route to their own chain) — no extra track spent.
