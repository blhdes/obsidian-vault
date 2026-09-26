---
topic: Operator
type: device
updated: 2026-09-26
related: [[techniques/kick]], [[techniques/sub-bass]], [[techniques/metallic-perc]]
---

# Operator

## Summary
An FM synth with 4 oscillators (A–D) that can modulate each other's frequency, connected by one of **11 algorithms**, plus a filter, LFO and pitch envelope. 7 envelopes in total: one per oscillator, filter, pitch, LFO. [manual] It's the main tool for kicks, subs, FM perc and metallic stabs.

## Core
| Parameter | What it does | Source |
|---|---|---|
| Algorithm | Defines which oscillators modulate others and which output directly (11 presets) | [manual] |
| Oscillator waveform (`Wave`) | Sine (first choice for FM), Sine 4/8 Bit, Saw/Square/Triangle resynthesized with N harmonics (e.g. "Square 6": lower N = mellower, less aliasing), Saw D / Square D (digital), Noise Looped / Noise White | [manual] |
| Coarse / Fine | Ratio of oscillator frequency to note pitch. Coarse = whole numbers (harmonic). Fine = fractions (inharmonic, metallic) | [manual] |
| Fixed mode (`A Fix On `) | Oscillator ignores note pitch and plays `Freq` × `Multi` in Hz, down to 0.1 Hz. Useful for drums | [manual] [live] |
| Osc Level | Output level. On a modulator it sets FM depth, so it strongly changes the timbre | [manual] |
| Osc < Vel (+ Q) | Velocity changes oscillator frequency; Q quantizes it | [manual] |
| Pitch Env (shell) | Overall intensity, ±100%. At 100% the pitch change follows the envelope levels exactly; negative inverts it | [manual] |
| Pitch envelope routing | Per-target on/off buttons (Destination A–D, LFO); `Dest. A` slider sets intensity; `Dest. B` + `Amt` modulate one extra parameter | [manual] |
| Envelopes | 3 rates + 3 levels each. Filter and pitch envelopes have adjustable slope (0 = linear). Modes: Loop, Beat, Sync | [manual] |
| Amp envelope (`Ae …`) | Per-oscillator level envelope. Sustain is in dB | [manual] [live] |
| Global `Time` | Scales all envelope rates at once (not Beat/Sync values). `Time < Key`, `Time < Vel` modify rates further | [manual] |
| Glide / Spread / Transpose | Pitch section: polyphonic glide; Spread = 2 detuned voices L/R (CPU-heavy); global transpose | [manual] |

## Gotchas
- Parameter names with trailing spaces, dB sustain, algorithm labels → see [[tools/producer-pal]]. [live]
- A modulator's level controls FM depth (brightness). [manual]
- High frequencies can alias: lower the global `Tone`, or pick waveforms with fewer harmonics. [manual]
- Which of the 11 algorithms has only Osc A as carrier isn't described in text in the manual (diagram only) → check the algorithm labels in Live. [?]
- Units of envelope rates (ms?) aren't stated in the manual → read back from Live. [?]

## Used in
<!-- [[Tracks/...]] -->

## Sources
- Live 12 manual, Operator: https://www.ableton.com/en/manual/live-instrument-reference/
