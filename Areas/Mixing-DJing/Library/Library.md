---
title: Library
date: 2026-06-07
tags: [library, dj, imports, index]
---

# Library

A running record of what's actually in `~/Music/Library/` — the files that feed Engine DJ. One **monthly note** per month lists every release imported that month with the **exact tags written on disk** (artist / title / album / year / genre / format), so I can audit the library without opening every file.

These notes only cover releases pulled from **Soulseek** and logged in `~/Soulseek Downloads/_downloaded-sources.md`. Anything not in that log (YouTube grabs, etc.) is left out on purpose.

## Why this exists

- **Genre is mine to own.** Engine DJ analyses BPM and key on import but only ever *reads* the `genre` tag — so the genre styles written by `/download-music tags genre` are what my crates depend on. These notes are where I eyeball that those genres are actually present and sane.
- **A flat snapshot** of provenance: which Soulseek uploader each release came from, when it was moved, and at what quality.

## Monthly notes

- [[june-2026|June 2026 — Library Imports]] — first month: 42 releases · 127 tracks · 34 uploaders

## How to add a month

1. Copy the previous month's note to `<month>-YYYY.md`.
2. For each release moved into the Library that month (per the Soulseek log), read its on-disk tags:
   ```bash
   python3 ~/.claude/skills/download-music/fix_metadata.py "<folder>" --genre-only
   ```
   (preview mode — writes nothing; shows current vs. proposed genre per track)
3. Fill the summary table and a per-release section.

## Related

- [[../Mixing-DJing|Mixing & DJing index]]
- [[../track-organisation-and-tagging|Track organisation & tagging]]
- [[../Tracklists/Tracklists|Tracklists]] — what I plan to *play*; this folder is what I *have*
- `/download-music` skill — the import + tagging pipeline (`~/.claude/commands/download-music.md`)
