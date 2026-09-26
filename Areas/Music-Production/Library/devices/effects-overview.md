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
| Colour | Saturator | Soft warmth to hard clip / folding (several curves). Analog Clip = rounded body. Trim Output after Drive for fair A/B | [?] |
| Colour | Roar | Multi-stage distortion with its own modulation and feedback. Industrial go-to | [?] |
| Colour | Drum Buss | Drive, transient shaping, low "boom" for drum groups | [?] |
| Colour | Redux / Erosion / Pedal / Vinyl Distortion | Digital crush / brittle artefacts / pedal grit / crackle | [?] |
| Dynamics | Compressor | Sidechain ducking, control | [?] |
| Dynamics | Glue Compressor | Bus glue | [?] |
| Dynamics | Multiband Dynamics | Band-specific control, aggressive upward compression | [?] |
| Tone | EQ Eight / EQ Three / Channel EQ / Auto Filter / Utility | Cleanup and sweeps / movement / gain, mono, phase | [?] |
| Space | Hybrid Reverb / Echo | Reverb / tempo-synced delay with character | [?] |
| Movement | Auto Filter | Filter (LP/BP/HP/Notch/Morph) + LFO (Hz or synced) + Envelope Follower | [?] |
| Movement | Chorus-Ensemble | Modulated short delays = width/thickness. Mode: Chorus (tighter) / Ensemble (wider). Has HP for the wet signal | [?] |
| Movement | Phaser-Flanger | Moving notches (Phaser, smooth) or swept short delay + feedback (Flanger, metallic) | [?] |
| Experimental | Beat Repeat, Grain Delay, Corpus, Spectral Resonator, Spectral Time, Shifter | Stutter, granular echo, resonant bodies, spectral freeze, pitch/frequency shift | [?] |
| Modulation (M4L) | LFO, Shaper, Envelope Follower | Map movement to any parameter without automation lanes | [?] |

## Gotchas
- Default chain order: tone → colour → dynamics. Space goes on returns. Saturating before the compressor tames it; saturating after keeps it rawer. [?]
- High-pass everything that isn't kick, rumble or bass. Sweep up until the sound loses body, then back off. Cut rather than boost. [ear] Solo Sketch 138, 2026-07-16
- EQ Three as a high-pass: set **FreqLow** to the cutoff and press the **L** kill button. FreqHi won't go low enough. [ear] Hardgroove 134, 2026-07-22
- Beat Repeat: Interval (chunk length), Grid, Chance, Gate, Pitch/Volume variation, onboard Filter. [?]

## Used in

## Sources
