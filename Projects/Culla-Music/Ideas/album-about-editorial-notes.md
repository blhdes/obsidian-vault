---
title: Album "About" section from Apple editorial notes
date: 2026-05-25
tags: [culla-music, idea, feature, album, musickit, discovery]
---

# Album "About" section from Apple editorial notes

A second "About" block — this time for the **album** — to sit alongside the artist bio that now ships on the hub. Where the artist bio answers "who is this person", an album blurb answers "what is this record".

## Key decision: use MusicKit, NOT Wikipedia

For albums the right source is Apple's own **`Album.editorialNotes`** (`.standard` / `.short`), available straight off the catalog `Album` resource — *not* Wikipedia.

Why this is the opposite call from the artist bio:

- **No disambiguation.** We resolve the catalog album directly, so there's no name-guessing. This sidesteps the exact album-page collision mess the artist bio had to fight (compilation/soundtrack pages leaking through). Album titles collide on Wikipedia *far worse* than artist names ("Greatest Hits", "1", "Home"…).
- **No external API** — no rate limits, no mandatory User-Agent, no caching layer to build.
- **No attribution burden** — it's first-party content already licensed inside MusicKit.
- **Right voice** — editorial notes are written *about the album*, which is the tone you want here.

### Tradeoffs

- **Uneven coverage** — plenty of albums (especially library-only / indie / older) have no editorial notes. Degrade silently, same "empty hides" rule the artist bio uses.
- **Promotional tone** — notes are marketing copy, not encyclopedic. For an album that's arguably fine, but it's a different register from the Wikipedia bio.

## Open question: placement

There is **no album surface in the app today** — `Album` only appears as an `albumTitle` string (HomeArtCarouselView, ArtistDetailSheet, MusicLibraryService). So the only existing home is the **artist hub**, and an album blurb inside an *artist*-scoped sheet (navigated via similar artists) could feel out of place.

Options:
1. A small **"From the album _X_"** card near the top-songs section on the hub, scoped to the song that opened the sheet. Lightweight, no new screen.
2. A future **dedicated album detail view** (tap an album anywhere → album hub with art, tracklist, this "About"). Bigger lift, but the natural long-term home.

Leaning option 1 as the MVP — it reuses the hub and the collapsible-card pattern already built for the artist bio.

## Implementation sketch

- Resolve the catalog `Album` for the opening song (via `song.albums` relationship, or a catalog lookup), then `.with([... editorialNotes])` if needed.
- Read `album.editorialNotes?.standard` (fall back to `.short`), render in the **same collapsible card** the artist bio uses (4-line clamp → tap to expand → one-way).
- Empty notes → hide the section, exactly like the artist bio's `.empty` state.
- No SafariView "read more" needed — there's no canonical external page; the Apple Music album link (already on the hub) covers "open in app".

## Related

- [[artist-bio-from-musicbrainz-wikipedia]] — the sibling artist "About"; reuse its collapsible card + empty-hides behavior.
- [[Projects/Culla-Music/culla-music|Culla Music]]
- `CullaMusic/Views/ArtistDetailSheet.swift` — where the artist bio lives; the collapsible-card pattern to copy.
