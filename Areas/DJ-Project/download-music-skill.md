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

## Known issues & improvement ideas (2026-05-03)

> **Status (2026-05-04):** all five findings below have been folded into `embed_cover.py` v2 and the skill markdown. Kept here as a record of the failure modes and the rationale.

Two failure modes hit while downloading Charlotte de Witte – *Doppler*:

1. **Album mismatch → zero results.** The MusicBrainz query requires an exact release-title match. `"Formula - EP"` vs `"Formula EP"` (or the placeholder `"Singles"`) returns nothing and the script errors out instead of falling back.
2. **First-release-wins picks comps.** When the search succeeds, the script grabs the first release with cover art — often a compilation (e.g. *Serious Beats 97*) instead of the canonical EP.

Possible fixes for `embed_cover.py`:
- Retry without the `release:` filter when the filtered query returns 0 results.
- Score releases: fuzzy-match album → prefer Album/EP/Single over Compilation → earliest date.
- Try Cover Art Archive by **release-group MBID** instead of release MBID for canonical art.
- Add a `--release-mbid` flag to bypass search when the right release is already known.

### More findings (2026-05-04)

3. **iTunes Search API works great as a fallback for new releases** that MusicBrainz hasn't indexed yet. Confirmed twice: *Lucky Iris – fall in love with the dj* (EP, 2026-01-23) and *North West – N0rth4evr* (EP, 2026-05-01). Free, no auth, no rate-limit hassles for low-volume use.
   - Endpoint: `https://itunes.apple.com/search?term=<artist>+<album>&entity=album`
   - The artwork URL ends in `100x100bb.jpg` — **swap to `3000x3000bb.jpg`** to get the original high-res cover.

4. **Cover Art Archive occasionally 500s on the actual image file** even when its JSON metadata says art exists (archive.org CDN flakiness). Hit while fetching Fred again.. – *Actual Life 3* — first matching pressing returned HTTP 500, second pressing's art downloaded fine.
   - Fix: iterate through **all** matching releases until one actually returns image bytes, not just the first one with a `front` image listed.

5. **`requests.get().content` can silently truncate large CAA downloads.** Same Fred again.. session: the alt pressing's 5.5 MB cover was saved as a 2.3 MB truncated JPEG with no error raised. `raise_for_status()` didn't fire (HTTP 200), and Pillow's `Image.verify()` passed (it only checks the header), but `Image.load()` failed with `image file is truncated`.
   - Fix: after download, compare bytes against the response's `Content-Length` header **and/or** check the JPEG ends with the EOI marker `FF D9` before embedding. If broken, retry or fall back to the next release.
   - Curl handles this fine — `curl -sL --fail -o file.jpg <url>` got the full 5.5 MB cleanly. Easiest workaround if the script stays in Python is to stream with `requests`'s `stream=True` + verify byte count.

### Suggested fallback chain

When implementing the rewrite, try sources in this order:
1. MusicBrainz + Cover Art Archive — try every matching release (not just the first), skip 500s.
2. iTunes Search API — high-res via `3000x3000bb` URL trick.
3. YouTube video thumbnail (yt-dlp `--write-thumbnail`) — last resort, often a frame grab but better than nothing.
