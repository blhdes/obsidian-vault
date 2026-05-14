---
title: Up-swipe = Heart / Loved
date: 2026-05-12
tags: [culla-music, idea, feature, gesture, swiping, shipped]
status: shipped
shipped_on: 2026-05-13
---

# Up-swipe = Heart / Loved

> **✅ Shipped 2026-05-13.** Commits `128e9d5` (gesture + auto-created *Culla Loves*) → `be56d03` (Settings picker `LovedPlaylistPickerSheet`) → `1c45fd6` (rollback on remote-write failure). Storage key: `@AppStorage("lovedPlaylistID")` — Apple Music playlist ID, empty = Auto / *Culla Loves*. Resolved open questions below.

The MVP explicitly reserved up/down swipes for "later". Wire **up-swipe** to a quick *Loved* action — for songs you want to keep without committing to a specific playlist target right now.

## Behavior

- **Up-swipe** → adds the song to a configurable "Loved" target. Two flavors to consider:
  - A dedicated Culla-created playlist (e.g. *Culla Loves*), or
  - Apple Music's native **favorite/star** action on the track, if MusicKit exposes it.
- Right-swipe still drops onto a sidebar playlist. Left-swipe still dismisses.
- The card flies upward off-screen with the same soft transition family the sides already use.

## Open questions — resolved

- **Gesture threshold.** Reused the existing 100pt threshold but added horizontal-dominance gating on the right/left branches, so a fast right-up flick still goes right. Up only fires when the drag is vertical-dominant past the threshold.
- **Apple Music native favorite?** Dropped — `MusicKit.Song` still doesn't expose a "rate as loved" mutation. Went with the dedicated playlist (fully under our control).
- **Settings entry.** Shipped as a `LovedPlaylistPickerSheet` (mirrors `SourcePlaylistPickerSheet`) with an "Auto (Culla Loves)" row at the top that clears the setting back to default.
- **Undo.** Restores deck position + reverses the Apple Music write via the same undo path used by right-swipe.

## Notes — as shipped

- Pink heart overlay mirrors the trash overlay on left-swipe.
- Loved chip in the membership chip row gets a small ♥ glyph.
- **Rollback path** (`1c45fd6`): Apple Music's *Smart Favorites* and other system-managed playlists silently reject `MusicLibrary.shared.add()`. On remote-write failure, `rollbackLoved` removes the action from history, deletes the `SortedSong` row, and reverses the in-memory exclusion + membership entries — otherwise songs vanished from the library deck on the next session.
- Down-swipe stays unbound for a future "Share" action.

## Follow-ups

- Membership chips already reflect the loved playlist (a second up-swipe on the same song no-ops).
- Onboarding screen mention: see [[onboarding-flow]] — now eligible for the fourth screen since this shipped.
