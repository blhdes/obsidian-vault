---
title: Techno Sketch 01 — Foundation
date: 2026-05-29
tags: [track-sketch, techno, wip, drums, early-90s]
---

# Techno Sketch 01 — Foundation

The first real original sketch. Target vibe: **early-90s techno club** — warehouse energy, driving four-on-the-floor, raw drum machine textures, sparse and hypnotic rather than polished.

## Stats

| Field | Value |
|---|---|
| **BPM** | 130 |
| **Key** | A minor (chosen — works well for techno's dark/hypnotic feel; leaves room for an acid bassline later) |
| **Time signature** | 4/4 |
| **Length goal** | 1.5–2 min finished track |
| **Project filename** | `techno-sketch-01.als` |

## Reference vibe (technical)

- Driving 4-on-floor kick, **no swing** (techno is usually rigid grid; house has more swing)
- TR-909-style drum sounds — punchy kick, snappy clap, crisp/sizzly hats
- Sparse arrangement — same loop for many bars before a change
- Bass + drums first; lead/stab later as ear-candy

## Devices used so far

- **Drum Rack** → 909-style kit preset (Browser → Categories → Drums → search "909" → pick a kit, double-click onto a MIDI track)
- **Bass synth** → sub-bass preset (Browser → Categories → Sounds → Bass → Sub → any clean preset; or Drift with a sub-bass init)
- **Lead synth** → Drift loaded with an acid preset (Browser → search "acid" → 303/Bass/Lead-tagged Drift preset; resonance ~60–80%, filter envelope active)

## Current pattern (1 bar, 1/16 grid)

```
              1 e & a 2 e & a 3 e & a 4 e & a
Kick        : ● · · · ● · · · ● · · · ● · · ·
Clap        : · · · · ● · · · · · · · ● · · ·
Closed Hat  : ● · · · ● · · · ● · · · ● · · ·
Open Hat    : · · ● · · · ● · · · ● · · · ● ·
Bass (A1)   : · · ● · · · ● · · · ● · · · ● ·
Lead        : ● · · · · · ● · ● · · · · · ● ·
```

Lead notes (left to right): **A2, C3, A2, E3** — outlines the A minor triad.

Drum Rack MIDI notes (on the Drums track):
- Kick: **C1** · Clap: **D#1** · Closed Hat: **F#1** · Open Hat: **A#1**

Bass: separate MIDI track, sub-bass preset, all notes on **A1**, **1/16 length** (staccato).

See:
- [[../Techniques/open-vs-closed-hihat|Open vs Closed Hi-Hat]] — why open hats on offbeats drive the loop
- [[../Techniques/kick-bass-interlock|Kick / Bass Interlock]] — why bass sits *between* the kicks, never *on* them
- [[../Theory-Basics/a-minor-pentatonic|A Minor and the Pentatonic Shortcut]] — the note vocabulary the lead draws from
- [[../Techniques/acid-lead-sound|Acid Lead Sound]] — filter + resonance = the squelchy 303 character

**Note:** The open hat and the bass land on the same column (offbeat 1/8s). Same rhythmic position, different instruments — they reinforce each other.

## Session log

### Session 1 — 2026-05-29 — Kickoff

- Set project tempo to **130 BPM**, decided key **A minor**.
- Loaded a 909-style Drum Rack on MIDI Track 1.
- Drew the 1-bar foundation pattern above into a single MIDI clip.
- **Worked:** the offbeat open hats give the loop instant techno energy — way more momentum than just closed hats.
- **Didn't work / to revisit:** clap on every 2&4 feels a little obvious — might delay clap's entry to a later section for tension. Open hats are at full velocity, can probably sit ~20% quieter so the kick stays dominant.
- **Status:** 1-bar drum loop done, plays in Session View.

### Session 2 — 2026-05-29 — Bass

- Added a second MIDI track (`Cmd+Shift+T`), loaded a sub-bass preset, renamed track to `Bass`.
- Created a 1-bar MIDI clip on the **same scene** as the drum clip.
- Drew 4 bass notes, all on **A1**, on every offbeat 1/8 (the "&" between kicks). **Staccato** length (1/16).
- Launched the scene → drums + bass play together in lockstep.
- **Worked:** Kick and bass interlock cleanly — no muddiness, the low end has space to breathe. Loop now has the unmistakable techno push-pull.
- **Worth noticing:** bass and open hat hit the same offbeat position. Together they make the "&" feel really strong; if it gets too thick, drop the open-hat velocity further.
- **Didn't work / to revisit:** monotone A is solid but a little static — variations are in the technique note ([[../Techniques/kick-bass-interlock]]).
- **Status:** drum + bass foundation loop done, playing in Session View. Ready for melodic content.

### Session 3 — 2026-05-30 — Acid Lead

- Added a third MIDI track named `Lead`, loaded **Drift** with an "acid" preset (search "acid" in Browser).
- Created a 1-bar MIDI clip on the same scene as drums + bass.
- Drew a 4-note motif using only A minor triad notes: **A2 → C3 → A2 → E3** at positions 1, 2&, 3, 4&.
- Confirmed the synth was set to **mono** (one note at a time — acid is always monophonic).
- Tested filter knobs in real time: turning **Cutoff** opens/closes brightness; **Resonance** at ~70% adds the signature squelch.
- **Worked:** The 4-note triad outline (A-C-A-E) sounds unmistakably "in A minor"; lead sits clearly above the bass; resonant filter gives each note that little "wow" character.
- **Worth noticing:** Because the lead uses only A, C, E (the A minor triad), it sounds resolved no matter the order. This is the "safe" subset of the safer-still pentatonic.
- **Didn't work / to revisit:** lead is a touch loud — pulled fader down ~3 dB so it sits *with* the loop rather than on top.
- **Status:** Drum + bass + lead loop playing in Session View. The "skeleton" of the track is done — same elements as a typical early-90s warehouse cut.

## What's next

- **Next session:** **Cutoff automation** — draw a slow filter sweep on the lead so it opens and closes over multiple bars (the classic acid build-up). Will introduce Live's automation lane.
- **After that:** Arrangement — break into Intro/Drop/Break scenes and record into Arrangement View, then mix → export.

## File location on disk

_(fill in once saved in Ableton — e.g. `~/Music/Ableton/techno-sketch-01/techno-sketch-01.als`)_
