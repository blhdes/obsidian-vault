---
title: Clip Envelopes (Automating Parameters Inside a Clip)
date: 2026-05-30
tags: [ableton, automation, clip-envelopes, modulation, session-view]
---

# Clip Envelopes (Automating Parameters Inside a Clip)

**Automation** = telling Live to *move* a knob or fader by itself over time. Instead of you turning the filter cutoff by hand, you draw the movement once and Live plays it back perfectly every loop.

**Clip envelopes** are the simplest form: automation that lives **inside a clip**. While that clip plays, the automation runs. When the clip stops, the parameter goes back to whatever value the knob is set at on the device.

This is the Session View way of doing automation. (Arrangement View has its own bigger automation system — same idea, different surface, comes later.)

## When you'd use a clip envelope

- Filter cutoff opening up over 8 bars (the classic acid build-up)
- Volume slowly rising on a clap entry
- Reverb wet amount creeping up before a drop
- Synth pitch bending across a phrase

Anything that's a knob, fader, or dropdown on a device or mixer → you can automate it inside a clip.

## How to add one (Live 12)

With a clip selected (Session or Arrangement), in Clip View:

1. Click the **Envelopes** tab — top-right of Clip View, next to **Notes** and **MPE**. That swaps the note grid for the envelope editor.
2. Two dropdowns sit at the **bottom** of that pane. First = **Device** → choose the device on the track (e.g. **Drift**, **Mixer**, **Reverb**, etc.). Defaults to whatever's already loaded.
3. Second = **Control** → choose the specific parameter (e.g. **Filter Freq**, **Track Volume**, **Dry/Wet**). It usually defaults to something unrelated (like LFO Wave) — always check and change it.
4. A horizontal line appears across the grid — that's the current value of the parameter. Press **Pencil tool `B`** and drag across the clip to draw a rising/falling ramp, or click to drop breakpoints and drag them into a curve.

### Stacking more than one envelope on the same clip

Only one Device/Control pair is shown at a time, but each pair's drawn automation is stored **independently** — switching the dropdowns to a different parameter and drawing there doesn't erase what you drew for the first one. This is how you build something like a [[../Techniques/riser-fx|riser]]: draw Filter Freq rising, then switch Control to Track Volume and draw that rising too — both play back together, even though you only ever see one at a time.

### Shortcut

You can also **right-click any knob/fader on a device** → **Show Automation** → it auto-fills the Device + Control dropdowns for you. Big time-saver.

## What the envelope view looks like

```
┌────────────────────────────────────────────┐
│  Device: [Simpler ▼]   Control: [Filter Freq ▼]   │
│                                            │
│  22 kHz ┤                            ╱─────│   ← high (open)
│         │                       ╱─── │     │
│         │                  ╱────     │     │
│         │             ╱────          │     │
│   200 Hz┤────────────╱               │     │   ← low (closed)
│         └────────────────────────────┴─────│
│         bar 1    bar 4    bar 6      bar 8 │
└────────────────────────────────────────────┘
```

A line from low to high over 8 bars = filter slowly opens.

## Clip length must accommodate the automation

A 1-bar clip with a slow filter sweep = the sweep happens in 1 bar (way too fast). For a *slow* sweep, **extend the clip length first**:

- In the MIDI editor, drag the **right edge of the loop brace** (the bracket above the grid) out to bar 8 (or 16).
- The notes you already drew stay in bar 1; bars 2–8 are empty — but the **clip plays for 8 bars** before looping, which is what the envelope needs.
- For an acid lead, empty bars are fine — the notes you already wrote will keep firing on bar 1 every time the clip loops back. *(If you want notes to play across all 8 bars, you'd duplicate the pattern with `Cmd+D`.)*

Meanwhile, drums and bass clips on the same scene can stay at 1 bar — they'll just loop 8 times underneath. Clips on a scene loop independently; they don't have to match length.

## Drawing tips

- **Pencil tool (`B`)** = freeform draw.
- Click without the pencil = drop **breakpoints** (anchor dots) that you can drag.
- **Right-click a breakpoint** → options like "Delete" or curve shape.
- Hold **`Shift`** while dragging = finer precision.

## Loop / Linked vs Unlinked envelopes

By default, a clip envelope is **Linked** to the clip — its length matches the clip's loop length, and it loops with the clip.

You can **Unlink** it (small chain icon in the envelope view) → then you can have, say, a 16-bar envelope inside a 1-bar clip. The envelope plays through its full 16 bars while the notes loop 16 times. Useful for very slow automation, but skip this for now.

## Related

- [[../Techniques/acid-lead-sound|Acid Lead Sound]] — the parameters you'd most want to automate on an acid lead (cutoff, resonance)
- [[../Track-Sketches/techno-sketch-01|Techno Sketch 01]] — first place clip envelopes get used in anger (Session 4)
- [[arrangement-view-basics|Arrangement View Basics]] — the *other* place automation lives (track-level, on the timeline)
