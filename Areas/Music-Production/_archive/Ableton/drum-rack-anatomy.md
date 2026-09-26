---
title: Drum Rack Anatomy
date: 2026-07-21
tags: [ableton, drum-rack, percussion]
---

# Drum Rack Anatomy

Up to now, "Drum Rack" only meant *loading a preset kit* (Session 3: drop one in, kick/snare/hats already sitting on the pads). This is the other half — building one **from empty**, pad by pad.

## The problem it solves

A percussion layer might want 3-4 different one-shot sounds (rim, shaker, clave, conga...) — that's 3-4 tracks gone if each got its own Simpler. A **Drum Rack holds all of them on one track**: one pad grid, one MIDI track, as many sounds as pads.

This is the same instrument-budget thinking from Hardgroove 134's kickoff (the 8-track plan) — Drum Rack is the tool that makes "PERC — all percussion lives here" possible as a single line in that budget.

## What's actually inside a pad

Each pad in a Drum Rack is its own mini **Simpler**, nested. Drop an audio sample onto a pad and Live auto-creates that pad's chain — same Start/Length trimming, same Classic/One-Shot choice already known from [[sampling-with-simpler|Sampling with Simpler]]. A Drum Rack is really just several Simplers stacked behind one set of pads, each one addressable by its own key/pad.

```
┌─────────────────────────────┐
│   Macro knobs (top, 8)       │  ← optional, map any pad param to a shared dial
├─────────────────────────────┤
│  [Pad] [Pad] [Pad] [Pad]     │
│  [Pad] [Pad] [Pad] [Pad]     │  ← 4x4 (or 8x8) grid, one chain per pad
│  [Pad] [Pad] [Pad] [Pad]     │
│  [Pad] [Pad] [Pad] [Pad]     │
├─────────────────────────────┤
│  Chain (selected pad's own   │  ← same Device Chain panel as any track,
│  Simpler + any FX after it)  │     just scoped to whichever pad is selected
└─────────────────────────────┘
```

Same octave gotcha as the preset version (Session 3): the rack's pads start at **C1**. If you're playing pads live via QWERTY, `Z` twice drops you to that range.

## Choke groups

Two one-shot chains (say, closed + open hi-hat) don't know about each other by default — nothing stops both from ringing at once, even though a real hi-hat physically can't do that (one pair of cymbals, one voice). A **choke group** fakes the physical constraint: give two chains the same group number and triggering either one cuts off whatever else in that group is still sounding.

Setting: look near the **I/O** toggle in the Chain List — Choke is one of the other optional per-chain columns in that same toggle row. Assign the same number to both hi-hat chains.

This is exactly the HATS use case: closed hat should always cut an open hat's ringing tail, matching [[../Techniques/open-vs-closed-hihat|the real physical behavior]].

## Reassigning a pad's note

A pad's position in the grid *is* its note — there's no separate "type a note number" field on the pad itself. **Drag the chain (or the pad) onto a different pad cell** to reassign it — dropping a sample onto the C1 pad makes it trigger on C1. This is the reliable method, confirmed working.

Loaded pads show the **sample's name** instead of the note name (e.g. a rim sample sitting on C1 displays "Rim DMX Lo Fi", not "C1") — the note assignment hasn't changed, only the label. Check the Pads grid itself to see which cell a chain actually occupies.

**Chain List view** — toggle via the bottom icon in the vertical icon strip on the left edge of the rack (below the highlighted "Pads" icon), not top-right as first guessed. It's a table (Chain name / Vol / Pan / Mute / Solo) confirmed to render at default panel width.

**Confirmed 2026-07-22: dragging a new sample onto an already-occupied pad REPLACES its chain, it does not layer.** (Tried dragging a shaker onto the rim's C1 pad — rim was gone, not stacked.)

**Key Range editing — confirmed location: the I/O button.** Toggling I/O (Input/Output) in the Chain List reveals each chain's Key Range (and Velocity Range), which is what actually controls which note(s) trigger a chain — the Pad grid position is just a visual shortcut for the common case of one chain per key.

**In practice, for layering two one-shots on the same beat: skip the same-key hunt.** Put each sample on its own pad/note, then in the clip's piano roll place both notes at the **same time position** — ordinary MIDI polyphony (the same mechanism already used for stab/pad chords). Audibly identical to sharing a key, and keeps independent Vol/Pan/Mute per layer — arguably better for mixing anyway.

## Editing notes for a Drum Rack in the piano roll

With **Fold** enabled, a Drum Rack track's clip editor doesn't show a chromatic keyboard or the clip's Scale setting (that Scale field is for melodic clips only — pads aren't musical pitches, they're triggers). Instead it shows one row per **loaded pad only**, labeled with the sample's own name (e.g. "Rim DMX Fi", "Shaker Tamuz") instead of a note name. To layer two one-shots on the same beat: draw each sample's note in its own row, aligned to the same time column — same Pencil tool (`B`) as any MIDI clip.

## Building it empty (this project's rule)

Browser → Drums → **Drum Rack** (the bare device, not a named kit preset) → drop on a new MIDI track. Every pad starts empty. Drag one-shot samples from the Browser onto individual pads by hand — this keeps the "100% hand-built, nothing pre-cooked" rule intact even though the device itself ships as a Live stock instrument.

## See also

- [[sampling-with-simpler|Sampling with Simpler]] — the per-pad playback mechanics (Start/Length, Classic vs One-Shot)
- [[playing-an-instrument|Playing an Instrument]] — the original Drum Rack mention (preset version) and the C1 octave gotcha
- [[../Techniques/percussion-layering|Percussion Layering]] — where the pads' hits actually go rhythmically
