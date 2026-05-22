---
title: Sort Songs From This Artist
date: 2026-05-18
tags: [culla-music, idea, swipe, discovery, artist]
---

# Sort Songs From This Artist

## Context

Captured while designing the **in-app artist hub** (v1):

- Triggered by a small `info.circle` button next to the artist name on the swipe card.
- Opens a native sheet powered by MusicKit's `Artist` resource: photo, genres, top songs (playable via the existing `ApplicationMusicPlayer`), similar artists (recursive drill-in), and a single "Search on Google" outbound button.
- Hybrid shape: native primary view, web as opt-in for socials.

The artist hub itself is in scope for v1. *This* idea — adding a **"Sort songs from this artist"** action inside the hub — was explicitly deferred.

## The Idea

A button on the artist hub that switches the swipe deck to only the user's library songs by that artist. Effectively a one-tap shortcut to "I want to triage everything I have by this person right now."

## Why Deferred

1. **Semantic overlap with the existing playlist source picker.** The picker already answers the question "where do these songs come from?" — adding an artist filter introduces a second axis (playlist OR artist) and the UX of combining them is unclear. Do you sort songs from this artist *within* a chosen playlist? Or does picking an artist reset the playlist scope?
2. **Non-trivial implementation.** Two plausible paths, both with caveats:
   - **`MusicLibraryRequest<Song>` with an artist filter** — requires the artist's `MusicItemID`, which library-only songs may not have. Would need a fallback to filter by `artistName` string match, which is fragile (featured artists, collabs, name variants).
   - **Catalog search by artist + intersect with library** — accurate but two round-trips per invocation.
3. **Cuts against the "swipe whatever comes next" feel.** Culla Music's core loop is review-as-it-arrives. A heavy filter button risks turning the swipe screen into a search tool.

## Sketch (for when v2 picks this up)

```swift
// In MusicSwipeViewModel
func setArtistScope(_ artist: Artist?) async {
    // 1. Resolve artist → set of song IDs in the user's library
    // 2. Reuse the existing scoping machinery (similar to sourcePlaylistID flow)
    // 3. Show a chip / banner at the top of the swipe screen so the scope is visible
}
```

The "scope chip" is the part most worth thinking about — without a visible affordance, users will forget they're filtered and wonder why their deck looks weird.

## Open Questions

- Does artist scope replace, layer on top of, or coexist with playlist scope?
- Should the artist scope persist across launches, or always reset?
- How does this interact with "unsorted only" mode — sort *unsorted songs* from this artist?
- Is the entry point only the artist hub, or also a long-press on the artist name on the card?

## Related

- [[Projects/Culla-Music/culla-music|Culla Music]]
- Artist hub v1 (info button → MusicKit-powered artist sheet) — currently being built.
- `CullaMusic/Views/HomeView.swift` — existing `SourcePlaylistPickerSheet` is the prior art for "scope the deck."
- `CullaMusic/ViewModels/MusicSwipeViewModel.swift` — where scope state lives.
