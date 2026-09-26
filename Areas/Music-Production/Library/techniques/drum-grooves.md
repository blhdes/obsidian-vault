---
topic: Drum grooves
type: technique
updated: 2026-09-26
related: [[techniques/sub-bass]], [[techniques/metallic-perc]], [[techniques/arrangement]]
---

# Drum grooves

## Summary
The hat and percussion layer that makes a four-on-the-floor loop move: offbeat hats, a 16th layer in the gaps, swing, ghost notes, fills and polymeter. Kick and sub placement → [[techniques/sub-bass]].

## Core
```
         1 e & a 2 e & a 3 e & a 4 e & a
Kick   : ● · · · ● · · · ● · · · ● · · ·
Clap   : · · · · ● · · · · · · · ● · · ·
Closed : ● ● · ● ● ● · ● ● ● · ● ● ● · ●
Open   : · · ● · · · ● · · · ● · · · ● ·
```
| Step | Direction | Source |
|---|---|---|
| Hats | Open hat on the `&`. Closed hats skip the `&` so they don't choke it. `e`/`a` hats at velocity ~60–80 | [ear] Ticket to Detroit, 2026-07-10 |
| Swing | Drag a 16th swing `.agr` groove onto the clip. ~54–58% = subtle roll | [ear] Ticket to Detroit, 2026-07-10 |
| Groove Pool controls | **Base** (grid the groove is measured against; on-grid groove notes don't move) · **Quantize** (straight quantize applied first; 100% = snap to Base) · **Timing**, **Random**, **Velocity** (−100 to +100; negative inverts accents) · **Global Amount** (scales Timing/Random/Velocity for all grooves, up to 130%, also in the Control Bar). All real-time and non-destructive. Timing/Random 0% + Quantize = non-destructive quantize | [manual] |
| Commit | Writes the groove into the clip (MIDI: moves notes; audio: adds Warp Markers) and sets the clip's Groove to None. Commit only once decided | [manual] |
| Perc layer | Short, high sound (shaker, rim) in the `e`/`a` gaps. Low velocity, slightly off-centre pan, HP ~150–250 Hz | [start] |
| Ghost notes | 2–4 per bar on `e`/`a`, velocity 20–40, never on the kick's quarters | [start] |
| Fills | Every 4 or 8 bars, one move only: rising-velocity clap roll, kick drop on the last beat, perc run, or an open hat ringing into bar 1 | [start] |
| Polymeter | One perc clip of 3 beats (Loop Length `0.3.0` = bars.beats.sixteenths) over the 4/4 floor. It realigns every 3 bars. Only one polymeter element per track | [ear] Solo Sketch 138 |

## Variants
Pattern archetypes for raw/hypnotic (style-specific):
- **Rolling interlock:** every element in its own slot, nothing overlaps.
- **Odd polymeter:** a 5- or 7-sixteenth clip drifts faster. Length `0.1.1` = 0 bars, 1 beat, 1 sixteenth = 5 sixteenths; `0.1.3` = 7. [manual] notation · [start] feel
- **Rolling roll:** a continuous soft 16th roll under everything, with 3–4 accents off the kick's quarters. More tribal. [start]
- **Perc call & response:** voice A in bars 1–2, voice B answers in bars 3–4. [start]
- **Found-sound hits:** a clang or machine hit placed on the grid as a percussion part. [start]

## Gotchas
- Swing only moves notes on `e`/`a`. An 8th-note pattern sounds the same with swing on. [ear]
- Ghosts at full velocity are just clutter. A fill every bar stops being a fill. [start]
- Two polymeter loops at once = chaos. [start]

## Used in
- Ticket to Detroit (hats, swing, 2026-07-10) · Solo Sketch 138 (polymeter perc)

## Sources
- Live 12 manual, Using Grooves: https://www.ableton.com/en/manual/using-grooves/
- Live 12 manual, Clip View (loop Position/Length): https://www.ableton.com/en/manual/clip-view/
