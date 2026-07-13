---
title: Sidechain Ducking
date: 2026-07-12
tags: [techniques, mixing, compressor, sidechain, ducking, techno, low-end]
---

# Sidechain Ducking

A **compressor** is a device that turns a track down automatically when the sound gets loud. **Sidechain** means the compressor doesn't listen to its *own* track — it listens to a **different** one. Put a sidechained compressor on the rumble, tell it to listen to the **kick**, and the rumble ducks out of the way every time the kick hits, then swells back between hits.

Two payoffs at once:

1. **Punch** — the kick gets the low end to itself for its transient; no more fighting the rumble.
2. **Pump** — the rhythmic swelling-back is the "breathing" motion of dance music. This is the *automatic* version of the manual [[kick-bass-interlock|kick/bass interlock]].

## Recipe (Live Lite, rumble track)

1. Drop a **Compressor** (Audio Effects) on the rumble track, *after* the EQ.
2. Top-left of the device: unfold the **Sidechain** section (▸ triangle) → turn **Sidechain on**.
3. **Audio From:** the drums track → in the second dropdown pick the **kick pad's chain** (e.g. *Kick Machine 4*) so only the kick triggers the duck, not the hats.
4. Pull **Threshold** down until the **GR (gain reduction) meter** dips ~6–10 dB on each kick.
5. Set **Attack** fast, tune **Release** by ear.

## Settings rules of thumb

| Control | Value | Why |
|---|---|---|
| Ratio | 4:1 or higher | Decisive duck, not a gentle nudge |
| Threshold | until GR ≈ 6–10 dB | Depth of the dip |
| Attack | 0.1–1 ms | Duck must start the instant the kick hits |
| **Release** | ~100–250 ms | **The groove knob** — how fast the swell-back is; tune while looping |
| | | Too short = no pump; too long = track never recovers between kicks |

## Where to apply

- **Rumble: essential.** It's continuous sound sitting exactly where the kick lives.
- **Bass: optional.** Offbeat bass already avoids the kick in time; ducking it adds extra pump — taste call.
- **Pads/atmosphere: classic** for the big EDM pump — style-specific, heavier-handed.
- Never on the drums themselves or the Master (for now).

## Verify

Loop the Drop scene, toggle the Compressor on/off (device LED): **on** should sound *punchier and cleaner*, with a subtle forward pump — not obviously quieter. If the pump is seasick-obvious, raise the Threshold or shorten the Release.
