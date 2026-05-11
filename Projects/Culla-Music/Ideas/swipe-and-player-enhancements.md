---
title: Swipe & Player Enhancements
date: 2026-05-11
tags: [culla, idea, swiping, player, settings, apple-music]
---

# Swipe & Player Enhancements

Three proposals to explore. Not specs yet — these are ideas to evaluate, prototype, and refine before committing to implementation.

---

## 1. Playlist membership indicator during swiping

**Idea:** While swiping a song, surface which playlist(s) it already belongs to (one or many). This gives us a clearer picture of where a track already lives — or doesn't — before we commit to a sorting decision.

**Why it matters:**
- Avoids re-sorting a song into a playlist it's already in.
- Helps decide between "this fits in two playlists" vs "this isn't filed anywhere yet."
- Reduces second-guessing mid-session.

**Open questions:**
- Where on the swipe card does this live without cluttering the UI? (small chip row under the title? overlay on long-press?)
- How do we query playlist membership efficiently for the current song? (MusicKit `Playlist.tracks` lookup, or pre-compute an index on session start?)
- Do we show *all* playlists, or only the user's editable/created ones (exclude Apple-curated)?
- Performance — Apple Music index errors have bitten us before; cache aggressively.

---

## 2. Start songs from Apple Music "hot" preview point

**Idea:** Investigate whether songs currently start at 0:00 by default. If so, add a Settings toggle so songs begin at the Apple Music preset preview / "hot" start point (when available) instead of from the beginning.

**Why it matters:**
- The hot point is curated to be the most recognizable part of a track — better for fast triage during swiping.
- 0:00 often means 10–20 seconds of intro before the user can judge the song.

**Open questions:**
- Confirm current behavior: does our playback path force `playbackTime = 0`, or are we just inheriting MusicKit defaults?
- Does MusicKit expose a "preview start time" / `previewAssets.start` field per song? (Need to check `Song.previewAssets` and related metadata.)
- Fallback when no hot point exists → start from 0:00 silently? Or from a fixed offset (e.g. 30s)?
- Setting label idea: *"Start songs at the highlight"* with a short description.
- Only apply during swiping, or also in the regular player?

---

## 3. Minimalist progress bar with transparent transition

**Idea:** Add a sleek, minimal progress bar to the player. On each track change, fade it in/out with a transparent transition so it feels like part of the artwork rather than a UI chrome element. Tappable/scrubbable so the user can jump to different parts of a song.

**Why it matters:**
- Visible song structure → user can preview the bridge, chorus, or outro without guessing.
- Improves UX for both swiping (quick scrubbing) and full-player listening.
- Transparent fade keeps the player feeling minimal and "Culla-like" between tracks.

**Open questions:**
- Style: thin hairline bar at the bottom of the artwork, or a wider gesture-friendly hit area?
- Animation: cross-fade on track change, or slide/wipe?
- Scrubbing UX — haptic ticks on drag? Snap to musical sections if MusicKit ever exposes them?
- Show elapsed/remaining time, or stay completely chrome-less and rely on the bar alone?
- Does it appear on the swipe card or only in the expanded player view?

---

## Next steps

- Pick whichever of the three is cheapest to spike first (probably #2 — single setting + playback offset).
- For #1, sketch the UI placement before touching code.
- For #3, prototype the transition in isolation (SwiftUI `.transition(.opacity)` on the bar) before wiring it to real playback state.

Related: [[Projects/Culla/Culla|Culla project index]]
