---
topic: Acid
type: technique
updated: 2026-09-26
related: [[devices/drift]], [[devices/effects-overview]]
---

# Acid

## Summary
A mono saw/pulse through a resonant low-pass with a short filter envelope. The character comes from **accent** (velocity opening the filter), **slide** (legato glide) and slow cutoff/resonance movement. The line is the track.

## Core
| Step | Direction | Source |
|---|---|---|
| Voice | Drift `Mode` Mono + `Legato` on + `Glide` time. Overlapping notes slide in pitch without retriggering the envelopes = the slide | [manual] |
| Oscillator | Osc 1 Saw, or Pulse / Rectangle (Drift has both) for a hollower tone | [manual] waveforms · [?] tone |
| Filter | Low-pass, high resonance (~60–80%), short envelope decay | [?] |
| Accent | Drift Mod section: Source **Velocity** → Destination **LP Frequency** (±100%) | [manual] |
| Pattern | 16ths, a few octave jumps, overlapping notes = slides [manual], 2–4 accents per bar [?] | [manual] · [?] |
| Movement | Automate cutoff + resonance over 16–32 bars | [?] |
| Chain | Saturator/Roar → Echo (low mix) → EQ Eight | [?] |

## Variants
- **Analog** as a source for a fatter, two-filter version.
- **MIDI Tools** (Clip View → Tools tabs): **Recombine** permutes Position, Pitch, Duration or Velocity across selected notes (Shuffle / Mirror / Rotate) — mutates a line while keeping its notes. **Euclidean** (M4L generator) spreads notes evenly for up to 4 voices, with Rotation. [manual] Other transformations: Arpeggiate, Connect, Ornament, Quantize, Span, Strum, Time Warp. [ext] Live 12.0 release notes
- Which tools suit acid best is a taste call. [?]

## Gotchas
- It sits above the bass, and should blend with the drums rather than sit on top of them. [?]

## Used in

## Sources
- Live 12 manual, Drift / MIDI Tools: https://www.ableton.com/en/manual/live-instrument-reference/ · https://www.ableton.com/en/manual/midi-tools/
- Live 12.0 release notes: https://www.ableton.com/en/release-notes/live-12/
