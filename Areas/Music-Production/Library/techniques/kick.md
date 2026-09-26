---
topic: Kick
type: technique
updated: 2026-09-26
related: [[devices/operator]], [[devices/drift]], [[techniques/rumble]], [[techniques/sub-bass]]
---

# Kick

## Summary
A synthesized kick in Operator: one sine carrier, a fast **pitch envelope** for the click and punch, and an **amp envelope** for body length. You get full control, and it can be tuned to the key. Drift works too (see Variants).

## Core
| Step | Direction | What it does | Source |
|---|---|---|---|
| Carrier | Osc A sine, single-carrier algorithm | Clean fundamental | [?] |
| Pitch env amount | High | Size of the downward sweep. More = more click | [?] |
| Pitch env decay | Very short (tens of ms) | Shorter = tight, longer = boomy/laser | [?] |
| Amp decay | ~150–400 ms, by ear | Body length | [?] |
| Tuning | Match the key, or leave it | A tuned kick sits with the sub | [?] |
| Chain | Saturator/Roar → EQ Eight (HP ~25–30 Hz) → optional Drum Buss | Grit, cleanup, punch | [?] |

## Variants
- **Raw / hardgroove:** short decay, more saturation, dry.
- **Hypnotic:** softer click, longer tail that feeds [[techniques/rumble]].
- **Industrial:** Roar with a little feedback, hard clip, short and aggressive.
- **Drift kick** (Hardgroove 134, 2026-07-17) [ear]. Device details → [[devices/drift]]:
  | Step | Value |
  |---|---|
  | Clear the default patch | Osc 2 + Noise off, Osc 1 Shape 0% (sine), Voices Mono |
  | Click | **Pitch Mod** ← Env 2 ~50%. Env 2: A ~0 ms, D ~30 ms, S 0% |
  | Body | Env 1 (amp): A 0–1 ms, D ~150–350 ms, S 0% |
  | Depth | Osc 1 **Oct −2**. The only move that lowers the fundamental |
  | Weight | Saturator Analog Clip, Drive 3–6 dB, trim Output to match level |
  | Room for SUB | EQ Three: FreqLow ~50 Hz, GainLow ≈ −2 dB, Slope 48 |
  | Second transient (optional) | LFO → Filter Freq, Retrigger on, Saw Down, 30–80 Hz |

## Gotchas
- Too long a pitch-envelope decay reads as a "laser" and clashes with the sub.
- EQ and saturation can't create a missing fundamental. For a deeper kick, change the octave, then lengthen amp decay, then deepen the pitch drop. [ear]
- Drift's free-running oscillators make each hit slightly different. That suits raw styles. Operator is the choice for identical hits. [?]

## Used in
- Hardgroove 134 (Drift variant, 2026-07-17)

## Sources
