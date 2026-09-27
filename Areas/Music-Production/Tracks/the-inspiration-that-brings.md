---
title: the inspiration that brings
status: building
lane: hypnotic
bpm: 130
key: C Phrygian
set: the inspiration that brings.als
started: 2026-09-26
updated: 2026-09-27
---

# the inspiration that brings

## Concept
Working title = Live Set name. Lane: hypnotic (chosen 2026-09-27). One 4-bar loop in scene 1: offbeat hats, a panned 16th shaker, a C Phrygian chord cycle and a C1 drone.

## Elements
Read back from Live, 2026-09-26.

| Track | Source | Chain | Notes |
|---|---|---|---|
| KICK | Operator "Kick": Alg. 11 · Osc A sine + Pitch Env (Init/Peak +42 st, Decay 40 ms), Ae Decay 350 ms · Osc B sine same pitch, no Pe, A 2 ms / D 500 ms, −9 dB · Transpose −17 | Saturator (Bass Shaper, Drive 15, Thr −20, Out −3) → EQ Eight (HP48 25 Hz, Bell 55 Hz +2 dB Q1) → Drum Buss (Crunch 30%, Drive 20% Soft, Boom 0) → Utility (Ale's) | Scene 1: C2 on every quarter, v65 → sounds ~G0 (49 Hz). Send C-RUMBLE −12 dB |
| BASS | Tension "String Bass": Mono, Hammer (Mass 60, Stiffness 70), Damper On + Gated (Mass 30), String Decay 70, Str Inharmon 60, Pickup 40%, LP 900 Hz, −6 dB | Compressor "Bass Duck" (SC KICK Post FX, SC LP 100 Hz, Thr −28.8, 8.4:1, Att 0.01, Rel 180 ms, RMS) → Auto Filter "Bass Breath" (LP24 SVF 500 Hz, Res 20%, LFO Sine synced 4 bars, Amount 40%) | 2 bars "Offbeat String": C1 on the offbeats (1/8 notes), Db1 at 1\|4.5, Eb1 1/16 at 2\|3.75 |
| HATS | Simpler "Hihat Closed Crisp" | EQ Eight | 2 bars "Airy Hats": offbeat 8ths v96 + one ghost at 2\|4.75 v58. Send A −18 dB. Armed |
| SHAKER | Simpler "Shaker Acoustic 1" | EQ Eight | 2 bars "Airy Shaker": 16ths, v30/48/38, pans 0.6 / 1. Send A −18 dB |
| SNTH CHORDS | Instrument Rack "Vinyl Stringz" (Operator "Vinyl Strings") | EQ Eight → Chorus (off) | 4 bars: whole-note chords Cm (C–Eb–G) → C–Eb–Ab → C–F–Ab → C–F–G, v64, plus an 8th-note C1 line (v100–127) in the same clip |
| 6-Clang Swarm | Max Instrument "Clang Swarm" | — | 1 bar: C1 held, v100 |
| 6-MIDI | Producer Pal | — | Don't touch |
| 7-Audio, 8-Audio | empty audio tracks | — | |

## Returns
| Return | Chain | Fed by |
|---|---|---|
| A-Reverb | Reverb | HATS −18 dB, SHAKER −18 dB |
| B-Delay | Delay | — |
| C-RUMBLE | Hybrid Reverb (Dark Hall, 100% wet, Decay 1.8 s, Damping 80%, BassMult 150% < 200 Hz, EQ off, Bass Mono) → Saturator (Analog Clip, Drive 10, Out −3) → EQ Eight (HP48 30 Hz, LP48 220 Hz) → Compressor (SC KICK Post FX, SC LP 100 Hz, Thr −30, 8:1, Att 0.01 ms, Rel 150 ms) | KICK −12 dB |

## Arrangement
| Section | Bars | What happens |
|---|---|---|
| — | — | Only scene 1 has clips. Nothing in Arrangement yet |

## Next
- [ ] Check the rumble level on a system with real low end (AirPods hide < 60 Hz)
- [ ] BASS: A/B Damper Gated on/off by ear
- [ ] Unmute the rest and check BASS + KICK + rumble together

## Log
- 2026-09-27 — Built the Operator kick (sine + pitch env + sub layer on Osc B), Saturator/EQ/Drum Buss, C-RUMBLE return; kick moved to C2 (~49 Hz); scale confirmed C Phrygian. BASS on Tension with sidechain + slow Auto Filter; lane = hypnotic. Live hung once (3 parallel writes with Tension playing) → restart.
- 2026-09-26 — First session in the vault: read the set, created this file.
