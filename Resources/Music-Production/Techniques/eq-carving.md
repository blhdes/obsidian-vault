---
title: EQ Carving (Subtractive EQ)
date: 2026-07-16
tags: [techniques, mixing, eq, techno]
---

# EQ Carving (Subtractive EQ)

With 6 tracks playing at once (drums, rumble, perc, bass, stab, riser), several of them naturally want the **same frequency space** — every synth and sample has some low-end content whether it needs it or not. Left unchecked, those overlaps stack into mud, and the kick/bass stop punching through.

**The subtractive philosophy:** when two things clash in the same range, **cut one of them there** instead of boosting the other louder. Boosting to "cut through" just raises the overall volume war; cutting the thing that doesn't need that range frees it up for the thing that does.

## The one move that matters most: high-pass everything that isn't bass

A **high-pass filter** removes everything *below* a chosen frequency. Almost everything except the kick, rumble, and bass has no business carrying deep low end — that's not where their character lives, it's just mud riding along underneath.

```
Kick / Rumble / Bass  →  own the low end, leave them alone
Everything else        →  high-pass filter, roll off what they don't need
```

## Applying it to Solo Sketch 138

| Track | Move | Why |
|---|---|---|
| Cashon Kit (drums) | Leave as-is | The kick *is* the low end here |
| Rumble | Leave as-is | Already EQ'd on purpose ([[rumble-bass\|built that way]]) |
| Chord Analog (bass) | Leave as-is | This *is* the bass |
| Polymeter perc | High-pass ~150–250 Hz | Percussive texture, no low end needed |
| Stab Dub Direct | High-pass ~150–300 Hz | Frees room for the bass underneath it |
| Raiser | Leave as-is | Already shaped by its own filter automation |

## How

Drop a **Channel EQ** or **EQ Eight** after the instrument on the track's Device chain. Both have a high-pass control — Channel EQ's is the **HP** knob/switch, EQ Eight lets you set Band 1 to **HP** and drag its frequency point up.

Sweep the frequency up while listening: **stop right before the sound loses its "body"** — that point is usually well below the sting/character of the sound, meaning it can go.

## Stock-devices-only version (EQ Three)

Hardgroove 134's rule bans Channel EQ/EQ Eight — high-pass has to come from **EQ Three** instead, and the knob to reach for isn't the obvious one:

- **FreqHi** is the Mid/High crossover (for brightness/shimmer) — by design it won't go low enough to serve as a rumble-removal high-pass (floor is ~200Hz on this build).
- **FreqLow** is the real tool: it's the Low/Mid crossover. Set it to the target cutoff (~150–250Hz for percussion), then hit the **"L"** button under GainLow to fully switch that band off. That L toggle — not the GainLow knob — is what turns it into a genuine hard cut rather than a partial shelf reduction.

## Gotchas

- **Cut don't boost** is the default instinct, not a hard rule — a small boost is fine once cuts have already made room.
- High-pass conservatively. Too aggressive and thin, weak-sounding elements are the result — sweep by ear, not to a fixed number.
- **A/B with the filter bypassed** (device on/off LED) — the difference should be "tighter low end, same character," not "thinner sound."
