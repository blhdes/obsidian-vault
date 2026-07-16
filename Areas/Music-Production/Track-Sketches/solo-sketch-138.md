---
title: Solo Sketch 138
date: 2026-07-12
tags: [track-sketch, techno, ableton, live-lite, self-driven]
---

# Solo Sketch 138

First **self-driven** sketch — no lesson plan, the user leads and sessions log what happens. Runs alongside [[ticket-to-detroit|Ticket to Detroit]], which stays the guided track.

## Stats

| | |
|---|---|
| **BPM** | 138 |
| **Key** | A minor |
| **Kit** | Cashon Kit (Drum Rack, Live Lite library) |
| **Setup** | Live Lite + APC Mini MK2 |

## State — 2026-07-12

Two 1-bar drum clips:

1. **Main loop** — kicks on the quarters (four-on-the-floor), Ride Machine on the `&`s (offbeat pattern, ride instead of open hat), Tamb Chop + Triangle Build accents at the end of the bar, velocity ramp drawn, **Swing 16ths** groove on the clip.
2. **Break variation** — same clip minus the kicks and the tamb chop (the empty-cell/break idea from the arrangement sessions, applied unprompted).

## Observations

- The offbeat pulse uses a **ride instead of an open hat** — same job (long metallic sound on the `&`s), darker color. Works.
- **The swing groove has almost nothing to move.** Every hit sits on quarters or `&`s, and Swing 16ths only shifts the `e`/`a` positions ([[../Techniques/swing-and-groove|known rule]]). Timing-wise the groove is near-silent right now; only its velocity component acts. Fix: add low-velocity `e`/`a` hits (16th ride/hat/shaker fills) so the swing has material.

### Arrangement take — 2026-07-15

- Drums (Cashon Kit) and the bass (Chord Analog) run continuously as the constant floor; Polymeter perc + Rumble enter together partway through as a real "something changed" moment; the Stab Dub Direct sample fires once later as a texture accent. Layered entrances instead of static scenes — good use of the arrangement, not just a straight scene dump.
- The **Riser** fired **twice back-to-back** right around where Polymeter/Rumble enter. Worth deciding on purpose: the riser's envelopes (Filter Freq + Volume) reset to their start value every time the clip retriggers, so two plays in a row is two short re-attacks, not one continuous longer swell. If a longer build was the goal, extending the riser clip itself (and its envelope lengths) to span both would read as one continuous rise instead. If two intentional short hits was the goal, this already does that.
- An unused **Audio** track (track 7, Ext. In, no clips) is sitting in the project — worth deciding whether to use that slot (Lite caps at 8 tracks) or remove it to free up the budget.
- Unclear from the take alone whether a Break/reduction section exists later in the timeline — check before moving to the mix pass.

### Arrangement take v2 — 2026-07-15 (rearranged)

- **Two-act shape now:** drums+bass constant floor throughout → **Build 1** (riser → Polymeter+Rumble enter + one Stab hit) → thins back to drums+bass only (the breakout/break moment) → **riser** → **Build 2 / bigger climax** (Polymeter+Rumble again + Stab now as an *extended repeated run* instead of one hit, more energy the second time).
- Turning the single Stab hit into a repeated rhythmic run for the second build is a real escalation move — gives the climax more identity than a simple repeat of Build 1.
- **Riser asymmetry:** Build 1's riser still fires twice back-to-back (same retrigger/envelope-reset behavior as before); Build 2's riser is a single hit. Worth confirming this is deliberate (shorter second build since the ear already knows what's coming) vs. an oversight on the first one.
- Track 7 (Audio) confirmed intentionally empty/reserved — only 6 MIDI/Sample tracks in use for now, no action needed.

### Riser debugging saga — resolved 2026-07-16

Extending the riser to 8 bars surfaced a chain of Ableton gotchas before it actually worked:
1. Typed the new length into the Loop section's Length field while **Loop was off** — inert, needed **End** (top of Clip box) instead.
2. Extended the clip but not the **note** — it kept releasing early via Drift's own Release time.
3. Tested via the **stale Session View clip** instead of the fixed Arrangement copy — the two are independent objects once captured, so edits to one never reached the other; deleted the old Session clip.
4. Still off — traced to **Drift's default internal modulation** (Freq Mod: Env 2 at 80%, present from Drift's default patch) fighting the drawn automation; zeroed it out.
5. Even then, leftover **duplicate/un-fixed riser blocks** from the earlier double-fire experiment were still sitting in Arrangement. Fix: rebuilt the riser clean in Session View, verified it solo, deleted every old Arrangement riser block, then **re-recorded fresh**. ✅ Confirmed working.

