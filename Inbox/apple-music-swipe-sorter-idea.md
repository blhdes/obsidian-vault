---
title: Apple Music swipe-sorter app idea
date: 2026-05-01
tags: [idea, app, music, musickit, swiftui]
---

# Apple Music Swipe-Sorter (working name: TBD)

A Culla-style swipe app, but instead of sorting photos into galleries, it sorts **library songs that aren't in any playlist yet** into playlists. Same UX language: swipe to triage your music backlog.

## The problem it solves

Apple Music users (especially heavy listeners) accumulate hundreds of "Loved/Favorited" songs and library additions that never make it into a playlist. They sit in the void of the main library view forever. This app gives them a fast, gamified way to clean it up — one song at a time.

## Technical feasibility — yes (MusicKit)

Apple's official `MusicKit` Swift framework supports everything needed:

- Read library songs, playlists, favorites
- Create new playlists and add songs to them
- Toggle favorite status (iOS 17+)
- Play full songs (Apple Music subscribers) or 30-second previews (non-subscribers)
- Request library access via `MusicAuthorization.request()`

**The "songs not in any playlist" filter** is the only piece with friction:
- Fetch all user playlists → collect every song ID across them → subtract from full library
- Slow on large libraries (10k+ songs) — must cache aggressively
- Re-sync incrementally on app launch, not every fetch

## Legal viability — yes

Apple Music client apps are an established App Store category. Existing apps that prove the model:
- **Marvis Pro** — alternative Apple Music player
- **Soor** — Apple Music UI replacement
- **MusicHarbor** — new release tracker
- **Soundiiz** — playlist management & transfers

Requirements to publish:
- Use official MusicKit (no scraping, no private APIs)
- Add `NSAppleMusicUsageDescription` in Info.plist
- Respect Apple Music branding rules ("Listen on Apple Music" badge if linking out)
- Don't impersonate the official Apple Music app

## Proposed swipe gestures

Mirror Culla's mental model:

| Gesture | Action |
|---------|--------|
| Swipe right | Add to a playlist (pick from sidebar of "active" playlists, like Culla galleries) |
| Swipe left | Dismiss / skip (mark as "reviewed but not playlisted") |
| Swipe up | Favorite (toggle ❤️) |
| Swipe down | Share song |
| Tap | Play/pause preview |

## Key technical challenges

1. **Library indexing performance** — diffing songs against playlists for a 10k library is expensive. Cache song-IDs-in-playlists in a local SwiftData store and refresh incrementally.
2. **Playback UX** — auto-play 15–30s of each song while swiping (sample the chorus if possible via the catalog metadata)
3. **Apple Music subscription gating** — non-subscribers only get previews. UI should still feel good.
4. **"Dismissed" state** — like Culla's `DismissedPhoto`, persist a list of songs the user already chose to skip so they don't reappear.
5. **Playlist limits** — Apple Music has practical playlist size limits; check before bulk adds.
6. **Rate limits** — MusicKit has per-app quotas; batch requests where possible.

## Minimal MVP scope

Cut to the bone for the first version:

1. Request MusicKit + Apple Music authorization
2. Fetch library songs + all playlists once → compute "unplaylisted" set
3. Show one card at a time (artwork, title, artist, 30s preview button)
4. Swipe right → modal picker of existing playlists (no creation in MVP)
5. Swipe left → mark dismissed (SwiftData)
6. Persist dismissed list across launches
7. Stop. No favorites, no sharing, no new-playlist creation, no stats.

This validates the core loop: "do people actually want to swipe-sort their music?" before investing in the polish.

## Open questions

- Naming — keep "Culla" branding (Culla for Music?) or new identity?
- Reuse Culla's swipe-card SwiftUI components, or rebuild?
- Should it support YouTube Music / Spotify too, or stay Apple Music–only? (Spotify SDK is much more restrictive on iOS — probably stay Apple-only.)
- Pricing model — same freemium as Culla (X swipes/day free, unlimited on Pro)?

## Related

- [[Projects/Culla/Culla|Culla]] — the source pattern this builds on
