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

## Related notes

- [[_index]] — Claude skills index
- [[claude-config-files]] — how Claude's config layering works
