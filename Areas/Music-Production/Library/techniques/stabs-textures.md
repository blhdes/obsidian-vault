---
topic: Stabs and textures
type: technique
updated: 2026-09-26
related: [[devices/wavetable]], [[devices/drift]], [[techniques/returns]], [[devices/effects-overview]]
---

# Stabs and textures

## Summary
Stabs are short and dissonant, and their space comes from returns. Textures are slow, low in the mix, and exist for tension rather than melody. Leads, if any, are small motifs. Zero melodic parts is a valid choice.

## Core — stabs
| Step | Direction | Source |
|---|---|---|
| Source | Wavetable or Analog. Operator for FM stabs. Drift works (see below) — a starting choice, not a rule | [?] |
| Voicing | Minor 2nds, tritones, or one detuned note. Drop the root if the kick/sub already state it | [ear] |
| Envelope | Short amp decay, short filter envelope | [ear] Hardgroove 134, 2026-07-22 (Drift stab below) |
| Rhythm | One chord on a weak 16th (e.g. the `a` of 3), never with the kick. Same groove file as the drums | [ear] Hardgroove 134, 2026-07-22 |
| Space | B-DELAY / A-SPACE throws, not a long release | [ear] |

**Drift stab** [ear] Hardgroove 134, 2026-07-22: Voices 32 (poly) · Osc 1 **Square**, the rest off · Env 1 A 0–2 ms, D 150–250 ms, S 0% · Low Pass **Type I** ~900 Hz · voicing Eb3–G3–Db4 (C Phrygian b9, no root, no 7th).

## Core — leads / bleeps
| Step | Direction | Source |
|---|---|---|
| Motif | 3–5 notes, call (bar 1) and response (bar 2). Same rhythm, different notes. End on the root | [ear] Ticket to Detroit, 2026-07-10 |
| Space | Leave a beat empty. Sparse = hypnotic | [ear] Ticket to Detroit, 2026-07-10 |
| Register | Above the stab's top note (octave 5 region) | [ear] Ticket to Detroit, 2026-07-10 |
| Bleep sound | Drift, mono, sine/triangle, fast attack, short decay | [ear] Ticket to Detroit, 2026-07-10 |
| Too clean? | Osc 2 on, same wave, detune ~5–15 cents, before adding more effects | [ear] Hardgroove 134, 2026-07-24 |

## Core — textures / drones / pads
| Step | Direction | Source |
|---|---|---|
| Source | Wavetable, **Meld**, or field recordings through Spectral Resonator / Spectral Time → [[devices/effects-overview]] | [manual] |
| Meld in short | 2 engines (A/B), each a full synth: 24 oscillator types (6 scale-aware, incl. Chord since 12.2), own filter, Amp + Mod envelopes with loop modes, 2 LFOs (LFO 1: Basic Shapes, Ramp, Wander, Alternate, Euclid, Pulsate + 2 LFO FX slots; LFO 2: classic shapes), MIDI/MPE Modulation Matrix, 2 oscillator-specific macro knobs | [manual] |
| Movement | LFOs in bars (not beats) on wavetable position, cutoff, pan. Routing: Wavetable Matrix tab ([[devices/wavetable]]) or an M4L LFO in Mod mode | [manual] routing · [?] bar-length rates |
| Pad | Slow attack, long release, low-pass darkened, one chord held for the clip | [ear] Ticket to Detroit, 2026-07-10 |
| Level | Low. Felt more than heard | [ear] |

## Variants
- **Stab movement:** Auto Filter (synced LFO 1/16–1/8), Chorus-Ensemble (width) or Phaser-Flanger (swirl). Pick one. Stacking all three turns a tight stab into mush. Chorus-Ensemble was the one kept. [ear] Hardgroove 134, 2026-07-23

## Gotchas
- An unfiltered square/poly stab sounds cheesy. Close the low-pass partway. [ear]

## Used in
- Ticket to Detroit (stab, bleep, pad, 2026-07-10) · Hardgroove 134 (stab, lead, 2026-07-22/24)

## Sources
- Live 12 manual, Meld / Wavetable: https://www.ableton.com/en/manual/live-instrument-reference/
