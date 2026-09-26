---
updated: 2026-09-25
---

# Verify queue

Precise questions for the **Ableton Knowledge connector**. When one is answered, fix the entry, change its tag to `[manual]`, and **delete the line**. This list is meant to empty.

Format: `- [ ] [[file]] — question`

- [ ] [[devices/operator]] — Exact names and units of the pitch envelope parameters (amount in % or semitones? decay in ms?)
- [ ] [[devices/operator]] — Which algorithms leave only Osc A audible as a single carrier?
- [ ] [[devices/drift]] — How do glide/legato work in mono mode, and how is velocity routed to filter cutoff/envelope in the mod matrix?
- [ ] [[devices/drift]] — Available filter types and their character
- [ ] [[devices/wavetable]] — Filter models available and how the modulation matrix assigns LFOs/envelopes to wavetable position
- [ ] [[devices/effects-overview]] — Full list of Saturator curve types in Live 12
- [ ] [[devices/effects-overview]] — Roar: stage routing modes, feedback and modulation options
- [ ] [[devices/effects-overview]] — Hybrid Reverb: which algorithm best suits dense, dark low tails (rumble)
- [ ] [[devices/effects-overview]] — Spectral Resonator / Spectral Time / Shifter: modes in Live 12
- [ ] [[techniques/sidechain]] — Compressor sidechain panel: parameter names, sidechain EQ, and audio-from options
- [ ] [[techniques/stabs-textures]] — Meld: oscillator types and modulation options
- [ ] [[tools/producer-pal]] — Are send levels writable via the Live Object Model? (test in a session: track mixer_device → sends → value) → answer by `[live]` test, not the connector

### Seed content (2026-09-25): review every `[?]` claim in these files against the manual
- [ ] [[techniques/kick]] — Operator kick method and chain
- [ ] [[techniques/rumble]] — Rumble chain (Hybrid Reverb, filtering, ducking)
- [ ] [[techniques/sub-bass]] — Sub sources and mono handling
- [ ] [[techniques/acid]] — Drift acid setup, and which MIDI Tools help with pattern generation
- [ ] [[techniques/metallic-perc]] — FM ratios, Corpus/Collision usage, Random MIDI effect
- [ ] [[techniques/stabs-textures]] — Wavetable/Analog stabs, texture modulation
- [ ] [[techniques/sidechain]] — Sidechain source options (Post FX / Post Mixer)
- [ ] [[techniques/returns]] — Return chains
- [ ] [[techniques/arrangement]] — Recording Session performance into Arrangement
- [ ] [[devices/effects-overview]] — Every row in the table

### Merged from archive (2026-09-26): `[?]` claims carried over from the old Techniques notes
- [ ] [[devices/drift]] — Confirm Env 1 is hardwired to amp, and the default patch routes Env 2 to Pitch Mod and Freq Mod
- [ ] [[devices/drift]] — Filter Type I / Type II: exact slopes and circuit models (DFM-1 / Cytomic MS2?)
- [ ] [[devices/drift]] — Does the oscillator phase reset on note-on, or free-run?
- [ ] [[devices/drift]] — Noise generator controls, and Osc 1 Shape range (sine → ?)
- [ ] [[devices/drift]] — Mod tab vs the LFO tab's local Amount; LFO Retrigger and sync options
- [ ] [[techniques/arrangement]] — Beat Repeat parameter names (Interval, Grid, Chance, Gate, Variation, Filter) and behaviour
- [ ] [[devices/effects-overview]] — Auto Filter types, LFO and Envelope Follower; Chorus-Ensemble and Phaser-Flanger modes and controls
- [ ] [[techniques/drum-grooves]] — Groove Pool parameters (Base, Timing, Random, Velocity, Amount) and Commit behaviour
- [ ] [[techniques/drum-grooves]] — Clip Length notation for sub-bar polymeter loops (`0.3.0`, `0.1.1`)
- [ ] [[techniques/drum-grooves]] — Ghost notes, fills, perc layer and pattern archetypes (review every `[?]`)
- [ ] [[techniques/sub-bass]] — Note length and register guidance (review every `[?]`)
