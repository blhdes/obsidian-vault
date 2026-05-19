---
title: Artist bio from MusicBrainz + Wikipedia
date: 2026-05-18
tags: [culla-music, idea, feature, artist, api, discovery]
---

# Artist bio from MusicBrainz + Wikipedia

Add a "About" section to the artist hub. MusicKit's `Artist` resource does **not** expose a bio field, so this needs an external data source. Both candidate APIs are free.

## Why

The artist hub currently has: photo, name, genres, top songs, similar artists, Google search button. The most obvious missing piece is a one-paragraph "who is this person" — the kind of context that turns the hub from a launcher into something you actually read.

## Candidate APIs

### MusicBrainz (CC0, free)

- Endpoint: `https://musicbrainz.org/ws/2/artist?query={name}&fmt=json` then `https://musicbrainz.org/ws/2/artist/{MBID}?inc=url-rels+wikipedia-rels&fmt=json`.
- **No auth required.** **Rate limit: 1 request/second per IP**, and a descriptive `User-Agent` header is mandatory (`CullaMusic/1.0 ( agomezurrea@gmail.com )`). Abusers get blocked.
- Strength: authoritative artist identity (MBID), plus official relationship links — Wikipedia, official website, Bandcamp, sometimes Instagram. The relationship graph is where the real value is, not the bio itself (it doesn't have one).
- Weakness: no bio text on its own. We use it for the *identity hop* — resolve "the right Coldplay" via MBID, then go fetch the bio elsewhere.

### Wikipedia REST API (CC-BY-SA, free)

- Endpoint: `https://en.wikipedia.org/api/rest_v1/page/summary/{title}`.
- **No auth, generous rate limits**, returns a clean plain-text `extract`, a thumbnail URL, and the canonical page URL.
- Strength: bio text. One round-trip per artist once we know the right page title.
- Weakness: disambiguation — "John" or "Madonna" hits the wrong page without help. That's exactly what MusicBrainz fixes.

## Recommended path: chain them

1. **MusicBrainz search by `artistName`** → returns ranked candidates. Pick best (exact-case match preferred, then top score).
2. **Fetch that artist's relationships** with `inc=url-rels+wikipedia-rels` → extract the `wikipedia` relationship's URL (which has the disambiguated title in the path).
3. **Wikipedia summary call** with that title → get the bio extract.
4. **Render**: 3-4 line truncated extract in the hub, with a "Read on Wikipedia" link (`SafariView`) for full article. Optional: an "Official site" link if MusicBrainz returned one.

MVP shortcut if Step 1-2 feel like too much: skip MusicBrainz, call Wikipedia summary with the raw artist name. Works for unambiguous artists, fails silently (no result) for common-name collisions — degrade to "no bio available" in those cases.

## Caching

Hard requirement for both APIs — repeated round-trips on every hub open burn rate limits and feel slow.

- Cache key: MusicBrainz MBID once we have it; fall back to lowercased artist name when we don't.
- Persist to `caches/` directory as JSON: `{ artistKey: { extract, wikipediaURL, mbid, fetchedAt } }`.
- Stale-after: a week is plenty for bio data.
- Pattern to mirror: existing `PlaylistTracksCache` (debounced disk writes, JSON snapshot) — same shape works here.

## Legal / attribution

- **MusicBrainz data is CC0** — no attribution required. Be polite and credit them anyway in Settings → About.
- **Wikipedia content is CC-BY-SA 3.0** — the "Read on Wikipedia" link doubles as attribution. Don't strip the link.

## Risks

- **User-Agent compliance.** MusicBrainz will block clients without a descriptive UA. Bake it in once via `URLSession` config or a shared `URLRequest` helper.
- **Rate limit storms.** A user drilling through many similar artists in one session could hit 1 req/sec easily. Throttle MusicBrainz calls, queue them serially.
- **Identity mismatch.** Even with MusicBrainz the search can hit the wrong artist for common names. Show the matched MBID's name next to the bio so the user can notice ("This is the Australian band, not the US one") — and fail-open: a wrong bio is worse than no bio.
- **Network failures.** Don't block the rest of the hub on this. Bio section loads independently, has its own loading/empty/error states.

## Implementation sketch

```swift
// Services/ArtistBioService.swift
@MainActor
final class ArtistBioService {
    static let shared = ArtistBioService()
    private let cache: ArtistBioCache  // disk-backed, debounced like PlaylistTracksCache

    func bio(for artistName: String) async -> ArtistBio? {
        if let cached = await cache.entry(forName: artistName) { return cached }
        // 1. MusicBrainz search → MBID + Wikipedia URL
        // 2. Wikipedia summary → extract + thumbnail
        // 3. Upsert and return
    }
}

struct ArtistBio: Codable, Sendable {
    let extract: String
    let wikipediaURL: URL
    let mbid: String?
    let fetchedAt: Date
}
```

The hub then `.task`s the bio fetch in parallel with the top-songs / similar-artists load, so its absence doesn't gate the rest.

## Open questions

- Do we want **language-aware** Wikipedia (`{lang}.wikipedia.org`) based on device locale? Simple to add, doubles the disambiguation pain — non-English Wikipedia often has thinner artist coverage.
- Truncation length for the in-hub extract: 3 lines? Until first paragraph break? Variable based on viewport?
- Should the bio section be a **collapsed-by-default expander** to keep the hub scannable, or always-expanded?
- If Wikipedia has a better artist photo than Apple Music, do we swap it in? (Probably no — that introduces visual flicker between sessions, and Apple's image is curated.)

## Related

- [[Projects/Culla-Music/culla-music|Culla Music]]
- [[sort-songs-from-this-artist]] — sibling deferred idea, same hub.
- Artist hub v1 already ships with: photo, genres, top songs, similar artists, Google search.
- `CullaMusic/Views/ArtistDetailSheet.swift` — where the bio section would render.
- `CullaMusic/Services/PlaylistTracksCache.swift` — pattern to copy for the disk cache.
