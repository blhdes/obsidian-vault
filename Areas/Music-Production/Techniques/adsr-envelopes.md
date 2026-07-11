---
title: ADSR Envelopes (Stab vs Pad)
date: 2026-07-10
tags: [sound-design, envelopes, adsr, pads, synthesis]
---

# ADSR Envelopes

An **envelope** is the shape of a sound's loudness over its lifetime. Every synth has one on its volume (the *amplitude envelope*), controlled by four dials — **ADSR**:

```
 level
   ▲      ╱╲  ← D
   │     ╱  ╲__________
   │  A ╱       S      ╲  ← R
   │   ╱                ╲
   └──┴─────────────────┴───► time
      key down        key up
```

| Dial | Means | Unit |
|---|---|---|
| **A**ttack | How long the sound takes to reach full volume after the key goes down | time |
| **D**ecay | How long it takes to fall from that peak to the sustain level | time |
| **S**ustain | The volume held for as long as the key stays down | **level**, not time |
| **R**elease | How long the sound takes to fade after the key is released | time |

The [[acid-lead-sound|filter envelope]] from the acid lead is the same idea aimed at the cutoff instead of the volume.

## One knob pair, two opposite instruments

| | Attack | Release | Result |
|---|---|---|---|
| **Stab** | fast (~0 ms) | short | percussive hit — rhythm |
| **Pad** | slow (100–500+ ms) | long (1 s+) | blooming bed — atmosphere |

Same synth, same chord — the envelope alone decides which one you have. That's why "envelope" is the first sound-design dial worth really knowing.

## Pad recipe (Detroit string bed)

- Strings/pad preset, **slow attack** until the chord *blooms* instead of starting, **long release** so bars melt into each other.
- Hold one chord ([[../Theory-Basics/sevenths-and-ninths|Am9]]) for a whole 2-bar clip — a bed, not a melody.
- **Darken with the low-pass filter** — the pad is felt, not heard.
- Mix it *quiet* (≈ −15 dB region): the test is muting it — you should notice the room got emptier, not that an instrument stopped.
- **No groove file needed**: held whole notes have nothing on the swung 16th positions — grooves only matter for rhythmic clips.
