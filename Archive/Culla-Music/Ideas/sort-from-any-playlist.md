---
title: Sort from any playlist with MOVE/COPY toggle
date: 2026-05-06
tags: [culla, idea, feature]
---

Allow the swipe deck to be sourced from any playlist, not just the general library. When the source is a specific playlist, surface a **MOVE / COPY** segmented control (mirrors how Culla for photos handles album-to-album sorting).

## Behavior

- **Source = General library (all)** → no segmented control. Right-swipe always copies the song into the target playlist (current behavior).
- **Source = a specific playlist** → segmented control appears:
  - **MOVE**: right-swipe adds to target playlist *and* removes from the source playlist.
  - **COPY**: right-swipe only adds to the target playlist; song stays in source.

## Notes

- Reuse the playlist removal path already implemented in `MusicLibraryService.removeSong` for the MOVE branch.
- The source picker likely lives next to (or replaces) the existing mode selector on `HomeView`.
- Dismissed mode already has a similar dual-action concept — the MOVE/COPY segmented control could share styling with it.
