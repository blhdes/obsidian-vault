---
topic: Wavetable
type: device
updated: 2026-09-26
related: [[techniques/stabs-textures]]
---

# Wavetable

## Summary
A wavetable synth: 2 wavetable oscillators plus a sub, 2 filters, 3 envelopes (Amp, Env 2, Env 3), LFOs and a modulation matrix. [manual] Use it for stabs, pads, drones and anything that should evolve in timbre.

## Core
| Parameter | What it does | Source |
|---|---|---|
| `Wave Position` | Position inside the wavetable (also drag in the display). Modulating it = timbral movement | [manual] |
| Oscillator effects | **FM** (`Amt`, `Tune`: ±50% = ±1 octave, ±100% = ±2 octaves, in between = inharmonic/noisy) · **Classic** (`PW` on any wavetable, `Sync`) · **Modern** (two waveshape distortions) | [manual] |
| Sub | On/off, `Gain`, `Tone` (0% = pure sine, higher = more harmonics), `Octave` −1/−2 | [manual] |
| Unison | 6 modes (or none). `Voices` = oscillators per wavetable osc (more = thicker). `Amount` = intensity, behaves differently per mode | [manual] |
| Poly / Mono + Glide | Mono = single voice with legato envelopes. Glide only works in Mono | [manual] |
| Filter types | Low-pass, high-pass, band-pass, notch, **Morph** (sweeps LP → BP → HP → notch). 12 or 24 dB slope | [manual] |
| Filter circuits | **Clean** (as EQ Eight, all types) · **OSR** (state-variable, hard-clipping diode limits resonance, all types) · **MS2** (Sallen-Key, soft clipping; LP/HP only) · **SMP** (custom) · **PRD** (ladder, no resonance limiting). Non-Clean LP/HP/BP get a `Drive` control | [manual] |
| Filter routing | **Serial** (all oscs → F1 → F2, sub to both) · **Parallel** (osc 1 → F1, osc 2 → F2) · **Split** | [manual] |
| Matrix tab | Grid: sources (envelopes, LFOs) across, targets down. Drag a cell to set the amount. Some targets are additive (sum around 0), others multiplicative | [manual] |
| Wave Position modulation | In the Matrix tab, drag the cell where an LFO/Env column meets the `Position` row | [manual] |
| MIDI tab | Velocity, Note (centred on C3; 100% on Filter Freq = exact key tracking), Pitch Bend, Aftertouch, Mod Wheel as sources. Shares rows with the Matrix | [manual] |
| Matrix `Time` / `Amount` | `Time` scales all modulator speeds (negative = faster). `Amount` scales all matrix modulation | [manual] |

## Gotchas

## Used in

## Sources
- Live 12 manual, Wavetable: https://www.ableton.com/en/manual/live-instrument-reference/
- Ableton KB, Managing CPU load when using Wavetable: https://help.ableton.com/hc/en-us/articles/360000036930
