---
topic: Rumble
type: technique
updated: 2026-09-26
related: [[techniques/kick]], [[techniques/returns]], [[techniques/sidechain]]
---

# Rumble

## Summary
The hypnotic/industrial low end: the kick feeds a long reverb, the reverb tail gets distorted and low-passed, then ducked by the kick. The result is a continuous, pulsing sub-texture. Style note: raw/hypnotic/industrial, ~130–145 BPM. House/Detroit usually use a played bassline instead.

## Core
```
KICK ─send─► C-RUMBLE
   Hybrid Reverb (100% wet, long, dark)
   → Saturator / Roar (drive)
   → EQ Eight (HP ~30 Hz, LP ~120–200 Hz)
   → Compressor (sidechain: KICK, fast release)
```
| Step | Direction | Source |
|---|---|---|
| Send | Only the kick. Automate the send per section | [start] |
| Reverb | 100% wet. Decay ~1.5–3 s: one kick's tail should reach the next kick | [ear] Solo Sketch 138, 2026-07-12 |
| Algorithm | Hybrid Reverb **Dark Hall**: `Damping` darkens, `Bass X` + `Bass Mult` stretch the low tail. Details → [[devices/effects-overview]] | [manual] controls · [start] best choice |
| Filter | Keep only the low end (below ~150–200 Hz) | [ear] Solo Sketch 138, 2026-07-12 |
| Duck | Sidechain from KICK so the kick stays clear → [[techniques/sidechain]] | [ear] Solo Sketch 138, 2026-07-13 |
| Level | Low, centred. Felt more than heard: muting it should make the room feel emptier | [ear] Solo Sketch 138, 2026-07-12 |

## Variants
- **Dedicated track** instead of a return: duplicate the drum track, keep only the kick notes, then Reverb (100% wet) → EQ. Easier to edit and automate. [ear] Solo Sketch 138, 2026-07-12

## Gotchas
- A rumble that isn't ducked eats the kick. Check it in mono.
- Too loud = mud. The most common failure. When in doubt, drop it another 3 dB. [ear]
- Decay too long stacks tails into a drone. Too short leaves gaps. Tune it at the track's BPM. [ear]

## Used in
- Solo Sketch 138 (2026-07-12)

## Sources
- Live 12 manual, Hybrid Reverb: https://www.ableton.com/en/manual/live-audio-effect-reference/
