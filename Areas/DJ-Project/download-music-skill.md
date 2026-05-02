---
title: Download Music Skill — Setup & Usage
date: 2026-05-02
tags: [dj, yt-dlp, music, skill]
---

# Download Music Skill

One command to download a YouTube song at max quality and embed the official album art.

## Usage

```
/download-music <YouTube URL>
```

Claude will automatically extract artist, album, and title from YouTube metadata, download the MP3, and embed the cover art. No extra input needed unless metadata is ambiguous.

## What it does (in order)

1. Extracts artist, album & title from YouTube metadata via yt-dlp
2. Downloads best available audio → converts to MP3 (VBR quality 0 = max)
3. Saves file to `~/Music/Mixxx/<Artist>/<Album>/` (falls back to `Singles/` if no album)
4. Searches MusicBrainz for the official album cover
5. Embeds the cover art into the MP3's ID3 tags
6. Saves a `cover.jpg` in the album folder (required for Mixxx to display art)

## Folder structure

```
~/Music/Mixxx/
└── Grimes/
    ├── Miss Anthropocene/
    │   ├── cover.jpg
    │   └── IDORU (Digital_Lust_Mix).mp3
    └── Singles/
        ├── cover.jpg
        └── some-single.mp3
```

Each album folder gets its own `cover.jpg` so Mixxx shows the right art per track.

## File system map

| What | Path |
|---|---|
| Downloaded music | `~/Music/Mixxx/<Artist>/<Album>/` |
| Cover art script | `~/Music/Mixxx/embed_cover.py` |
| Beets config | `~/.config/beets/config.yaml` |
| Skill definition | `~/.claude/commands/download-music.md` |

## Installed tools

| Tool | Installed via | Purpose |
|---|---|---|
| `yt-dlp` | Homebrew | Download audio from YouTube |
| `ffmpeg` | Homebrew | Convert audio to MP3 |
| `beets` | pip | Music library manager (available for batch tagging) |
| `mutagen` | pip (beets dep) | Read/write MP3 ID3 tags |
| `requests` | pip | Fetch cover art from MusicBrainz API |

## Manual cover art embedding

```bash
# With album (more accurate MusicBrainz match)
python3 ~/Music/Mixxx/embed_cover.py "Artist" "Song Title" "path/to/file.mp3" "Album Name"

# Without album
python3 ~/Music/Mixxx/embed_cover.py "Artist" "Song Title" "path/to/file.mp3"
```

## Manual download (without the skill)

```bash
yt-dlp -f "bestaudio/best" -x --audio-format mp3 --audio-quality 0 \
  -o "~/Music/Mixxx/%(artist|channel)s/%(album|Singles)s/%(title)s.%(ext)s" "YOUTUBE_URL"
```
