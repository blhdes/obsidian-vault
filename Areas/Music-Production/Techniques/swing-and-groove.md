---
title: Swing & Groove (The Detroit Shuffle)
date: 2026-07-10
tags: [groove, swing, drums, groove-pool, ableton, detroit]
---

# Swing & Groove

**Swing** = pushing the *offbeat 16ths* (the `e` and `a` positions) slightly **late**, so the beat rolls instead of marching. It's the difference between a drum machine sounding stiff and sounding funky. Genre-wise: house, garage, and Detroit techno lean on it heavily; a lot of harder/industrial techno stays nearly straight — it's a dial, not a rule.

## The percentage

Swing amount is written as a **%** — how far the offbeat 16th is pushed toward the *next* 16th:

| % | Feel |
|---|---|
| **50%** | Perfectly straight (no swing) |
| **54–58%** | Subtle roll — you feel it more than hear it (classic house/Detroit zone) |
| **60–66%** | Obvious shuffle; 66% ≈ full triplet feel |

The TR-909's **shuffle** function did exactly this per-pattern — a big part of why Detroit and Chicago records roll the way they do.

## Key insight: swing needs 16ths to act on

16th swing only moves notes sitting **on** `e`/`a`. Kick on quarters, clap on 2 & 4, open hats on `&` — none of those move. So a pattern made only of 8ths sounds identical with swing on. First fill the hats to a 16th stream, *then* swing:

```
         1 e & a 2 e & a 3 e & a 4 e & a
Kick   : ● · · · ● · · · ● · · · ● · · ·
Clap   : · · · · ● · · · · · · · ● · · ·
Closed : ● ● · ● ● ● · ● ● ● · ● ● ● · ●
Open   : · · ● · · · ● · · · ● · · · ● ·
```

- Closed hats skip the `&` so they don't choke the ringing open hat.
- The new `e`/`a` closed hats get **lower velocity** (~60–80) — texture, not lead. These are exactly the notes swing will move.

## Applying it in Live: the Groove Pool

Grooves are **non-destructive timing/velocity templates** you drop on a clip:

1. **Browser → search "swing"** (groove files, `.agr`). Pick a 16th one — the MPC-style swing grooves with a % in the high 50s are the classic zone.
2. **Drag the groove onto the clip.** The clip plays swung immediately; the notes on screen don't move.
3. Open the **Groove Pool** — the wave button at the bottom-left of the Browser. Every loaded groove shows parameters:
   - **Base** — the grid resolution the groove reads (16ths here)
   - **Timing** — how strongly the timing shifts apply (your main dial)
   - **Random** — adds humanizing timing jitter (small doses)
   - **Velocity** — how much the groove's velocity pattern overrides yours
   - **Amount** (global, bottom of the pool) — master multiplier for all grooves
4. **A/B it:** set the clip's Groove chooser (Clip View) back to **None**, or swing the global Amount between 0% and 100%.
5. **Commit** (button in Clip View next to the Groove chooser) *prints* the groove into the actual notes and clears the slot. Leave it uncommitted while still deciding — it stays adjustable.

## Rule of thumb

Set Timing/Amount **higher than feels right, then back it off**. Swing is like salt — the right amount is barely noticeable, you only notice when it's gone (A/B against None to check).
