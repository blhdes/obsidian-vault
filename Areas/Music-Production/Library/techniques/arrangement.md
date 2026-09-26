---
topic: Arrangement
type: technique
updated: 2026-09-26
related: [[techniques/session-template]], [[techniques/drum-grooves]]
---

# Arrangement

## Summary
Hypnotic and raw arrangements change through **subtraction, filtering and modulation**, not by adding a new element every 8 bars. The strongest move is still the kick leaving and coming back.

## Core
| Step | Direction | Source |
|---|---|---|
| Build | Loops per scene in Session View, one element per track. An empty cell stops that track when the scene launches | [ear] |
| Capture | Record scene launches and macro moves into Arrangement | [ear] Solo Sketch 138, 2026-07-15 |
| How capture works | Control Bar **Arrangement Record** on, then launch from Session. Live logs launched clips, clip property changes, mixer/device moves (automation) and tempo/time-signature changes named in scenes. It copies clips, no new audio. Stop with the button or by stopping playback | [manual] |
| Session vs Arrangement | Per track, only one plays at a time. After launching a Session clip, press **Back to Arrangement** (global or per track) to hear the Arrangement again | [manual] |
| Sections | 16–32 bars. Micro-changes every 4–8 (a hat in, a filter opening, a send throw) | [?] |
| DJ ends | 16–32 bars of stripped drums at the start and the end | [?] |
| Breakdowns | Can keep the rumble/sub. The "drop" can simply be the kick returning | [?] |
| Edit | Subtract first. Automate sends, cutoff and macros for motion | [?] |
| Budget | 5–7 sounds total is common. Interest comes from varying them, not from adding more | [?] |

## Variants
- **Sub as hook:** the sub or rumble carries the peak instead of a new element.
- **No-drop:** continuous tension with filter and send automation only.
- **Classic sections:** Intro (drums) → Build (+ bass, filtered lead) → Drop (everything) → Break (no kick) → Outro (mirror of intro). [ear] Solo Sketch 138, 2026-07-15
- **Noise riser:** Drift with only Noise on, one held note over 1–2 bars, two clip envelopes on the same clip (cutoff closed→open + volume quiet→loud), Loop off, launched by hand 1–2 bars before the drop. Very EDM-coded. Keep it short and restrained for techno. [ear] Solo Sketch 138, 2026-07-14
- **Stutter build:** Beat Repeat last on a playing track (e.g. HATS). Automate **Grid** 1/8→1/32 (slice size) and Chance ~30%→100% over 1–2 bars; Chance 0% elsewhere = no repeats. Built from the track's own material. [manual] parameters · [?] recipe
- **Beat Repeat map:** `Interval` = how often it captures (1/32 to 4 Bars), `Offset` shifts that point · `Chance` = probability a repeat happens · `Gate` = total repeat length in 16ths · `Grid` = slice size (`No Triplets`, `Variation` + modes Trigger / 1/4 / 1/8 / 1/16 / Auto) · `Pitch` (resampling, down only) + `Pitch Decay` · `Decay`, `Volume` · output modes Mix / Insert / Gate (Gate suits a return track). [manual]

## Gotchas
- Riser clip with Loop off: extend the clip **End** (not Loop Length) *and* drag the held note out to match, or the extra bars are silent. [ear] Solo Sketch 138, 2026-07-16
- Beat Repeat only repeats incoming audio: nothing playing through it = silence. [manual] Keep the smallest Grid to the last few beats, or it turns into noise. [?]

## Used in
- Solo Sketch 138 (sections, riser, 2026-07-14/15)

## Sources
- Live 12 manual, Recording Sessions into the Arrangement: https://www.ableton.com/en/manual/session-view/
- Live 12 manual, Beat Repeat: https://www.ableton.com/en/manual/live-audio-effect-reference/
