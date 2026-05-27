---
title: Swipe play/pause button drift on pause (RESOLVED)
date: 2026-05-27
tags: [culla-music, bug, swiftui, resolved]
---

# Swipe play/pause button drift on pause — RESOLVED ✅

> Resolved **2026-05-27** after ~9 failed attempts. The fix was a one-line frame pin. The breakthrough was **getting evidence before guessing a 10th time**.

## Root cause
The play disc and the hot-preview **progress ring share one ZStack** in `SongCardView`'s `.overlay(alignment: .center)`. That ZStack had **no fixed size**, so it sized to its biggest child:
- ring present → **86×86**
- ring absent → **72×72**

On pause, `showHotProgressRing` flips false, the ring is **removed**, the box **shrinks 86→72**, and the centred play disc gets **re-resolved to a new position** as it shrinks. That re-resolution *is* the "drift bottom-right then spring back". This is exactly the old "critical finding #6": a static material still drifted because **a parent re-resolves the disc's position** — the resizing box was that parent.

## Why it masqueraded as "autoplay-only" (the clue that cracked it)
The ring only shows when `playbackDuration > 0`. For a hot clip, the duration **loads asynchronously a beat after playback starts** (`MusicLibraryService.playHotClip` sets `playbackDuration = 0`; the clip observer fills it in ~0.1s+ later). So:
- **Autoplay ON** → preview has played a while before you reach over to pause → duration loaded → **ring is on screen** → pausing removes it → drift.
- **Manual quick play→pause** → duration hadn't loaded yet → **ring never appeared** → nothing to remove → no drift.

It was never about autoplay. It was about whether the ring was actually on screen at pause time. Autoplay just guarantees it is.

## The fix
`SongCardView.swift`, the centre overlay:
```swift
ZStack {
    if showHotProgressRing { hotProgressRing }
    playButton
}
.frame(width: 86, height: 86)   // pin to the ring's size — box can't resize
.opacity(chromeRevealed ? 1 : 0)
.scaleEffect(chromeRevealed ? 1 : 0.85)
```
The box is now constant size whether or not the ring is mounted, so the disc has no layout change to be dragged along by. Liquid Glass, the ring, and centring are all visually unchanged (the box was already 86×86 whenever the ring showed). **Verified on device: no drift.**

## How it was diagnosed (the method that worked)
Three cheap observations bisected the whole problem before any code changed:
1. **What moves?** → *only the disc, not the card.* Killed the `snapBack`/`cardOffset` whole-card theory that was the prior "START HERE".
2. **Manual play→pause with autoplay off?** → *no drift.* Pointed at a state that's only present after a preview has run a while.
3. **Hot preview on/off?** → *on.* Put the ring in frame.
4. **Confirming test:** hot preview **off** + pause → *no drift.* Proved the ring's removal was the cause before touching code.

## Lesson (reinforced)
After ~2 failed blind guesses on a visual/motion bug, **stop and get ground truth** (what exactly moves, when, under which setting). Three 15-second observations succeeded where 9 code-only attempts failed. See [[culla-music]].

## Kept from earlier (still correct)
- `b1c5861` — `.animation(nil, value: progress)` on `ProgressBarView`'s fill (separate bar-retract bug, stays fixed).
