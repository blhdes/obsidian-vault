---
title: download-music skill
date: 2026-05-22
tags: [claude, skill, music, dj, yt-dlp]
---

# 🎵 `download-music` skill

A custom slash command that downloads a song from YouTube at max audio quality and embeds the official album cover art — all in one step. Created for DJ library management.

## Where it lives

```
~/.claude/commands/download-music.md            ← the skill definition (slash command)
~/.claude/skills/download-music/embed_cover.py  ← cover-art helper script
```

This is implemented as a **slash command**, not a `SKILL.md` skill. When the user types `/download-music`, the markdown file is loaded into the conversation verbatim and Claude follows its instructions.

## How to use it

```
/download-music <YouTube URL>
```

Examples:
- Single track: `/download-music https://www.youtube.com/watch?v=...`
- Full EP/album: `/download-music https://www.youtube.com/playlist?list=...`
- Album from one track: `/download-music <track URL> and grab the rest of the EP too`

## Where files land

```
~/Music/Library/
└── <Artist>/
    ├── <Album>/
    │   ├── cover.jpg        ← one per album folder
    │   └── track.mp3
    └── Singles/
        ├── cover.jpg        ← shared across all the artist's singles
        └── single.mp3
```

**Only writes under `~/Music/Library/`** — never into sibling app folders (`Mixxx/`, Apple Music's `Music Library.musiclibrary/`, `Engine Library/`).

## How cover art is sourced

The `embed_cover.py` script tries sources in order until one returns a valid image:

0. **Existing `cover.jpg` in the destination folder** (skipped for `Singles/`) — multi-track album downloads reuse the cover fetched for track 1.
1. **MusicBrainz + Cover Art Archive** — retries without album filter on 0 results, ranks releases (skips DJ-mixes, prefers non-compilations, fuzzy-matches album hint, earliest release date). Validates each download.
2. **iTunes Search API** — fallback for new releases not yet indexed on MusicBrainz. Uses the `100x100bb` → `3000x3000bb` URL trick for max-res.
3. **YouTube thumbnail** — last-resort fallback. Auto-crops the 1280×720 thumbnail to the center square (YT Music thumbnails letterbox the square cover in grey bars).

The script prints a `Source:` line so you know where the art came from.

## Dependencies

| Tool | Install |
|---|---|
| `yt-dlp` | `brew install yt-dlp` |
| `ffmpeg` | `brew install ffmpeg` |
| `mutagen`, `requests`, `Pillow` | `pip install mutagen requests Pillow` |

## How it handles edge cases

- **Bad YouTube metadata** (artist = channel name, title noise like `(Official Audio)`) → cleanup rules in the skill markdown parse the real artist from `Artist - Title` patterns and strip noise.
- **Multi-track playlists** → downloads in parallel, embeds covers sequentially (first track hits network, rest reuse `cover.jpg`).
- **Missing album** → defaults to `Singles/` folder.
- **Artistic stylings** (lowercase, leetspeak, `Fred again..`) → preserved, not normalized.

## History

- **2026-05-22** — moved music storage from `~/Music/Mixxx/` to `~/Music/Library/` for clean separation from app folders (Mixxx, Apple Music, Engine Library). Helper script moved from `~/Music/Mixxx/embed_cover.py` to `~/.claude/skills/download-music/embed_cover.py`.
- **2026-05-04** — `embed_cover.py` v2 shipped, folding in five failure modes discovered while downloading Charlotte de Witte and Fred again.. (see below). The v2 fallback chain (MusicBrainz → iTunes → YouTube thumbnail) and the byte-validation logic come directly from this debugging.
- **2026-05-02** — original skill created. One yt-dlp command + MusicBrainz cover-art lookup.

## Failure modes & rationale (history from 2026-05-03/04)

> Kept as a record of *why* the script works the way it does. All five findings were folded into `embed_cover.py` v2.

Two failure modes hit while downloading **Charlotte de Witte — _Doppler_**:

1. **Album mismatch → zero results.** MusicBrainz requires an exact release-title match. `"Formula - EP"` vs `"Formula EP"` (or the placeholder `"Singles"`) returned nothing and the script errored out instead of falling back.
   - **Fix:** retry without the `release:` filter when the filtered query returns 0 results.
2. **First-release-wins picks comps.** When search succeeded, the script grabbed the first release with art — often a compilation (e.g. *Serious Beats 97*) instead of the canonical EP.
   - **Fix:** score releases: fuzzy-match album → prefer Album/EP/Single over Compilation → earliest date → skip DJ-mixes entirely.

Three more found 2026-05-04:

3. **iTunes Search API as fallback for new releases.** MusicBrainz hasn't indexed brand-new EPs yet. Confirmed on *Lucky Iris — fall in love with the dj* (2026-01-23) and *North West — N0rth4evr* (2026-05-01). Free, no auth.
   - Endpoint: `https://itunes.apple.com/search?term=<artist>+<album>&entity=album`
   - The artwork URL ends in `100x100bb.jpg` — **swap to `3000x3000bb.jpg`** for max-res originals.
4. **Cover Art Archive occasionally 500s on the actual image file** even when its JSON metadata says art exists (archive.org CDN flakiness). Hit while fetching *Fred again.. — Actual Life 3* — first matching pressing returned HTTP 500, second pressing's art downloaded fine.
   - **Fix:** iterate through **all** matching releases until one returns valid bytes, not just the first one with a `front` image listed.
5. **`requests.get().content` can silently truncate large CAA downloads.** Same Fred again.. session: a 5.5 MB cover was saved as a 2.3 MB truncated JPEG with no error raised. `raise_for_status()` didn't fire (HTTP 200), and Pillow's `Image.verify()` passed (it only checks the header), but `Image.load()` failed with `image file is truncated`.
   - **Fix:** after download, compare bytes against the response's `Content-Length` header and run Pillow's `Image.load()` (not just `verify()`). If broken, retry or fall back to the next release.
   - Side note: `curl -sL --fail -o file.jpg <url>` handled the same download fine — the truncation is a `requests` quirk.

## Related notes

- [[_index]] — Claude skills index
- [[claude-config-files]] — how Claude's config layering works
- [[../../Mixing-DJing/Mixing-DJing|Mixing & DJing area]] — main consumer of this skill
