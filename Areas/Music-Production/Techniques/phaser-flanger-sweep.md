---
title: Phaser-Flanger Sweep
date: 2026-07-22
tags: [ableton, effects, phaser, flanger, sound-design, stab]
---

# Phaser-Flanger Sweep

Also a merged device: **Phaser** and **Flanger** are both sweeping modulation effects, but built on different mechanics, giving different characters. A **Mode** switch picks between them.

## Phaser vs. Flanger

| | Phaser | Flanger |
|---|---|---|
| **Mechanism** | All-pass filter stages create moving *notches* in the frequency spectrum | A very short delay (milliseconds) with feedback, swept over time |
| **Character** | Smooth, swirling "swoosh" — subtler | Metallic, "jet plane" sweep — more pronounced, can self-resonate at high Feedback |

Both are still LFO-driven movement, same as [[auto-filter-movement|Auto Filter]] and [[chorus-ensemble-width|Chorus-Ensemble]] — the difference is *what* the LFO modulates (filter notches vs. delay time) and how dramatic the resulting sweep sounds.

## Key controls

| Control | What it does |
|---|---|
| **Mode** | Phaser or Flanger |
| **Rate** | Speed of the sweep |
| **Amount** | Depth of the sweep |
| **Feedback** | How much of the effected signal re-enters — higher on Flanger = more resonant/metallic |
| **Poles / Notch count** (Phaser) | More stages = denser, more complex sweep |

## Starter recipe — if used on STAB (Hardgroove 134)

- Mode: **Phaser** first (smoother, less likely to clash with Auto Filter's own filter movement already on this chain).
- Rate in a similar ballpark to Auto Filter's LFO, or deliberately different, to A/B which feels more musical against the existing pulse.
- Keep Feedback low at first — Flanger especially can turn harsh/resonant fast.
- A/B against bypass, and against Chorus-Ensemble, to judge which (if either) actually earns a permanent slot here.

## A note on stacking

Auto Filter + Chorus-Ensemble + Phaser-Flanger all at once on one STAB voice is three independent modulation sources moving simultaneously — a real risk of turning a "tight and dry" hardgroove stab into something mushy/undefined. Worth choosing at most one or two to keep here, and saving the rest as options for **LEAD**, a different role where a different character might fit better.
