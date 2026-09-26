---
title: Building a Kick From Scratch in Drift
date: 2026-07-17
tags: [ableton, drift, sound-design, synthesis, kick, saturator, eq-three]
---

# Building a Kick From Scratch in Drift

A from-zero recipe for a punchy, clicky kick using only Drift + Saturator + EQ Three — no presets. Built on Hardgroove 134.

## 1. Isolate the oscillator

A fresh Drift instance is not blank — it ships with a default patch (Osc 2 active as a sub-like layer, Envelope 2 pre-routed into filter modulation). To get a true starting point:

- Turn off **Osc 2** and **Noise** (fader to -∞dB, or the on/off toggle).
- **Osc 1 Shape** to 0% — Shape morphs sine → triangle → saw as it turns up; 0% is pure sine.
- **Voices** to **Mono** (a kick is always one note at a time).
- Check **Osc 1's own level fader** (in the Osc Mix column) isn't at -∞dB — Shape only changes waveform character, it doesn't control volume. A silent Shape-0% sine is usually a muted fader, not a Shape problem.

## 2. Pitch Mod vs. Freq Mod — easy to confuse

Drift has **two separate modulation slots that both default to sourcing "Env 2"**, in two different panels:

| Control | Location | Target |
|---|---|---|
| **Pitch Mod** | Osc Mix panel, left side | Oscillator pitch |
| **Freq Mod** | Filter panel, bottom | Filter cutoff |

They look similar (same "Env 2" label) and it's easy to raise the wrong one — doing so gives a filter-cutoff pop that can sound percussive/clicky, but isn't an actual pitch envelope. If the "click" isn't behaving as expected, check both slots' actual amounts before assuming either one is broken.

**For the kick's pitch-drop click:** raise **Pitch Mod's** Env 2 amount (not Freq Mod) to ~50%, and shape **Envelope 2**: Attack ~0ms, Decay ~30ms (this is the whole "speed of the click"), Sustain 0% (so pitch fully resets, nothing lingers). Freq Mod's Env 2 amount should be zeroed unless a filter pop is deliberately wanted too.

## 3. Envelope 1 = the dedicated Amp Envelope

Envelope 1 is hardwired to volume — no Mod Matrix routing needed, unlike Envelope 2. For a punchy one-shot kick:
- Attack ~0–1ms (instant)
- Decay ~150–250ms — this is the real "punch" dial (shorter = tighter, longer = rounder body)
- Sustain 0% — a kick doesn't hold like a pad
- Release irrelevant once Sustain is 0%

## 4. Kill hidden sources of drift/wobble

Two Drift parameters add per-note or per-loop variation that can be mistaken for a bug:
- **LFO Rate in Hz vs. tempo-synced (`1:1`)** — a free-running Hz rate slowly drifts out of phase with the beat grid, so if it's routed to anything, its effect lands differently on every pass. Switch to `1:1` if the LFO is in use.
- **The "Drift" macro** (global, next to Voices/Mode) — deliberate small random amplitude/pitch wobble per note, on purpose. Subtle at low %, but can read as "why do some hits sound different" if you're doing exact A/B testing. Zero it while diagnosing; reintroduce later for analog "aliveness."
- Also check the **"Mod" tab** (next to the LFO tab) — the actual Mod Matrix. An LFO with a Sine shape routed to **Volume** at even a tiny amount produces a slow, subtle sine-shaped loudness swell across many loop repeats — easy to mistake for something else since it's so gradual.

## 5. Saturator — harmonic weight

Drive the signal into a waveshaping curve to add harmonics (like tape/tube warmth, not obvious distortion):
- **Type: Analog Clip** — rounded, smooth, adds body without harshness. (Soft Sine is a mellower alternative if it reads too bright/sharp.)
- **Drive:** ~3–6dB to start, more thickness as it goes up
- **Output:** trim down slightly to compensate for the level Drive adds, so A/B comparisons are about tone, not loudness

Added harmonics extend upward as well as adding low-mid weight — some extra brightness/edge is a normal side effect, not a mistake. EQ Three (next) is where that gets tamed if needed.

## 6. EQ Three — HP + low shaping

