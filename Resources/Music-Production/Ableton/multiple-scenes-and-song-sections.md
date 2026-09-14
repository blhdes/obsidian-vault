---
title: Multiple Scenes & Song Sections
date: 2026-05-29
tags: [ableton, session-view, scenes, song-structure, arrangement]
---

# Multiple Scenes & Song Sections

One scene = one moment of your track. **Multiple scenes** = multiple moments you can jump between → the first taste of **song structure**.

This is where Session View shines: you sketch out an Intro, a Drop, a Break, etc. as separate scenes, then play with the order before committing to an arrangement.

## Why multiple scenes?

A track is rarely "the same 2 bars for 4 minutes." It has **sections** that come and go:

| Section | Typical role | Often in electronic music |
|---|---|---|
| **Intro** | Sets the vibe, sparse | Just bass, or just hi-hats — builds tension |
| **Drop** | Full energy, all elements playing | Drums + bass + lead — the payoff |
| **Break** | Sudden contrast, less elements | Drop the drums, leave the bass, or vice versa |
| **Outro** | Winds down | Reverse of intro |

Each section = **a different combination of clips** = **one scene**.

## Creating a new scene

- **Mac:** `Cmd + I` (Insert Scene)
- **Win/Linux:** `Ctrl + I`
- Or: top menu → **Create → Insert Scene**

A new empty row appears below the selected scene.

## Duplicating a scene (the fast way to create variations)

If your current scene has drums + bass and you want a *variation* (e.g. same bass but no drums):

1. **Right-click** the scene name (right side of Master) → **Duplicate**.
2. An identical copy appears below.
3. Edit the new scene — e.g. delete the drum clip to create a break.

This way you don't redraw the bass; you're just **modifying a copy**.

## Copying a single clip to another scene

If you only want to move/copy one clip:

- **Hold Option (Mac) / Ctrl (Win)** and drag a clip to another cell → makes a **copy**.
- Or: select clip → `Cmd+C` → click target cell → `Cmd+V`.
- **Without** holding Option, dragging just **moves** the clip.

## The empty-cell rule (important!)

When you launch a scene, **empty cells in that scene act as STOP signals** for their track.

So if:
- Scene 1: drums + bass
- Scene 2: bass only (empty drum cell)

→ Launching scene 2 **stops the drums** (because the drum cell is empty in scene 2).

If you want drums to **keep playing**, the drum clip must exist in scene 2 too (duplicate it across).

## A 3-scene mini-arrangement

A classic dance-music intro → drop → break:

```
            Drums       Bass        Scene
Scene 1     [ empty ]   [ bass ]    ▶  Intro    ← bass only
Scene 2     [ drums ]   [ bass ]    ▶  Drop     ← full groove
Scene 3     [ drums ]   [ empty ]   ▶  Break    ← drums only
```

- Launch **Intro** → only bass plays.
- Switch to **Drop** → drums kick in, bass continues.
- Switch to **Break** → drums continue, bass drops out.
- Switch back to **Drop** → bass returns.

You've just performed a small live arrangement.

## Launch Quantization (why scene jumps sound musical)

When you click a scene play, Live doesn't switch *instantly* — it waits for the next bar boundary so the transition lands on the beat.

This is controlled by **Global Launch Quantization** in the **Transport bar (top)** — a small dropdown that defaults to **"1 Bar"**.

| Setting | Behavior |
|---|---|
| **None** | Instant switch (usually sounds off-beat / messy) |
| **1 Bar** *(default)* | Waits until the next bar → clean musical jumps |
| **2 / 4 / 8 Bars** | Even longer wait — great for big transitions in long-form sets |

Leave it on **1 Bar** for now. Just know it's there.

## Renaming scenes

Right-click the scene name → **Rename**. Always do this once you know what each scene represents (`Intro`, `Drop`, `Break`). Makes the grid instantly readable.

## What's *not* here yet

You can now perform a small track *live* by jumping between scenes — but nothing is **recorded as a finished song**. Next session: bring these scenes into **Arrangement View** to commit a real, exportable track timeline.
