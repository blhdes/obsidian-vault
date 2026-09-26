---
topic: Stock effects overview
type: device
updated: 2026-09-26
related: [[techniques/returns]], [[techniques/sidechain]]
---

# Stock effects — overview

## Summary
A map of Live 12 Suite's stock effects by role. When one device gathers enough knowledge, split it into its own `devices/<name>.md` and replace its row here with a link.

## Core
| Role | Device | Character | Source |
|---|---|---|---|
| Colour | Saturator | Waveshaper. 8 curves: Analog Clip (smooth knee), Soft Sine, **Bass Shaper** (own Threshold 0 to −50 dB: low = soft, high = hard clip; for kicks/bass), Medium Curve, Hard Curve, Sinoid Fold, Digital Clip (instant hard clip), Waveshaper (expanded view: Drive, Curve, Depth, Linear, Damp, Period). Second clip stage: Soft or Hard | [manual] |
| Colour | Roar | Multi-stage saturation. Routing: Single, Serial, Parallel, Multi Band (3 bands, 2 crossovers), Mid Side, Feedback, Delay (12.2). Each stage: 12 shaper curves + `Amount`, `Bias` (asymmetry, "broken circuit"), filter pre/post. Feedback modes Time / Synced / Triplet / Dotted / Note (rings at a pitch), with Invert and Gate; a compressor in the loop tames it. Mod: 2 LFOs, Envelope Follower (ext. sidechain in 12.2), Noise, matrix | [manual] |
| Colour | Drum Buss | Fixed drum comp (`Comp`), distortion Soft / Medium / Hard (+bass boost), `Drive`, `Crunch` (mid-high sine distortion), `Damp` (LP), `Transients` (>100 Hz; + = punch & sustain, − = tighter). Low end: `Boom` resonator + `Freq` (Force To Note), `Decay`, Boom Audition | [manual] |
| Colour | Redux | Downsampling (`Rate`, `Jitter`, Pre/Post filter) + bit reduction (`Bits`, `Shape`, `DC Shift`) | [manual] |
| Colour | Erosion | Degradation by modulating a short delay with sine + filtered noise (`Noise Blend`, X-Y Freq/Amount) | [manual] |
| Colour | Pedal / Overdrive | Pedal: guitar distortion, modes Overdrive / Distortion / Fuzz. Overdrive: band-pass → drive, `Dynamics`. In both, 0% gain still distorts | [manual] |
| Colour | Vinyl Distortion | Tracing (even harmonics), Pinch (odd, wider stereo), crackle generator | [manual] |
| Dynamics | Compressor | Sidechain ducking and control → sidechain panel in [[techniques/sidechain]] | [manual] |
| Dynamics | Glue Compressor | Bus compressor modelled on an 80s console; no knee control (sharpens with ratio); Attack in ms, Release in s. For Main / Group tracks | [manual] |
| Dynamics | Multiband Dynamics | Up to 3 bands, upper + lower threshold each: upward/downward compression and expansion | [manual] |
| Tone | EQ Eight | Up to 8 parametric filters, each with 8 responses (gain not adjustable on low cut, notch, high cut: vertical drag = Q). Modes Stereo / L/R / M/S, Analyze spectrum, `Scale` (all gains), expandable display | [manual] |
| Tone | EQ Three | DJ-style 3 bands, each −inf to +6 dB with On/Off (kill) buttons. Crossovers `FreqLo` / `FreqHi` (e.g. 500 / 2000 Hz = low 0–500, mid 500–2k, high 2k+). 24 / 48 dB slope switch. Band LEDs at −24 dB | [manual] |
| Tone | Channel EQ | Desk-style: `HP 80 Hz` switch, Low shelf 100 Hz ±15 dB, sweepable Mid 120 Hz–7.5 kHz ±12 dB, High shelf (+15 dB; cutting adds a low-pass) | [manual] |
| Tone | Utility | Phase invert per side, Channel Mode, `Width` (0% = mono) or Mid/Side, `Mono`, **Bass Mono** + frequency + Audition, `Gain` −inf to +35 dB, `Balance`, `Mute` (cuts a delay/reverb input, tail keeps ringing), `DC` filter | [manual] |
| Space | Hybrid Reverb | Convolution + algorithmic (Dark Hall, Quartz, Shimmer, Tides, Prism). Shared: `Decay` (to −60 dB), `Size`, `Delay`, `Freeze`/`Freeze In` | [manual] |
| Space | Echo | Modulated delay, tape/BBD to clean; LFO + env follower, Noise/Wobble, distortion, reverb, ducking, gate | [manual] |
| Movement | Auto Filter | 10 types: LP, HP, BP (12/24 dB), Notch, Morph (LP → BP → HP), DJ (one `Control` knob LP↔HP), Comb, Resampling (aliasing, no Res), Notch + LP, Vowel (`Pitch`). Circuits SVF / DFM / MS2 / PRD + `Drive`. LFO with stereo Phase/Spin. Envelope follower with external sidechain (Pre FX / Post FX / Post Mixer) | [manual] |
| Movement | Chorus-Ensemble | Modes: **Chorus** (2 delay lines; Delay Time Auto/fixed, 1–2 taps), **Ensemble** (3 lines, richer), **Vibrato** (pitch mod only, no delayed layer). HP on the wet signal; `Width` 0–200% | [manual] |
| Movement | Phaser-Flanger | Modes: **Phaser** (all-pass notches), **Flanger** (modulated delay + feedback = comb), **Doubler**. 2 LFOs (free/synced), env follower, `Safe Bass` HP, Feedback, Warmth | [manual] |
| Experimental | Beat Repeat | Stutter → details in [[techniques/arrangement]] | [manual] |
| Experimental | Spectral Resonator | Resonates partials at `Freq` (Internal) or at incoming notes (MIDI mode, Mono/Poly 2–16 voices, MIDI Gate). Mod modes: None, Chorus, Wander, Granular | [manual] |
| Experimental | Spectral Time | **Freezer** (Manual with fades, or Retrigger: Onsets / Sync interval) → **Delay** (Time / Notes / 16th modes, Feedback, `Shift` Hz per repeat, Tilt, Spray) | [manual] |
| Experimental | Shifter | Modes: **Pitch** (st + cents), **Freq** (Hz shift: small = phasing, large = metallic), **Ring** (+/− Hz, `Drive` only here) | [manual] |
| Experimental | Corpus | 7 physically modelled resonators (Beam, Marimba, String, Membrane, Plate, Pipe, Tube); tune in Hz or follow MIDI → [[techniques/metallic-perc]] | [manual] |
| Experimental | Grain Delay | Slices input into grains, each delayed and pitched. `Frequency` sets grain size (shapes how Pitch and Spray sound), `Pitch` (crude shifter), `Random Pitch` (low = mutant chorus, high = unintelligible), `Spray`, `Feedback` (high = runaway oscillation), Dry/Wet; `Sync` delay in 16ths; any parameter on the X-Y pad | [manual] |
| Modulation (M4L) | LFO, Shaper, Envelope Follower | Map up to 8 parameters. `Mod` mode (default): offsets the knob, which stays editable; Bipolar/Unipolar + Amount. Remote mode takes the knob over | [manual] |

## Gotchas
- Default chain order: tone → colour → dynamics. Space goes on returns. Saturating before the compressor tames it; saturating after keeps it rawer. [start]
- Hybrid Reverb for dense, dark low tails (rumble): the manual doesn't recommend one algorithm. **Dark Hall** is the candidate — `Damping` darkens the tail, `Bass X` + `Bass Mult` lengthen the low end; long Decay with very small Size turns into metallic gong resonances. [manual] Test by ear in a track.
- High-pass everything that isn't kick, rumble or bass. Sweep up until the sound loses body, then back off. Cut rather than boost. [ear] Solo Sketch 138, 2026-07-16
- EQ Three as a high-pass: set **FreqLow** to the cutoff and press the **L** kill button. FreqHi won't go low enough. [ear] Hardgroove 134, 2026-07-22

## Used in

## Sources
- Live 12 manual, audio effects: https://www.ableton.com/en/manual/live-audio-effect-reference/
- Live 12 manual, Max for Live devices: https://www.ableton.com/en/manual/max-for-live-devices/
- Live 12 release notes (Saturator 12.1, Roar/Auto Filter 12.2): https://www.ableton.com/en/release-notes/live-12/
