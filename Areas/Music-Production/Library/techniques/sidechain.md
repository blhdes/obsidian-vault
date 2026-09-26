---
topic: Sidechain
type: technique
updated: 2026-09-26
related: [[techniques/sub-bass]], [[techniques/rumble]], [[tools/producer-pal]]
---

# Sidechain

## Summary
The kick ducks other elements (sub, rumble, pads) so the low end stays clear and the groove pumps. When the target never overlaps the kick (an interlocked sub), the duck becomes a **groove tool** instead: the target swells in as the duck releases.

## Core
```
TARGET → Compressor
   Sidechain: On · source = KICK
   Ratio high · Attack fast · Release tuned to tempo
```
| Step | Direction | Source |
|---|---|---|
| Source | KICK track (Post FX / Post Mixer) | [?] |
| Single pad | `"Drum Rack \| [Pad Sample Name] \| Post Mixer"`. In the UI: Audio From → drum track → the kick pad's chain | [live] |
| Ratio | 4:1 or higher | [ear] Solo Sketch 138, 2026-07-13 |
| Threshold | Lower it until GR shows ~6–10 dB on each kick | [ear] Solo Sketch 138, 2026-07-13 |
| Attack | 0.01–1 ms | [ear] Solo Sketch 138, 2026-07-13 |
| Release | **The groove knob**, ~100–250 ms. Let the target breathe between kicks. Set it by ear | [ear] |
| SC filter | ~80 Hz on the trigger, so only the kick's thump fires the compressor | [ear] Hardgroove 134, 2026-07-17 |
| Toggles via Producer Pal | `"On"` / `"Off"` | [live] |

## Variants
- **Ghost trigger:** a muted track with a short click as the sidechain source, so ducking stays independent of the kick's sound.
- **Interlock swell (kick/sub):** the sub plays between kicks, so the duck is still releasing when the sub note starts. Too short a Release = static. Too long = choked. Hardgroove 134 values: Threshold −28.8 dB, Ratio 8.4:1, Attack 0.01 ms, Release 137 ms, RMS detection. [ear] Hardgroove 134, 2026-07-17

## Gotchas
- Where: rumble = essential. Bass = optional (adds pump). Pads = classic big pump, but heavy-handed and style-specific. Not on the drums or the Master. [?]
- Check: toggle the Compressor on/off. On should sound punchier and cleaner, not quieter. If the pump is obvious and seasick, raise the Threshold or shorten the Release. [ear]

## Used in
- Solo Sketch 138 (rumble, 2026-07-13) · Hardgroove 134 (sub, 2026-07-17)

## Sources
