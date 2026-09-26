---
title: Drift Stab From Scratch (Phrygian b9)
date: 2026-07-22
tags: [ableton, drift, sound-design, stab, techno, hardgroove]
---

# Drift Stab From Scratch (Phrygian b9)

Hardgroove 134's STAB layer, built the same way as [[drift-kick-from-scratch|the kick]] — from a cleared Drift patch, one parameter at a time — but polyphonic and pitched, where the kick was mono and effectively unpitched.

## The recipe

| Stage | Setting | Why |
|---|---|---|
| **Voices** | 32 (poly) | Opposite of the kick/sub's mono rule — a chord needs several notes ringing at once |
| **Oscillator** | Osc 1 only, **Square**, Osc 2/Sub/Noise off | Square carries more harmonic content than the kick's plain sine — needed so a filtered chord still reads clearly as a chord |
| **Envelope 1** (hardwired amp env) | Attack ~0-2ms, Decay ~150-250ms, Sustain 0% | Stab shape, not pad — self-terminates like the kick, just with a touch more decay time so the chord's color is audible before it cuts |
| **Filter** | Low Pass **Type I** (12dB/oct, DFM-1 circuit — grittier, feeds its own distortion back internally), Freq ~900Hz | Square is bright/buzzy; darkening it is what turns "raw square wave" into "stab." Type I chosen over Type II (24dB/oct, cleaner Cytomic MS2 circuit) for extra grit matching the raw/industrial aesthetic |

## Drift's two Low Pass filter types

New to this session: Drift's Filter section offers a **Type** switch, not a Low/High/Band-pass choice — both options are low-pass, differing in circuit character:

- **Type I** — 12 dB/octave, modeled on a DFM-1 circuit that internally feeds back more of its own distortion. Gentler slope, dirtier.
- **Type II** — 24 dB/octave, modeled on a Cytomic MS2 circuit (Sallen-Key design, soft resonance clipping). Steeper slope, cleaner.

There's also a separate, always-present **HP** knob in the same section — an independent fixed high-pass, not part of the Type toggle.

## The chord: Cm(b9), no root, no 7th

See [[../Theory-Basics/phrygian-mode|the Phrygian mode]] for why the b9 (not a plain 9) is the color tone here. Four voicings were compared before choosing:

| Voicing | Notes | Character |
|---|---|---|
| **Chosen: no b7, no root** | Eb3 - G3 - Db4 | Leanest — just b3/5/b9, most tension, most "raw" |
| With b7, no root | Eb3 - G3 - Bb3 - Db4 | Fuller, more "chord," less stark |
| With root, no b7 | C3 - Eb3 - G3 - Db4 | Re-states the root the kick/sub already own |
| Full (root + b7) | C3 - Eb3 - G3 - Bb3 - Db4 | Most complete/jazzy, least raw |

**Root dropped deliberately** — same logic as Ticket to Detroit's stab: KICK and SUB already state C firmly in the low end, so the stab doesn't need to repeat it. Fewer notes = more tension per note, which suited this track's rawer aesthetic better than the fuller jazz-chord versions.

## Placement in the existing groove

Stab is a rhythm instrument, not a constant pad — one hit, placed in a genuinely free slot. Checking what the rest of the kit already occupies (kick on the quarters, sub on the `&`s, rim/shaker in two of the `e`/`a` 16ths) left several 16th slots open; the stab took **the `a` of beat 3** — a 16th-note anticipation into beat 4, same "push toward the next strong hit" logic as [[syncopated-bassline|the syncopated bassline]]'s turnaround.

```
         1 e & a 2 e & a 3 e & a 4 e & a
Kick   : ●  ·  ·  ·  ●  ·  ·  ·  ●  ·  ·  ·  ●  ·  ·  ·
Sub    : ·  ·  ●  ·  ·  ·  ●  ·  ·  ·  ●  ·  ·  ·  ●  ·
Perc   : ·  ·  ·  ·  ·  ·  ·  ●  ·  ·  ·  ·  ·  ·  ·  ●
Stab   : ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ●  ·  ·  ·  ·
```

One hit per bar to start — confirmed sounding good; a second hit can be added later if it feels too sparse once heard against the full mix.

## See also

- [[drift-kick-from-scratch|Building a Kick From Scratch in Drift]] — the mono/percussive counterpart to this poly/tonal build
- [[../Theory-Basics/phrygian-mode|The Phrygian Mode]] — the theory behind the b9 chord choice
- [[detroit-chord-stab|Detroit Chord Stab]] — the earlier (preset-based, A minor) stab this reuses the "rhythm instrument, syncopated weak position, drop the root" logic from