Lesson banked: when a device/automation "isn't working," check in this order — clip End vs. Loop length, note length matching clip length, which physical clip you're actually auditioning (Session vs. Arrangement copies), and any internal device modulation already routed to the same parameter.

## Techniques used

- Four-on-the-floor + offbeat long-sound pattern ([[../Techniques/open-vs-closed-hihat|known]])
- Groove Pool swing ([[../Techniques/swing-and-groove|known]])
- Break variation clip (empty-cell rule, known)
- Next up: [[../Techniques/rumble-bass|the rumble]] — reverb-generated low-end layer under the kick

## What to try next

1. ✅ **Rumble layer** — built 2026-07-12; see [[../Techniques/rumble-bass|Rumble]]. Kick track + rumble track now play together.
2. ✅ **Offbeat bass** — built 2026-07-12: analog-style bass preset, A1, four hits per bar on the `&`s ([[../Techniques/kick-bass-interlock|interlock]]). Checks: mono voice, staccato ~1/16, same Swing 16ths groove on the clip.
3. ⏭ **Stab/bleep — deliberately skipped for now.** Direction decided 2026-07-12: drums-focused, punchy hard groove — identity from percussion/texture, not melody ([[../Techniques/stab-vs-bleep|stab vs bleep]]). Revisit only if the track wants a hook later.
4. ✅ **Ghosts + fills** — built 2026-07-12 ([[../Techniques/ghost-notes-and-fills|note]]): ghosts at low velocity, clip duplicated to 4 bars, TWO fill versions as separate clips — ride roll + kick drop, and a perc-run variant. (Also fixed: pads dead = drum track lost record-arm when new tracks were added.)
5. ✅ **Polymeter perc clip** — built 2026-07-12 ([[../Techniques/polymeter-percussion|note]]): "Wood Under The Rug" preset, track 4, Length 0.3.0, hits every 3 sixteenths (constant dotted-8th roll). Fixes flagged: raise notes A1 → A3/A4 (was in bass register), add the Swing 16ths groove to the clip.
6. ✅ **Scenes** — built 2026-07-12: 4-scene structure (Intro/Build/Drop/Break), performed from the APC.
7. ✅ **Sidechain ducking** — built 2026-07-13: rumble sidechained to the kick (the essential case), and the bass ducked too on top ([[../Techniques/sidechain-ducking|note]] — the "optional" case, the user's own call).
8. ✅ **Sampling** — built 2026-07-13: **Stab Dub Direct** sample loaded into Simpler on a new track, trimmed (Start past the dead air), mode set to **One-Shot** — a dub-techno-flavored stab used as a texture accent, not a repeated harmonic element (keeps the drums-first direction intact). See [[../Ableton/sampling-with-simpler|Sampling with Simpler]].
9. ✅ **FX/riser** — built 2026-07-14: Riser track on Drift (Noise on, Osc 1/2 off), Filter Freq + Track Volume both automated rising across the clip via stacked Envelopes-tab lanes, Loop off. See [[../Techniques/riser-fx|Riser FX]].
10. ✅ **Recorded to Arrangement** — 2026-07-15: performed a take mixing scene launches with individual track entrances ([[../Ableton/arrangement-view-basics|known move]], extended per the mixed-source addendum) — see Observations below for what landed and what to check.
11. ✅ **Mix pass** — built 2026-07-16: [[../Techniques/eq-carving|EQ Carving]] applied (high-pass on Polymeter perc + Stab Dub Direct), [[../Ableton/master-limiter|Master Limiter]] added (Ceiling ~-0.3dB).
12. ✅ **Exported** — 2026-07-16: rendered to WAV via Main, Render Length padded past the last clip for the Reverb/Delay tail (Live 12 dropped the separate Render Tail field). **First fully self-driven track, start to finish.** 🎉

## State — 2026-07-16 (Complete)

All 8 planned layers built, arranged into a two-act structure, mixed, and exported. This is the first Solo Sketch 138 milestone: entirely self-directed from the original drum loop through export, including working through several genuine Ableton debugging chains independently (Loop vs. End fields, note length vs. clip length, Session/Arrangement clip independence, Drift's internal modulation). High-level map: [[../Techniques/techno-production-arc|Techno Production Arc]].