EQ Three: 3 bands (Low/Mid/High), each with a Gain knob and an instant on/off "kill" button; two Freq knobs set the Low/Mid and Mid/High crossover points; a Slope switch (24 or 48 dB/oct) sets how steep those crossovers are.

For a kick that needs to coexist with a separate SUB track:
- **Low/Mid crossover Freq** around **50–60Hz** — narrows what the Low band actually touches
- **Low Gain:** trim a couple dB (not a full kill) if the low end feels loose after Saturator — the kick still wants some low body, just not encroaching on SUB's dedicated territory
- Leave Mid/High alone unless taming Saturator's added edge specifically

Result on this build: FreqLow 50Hz, GainLow -1.81dB, Slope 48, Mid/High untouched.

## 7. A second, independent transient via the LFO (extra credit)

So far only Envelope 2 (via Pitch Mod) shapes the kick's transient. Drift's **LFO** can act as a second, independent modulation source for a *different* destination — e.g. Filter Freq — giving the kick two separately-shaped transient layers instead of one.

- **Retrigger:** turn it on (LFO tab) so it fires fresh on every note instead of free-running — otherwise you get the same phase-drift problem as an unsynced LFO on Volume.
- **Shape matters:** a symmetric **Sine** swings both above *and* below center — the "below center" half briefly darkens the filter, which reads as the sound getting **more grave/dark** rather than a clean bright pop. A **Saw Down** shape only falls, which behaves more like an actual decay envelope (starts open/bright, falls once, stays there) — closer to what "one-shot pop" usually means.
- **Rate has a real audible threshold, not just "fast vs slow":**
  - Below ~20Hz: felt as a shaped movement — a sweep or a snap with an actual contour.
  - At/above ~20Hz: enters **audio rate** — the modulation itself starts to sound like a *texture or tone* (a subtle buzz/ring), because the ear now hears the modulation frequency directly, not just its effect.
  - Tested on this build: **999Hz** (near-instant, audio-rate) read as texture/buzz; **30–80Hz** read as an actual shaped hit. 30–80Hz was the preferred choice.
- The **destination assignment lives in the separate "Mod" tab** (Drift's actual Mod Matrix — Source/Target/Amount), not in the LFO tab's own local "Amount/Mod" pair, which is just an internal send level, not a real parameter target.

This is a general Drift/synthesis principle, not kick-specific: **any LFO's Rate decides whether it reads as movement or as tone** — worth remembering for future patches (pads, risers, anything with modulation).

## 8. Octave down for real depth, and why hits still aren't perfectly identical

**Making the kick actually sound lower/deeper** — EQ and Saturator can't manufacture a missing fundamental, they only rebalance what's already there. The real levers, in order of directness:
1. **Osc 1's Oct knob** (or transposing the note down) — the only thing that changes the actual fundamental. Confirmed on this build: **Oct -2** made the kick noticeably deeper.
2. **Amp Envelope (Envelope 1) Decay** — stretching it slightly (e.g. 250-350ms) gives the low frequency more time to actually register as bass rather than being cut off before it's audible.
3. **Pitch envelope depth** (Envelope 2 → Pitch Mod amount) — a bigger drop means more of the transient starts genuinely sub-range before settling.

**Why the compressor's GR curve — and the kick's actual sound — isn't perfectly identical hit to hit**, even with Drift's instability macro at 0%, Auto Release off, no external sidechain, and uniform velocity: the most likely remaining cause is that **Drift's oscillator phase isn't reset on every note-on**. This is separate from the LFO's own Retrigger setting (which only resets the LFO's phase, not the oscillator's) — many analog-modeled oscillators (Drift's whole design premise) deliberately let the waveform free-run continuously rather than snapping to a fixed start point per note, mirroring how real analog hardware oscillators never actually stop. Each note's first few milliseconds then start from a slightly different point in the cycle, which a fast-Attack Peak-detecting compressor will register as a slightly different transient every time.

**Decision on this build:** kept as-is rather than chased further. This kind of subtle non-quantized inconsistency is consistent with a raw/hardgroove aesthetic that leans on alive, non-identical repetition rather than pristine digital uniformity — real drum machines and analog synths aren't perfectly identical hit to hit either.
