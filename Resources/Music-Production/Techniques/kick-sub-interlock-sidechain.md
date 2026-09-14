---
title: Kick/Sub Interlock as a Sidechain Groove Tool
date: 2026-07-17
tags: [ableton, sidechain, compressor, groove, techno, hardgroove]
---

# Kick/Sub Interlock as a Sidechain Groove Tool

A different use of [[sidechain-ducking|sidechain ducking]] than the usual case. Built on Hardgroove 134.

## The usual case vs. this one

The earlier rumble/bass sidechain (Solo Sketch 138) existed to solve a **clash**: a continuous low-end layer had to duck out of the kick's way on every hit, or the two would fight for the same frequency space.

Here, **KICK and SUB never play at the same time** — they're already rhythmically interlocked (kick on the quarter notes, sub on the offbeat 8th notes between them). There's no frequency clash to fix. So the sidechain isn't cleanup — it's a **groove/motion tool**.

## Why it still matters

Even though the sub note starts *after* the kick's hit, the compressor's gain reduction from the kick is often still recovering (releasing) by the time the sub note begins. If Release is tuned right, the sub doesn't just start at full volume — it **swells up** into its own hit, because the duck is still lifting as the note enters. That swell is exactly the "rolling" quality the kick/sub interlock is supposed to have, rather than two elements just alternately thumping.

## Release = the groove knob (again)

Same principle as the rumble duck: **Release time is what shapes the feel.** But here it's shaping something more specific — how much "swell" happens right at the sub's note-on.

- Too short a Release: fully recovered before the sub hits → no swell, sounds static.
- Too long a Release: sub is still heavily ducked when its own note starts → sounds choked/late.
- Right in between: the sub visibly rises as it enters → the "rolling" feel.

## This build's settings

- **Sidechain source:** KICK, Post FX
- **SC Filter:** ~80Hz — filters the *trigger* signal (not the sub's audio) so only the kick's low thump fires the compressor, ignoring the click/saturation edge on top
- **Threshold:** -28.8dB, **Ratio:** 8.4:1, **Attack:** 0.01ms (instant), **Release:** 137ms
- **Detection:** RMS (smoother, more program-dependent than Peak — a good fit for a sustained sub rather than a transient)

Confirmed by ear: the sub audibly swells into each hit rather than sounding static or choked.
