---
title: Beat Repeat Stutter Build
date: 2026-07-25
tags: [ableton, beat-repeat, glitch, transitions, techno]
---

# Beat Repeat Stutter Build

**Beat Repeat** is a rhythmic effect that grabs a short segment of whatever audio is passing through it and loops that segment in place of the signal continuing normally. Unlike [[riser-fx|the Noise riser]], it doesn't generate its own sound — it needs real audio already playing on the track to chop up.

## Core parameters

| Parameter | What it does |
|---|---|
| **Interval** | The length of the chunk grabbed and repeated (a note value: 1/4, 1/8, 1/16, 1/32...). The main "speed" knob — shorter Interval = faster, choppier stutter. |
| **Grid** | Quantizes exactly when a new Interval can start, keeping the chop locked to the beat. |
| **Chance** | Probability (0–100%) that a repeat actually triggers at each Interval boundary. Low = occasional glitches poking through the normal signal; 100% = the repeat takes over completely. |
| **Gate** | How much of each Interval is actually audible (a duty cycle within the chunk) — short Gate reads choppier/percussive, full Gate reads as a smoother loop. |
| **Variation: Pitch / Volume** | Randomizes each successive repeat's pitch and level — stops the stutter sounding perfectly mechanical, gives it a "breaking down" character. |
| **Filter** | An onboard filter shaping the tone of the repeated material, separate from anything already on the track. |

## The build technique

Same underlying principle as the Noise riser — **two parameters climbing together read as one build event** — just rhythmic instead of tonal:

1. Automate **Interval** stepping down from a longer value (e.g. 1/8) to a much shorter one (e.g. 1/32) across 1–2 bars. The repeated chunk gets shorter and shorter, so the stutter audibly accelerates — the classic "machine-gun" rush into a transition.
2. Optionally also automate **Chance** rising from a lower value (~30%) to 100% over the same span, so the glitch fades in rather than snapping on at full intensity immediately.
3. Outside the transition bars, **Chance sits at 0%** (or the device is bypassed) — the track passes through completely unaffected, same as the Noise riser's Loop-off "fires once" behavior.

## Placement — it needs a host, not its own empty track

Because Beat Repeat has nothing to chop without existing audio, it's inserted as the **last device on an already-playing track's chain** — not a fresh empty MIDI track like the Noise riser was. On Hardgroove 134, it goes at the end of **HATS**'s chain: hats are already high-frequency, percussive one-shots, so a shrinking-Interval stutter reads cleanly as a hi-hat-roll-style build without disturbing the KICK/SUB low-end groove underneath.

Automating Interval/Chance only during a transition clip reuses the already-known [[../Ableton/clip-envelopes|clip envelope]] mechanic — no new automation workflow, just a new destination.

## Why this over the Noise riser here

A synthesized noise sweep is a very EDM-coded build. A stutter/glitch edit built from the track's *own* drum content is a more idiomatic techno transition device, and it exercises a genuinely new stock Lite effect (Beat Repeat) rather than reapplying an already-mastered recipe verbatim.

## Gotchas

- Beat Repeat is silent/inert with nothing playing through it — confirm the host track actually has audio at the moment the effect engages.
- A Chance of 100% with a very short Interval for too long reads as noise/texture rather than a rhythmic figure — same audio-rate-vs-movement threshold idea seen with LFOs elsewhere in this project; keep the shortest Interval values brief (the last few beats of the build only).
