---
title: tunebat skill
date: 2026-09-14
tags: [claude, skill, dj, tunebat, engine-dj, meta]
---

# 🎧 `tunebat` skill

Looks up a track's Key, Camelot, BPM, and feel-tags (energy, danceability, happiness, popularity), routing results into the DJ vault at `Areas/Mixing-DJing/`. Prefers the user's own Engine DJ library over any web scrape.

## Where it lives

```
~/.claude/skills/tunebat/SKILL.md
~/.claude/skills/tunebat/engine_dj_lookup.py   ← queries the local Engine DJ database
~/.claude/skills/tunebat/tunebat_fetch.py      ← headless-Chrome scrape of tunebat.com
```

## How to invoke

**Auto-fires** on: "look up the BPM/key for X", "what's the camelot for X", "tunebat X", "add X to the tracklist", "get song info for X", or a pasted `tunebat.com` URL. Does **not** fire for general music questions (history, genre theory, recommendations).

## Lookup priority — Engine DJ is the ground truth

The user mixes on Engine DJ, so its values are the only ones that matter for the actual workflow. The skill always tries sources in this order, stopping at the first hit:

1. **Engine DJ database** (`engine_dj_lookup.py`, reads `~/Music/Engine Library/Database2/m.db`) — by absolute file path or fuzzy artist+title query. Result marked `source: "engine-dj"`.
2. **Tunebat** (`tunebat_fetch.py`) — only when Engine DJ has no match. Result marked `source: "tunebat"`, with an explicit note that it's a fallback and DJ-grade accuracy needs the track analyzed in Engine DJ.

It never mixes fields from two sources into one result, and never lets a cross-check against `keyfinder-cli`/`aubio`/`librosa` override an Engine DJ disagreement — Engine DJ is the only arbiter.

## Gotchas

- **Cloudflare**: tunebat.com is gated behind a managed JS challenge; `tunebat_fetch.py` handles it by driving real Chrome (`channel="chrome"`), not a bare headless browser.
- **Spotify API deprecation**: an earlier version of this skill used the Spotify Web API for audio features; that endpoint was deprecated, which is why the scrape goes through tunebat.com's own page instead.
- **Engine key-code table**: the integer→key mapping in `ENGINE_KEY_CODES` is only fully verified at one data point (`key=1` → A minor / 8A); if a future track's reported key disagrees with the Engine DJ UI, fix the mapping row rather than assuming the track is mistagged.

## Backup

`SKILL.md` + both scripts are mirrored at [[backup/README|Areas/Claude/Skills/backup/tunebat/]], last synced **2026-09-14**.

## Related notes

- [[download-music]] — the DJ-library skill this one commonly feeds into (`engine_dj_lookup.py` reuse)
- [[../../Mixing-DJing/Manuals/engine-dj-sc-live-4-workflow|Engine DJ → SC Live 4 Workflow]]
- [[_index]] — Claude skills index
