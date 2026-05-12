---
title: Lazy library count on Home
date: 2026-05-12
tags: [culla-music, idea, polish, home-screen, performance]
---

# Lazy library count on Home

The **Library** mode card on `HomeView` currently shows `—` — we intentionally skip the count to avoid a 5k-song scan on first launch. Resolve it lazily so the slot eventually shows a real number, matching what *Unsorted* and *Dismissed* already do.

## Why

- The empty slot is mildly off-brand: Unsorted and Dismissed both show numbers; Library doesn't.
- Phase 3's *Outstanding* list flagged this.

## Behavior

- Compute the count **after** the unsorted count resolves (the user already has something to look at while it computes).
- Cache it with the same fingerprint pattern: `sortedCount + dismissedCount + calendar-day`. Library count is unaffected by the chip toggle, so leave that out of the fingerprint.
- On cache hit → instant. On cache miss → kick off a paged `MusicLibraryRequest<Song>` count query in the background, replace `—` with the result when done.

## Open questions

- **API.** Does `MusicLibraryRequest<Song>` expose a count without paginating the whole library? If not, do a paged total-only walk and bail early once the page is < pageSize.
- **Invalidation.** Library size doesn't change on local sort/dismiss — but it *does* change when the user adds or removes songs in Apple Music. The daily rollover catches that; explicit invalidation isn't worth it.

## Size / risk

Small. Mostly an extraction of the existing pattern in `HomeViewModel.recomputeUnsortedCount()`. Main risk: first-run query latency on large libraries — mitigate by showing the loader only after the unsorted count has settled.
