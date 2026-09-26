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
- Algorithm values read as bare labels `Alg. 1`–`Alg. 11`, with no carrier info. [live] Which one leaves only Osc A as carrier is visible only in the algorithm diagram in Live's UI. [?]
- Envelope units: Attack 0–20000 ms, Decay/Release 1–60000 ms, Loop 0.2–20000 ms. Osc envelope levels in dB (−70 to 0). Pitch envelope levels (`Pe Init/Peak/Sustain/End`) in semitones, ±48. `Pe Amount` ±100%, `Pe Amt A` ±100% per destination. [live] 2026-09-26
- Each oscillator has `Osc-X Retrig` (phase reset per note) + `Osc-X Phase` (start point %). Retrig On = identical hits. [live] 2026-09-26

## Used in
<!-- [[Tracks/...]] -->

## Sources
- Live 12 manual, Operator: https://www.ableton.com/en/manual/live-instrument-reference/
