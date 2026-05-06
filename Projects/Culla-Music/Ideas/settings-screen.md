---
title: Settings screen
date: 2026-05-06
tags: [culla, idea, feature]
---

A dedicated Settings screen to consolidate user preferences, mirroring the one in the original Culla app.

## Items

- **Author display name**: let the user override `authorDisplayName` passed to `MusicLibrary.shared.createPlaylist(...)` so playlists created by Culla aren't stamped with the app's bundle name in Apple Music.
- **Haptics**: master toggle for swipe / sort feedback (already wired through `Haptics` helper, just needs UI surfacing).
- **Sidebar colour palettes**: themable palette for `PlaylistSidebarView` highlight and accent. Reuse the palette concept from the original Culla app.
- **App theme**: System / Light / Dark switcher.

Keep the screen lean — single grouped form, accessible from `HomeView` or a gear button on `MusicSwipeView`.
