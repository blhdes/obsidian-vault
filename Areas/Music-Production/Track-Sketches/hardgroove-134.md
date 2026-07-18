---
title: Hardgroove 134
date: 2026-07-16
tags: [ableton, track-sketch, techno, hardgroove, drift, live-lite]
---

# Hardgroove 134

The third track sketch. [[ticket-to-detroit|Ticket to Detroit]] is **parked** (not abandoned) — this is a deliberate fresh start with a different aesthetic and a stricter build discipline: everything hand-built in Ableton's UI, no programmatic DAW control of any kind for this project.

## Stats

| | |
|---|---|
| **Project** | *(to be saved — new .als, Live Lite)* |
| **BPM** | 134 |
| **Key** | C major *(nominal for now — kick/sub don't care about key; matters once STAB/LEAD and ATMOS arrive)* |
| **Goal** | Hardgroove techno — rolling, percussive, relentless low end; tight and dry, no reverb wash |
| **Setup** | Live Lite (8-track cap) + hardware controller — parts played in, not drawn, wherever it makes sense |
| **Build rule** | 100% hand-built in Ableton's UI. No Producer Pal, no MCP, no programmatic control — the point is to learn the interface directly |

## Track budget (fits Lite's 8 tracks)

| # | Track | Role |
|---|---|---|
| 1 | **KICK** | Drift → Saturator → EQ Three |
| 2 | **SUB** | Drift → EQ Three |
| 3 | **PERC** | Drum Rack — all percussion lives here |
| 4 | **HATS** | — |
| 5 | **STAB/LEAD** | — |
| 6 | **ATMOS** | — |
| 7 | **FX/RISER** | — |
| 8 | **RETURN** | shared return track |

## Devices allowed

Stock Lite only: **Drift, EQ Three, Saturator, Compressor, Drum Rack, Simpler**. No Operator, no Wavetable, no EQ Eight, no third-party plugins.

## Weeks 1–2 goal

Rebuild the low end from zero in Drift — **just KICK and SUB, nothing else yet**. The point is understanding Drift's synthesis parameters deeply, not finishing a track. Target: **3 distinct 8-bar kick+sub loops**, each with its own character, that groove on their own with nothing else in the mix.

- **KICK:** single sine, short pitch envelope for the thump/click, amp envelope tuned for punch. Four-on-the-floor, C1, velocity 120.
- **SUB:** pure sine, no pitch envelope, full sustain, EQ Three killing everything above ~180Hz. Offbeat pattern interlocked with the kick, C1, 8th-note duration.
- **Sidechain:** SUB ducks against KICK via Compressor.

## Session log

### 2026-07-16 — Kickoff

- Pivoted from Ticket to Detroit to a fresh sketch with new constraints: hardgroove techno at 134 BPM, strict hand-built-only workflow.
- New project set up: 134 BPM, C major, Session view.
- Track 1 renamed **KICK**, Drift loaded, oscillator isolated to a single plain sine (Osc 2 / Sub / Noise off) — first checkpoint before touching the pitch envelope.

**What's next:** the pitch envelope on the kick (short decay routed to pitch → the thump/click transient), then the amp envelope, Saturator, EQ Three. Then mirror the process for SUB.

### 2026-07-17 — KICK patch complete

- Full recipe documented in [[../Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] — worth reading in full; summary below.
- Debugged a real mix-up: Drift's **Pitch Mod** (oscillator pitch) and **Freq Mod** (filter cutoff) both default to sourcing "Env 2" and look similar — the first "click" heard was actually the filter popping (Freq Mod), not a true pitch drop, since Pitch Mod's amount was still 0%. Fixed by raising Pitch Mod instead and zeroing Freq Mod.
- Chased a subtle periodic volume drift down through: Envelope 1 Attack (ruled out — a fixed value can't be periodic) → LFO Rate in Hz vs. tempo-synced (switched to `1:1`) → the global **Drift** macro (zeroed) → finally the **Mod tab**'s actual Mod Matrix, likely an LFO→Volume routing at a tiny amount (sine-shaped, hence the "sine wave" loudness swell across loop repeats).
- **Envelope 1** confirmed as Drift's hardwired Amp Envelope (no Mod Matrix routing needed) — Attack ~0.5ms, Decay 175ms, Sustain 0%, Release 600ms (irrelevant since Sustain is 0).
- **Envelope 2** final shape (drives Pitch Mod): Attack 0ms, Decay 30ms, Sustain 0%.
- **Saturator** added: Analog Clip, Drive ~4dB — result: thicker but noticeably sharper (added harmonics extend upward as well as adding low-mid weight — expected, not a mistake).
- **EQ Three** added: FreqLow 50Hz, GainLow -1.81dB, Slope 48, Mid/High untouched — cleaned up sub-rumble below what the kick needs (reserving deep low end for SUB) without losing punch. Confirmed sounding "groovier."
- **KICK chain is now complete: Drift → Saturator → EQ Three.**

**What's next:** Mirror the whole process for **SUB** — pure sine, no pitch envelope, full sustain, EQ Three killing everything above ~180Hz, offbeat pattern interlocked with the kick. Then sidechain SUB to KICK, then build out the 3 target 8-bar loop variations.

### 2026-07-17 — SUB built, interlock + sidechain done

- **SUB** patch built mirroring KICK: Drift isolated to a single sine, no Pitch/Freq Mod, Envelope 1 set for full sustain (Attack ~0-5ms, Decay irrelevant, Sustain 100%, Release ~50-100ms), EQ Three killing Mid+High bands entirely (crossover at 180Hz) — pure sub tone confirmed.
- **Kick/sub interlock pattern** placed — straight 8th-note grid, **no swing** (this project's groove comes from placement/velocity only, per the original brief):

```
         1 & 2 & 3 & 4 &
Kick   : ● · ● · ● · ● ·
Sub    : · ● · ● · ● · ●
```

- Kick notes: 8th-note length (doesn't matter much — Sustain 0% self-terminates). Sub notes: 8th-note length is *load-bearing* here (Sustain 100% means note length is the only thing controlling duration). Velocity 120 on both for now.
- **Sidechain** wired: Compressor on SUB, sidechained from KICK (Post FX), SC Filter ~80Hz to focus the trigger on the kick's thump. Threshold -28.8dB, Ratio 8.4:1, Attack 0.01ms, Release 137ms, RMS detection. Confirmed by ear: the sub swells up into each hit rather than sounding static or choked — see [[../Techniques/kick-sub-interlock-sidechain|Kick/Sub Interlock as a Sidechain Groove Tool]] for why this works (Release timing shapes the swell since the two never actually overlap).
- **All of the Weeks 1–2 workflow (steps 1–4) is now done.**

**What's next:** Build out the **3 distinct 8-bar kick+sub loops**, each with its own character — the final target for this phase, using velocity variation and placement tweaks (not swing/FX) as the differentiation tools.

### 2026-07-17 — 3 loop variations done — Weeks 1–2 goal complete 🎉

- Built all three target loops from one duplicated 8-bar clip — see [[../Techniques/loop-character-variations|Loop Character Variations (Placement-Only)]] for the general technique:
  - **Loop 1 — Straight Roller:** the base interlock, unedited, all 8 bars — its character is the unwavering repetition.
  - **Loop 2 — Rolling Push:** added sub hit on the `a` of beat 3 in bars 4 and 8 — a 16th-note anticipation into the phrase-ending kick. Confirmed: swells audibly via the sidechain, reads as "rolling."
  - **Loop 3 — Stripped/Hypnotic:** removed the sub hit on beat 3's `&` in bars 2, 4, 6, 8 — sparser, more space, clear contrast against Loop 1.
- **This closes out the entire original Weeks 1–2 goal:** KICK ✅, SUB ✅, interlock ✅, sidechain ✅, 3 distinct 8-bar loops ✅ — all built entirely by hand, no programmatic control, one parameter/concept at a time.

**What's next:** Open — the low end is done and grooving on its own. Next phase moves into the rest of the 8-track budget: **PERC** (Drum Rack, all percussion), then **HATS**, building outward from the kick/sub foundation.
