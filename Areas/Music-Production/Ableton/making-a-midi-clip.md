---
title: Making a MIDI Clip (Piano Roll + Recording)
date: 2026-05-28
tags: [ableton, midi, clips, piano-roll, patterns]
---

# Making a MIDI Clip

So far we've **played** notes live — but the moment you stop pressing keys, the sound dies. A **MIDI clip** captures notes so they **loop on their own**, freeing your hands to do other things (load another track, play another part on top).

This is where you go from "playing" → "making a pattern."

## What's a MIDI clip?

A **container of notes** sitting in a cell on a MIDI track. When you play it, Live reads those notes and feeds them to the instrument on the track.

Two ways to fill one:

| Method | Best for |
|---|---|
| **Drawing** with the mouse in the piano roll | Beginners, exact patterns, no rhythm pressure |
| **Recording** live from QWERTY (or a keyboard) | Capturing ideas you play by feel |

We'll learn drawing first — it's cleaner and removes performance anxiety. Recording comes right after.

## Quick theory: beats and bars

Before drawing anything, you need to know what the grid means.

- **BPM (beats per minute)** = the speed. Default in Live is **120 BPM** = 120 beats every minute = 2 per second. (Adjust top-left of the Transport Bar.)
- **Beat** = one "click" of the metronome. Tap your foot — that's a beat.
- **Bar** = a group of beats. In most electronic music: **4 beats per bar** (called "4/4 time"). One bar at 120 BPM = 2 seconds.

So a **1-bar loop at 120 BPM** is 2 seconds long, with 4 beats inside it.

## Creating an empty MIDI clip

1. On a **MIDI track** (with an instrument loaded), find an empty cell.
2. **Double-click** the empty cell → Live creates an empty 1-bar MIDI clip.
3. The clip is automatically selected, and the **MIDI Editor** opens at the **bottom of the screen** (this is called *Clip View*).

If you don't see Clip View at the bottom, press **`Shift + Tab`** to toggle between **Device chain view** and **Clip view**.

## Anatomy of the MIDI Editor (the piano roll)

```
┌─────────────────────────────────────────┐
│  [Loop brace] ←—— defines what loops    │
│  ─────────────────────────────────────  │
│  ♪│                                     │  ← Piano keyboard
│   │  ░░░░░    ░░░░░    ░░░░░    ░░░░░  │     (vertical = pitch)
│  ♪│                                     │
│   │                                     │  → horizontal = time
│  ♪│            ███                      │     (beats and grid)
│   │  ███             ███         ███    │
└─────────────────────────────────────────┘
   1.1.1     1.2     1.3     1.4    2.1
```

- **Piano keyboard on the left** → vertical axis = which note (higher = higher pitch).
- **Horizontal axis** → time, divided into beats (1, 2, 3, 4) and finer grid lines.
- **Loop brace at the top** → the gold/grey bracket that marks what part of the clip loops.

## Drawing notes (the Pencil tool)

1. Press **`B`** to toggle the **Pencil tool** (or click the pencil icon in the top bar).
2. **Click on the grid** → places a note where you clicked. The vertical position picks the pitch, the horizontal position picks the timing.
3. **Click on an existing note with the pencil** → deletes it.
4. Press **`B`** again to go back to the **arrow** (selection) tool — useful for moving notes by dragging.

> 🔍 Hold **`Cmd + scroll`** to zoom horizontally; scroll vertically with the side scrollbar. Things get easier when you can see the grid clearly.

## Your first pattern: four-on-the-floor + backbeat

This is the **foundational electronic dance pattern** (house, techno, disco — everywhere). Genre-neutral starting point.

On a Drum Rack with your standard kit:

```
         1 & 2 & 3 & 4 &
Kick   : ● · ● · ● · ● ·
Snare  : · · ● · · · ● ·
Hi-Hat : ● ● ● ● ● ● ● ●
```

**How to read it:**
- Top row = the count. Musicians count a bar of 4/4 as **"one-and-two-and-three-and-four-and"** — numbers are the beats, `&` are the 1/8 notes in between.
- `●` = a drum hit, `·` = silence.
- Read each row left-to-right in time.

What's happening:
- **Kick** on every beat (1, 2, 3, 4) — the "four-on-the-floor"
- **Snare/Clap** on beats 2 and 4 — the "backbeat"
- **Hi-Hat** on every 1/8 (every column) — the constant tick

Find the kick/snare/hi-hat rows on the piano roll (they correspond to specific drum-rack pads — typically C1, D1, F#1) and place notes accordingly.

Hit the **play triangle** on the clip → you have a loop.

## Recording instead of drawing

If you'd rather **play** the notes in:

1. **Arm** the MIDI track (red round button on track).
2. Make sure **Computer MIDI Keyboard** is on (`Shift+Cmd+K`).
3. Click the small **circle (record) button** at the bottom of an empty clip slot. Live counts you in (if the metronome is on) and records what you play.
4. When you stop, the clip plays back what you recorded.

**Clean up the timing** with **quantize**: select all notes (`Cmd+A` inside the clip) → press **`Cmd+U`**. Notes snap to the nearest grid line, fixing wobbly timing.

## Looping

- Clips in Session View **loop automatically** for as long as you let them play.
- The **loop brace** at the top of the piano roll controls *what* loops. Drag its edges to make the loop shorter or longer.
- The clip length is shown in Clip View on the left side panel (default: 1 bar).

## What's *not* here yet

- We've only built **one loop**. Next: build a **second loop** (e.g. a bassline on another MIDI track), play them together, then bring them into **Arrangement View** to start shaping a full track.
