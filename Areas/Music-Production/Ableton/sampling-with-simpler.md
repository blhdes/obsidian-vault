---
title: Sampling with Simpler
date: 2026-07-13
tags: [ableton, sampling, simpler, sound-design]
---

# Sampling with Simpler

Path 4 opener. Everything played so far has come from a synth (Drift) or a built-in drum kit. **Simpler** is the same *kind* of device — an instrument on a MIDI track — except the sound source is a chunk of **your own audio** instead of an oscillator.

You've actually touched Simpler once already: the acid bass on Sketch 01 was a Simpler preset (`Synth Bass Acid F`). That time the sample was hidden inside the preset. Today: drag in a raw file yourself.

## Getting audio in

- **Browser → Samples** (Live Lite's built-in library, smaller than Suite's), or drag **any audio file from Finder** straight onto a track.
- Drop it on an **empty MIDI track slot** → Simpler loads automatically with that file as its source.
- Drop it into an **existing track's Device chain** → same result, replaces/adds the instrument.
- **Capturing external/found audio (not already a file):** record it into Live first. On Mac, install a loopback driver (**BlackHole**, free) and build a **Multi-Output Device** in Audio MIDI Setup (BlackHole + your normal speakers, so you still hear it while it's captured) → set that as the system output → in Live, Preferences → Audio → enable BlackHole's channels in Input Config → new **Audio track**, Input = BlackHole → arm, record, play the source. The result lands as a normal clip (in Arrangement if you used the transport's Record button, since arming a track only enables it, it doesn't itself choose Session vs Arrangement).
- **Moving a clip you already recorded into Simpler:** drag the clip itself (from Arrangement or Session) onto an empty MIDI track (auto-creates a Simpler) or onto an already-open Simpler's waveform zone. If the drag between views misbehaves, the recording also exists as a real file in the project's `Samples/Recorded` folder — drag that from Finder instead, identical to any other sample.

## Key mapping — the new concept

Simpler maps your sample across the keyboard like any instrument: one **root key** plays it back at its original pitch, every semitone away transposes it up or down.

```
   C2        C3 (root)       C4
   ↓              ↓            ↓
 sample        sample        sample
 pitched      at original    pitched
 down 1 8ve     speed        up 1 8ve
 (slower,                    (faster,
  deeper)                     thinner)
```

- Root defaults to **C3** (mirrors where you dropped it in) — adjustable if needed.
- Same mechanism as a synth oscillator, except the "waveform" is literally your recording. Push it far from the root and it stretches/pitches audibly — sometimes wrong, sometimes a deliberate industrial/lo-fi texture move.

## Three playback modes

Top-left of the Simpler device, a **Classic / One-Shot / Slice** selector:

| Mode | Behavior | Use for |
|---|---|---|
| **Classic** | Plays (and can loop/sustain) for as long as the key is held — a synth voice built from your sample | Tonal or sustained material (a vocal note, a pad-like texture) |
| **One-Shot** | Plays the *entire* sample through once, no matter how long you hold or release the key | Percussive hits, foley, texture stabs — fire-and-forget accents |
| **Slice** | Auto-chops the sample into segments, one per key across the keyboard | Chopping a drum break/loop into playable pieces (flagged for a later session) |

For a drums/texture-first sketch, **One-Shot** is the natural starting mode — it behaves like an extra drum hit, not a held note.

## Trimming — Start / Length

The sample waveform is drawn across the middle of the device with two draggable markers:

- **Start** — drag right past any dead air/silence so the hit fires the instant you press the key.
- **Length** (the S/L markers, or the loop brace in Classic) — drag the tail in to cut unwanted ring-out.

Trimming is non-destructive — it only changes playback, the source file is untouched.

## What's not covered yet

**Warp** (time-stretching a sample to match project BPM) matters once you're pulling in a full loop instead of a one-shot hit — save it for when that comes up.
