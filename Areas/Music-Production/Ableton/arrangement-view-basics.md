---
title: Arrangement View Basics
date: 2026-05-29
tags: [ableton, arrangement-view, timeline, recording, song]
---

# Arrangement View Basics

So far we've lived in **Session View** — the grid for sketching and performing. Now we cross into **Arrangement View** — the **timeline** where a sketch becomes a **finished, exportable track**.

The fastest way to get there: **record your Session performance into Arrangement** with one button.

## Tab to switch views

Press **`Tab`** → Arrangement View opens. Same project, totally different layout.

## Anatomy of Arrangement View

```
┌─────────────────────────────────────────────┐
│ ▶ Timeline ruler  |1   2   3   4   5   6 …  │  ← bars across the top
│ ─────────────────────────────────────────── │
│ Drums   ▶   ███████   ███████               │  ← tracks stacked vertically
│ Bass    ▶   ░░░░░░░   ░░░░░░░   ░░░░░░░     │     clips = horizontal blocks
│ Master                                      │
└─────────────────────────────────────────────┘
                ↑ Playhead (vertical line) moves during playback
```

- **Timeline ruler (top)** — numbered bars (1, 2, 3, …). Click anywhere to move the playhead.
- **Tracks** — the same tracks as Session, now stacked horizontally.
- **Clips** — appear as **rectangular blocks** on their track, positioned in time.
- **Playhead** — the vertical line showing the current play position.
- **Loop brace** — the bracket at the very top (above the ruler) that defines a loop region.

## The magic workflow — record Session into Arrangement

This is the fastest way to turn your Session scenes into a real timeline.

1. **Switch to Session View** (`Tab`) — make sure nothing is currently playing (hit Stop in transport if needed).
2. In the **Transport bar (top)**, click the **Global Record button** — the round circle next to Play. It turns **red** = armed for arrangement recording.
3. **Click your first scene's play button** (e.g. `Intro`). This starts playback **and** starts recording into Arrangement at bar 1.
4. **Perform** — launch your other scenes (`Drop`, `Break`, back to `Drop`, etc.) as you'd play them live.
5. When done, hit **Stop** in transport (or `Spacebar`).
6. Press **`Tab`** → you're in Arrangement → **your performance is laid out as clips on the timeline.** 🎉

> 💡 Don't worry about timing your scene launches perfectly — **Launch Quantization** still works during recording, so scene jumps land on bar boundaries.

### Recording individual clip launches too (not just scenes)

Global Record captures **every** launch you make in Session View while it's armed — not only whole-scene launches. If a clip lives outside your scene rows (like a one-shot [[../Techniques/riser-fx|riser]] you trigger by hand a bar or two before the Drop), just click that clip's play button at the right moment during the same take. It lands on the timeline exactly where you fired it, alongside the scene clips. One take, mixed sources, still one continuous recording.

## Playing back the Arrangement

- **`Spacebar`** → play / stop.
- Click anywhere on the **timeline ruler** → moves the playhead there.
- **Press Stop twice** → playhead jumps back to bar 1.

### "Why is my Session playing instead of Arrangement?"

If you trigger a Session clip *while* Arrangement is playing, the Session takes over for that track. A small **yellow rectangle icon** appears at the top of Arrangement View → click it to **return to Arrangement playback** for all tracks.

## Basic editing on the timeline

Once your clips are in Arrangement, you can shape them:

| Action | How |
|---|---|
| **Move a clip** | Click and drag the body of the clip |
| **Trim** (shorten/extend) | Drag the **left or right edge** of the clip |
| **Duplicate** | Select clip → **`Cmd+D`** (creates a copy right after it on the timeline) |
| **Delete** | Select → `Delete` key |
| **Split** | Place playhead → **`Cmd+E`** to cut the clip at that point |

> 🔍 Zoom horizontally: **`+` / `−`** keys, or `Cmd+scroll`. Zoom vertically with the small `+`/`−` near the track headers.

## The Loop region (working on one section)

The **bracket above the timeline ruler** is the **loop region**. Useful when you want to focus on one part of the track.

1. Click the **loop toggle** in the Transport (an orange-bracket icon) to turn looping on.
2. Drag the loop brace to cover the bars you want to loop (e.g. bars 5–12).
3. Hit play → it loops those bars only.

## Locators (timeline markers)

Locators are **named markers** on the timeline — useful for navigating long tracks (`Intro`, `Drop 1`, `Break`, `Drop 2`).

- Place a locator: with playhead at the desired position → **Create → Add Locator** (or right-click on the scrub area → Add Locator).
- Click the locator name to jump the playhead there.

## What's *not* here yet

You can record, edit and play back a real track timeline. Next: a touch of **mixing** (track volumes, panning, basic effects) and **exporting** to an audio file (MP3 / WAV) you can share or DJ with.
