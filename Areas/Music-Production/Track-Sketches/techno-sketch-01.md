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

## Current pattern (1 bar, 1/16 grid)

```
              1 e & a 2 e & a 3 e & a 4 e & a
Kick        : ● · · · ● · · · ● · · · ● · · ·
Clap        : · · · · ● · · · · · · · ● · · ·
Closed Hat  : ● · · · ● · · · ● · · · ● · · ·
Open Hat    : · · ● · · · ● · · · ● · · · ● ·
Bass (A1)   : · · ● · · · ● · · · ● · · · ● ·
```

Drum Rack MIDI notes (on the Drums track):
- Kick: **C1** · Clap: **D#1** · Closed Hat: **F#1** · Open Hat: **A#1**

Bass: separate MIDI track, sub-bass preset, all notes on **A1**, **1/16 length** (staccato).

See:
- [[../Techniques/open-vs-closed-hihat|Open vs Closed Hi-Hat]] — why open hats on offbeats drive the loop
- [[../Techniques/kick-bass-interlock|Kick / Bass Interlock]] — why bass sits *between* the kicks, never *on* them

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

## What's next

- **Next session:** Add a **synth lead or stab** — short, filter-modulated, in A minor. Probably an "acid" flavor (303-style filter sweep) since it's the iconic early-90s techno texture. Will involve a tiny bit of theory (which notes from A minor sound good).
- **After that:** Arrangement — break into Intro/Drop/Break scenes and record into Arrangement View.

## File location on disk

_(fill in once saved in Ableton — e.g. `~/Music/Ableton/techno-sketch-01/techno-sketch-01.als`)_
