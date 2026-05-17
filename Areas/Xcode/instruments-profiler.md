---
title: Instruments — profiling stutters and dropped frames
date: 2026-05-17
tags: [xcode, instruments, profiling, performance]
---

# Instruments

Apple's profiler. Ships with Xcode. You attach it to the app running on a **real iPhone** (not the simulator — the simulator lies about performance) and it records exactly where each frame's time went: main-thread blocks, slow image decodes, SwiftUI body recomputes, Core Animation commits, etc.

## Why it matters

A **stutter** is a frame that misses the display refresh budget — 16.6 ms for 60 Hz, 8.3 ms for 120 Hz ProMotion. The eye reads a missed frame as a hiccup or jank.

Instruments tells you **which line of code caused the miss**. That's the difference between:

- *"I read the code and it looks fast"* — a guess.
- *"I measured it running, and these 3 frames dropped because X"* — a fact.

You can't optimize what you haven't measured. Reading code can rule out obvious bugs but it can't find the surprises (an image decoder running on the main thread, a `body` recomputing 40× per swipe, a synchronous Core Data fetch).

## The main templates

When you launch Instruments (Xcode → Product → Profile, or ⌘I), you pick a template:

- **Time Profiler** — samples the CPU every 1 ms. Shows which functions ate the time. The go-to first stop.
- **SwiftUI** — shows view body invocations, state changes, and which views re-rendered. Critical for SwiftUI perf.
- **Animation Hitches** — flags every frame that missed its budget, with a stack trace per hitch.
- **Core Animation** — frame-by-frame breakdown of the render server.
- **Allocations / Leaks** — memory, not stutters, but useful when scrolls slow down over time.

For swipe-card stutters in Culla, the right combo is **Animation Hitches + SwiftUI + Time Profiler**.

## Worked example — profiling Culla's swipe deck

Goal: figure out why a swipe sometimes stutters when a new card comes in.

### 1. Build for profiling

In Xcode:
1. Plug in a real iPhone (the one you actually use Culla on).
2. Select the device as the run target (not "Any iOS Device" and not a simulator).
3. **Product → Profile** (⌘I). This builds a Release-configuration version with profiling symbols and launches Instruments.

> Profile builds matter. A Debug build is 5–10× slower in some paths and will mislead you.

### 2. Pick the template

In the template chooser:
- Choose **Animation Hitches** if you want every dropped frame flagged.
- Or **SwiftUI** if you suspect body recomputes (very likely for a card stack).
- Pro move: start with **Animation Hitches**, then re-run with **SwiftUI** once you know which interaction is bad.

### 3. Record the interaction

1. Hit the red ● record button.
2. On the phone: open Culla, go to the swipe deck, do **10–15 swipes** as you normally would. Mix left-swipes and right-swipes. Include the moment a new card appears under the top one.
3. Hit ■ stop.

Keep the recording short (≤30 s). Longer recordings make the timeline harder to read.

### 4. Read the timeline

- The top track shows the timeline of the session.
- **Animation Hitches** marks each missed frame with a red bar. Click one.
- The bottom panel shows the **stack trace at the moment of the hitch** — the actual function that was running when the frame budget blew.

What you're hunting for:
- `ArtworkImage` or `UIImage(data:)` on the main thread → image decode is blocking.
- `View.body` for the card view called 20+ times in one swipe → state churn.
- `CoreData` / `SwiftData` fetch on the main queue → a synchronous DB hit during the swipe.
- Long `CATransaction` commits → too many layers being rasterized.

### 5. Cross-check with SwiftUI instrument

Run again with the SwiftUI template. Look at the **View Body** track:
- Filter to the card view (e.g. `SwipeCardView`).
- If you see a row of body invocations clustered around each swipe, something is invalidating state more than it should — usually an `@State` or `@Observable` write on a parent that should be local.

### 6. Fix → measure again

After each fix, re-record and compare. The goal is to **prove the fix worked**, not assume it did. A win is: hitches go from N → 0 (or near 0) for the same interaction.

## Culla-specific things to watch for

Based on what's in the app today:

- **Artwork decode on the main thread** — see [[feedback_musickit_capability]]. `ArtworkImage` is the right primitive on iOS 19; if anything is still going through `AsyncImage` + `UIImage(data:)`, that's a prime suspect.
- **Palette extraction during swipe** — if the dynamic sidebar accent recomputes a palette synchronously when the top card changes, it'll show up as a fat block right at the swipe-commit moment. The recent `musicKit://` fix (commit `ac233f8`) is in this area — worth profiling.
- **Playlist membership lookups** — the recent cache (commit `9583912`) was for exactly this reason; chips used to compute synchronously. Confirm the cache is hit during swipes, not bypassed.

## Quick reference

| Symptom | Instrument to use | What to look for |
|---|---|---|
| Jank during swipe | Animation Hitches | Red bars → stack trace |
| Cards re-render too often | SwiftUI | View Body invocations per card |
| App heats up / battery drain | Time Profiler | Hot functions across the timeline |
| Slowdown after many swipes | Allocations | Memory growing without bound |

## Related

- [[Projects/Culla/Culla|Culla]]
- [[feedback_musickit_capability]] — artwork loading gotchas that often show up in profiles
