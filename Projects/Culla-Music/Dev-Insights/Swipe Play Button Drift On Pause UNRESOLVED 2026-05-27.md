---
title: Swipe play/pause button drift on pause (UNRESOLVED)
date: 2026-05-27
tags: [culla-music, bug, swiftui, unresolved, handoff]
---

# Swipe play/pause button drift on pause — UNRESOLVED

> **Handoff note.** Open this in a fresh session (after `/clear`) to keep iterating on this single bug. Start with the **Strongest remaining hypothesis** section, then **Questions to confirm**.

## Status
- **UNRESOLVED** as of **2026-05-27**.
- We spent **more than 10% of the weekly Claude usage** on this one bug, across ~9 distinct fix attempts, and **it is still happening**.
- Reasoning from the code alone has failed repeatedly. Next session should get **visual ground truth** (slow-mo screen recording) and/or **instrument the code** before guessing again.

## Symptom
- The round **Liquid Glass play/pause disc** on the swipe card shifts slightly to the **bottom-right**, then **jumps/springs back to centre**, when you tap to **PAUSE**.
- It is a **pure translation** — no grow/shrink, just a positional shift, then it settles back in the correct centred spot.
- Timing: "a beat after" the tap, almost instant.

## KEY CLUE (most important)
- It **only happens when the "autoplay on swipe" setting is ON** — i.e. only when **pausing a currently-playing preview**.
- With autoplay OFF (nothing playing), there is **no drift**.
- So the trigger lives in the **pause-of-a-playing-preview** path.

## Relevant files
- `CullaMusic/CullaMusic/Views/SongCardView.swift` — the disc (`playButton`), the `.overlay(alignment: .center)` that hosts it on the artwork, `hotProgressRing`, `progressOverlay`, `timeLabels`.
- `CullaMusic/CullaMusic/Views/MusicSwipeView.swift` — `cardStack` computes `isPlayingThis` and passes `playbackPosition`/`playbackDuration` (gated `isPlayingThis ? … : 0`); the card's `.rotationEffect(.degrees(offset.width/40))` + `.offset(x: offset.width, y: offset.height * yVisualDamping)` driven by `cardOffset`; `dragGesture` (a `DragGesture` attached via `.highPriorityGesture`); `snapBack()` returns `cardOffset` to `.zero` via `.interpolatingSpring(stiffness: 150, damping: 15)`.
- `CullaMusic/CullaMusic/Services/MusicLibraryService.swift` — `stopPreview()`, `startFullSongPositionTimer()` (0.2s poll), `startClipPositionObserver()` (0.1s observer).

## Things tried and RULED OUT (none fixed it)
1. Play/pause icon symbol transition: `.contentTransition(.symbolEffect(.replace))` → `.opacity` → removed entirely. No effect.
2. Moved disc from `.overlay(alignment: .center)` on the artwork to a **ZStack sibling**. No effect.
3. Removed `interactive: true` from the disc's `.glassSurface`. No effect.
4. `.transaction { $0.animation = nil }` on the disc / play-controls ZStack. No effect.
5. Frame-locked the outer ZStack to a fixed square. No effect.
6. Replaced Liquid Glass with a **static `.ultraThinMaterial`** — the disc **STILL drifted**. **CRITICAL FINDING:** a static material cannot animate itself, so the disc's pixels move because a **parent re-resolves its position**. It is NOT the glass "flowing" and NOT the disc animating itself. (User wanted Liquid Glass restored — it has been.)
7. `.geometryGroup()` on the disc overlay: no effect, **and** it introduced a visible **black ring** artifact around the disc (reverted).
8. Removed the `progressOpacity` fades (`.animation(.easeInOut(0.35), value: progressOpacity)` on `timeLabels` and `progressOverlay`). No effect.
9. Removed the hot-preview ring's `.animation(.linear(0.2), value: playbackPosition)`. No effect — still happening. **Current committed state: `a0445dc`.**

## Separate, real fix already landed (KEEP)
- Commit `b1c5861` added `.animation(nil, value: progress)` to `ProgressBarView`'s fill so the bar doesn't retract-animate on pause. **Different issue, stays fixed.**

## Strongest remaining hypothesis — START HERE
The drift looks **exactly** like `snapBack()`: `cardOffset` springing from a small **positive (right + down)** value back to `.zero` via `.interpolatingSpring(stiffness: 150, damping: 15)`. **`snapBack` is the only right+down → centre spring in the whole codebase.**

- The play button is a `Button` **inside** `cardStack`, and `cardStack` carries `.highPriorityGesture(dragGesture)`.
- **Hypothesis:** tapping the disc registers a tiny drag → `cardOffset` gets set to a small right+down value → `snapBack()` springs the **whole card** (and the disc rides along, because the disc lives inside the card and the card's `.offset`/`.rotationEffect` transform everything).
- This neatly explains why **every disc-level fix failed** — the disc was never the thing moving; the **card** is.
- The puzzle to resolve: a tap-drag should be play/pause-agnostic, yet it's reported as "only with autoplay." Possible reason: during playback the position timer/observer re-renders the card every 0.1–0.2s, which may perturb gesture arbitration **only while a preview is playing**. Need to confirm.

**Next steps for this hypothesis:**
- Instrument: log `cardOffset` and whether `dragGesture.onChanged` / `onEnded` fire when tapping the play button (vs. dragging the card).
- Try: exclude the play button's hit area from the card drag; OR raise `dragGesture`'s `minimumDistance`; OR in `handleSwipeEnd`/`snapBack`, do **not** spring-snap sub-threshold (basically-a-tap) drags — set `cardOffset = .zero` without animation when the translation is tiny.

## Other hypotheses
- (a) `ArtworkImage` transiently reporting a different frame on the pause re-render, shifting the `.overlay(alignment: .center)` anchor down-right for a frame; lock the artwork's container frame.
- (b) **Get a slow-mo screen recording.** Reasoning from code has failed ~9 times — need to see exactly what moves relative to the card edges (is it the disc alone, or the whole card?).

## Questions to confirm next time
1. Is the **"hot preview" (`useHotPreview`, 30s clip)** setting ON? (Determines whether the ring or the bar is the active progress UI.)
2. Does the drift **also** happen on **manual play-then-pause with autoplay OFF**? This distinguishes "autoplay-specific" from "any playing preview being paused." If manual pause also drifts, the cause is the playing→paused transition generally (favours the `snapBack`/`cardOffset` hypothesis or a re-render glitch), not anything autoplay-specific.

## Context
Part of [[culla-music]]. See also the QA tracker in the project folder.
