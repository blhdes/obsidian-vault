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
| Tone | EQ Eight / EQ Three / Channel EQ / Utility | Cleanup, kills, gain, mono, phase | [?] |
| Space | Hybrid Reverb | Convolution + algorithmic (Dark Hall, Quartz, Shimmer, Tides, Prism). Shared: `Decay` (to −60 dB), `Size`, `Delay`, `Freeze`/`Freeze In` | [manual] |
| Space | Echo | Modulated delay, tape/BBD to clean; LFO + env follower, Noise/Wobble, distortion, reverb, ducking, gate | [manual] |
| Movement | Auto Filter | 10 types: LP, HP, BP (12/24 dB), Notch, Morph (LP → BP → HP), DJ (one `Control` knob LP↔HP), Comb, Resampling (aliasing, no Res), Notch + LP, Vowel (`Pitch`). Circuits SVF / DFM / MS2 / PRD + `Drive`. LFO with stereo Phase/Spin. Envelope follower with external sidechain (Pre FX / Post FX / Post Mixer) | [manual] |
| Movement | Chorus-Ensemble | Modes: **Chorus** (2 delay lines; Delay Time Auto/fixed, 1–2 taps), **Ensemble** (3 lines, richer), **Vibrato** (pitch mod only, no delayed layer). HP on the wet signal; `Width` 0–200% | [manual] |
| Movement | Phaser-Flanger | Modes: **Phaser** (all-pass notches), **Flanger** (modulated delay + feedback = comb), **Doubler**. 2 LFOs (free/synced), env follower, `Safe Bass` HP, Feedback, Warmth | [manual] |
| Experimental | Beat Repeat | Stutter → details in [[techniques/arrangement]] | [manual] |
| Experimental | Spectral Resonator | Resonates partials at `Freq` (Internal) or at incoming notes (MIDI mode, Mono/Poly 2–16 voices, MIDI Gate). Mod modes: None, Chorus, Wander, Granular | [manual] |
| Experimental | Spectral Time | **Freezer** (Manual with fades, or Retrigger: Onsets / Sync interval) → **Delay** (Time / Notes / 16th modes, Feedback, `Shift` Hz per repeat, Tilt, Spray) | [manual] |
| Experimental | Shifter | Modes: **Pitch** (st + cents), **Freq** (Hz shift: small = phasing, large = metallic), **Ring** (+/− Hz, `Drive` only here) | [manual] |
| Experimental | Grain Delay, Corpus | Granular echo; resonant physical bodies → see [[techniques/metallic-perc]] | [?] |
| Modulation (M4L) | LFO, Shaper, Envelope Follower | Map up to 8 parameters. `Mod` mode (default): offsets the knob, which stays editable; Bipolar/Unipolar + Amount. Remote mode takes the knob over | [manual] |

## Gotchas
- Default chain order: tone → colour → dynamics. Space goes on returns. Saturating before the compressor tames it; saturating after keeps it rawer. [?]
- Hybrid Reverb for dense, dark low tails (rumble): the manual doesn't recommend one algorithm. **Dark Hall** is the candidate — `Damping` darkens the tail, `Bass X` + `Bass Mult` lengthen the low end; long Decay with very small Size turns into metallic gong resonances. [manual] Test by ear in a track.
- High-pass everything that isn't kick, rumble or bass. Sweep up until the sound loses body, then back off. Cut rather than boost. [ear] Solo Sketch 138, 2026-07-16
- EQ Three as a high-pass: set **FreqLow** to the cutoff and press the **L** kill button. FreqHi won't go low enough. [ear] Hardgroove 134, 2026-07-22

## Used in

## Sources
- Live 12 manual, audio effects: https://www.ableton.com/en/manual/live-audio-effect-reference/
- Live 12 manual, Max for Live devices: https://www.ableton.com/en/manual/max-for-live-devices/
- Live 12 release notes (Saturator 12.1, Roar/Auto Filter 12.2): https://www.ableton.com/en/release-notes/live-12/
