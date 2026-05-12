---
title: Up-swipe = Heart / Loved
date: 2026-05-12
tags: [culla-music, idea, feature, gesture, swiping]
---

# Up-swipe = Heart / Loved

The MVP explicitly reserved up/down swipes for "later". Wire **up-swipe** to a quick *Loved* action — for songs you want to keep without committing to a specific playlist target right now.

## Behavior

- **Up-swipe** → adds the song to a configurable "Loved" target. Two flavors to consider:
  - A dedicated Culla-created playlist (e.g. *Culla Loves*), or
  - Apple Music's native **favorite/star** action on the track, if MusicKit exposes it.
- Right-swipe still drops onto a sidebar playlist. Left-swipe still dismisses.
- The card flies upward off-screen with the same soft transition family the sides already use.

## Open questions

- **Gesture threshold.** Up needs a clear minimum vertical distance so it doesn't fight a casual right-swipe that drifts upward. Reuse the existing thresholds or pick a stricter one for vertical.
- **Apple Music native favorite?** `MusicKit.Song` doesn't currently expose a "rate as loved" mutation in the public API. If we can't reach the native star, the dedicated playlist is the fallback — simpler and fully under our control.
- **Settings entry:** *"Up-swipe target"* with a row that opens the same `SourcePlaylistPickerSheet` we already have, defaulting to *Culla Loves* (auto-created on first up-swipe).
- **Undo:** must restore the loved-playlist write the same way right-swipe undo restores the playlist add.

## Notes

- Down-swipe stays unbound for a future "Share" action — keep it separate from this idea.
- Membership chips should reflect the loved playlist too, so a second up-swipe on the same song no-ops gracefully.

## Size / risk

Small. Main risk: gesture-threshold tuning so vertical and horizontal don't conflict.
