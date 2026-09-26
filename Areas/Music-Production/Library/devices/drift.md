---
topic: Drift
type: device
updated: 2026-09-26
related: [[techniques/acid]], [[techniques/sub-bass]], [[techniques/kick]], [[techniques/stabs-textures]]
---

# Drift

## Summary
A compact subtractive synth (2 oscillators, filter, envelopes, modulation matrix) with a built-in "drift" of analog-style instability. Well suited to acid lines, basses and simple leads. It also handles kicks, stabs and noise risers.

## Core
| Parameter | What it does | Source |
|---|---|---|
| Voice mode (mono) + glide | Legato notes slide in pitch. This is the acid slide | [?] |
| Voices | Mono for kick/bass/lead. Poly (e.g. 32) for chords | [?] |
| Osc 1 Shape | 0% = pure sine. Morphs towards triangle/saw as it rises. Level is a separate fader in Osc Mix | [?] |
| Noise | Separate generator with its own toggle and dB level (default −∞). Pitchless source for risers | [?] |
| Env 1 | Hardwired to amplitude. No routing needed | [?] |
| Env 2 | Free modulation envelope. Default patch already routes it to Pitch Mod and Freq Mod | [?] |
| Pitch Mod (Osc Mix panel) vs Freq Mod (Filter panel) | Both default to Env 2. Pitch Mod = oscillator pitch, Freq Mod = filter cutoff. Easy to confuse | [?] |
| Filter type | Low Pass **Type I** (12 dB/oct, DFM-1 style, grittier) or **Type II** (24 dB/oct, Cytomic MS2 style, cleaner). Separate always-on HP knob | [?] |
| Filter envelope amount / decay | Short decay = "pluck/squelch" per note | [?] |
| Mod matrix ("Mod" tab) | Real Source/Target/Amount routing. The LFO tab's own Amount is only a local send | [?] |
| LFO | Rate in Hz or synced (e.g. `1:1`). Retrigger resets its phase per note | [?] |
| Mod matrix: velocity → cutoff/env | Accented notes open the filter | [?] |
| Drift | Amount of random pitch/timbre variation | [?] |

## Gotchas
- Toggles take `"On"`/`"Off"` via Producer Pal. [live]
- A new Drift isn't blank: Osc 2 is on and Env 2 is pre-routed. Clear it before building from scratch. [ear] Hardgroove 134, 2026-07-17
- A free Hz LFO drifts against the beat grid. A small sine LFO → Volume in the Mod tab causes a slow loudness swell that's easy to miss. [ear] Hardgroove 134, 2026-07-18
- LFO rate below ~20 Hz = audible movement. Above ~20 Hz (audio rate) it becomes texture or buzz. 30–80 Hz gave a shaped transient on a kick. [ear] Hardgroove 134, 2026-07-18
- Sine LFO swings both ways (it darkens as well as brightens). Saw Down behaves like a one-shot decay. [ear] Hardgroove 134, 2026-07-18
- Oscillator phase seems to free-run (it doesn't reset per note), so hits differ slightly even with Drift at 0%. [?]

## Used in
- Hardgroove 134 (kick, stab, lead) · Solo Sketch 138 (noise riser)

## Sources
