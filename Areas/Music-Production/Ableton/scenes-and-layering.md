---
title: Scenes and Layering Clips
date: 2026-05-28
tags: [ableton, session-view, scenes, layering, bass]
---

# Scenes and Layering Clips

Your drum pattern is alone. Now we add a **second clip on a second MIDI track** (a bassline) and learn how **scenes** let us launch both clips at the exact same time.

This is the first step toward an actual track: **layering parts**.

## Adding a new MIDI track

If you don't already have a free MIDI track:

- **Mac:** `Cmd + Shift + T`
- **Win/Linux:** `Ctrl + Shift + T`
- Or: top menu → **Create → Insert MIDI Track**

A new empty MIDI column appears.

## Loading a bass instrument

1. Click the new MIDI track to select it.
2. Browser → **Sounds → Bass** → pick any preset (start with something simple like "Sub Bass" or "Analog Bass").
3. **Double-click** it to load.

> 💡 If "Bass" looks empty, try **Categories → Instruments → Drift / Wavetable / Analog** and pick a Bass preset from there instead.

## Placing the clip on the **same scene** as the drums

Each **row** in Session View is a scene. We want both clips to belong to the *same* scene so they play together.

1. Find the row where your drum clip sits.
2. **Double-click** the empty cell in that same row, in the bass track's column → empty MIDI clip + piano roll opens.

```
            Drums MIDI    Bass MIDI    Master
Scene 1     [ drums ]     [ bass ]     ▶  ← launches both
Scene 2     [       ]     [       ]     ▶
Scene 3     [       ]     [       ]     ▶
```

## Drawing a simple bassline

Goal: **one note per beat**, locked with the kick.

1. In the piano roll, find **C2** on the left keyboard (lower than middle C, but still in bass range).
2. Press **`B`** for the Pencil tool.
3. **Click on C2 at each beat** (positions 1.1.1, 1.2.1, 1.3.1, 1.4.1) → 4 notes total.
4. **Important — make the notes longer:** the pencil draws short 1/16 notes by default. For a sustained bass thump, **drag horizontally** while clicking, or **drag the right edge** of each note after placing it. Aim for one full beat (a quarter note).

```
         1 & 2 & 3 & 4 &
Bass C2: ●—— ●—— ●—— ●——
```

Each `●——` is a single note that sustains for one full beat.

> 💡 If C2 sounds too low / muddy, try C3. If too high, try C1. Bass should *feel* — not muddy, not weak. Trust your ears.

## Scenes — playing both clips together

Up to now we've launched single clips. **Scenes launch a whole row at once.**

- On the **right side of the Master track** (far right), each row has a small **triangular play button** plus a name (default: "1", "2", "3"...). That's the **scene launch**.
- Click a scene's play button → **every clip in that row** starts playing in sync.

So: drum clip + bass clip on the same row → hit the scene play → **both play together, perfectly aligned**.

### Renaming scenes

- Right-click a scene name (right of Master) → **Rename**.
- Useful names: `Intro`, `Drop`, `Verse`, `Break`. Helps you think of each scene as a *song section*.

## Why this matters

This is the **non-linear sketching** Session View is built for:
- Scene 1: just drums
- Scene 2: drums + bass
- Scene 3: drums + bass + melody
- Scene 4: just bass + melody (drop break)

You can jump between them live to test different combinations *before* committing to an arrangement.

## What's *not* here yet

We've layered **two clips** on **one scene**. Next: build **multiple scenes** (different combinations of clips) and start to think in **song sections**. After that, we move into Arrangement View to commit a real track timeline.
