---
topic: Drift
type: device
updated: 2026-09-26
related: [[techniques/acid]], [[techniques/sub-bass]], [[techniques/kick]], [[techniques/stabs-textures]]
---

# Drift

## Summary
A compact subtractive synth (2 oscillators, filter, envelopes, modulation matrix) with a built-in "drift" of analog-style instability. Well suited to acid lines, basses and simple leads. It also handles kicks, stabs and noise risers.

## Core
| Parameter | What it does | Source |
|---|---|---|
| Voice `Mode` | **Poly** (1 voice/note, up to 32) · **Mono** (1 note, rendered by 4 voices; `Thickness` 0 = single voice) · **Stereo** (2 voices panned, `Spread`) · **Unison** (4 detuned voices/note, max 8 notes) | [manual] |
| `Legato` + `Glide` (Mono) | Legato: a new overlapping note changes pitch **without retriggering the envelopes**. Glide sets how long overlapping notes take to slide. This is the acid slide | [manual] |
| Osc 1 waveform | Chooser: Sine, Triangle, Shark Tooth, Saturated (good for bass), Saw, Pulse, Rectangle. `Oct` transposes in octaves | [manual] |
| Osc 1 `Shape` | Changes harmonic content, similar to pulse-width modulation. Each waveform responds differently. It doesn't morph between waveforms | [manual] |
| Oscillator Mixer | On/off switch + gain for Osc 1, Osc 2 and **Noise** (white noise). Arrow toggle per source = route through the filter or bypass it | [manual] |
| Osc gain saturation | Default gain −6 dB. Raising it drives the filter's pre-saturation stage; above 0 dB also the post stage → analog-style distortion | [manual] |
| Oscillator `R` | Retrigger for the oscillators (phase reset on each note) on/off | [manual] |
| Env 1 | Amplitude envelope (ADSR). Also usable as a mod source | [manual] |
| Env 2 / Cyc | ADSR not mapped to amplitude, free as a mod source. Switch to **Cycling Envelope**: an LFO-like shape that restarts per note, with `Tilt`, `Hold` and time modes Rate / Ratio / Time / Sync | [manual] |
| Env 2 default routing | A new Drift already routes Env 2 to Pitch Mod and filter Freq Mod (not stated in the manual) | [?] |
| Pitch Mod | 2 source slots that modulate the pitch of both oscillators, ±100%. LFO in Ratio mode on pitch = FM tones | [manual] |
| Filter | Low-pass `Freq`, `Res`, `Key` tracking, a separate high-pass, and 2 frequency-mod slots | [manual] |
| Filter `Type` | **Type I** 12 dB/oct, DFM-1: feeds back more distortion internally (clean sweeps → warm drive). **Type II** 24 dB/oct, Cytomic MS2: Sallen-Key with soft clipping that limits resonance | [manual] |
| Filter envelope amount / decay | Short decay = "pluck/squelch" per note | [start] |
| Mod section | 3 slots. Sources: Env 1, Env 2/Cyc, LFO, Key, Velocity, Modwheel, Pressure, Slide. Destinations: Osc 1 Gain/Shape, Osc 2 Gain/Detune, Noise Gain, LP Freq/Res, HP Freq, LFO Rate, Cyc Env Rate, Main Volume. Amount ±100% | [manual] |
| Velocity → LP Frequency | Accented notes open the filter. `Vel > Vol` sets velocity → volume separately | [manual] |
| LFO | Time modes Rate (Hz) / Ratio / Time (ms) / Sync. 9 shapes: Sine, Triangle, Saw Up/Down, Square, S&H, Wander, Linear Env, Exp Env. `R` = retrigger phase per note, off = free-running. `Amount` = overall LFO intensity; it has its own mod source + amount | [manual] |
| `Drift` | Per-voice random variation of pitch and filter cutoff; higher = more out of tune | [manual] |
| `Transpose` | Global, −48 to +48 st. `Note PB` = per-note pitch bend | [manual] |

## Gotchas
- Toggles take `"On"`/`"Off"` via Producer Pal. [live]
- A new Drift isn't blank: Osc 2 is on and Env 2 is pre-routed. Clear it before building from scratch. [ear] Hardgroove 134, 2026-07-17
- A free Hz LFO drifts against the beat grid. A small sine LFO → Volume in the Mod tab causes a slow loudness swell that's easy to miss. [ear] Hardgroove 134, 2026-07-18
- LFO rate below ~20 Hz = audible movement. Above ~20 Hz (audio rate) it becomes texture or buzz. 30–80 Hz gave a shaped transient on a kick. [ear] Hardgroove 134, 2026-07-18
- Sine LFO swings both ways (it darkens as well as brightens). Saw Down behaves like a one-shot decay. [ear] Hardgroove 134, 2026-07-18
- Hits differing slightly even with Drift at 0% → the oscillator `R` (retrigger) toggle is off, so phase free-runs. Turn `R` on for identical hits (kicks). [manual]

## Used in
- Hardgroove 134 (kick, stab, lead) · Solo Sketch 138 (noise riser)

## Sources
- Live 12 manual, Drift: https://www.ableton.com/en/manual/live-instrument-reference/
