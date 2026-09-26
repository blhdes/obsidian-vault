---
title: Acid Lead Sound (Filter + Resonance)
date: 2026-05-30
tags: [sound-design, synth, filter, resonance, acid, 303, techno]
---

# Acid Lead Sound (Filter + Resonance)

The "acid" sound — squelchy, talking, alive — is the signature of early-90s techno. It came from the **Roland TB-303**, a small bass synth from 1981 that nobody bought (it was sold as a bass-guitar substitute and was terrible at it). Cheap second-hand units ended up in the hands of Chicago and Detroit producers, who discovered that turning two specific knobs while it played made it scream and gurgle. Acid was born by accident.

The "acid sound" isn't really about which synth you use — it's about **what you do with the filter**. Any monophonic synth with a resonant filter and a filter envelope can do it.

## The two knobs that make the sound

### Filter cutoff

A **filter** removes frequencies from a sound. The most common type is a **low-pass filter** — it lets *low* frequencies through and **cuts** the *high* frequencies. The **cutoff** is the dividing line.

```
Frequency →   low ─────────────── high
Low-pass:     ━━━━━━━━━━━━┓
                          ┗━━━━━━━━━━━ cut
                          ↑
                       cutoff
```

- **Cutoff fully open** = full bright sound, all frequencies pass.
- **Cutoff fully closed** = dull/muffled, almost silent (only the lowest frequencies survive).
- **Sweeping the cutoff** while a note plays = the sound opens up or closes down — the "wow" effect.

### Resonance

**Resonance** boosts the frequencies *right around* the cutoff point — a narrow spike. Add enough resonance and the filter starts to whistle / squeal at the cutoff frequency itself.

```
Without resonance:    ━━━━━━━━━┓
                               ┗━━━━━━━

With resonance:       ━━━━━━━━┳▲┓
                              ┗ ┗━━━━━━     ← peak at cutoff
```

- **Low resonance** = smooth, just removes highs.
- **High resonance** = the cutoff frequency *sings* — that's the acid squelch.
- **Very high resonance** = self-oscillates (whistles on its own).

## The combo that makes the acid sound

The signature acid character comes from **all three of these together**:

1. **Resonance turned up high** (60–80% in most synths) — gives the squelch.
2. **Filter envelope** modulating the cutoff — every time a note plays, the cutoff briefly opens then closes back down. That's the automatic "wow" on every note.
3. **A monophonic sawtooth-wave synth** — gives the buzzy, rich source material the filter has something to chew on.

## In Ableton (Drift synth)

[Ableton Live Suite ships **Drift**, a clean, beginner-friendly synth that has everything you need.]

Easiest path:
1. **Load an acid preset** to start — Browser → search **"acid"** → pick a Drift preset that says Bass/Lead/303.
2. Find the **filter section** in Drift's interface (middle of the device). Look for **Cutoff** and **Resonance** knobs.
3. With the loop playing, **slowly turn the Cutoff knob** left and right. Listen to the sound change — bright when open, dark when closed.
4. **Turn up Resonance** — hear the squelch emerge as you sweep the cutoff.

### What each Drift control does (quick reference)

| Control | What it does | Acid setting |
|---|---|---|
| **Cutoff** | The filter's frequency dividing line | Mid (we'll automate it later) |
| **Resonance** | Peak at cutoff (the squelch) | Up high — 60–80% |
| **Filter env amount** | How much the envelope opens the cutoff per note | Medium — moves the cutoff each time |
| **Filter env decay** | How fast the envelope closes back down | Short-medium — gives the "wow then close" feel |
| **Voicing → Mono** | One note at a time, no chord-stacking | Mono / unison — acid is monophonic |

If your loaded preset already has these dialed in — even better. **Don't try to build the sound from scratch yet.** Use a preset, then tweak.

## What to listen for

Play your 4-note lead motif and listen for:

- **Squelch on each note** — every note should have a little "wow" character, not just plain.
- **Sits above the bass** — should be clearly audible in the upper-mid range, not stepping on the bass.
- **Not too loud** — it's a hook, not a melody you're trying to remember. Pull the Lead fader down until it sits *with* the drums, not on top of them.

## What comes later (don't worry about yet)

- **Automating cutoff over time** — drawing the cutoff sweep into Arrangement View so the whole track breathes (the famous "filter sweep build-up").
- **Distortion / overdrive** — pushing the lead into a Saturator for grit. Optional grime.
- **Slide / glide / portamento** — making notes "bend" into each other (the classic 303 trait).
- **Sound design from scratch** — building this from an init patch (Path 2 territory, deeper).

## Related

- [[Resources/Music-Production/Theory-Basics/a-minor-pentatonic|A Minor Pentatonic]] is not a typo — meant [[../Theory-Basics/a-minor-pentatonic|A Minor and the Pentatonic Shortcut]] — what notes the lead plays
- *(first used in an early sketch, since retired)*
- [[kick-bass-interlock|Kick / Bass Interlock]] — the rhythm bed this lead sits on top of
