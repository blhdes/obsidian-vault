---
title: Name-Based Fallback for Missing Artist Counts
date: 2026-05-20
tags: [culla-music, idea, source-picker, musickit, follow-up]
---

# Name-Based Fallback for Missing Artist Counts

## Context

Follow-up to commit `5972cda` ("paginate library artists and drop misleading zero counts") in the [[Projects/Culla-Music/culla-music|Culla Music]] source picker.

After that fix, the artist tab of the source picker:

- Pages through the full library instead of stopping at the first ~100 alphabetical names.
- Omits the count badge for any artist where MusicKit's `\.artists, contains:` filter returns 0 results (uploaded tracks, fuzzy metadata, featured-only credits).

The omission is honest but leaves those rows visually inconsistent — most artists show a count, a handful don't.

## The idea

For the small subset of artists that came back with no count from the per-artist library filter:

1. Run a **one-time name-based catalog lookup** as a fallback to estimate their library track count.
2. Cache the resolved count on disk alongside the existing `artist_track_counts.json` snapshot so subsequent picker opens stay fast.
3. Only run the fallback for the artists missing counts — never the whole library.

## Why "later, not now"

The current per-artist filter is already the cheapest accurate path we have. Alternatives like iterating every library song and tallying via `Song.artists` would need 5000+ extra `song.with([.artists])` round-trips, which would meaningfully slow down picker open and goes against the lightweight-app goal.

The name-based fallback is a small, scoped improvement — worth doing once we have user feedback on whether the missing badges are actually noticeable in practice.

## Files involved

- `CullaMusic/CullaMusic/Services/MusicLibraryService.swift` — `refreshLibraryArtists` (pagination), `safeCountLibrarySongs` (nil-on-zero), `fetchAllArtistTrackCounts` (where the fallback would slot in)
- `CullaMusic/CullaMusic/Views/SourceScopePickerSheet.swift` — `loadArtistCountsIfNeeded` (stale snapshot re-fetch logic)
- `CullaMusic/CullaMusic/ViewModels/MembershipIndex.swift` — `writeArtistCounts` / `diskArtistCountsSnapshot` (cache layer)

## Related

- [[Projects/Culla-Music/Ideas/sort-songs-from-this-artist|Sort Songs From This Artist]] — the picker mode this badge lives in.
- [[Projects/Culla-Music/Ideas/lazy-library-count|Lazy Library Count]] — adjacent thinking on lightweight count strategies.
