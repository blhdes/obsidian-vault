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
Whole set colored #FFF034 (tracks, returns, clips). Ale's rule: hats stay bright in normal sections; filter dips on hats only for special moments (breaks, transitions).

## Elements
Read back from Live, 2026-09-27. Every chain ends with a Utility (defaults unless noted).

| Track | Source | Chain | Notes |
|---|---|---|---|
| KICK | Operator "Kick": Alg. 11 · Osc A sine + Pitch Env (Init/Peak +42 st, Decay 40 ms), Ae Decay 350 ms · Osc B sine same pitch, no Pe, A 2 ms / D 500 ms, −9 dB · Transpose −17 | Saturator (Bass Shaper, Drive 15, Thr −20, Out −3) → EQ Eight (HP48 25 Hz, Bell 55 Hz +2 dB Q1) → Drum Buss (Crunch 30%, Drive 20% Soft, Boom 0) → Utility (Ale's) | Scene 1: C2 on every quarter, v65 → sounds ~G0 (49 Hz). Send C-RUMBLE −12 dB |
| BASS | Tension "String Bass": Mono, Hammer (Mass 60, Stiffness 70), Damper On + Gated (Mass 30), String Decay 70, Str Inharmon 60, Pickup 40%, LP 900 Hz, −6 dB | Compressor (SC KICK Post FX, SC LP 100 Hz, Thr −28.8, 8.4:1, Att 0.01, Rel 180 ms, RMS) → Auto Filter (LP24 SVF 500 Hz, Res 35%, LFO S & H synced 3/4, Amount 40%, Phase 90°) → Roar (single, Tube Preamp 30%, Flt 1 LP 5.08 kHz (Ale), Feedback 25% Note C#2/Db2, Fb Gate, Dry/Wet 40%) → EQ Eight (Bell 2.5 kHz −3 dB Q1, LP12 4 kHz) → Utility (Out −3 dB, Width 140%, Bass Mono < 120 Hz) | Armed. 2 bars "Offbeat String": C1 on the offbeats (1/8 notes, v100 on each bar's first, v80 the rest), Db1 at 1\|4.5 v95, Eb1 1/16 at 2\|3.75 v85. Roar mod sources tweaked by Ale (LFO1 Sine, LFO2 Ramp Up, Noise Brown); mod routing not checked |
| OPEN HATS | Simpler "Hihat Open Electronic" (Ale) (one-shot, Gate, Fade Out 150 ms, Vol −12, Vol < Vel 60%, LP24 Clean 12 kHz, LFO Sine synced "3", Retrig Off → Filt < LFO 4) — sample chosen by Ale | EQ Eight (HP48 400 Hz, High Shelf 12 kHz +5 dB) → Saturator (Soft Sine, Drive 6, Out −4, Dry/Wet 40%) → Reverb (Dry/Wet 15%, Decay 700 ms, Predelay 15 ms, In Lo+Hi Cut @ 2 kHz) → Utility | 2 bars "Airy Hats": offbeat 8ths accented 100/70/88/64 (bar 2 ends v60) + ghost at 2\|4.75 v58. Track −9 dB. In group PERC. Send A off (reverb now in-chain) |
| CLOSED HATS | Simpler "Hihat Closed Noise Short" (one-shot, Vol −12, Vol < Vel 60%) | EQ Eight (HP48 500 Hz) → Utility | In PERC. Track −10 dB. 2 bars "Closed Rotate": 16ths skipping the offbeats (open hat's slot), accents cycle every 3 sixteenths (92/48/64) → rotates against the 4/4 grid |
| PERC | Group Track (HATS + SHAKER) | Utility (default) | Glue Compressor to come |
| SHAKER | Simpler "Shaker Acoustic 1" | EQ Eight | 2 bars "Airy Shaker": 16ths, v30/48/38, pans 0.6 / 1. Send A −18 dB |
| SNTH CHORDS | Instrument Rack "Vinyl Stringz" (Operator "Vinyl Strings") | EQ Eight → Chorus (off) | 4 bars: whole-note chords Cm (C–Eb–G) → C–Eb–Ab → C–F–Ab → C–F–G, v64, plus an 8th-note C1 line (v100–127) in the same clip |
| 7-Clang Swarm | Max Instrument "Clang Swarm" | — | 1 bar: C1 held, v100 |
| 6-MIDI | Producer Pal | — | Don't touch |
| 8-Audio, 9-Audio | empty audio tracks | — | |

## Returns
| Return | Chain | Fed by |
|---|---|---|
| A-Reverb | Reverb | SHAKER −18 dB |
| B-Delay | Delay | — |
| C-RUMBLE | Hybrid Reverb (Dark Hall, 100% wet, Decay 1.8 s, Damping 80%, BassMult 150% < 200 Hz, EQ off, Bass Mono) → Saturator (Analog Clip, Drive 10, Out −3) → EQ Eight (HP48 30 Hz, LP48 220 Hz) → Compressor (SC KICK Post FX, SC LP 100 Hz, Thr −30, 8:1, Att 0.01 ms, Rel 150 ms) → Utility (default) | KICK −12 dB |

## Variations (session clips for the APC mini mk2)
| Track | s0 (main) | s1 | s2 | s3 |
|---|---|---|---|---|
| BASS | Offbeat String | Bass Pulse — least: 4 notes (C1 on 2.5/4.5, Db1 at 2\|4.5) | Bass Rise — main + Eb1 1\|3.5, C1 ghost 2\|2.75, F1 2\|4.5 | Bass Drive — most: offbeats + 16th ghosts on x.75, Eb/Db/F moves, C2 jump at 2\|4.75 |
| OPEN HATS | Airy Hats | Hats Push — main + v48 ghost 16ths on every x.75 | Hats Open — longer notes (n/8 at 1\|2.5, n/4 at 1\|4.5 and 2\|4.5) → open tails via Gate | Hats Sparse — only beats 2.5 / 4.5 |
| CLOSED HATS | Closed Rotate | Closed Sparse — least: only x.75, 80/58 | Closed Five — offbeats skipped, accents cycle every 5 (96/44/58/44/70) | Closed Rush — most: all 16ths (offbeats v40) + 32nd roll 70→120 on 2\|4.5 |

## Arrangement
| Section | Bars | What happens |
|---|---|---|
| — | — | Only scene 1 has clips. Nothing in Arrangement yet |

## Next
- [ ] Check the rumble level on a system with real low end (AirPods hide < 60 Hz)
- [x] BASS: Damper Gated stays On — softer by ear (2026-09-27)
- [ ] BASS: check harshness (Roar Tube Preamp / Str Inharmon are the levers, not Utility)
- [ ] Unmute the rest and check BASS + KICK + rumble together

## Log
- 2026-09-27 — Built the Operator kick (sine + pitch env + sub layer on Osc B), Saturator/EQ/Drum Buss, C-RUMBLE return; kick moved to C2 (~49 Hz); scale confirmed C Phrygian. BASS on Tension with sidechain + slow Auto Filter; lane = hypnotic. Live hung once (3 parallel writes with Tension playing) → restart. Bass: S&H filter, Roar feedback on Db, Utility width + bass mono. Utility added to every chain.
- 2026-09-26 — First session in the vault: read the set, created this file.
