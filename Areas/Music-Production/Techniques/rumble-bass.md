---
title: Rumble (Reverb Low-End Layer)
date: 2026-07-12
tags: [ableton, techniques, techno, low-end, reverb, rumble]
---

# Rumble (Reverb Low-End Layer)

A **rumble** is a sustained low-frequency tail that rolls *under* the kick, filling the space between kick hits so the floor never goes silent. It isn't played with notes — it's **generated from the kick itself**: a copy of the kick is run 100% through a reverb, then everything except the lows is filtered away. What's left is a dark wash that swells behind every kick.

> **Style note:** genre-specific. It's a staple of raw/hypnotic/industrial-leaning techno around 130–145 BPM. House and Detroit-style tracks usually use a played bassline instead ([[syncopated-bassline|known]]). A track can also use both — rumble low, bassline above it.

## Why a copy, not the kick itself

Reverb on the dry kick track would smear the punch ([[../Ableton/mixing-basics-and-effects|known rule: keep reverb off kick & bass]]). The rumble sidesteps this: the **dry kick track stays untouched**, and a *separate* track carries only the wet tail. Punch and wash coexist because they're on different faders.

## The Live Lite recipe

```
Kick copy ──▶ Reverb (100% wet) ──▶ Channel EQ (highs out) ──▶ fader LOW
```

1. **Duplicate the drum track** (`Cmd+D` on the track title). In the duplicate's clip, delete every note except the kicks.
2. **Reverb** after the Drum Rack: **Dry/Wet 100%** (only the wash, no dry click), **Decay ~1.5–3 s** — long enough that one kick's tail reaches the next kick.
3. **Channel EQ** after the Reverb: pull the **High** band all the way down and the **Mid** most of the way down. Only the low rumble should survive.
4. **Fader well down.** The rumble passes the mute test ([[adsr-envelopes|same as the pad]]): muted, the room feels emptier — unmuted, you feel it more than hear it.

## Settings rules of thumb

| Parameter | Range | Why |
|---|---|---|
| Reverb Dry/Wet | 100% | The dry kick already exists on the original track |
| Reverb Decay | 1.5–3 s | Tail must bridge the gap to the next kick at your BPM |
| EQ High / Mid | way down | Rumble lives below ~150–200 Hz; anything higher turns to mush |
| Track fader | low | Felt, not heard |
| Pan | center | Low end stays mono/center (known mixing rule) |

## Gotchas

- **Too loud = mud.** The most common failure. When in doubt, drop it another 3 dB.
- Decay too long stacks tails on top of each other and drones; too short leaves gaps. Tune by ear at the track's BPM.
- The rumble track counts against Lite's 8-track cap — budget for it.
- The kick + rumble pumping together is later perfected with **sidechain ducking** (Path 3's headline topic — not yet covered).
