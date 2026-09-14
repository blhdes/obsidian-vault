---
name: tunebat
description: Look up a song's musical attributes (Key, Camelot, BPM, Popularity, Energy, Danceability, Happiness) from tunebat.com, and optionally save them into the user's DJ vault. Use this skill WHENEVER the user asks to "look up the BPM/key for X", "what's the camelot for X", "add X to the tracklist", "tunebat X", "get song info for X", or otherwise wants musical-analysis tags for a track. Also use when the user pastes a tunebat.com URL.
---

# Tunebat lookup

Fetches a song's key, camelot, BPM, and feel-tags (energy, danceability, happiness, popularity) from tunebat.com via a headless Chrome browser, and routes the result into the user's `Areas/Mixing-DJing/` vault.

## When to invoke

Trigger this skill when the user:
- Asks for **key**, **BPM**, **camelot**, **energy**, **danceability**, or **happiness** of a specific song
- Pastes a `tunebat.com/Info/...` URL
- Says "tunebat X", "look up X", "add X to my tracklist", "get info for X"
- Is editing a tracklist note in `Areas/Mixing-DJing/Tracklists/` and references a new track

Do NOT trigger for general music questions (history, genre theory, recommendations).

## Lookup priority (READ THIS FIRST)

**Engine DJ is the ground truth.** The user mixes on Engine DJ — its `key`/`bpm` values are the only ones that matter for their actual workflow. Tunebat and other automated sources frequently disagree with Engine DJ; when they do, Engine DJ always wins.

Always try sources in this order, stopping at the first hit:

1. **Engine DJ database** (`engine_dj_lookup.py`) — reads `~/Music/Engine Library/Database2/m.db`. If the track is in there and analyzed, return that. Mark the result clearly: `source: "engine-dj"`.
2. **Tunebat** (`tunebat_fetch.py`) — only when Engine DJ has no match. Mark `source: "tunebat"` and tell the user: *"Not analyzed in Engine DJ — falling back to Tunebat. For DJ-grade accuracy, drag this into Engine DJ and re-run."*

NEVER:
- Mix values from different sources into one result (e.g. Tunebat key + Engine DJ BPM). Pick one source per track.
- Silently substitute Tunebat data when Engine DJ disagrees.
- Cross-check Tunebat against `keyfinder-cli`, `aubio`, `librosa`, etc. and pretend the cross-check makes it authoritative. It doesn't — Engine DJ is the only arbiter.

See [[feedback-dj-key-source]] for the user's standing instruction on this.

## How it works

### Engine DJ lookup — `engine_dj_lookup.py`

Queries the local Engine DJ SQLite database. Two modes:

```bash
# By absolute file path (preferred when you have the MP3 from /download-music):
python3 /Users/agomezu/.claude/skills/tunebat/engine_dj_lookup.py --path "/Users/agomezu/Music/Library/.../Song.mp3"

# By artist + title query (fuzzy match across all tracks in the Engine DJ library):
python3 /Users/agomezu/.claude/skills/tunebat/engine_dj_lookup.py --query "message of love st david"
```

On hit, prints JSON with `source: "engine-dj"`, `key`, `camelot`, `engine_key_code`, `bpm`. On miss, prints `{"error": ...}` to stderr and exits non-zero — fall back to `tunebat_fetch.py`.

The integer-to-key mapping in `ENGINE_KEY_CODES` (inside the script) was derived from a single confirmed data point (key=1 → A minor / 8A on 2026-05-23) plus Open Key notation conventions. The full table is consistent with the publicly documented Engine SDK ordering but only the `key=1` row has been user-verified. **If a future track reports a key that disagrees with what the Engine DJ UI shows, fix the offending row in `ENGINE_KEY_CODES` rather than guessing the song is wrong.**

### Tunebat scrape — `tunebat_fetch.py`

The script drives headless Chromium against tunebat.com. Tunebat is gated behind Cloudflare's managed challenge — the script handles the JS challenge transparently via real Chrome (`channel="chrome"`).

### Calling the script

Always run from the skill's directory or with an absolute path:

```bash
python3 /Users/agomezu/.claude/skills/tunebat/tunebat_fetch.py "<query>"
```

`<query>` can be either:
- A free-text search: `"blinding lights weeknd"` — uses tunebat's search, returns the top match
- A direct URL: `"https://tunebat.com/Info/Blinding-Lights-The-Weeknd/0VjIjW4..."` — fetches that exact page

The script prints a JSON object to stdout:

```json
{
  "artist": "The Weeknd",
  "title": "Blinding Lights",
  "key": "C♯ major",
  "bpm": 171,
  "camelot": "3B",
  "popularity": 90,
  "energy": 73,
  "danceability": 51,
  "happiness": 33,
  "url": "https://tunebat.com/Info/Blinding-Lights-The-Weeknd/0VjIjW4GlUZAMYd2vXMi3b"
}
```

On error, prints `{"error": "..."}` to **stderr** and exits non-zero.

### Expected latency

Each fetch takes **3–15 seconds** depending on Cloudflare's mood (longer on first run of a session because of the challenge, faster subsequently). Tell the user "fetching from tunebat…" before invoking so they understand the wait.

## Critical: verify the match before saving

The search returns the **top result** for any query — even nonsense queries return something. Before writing to the vault:

1. **Show the parsed JSON to the user** with the artist + title highlighted.
2. **Ask the user to confirm** if the returned artist/title doesn't obviously match what they asked for. For example, if they said "strobe" and you got "Strobe by deadmau5" — that's likely right. But if they said "drift" and you got something weird like "Drift Away by some unknown artist", confirm before saving.
3. If wrong, ask the user for a more specific query (e.g. add the artist name) and re-run.

## Where to save the result

The user picked all three save options in their initial spec, so choose based on context:

### A. Append to an existing tracklist note (default when context fits)

If the user is currently editing or referencing a file in `/Users/agomezu/Claude/Obsidian/Areas/Mixing-DJing/Tracklists/`, append a new row to the file's Tracks table. The expected schema (from the tracklist template) is:

```markdown
| # | Artist — Title | BPM | Key | Notes |
```

Extend it with a Camelot column when adding via this skill (tracklists in the vault tolerate column additions). Final row format:

```markdown
| <n> | <artist> — <title> | <bpm> | <key> | <camelot> | [tunebat](<url>) |
```

If the user wants the feel-tags inline, add them to the Notes column: `E:73 D:51 H:33`.

### B. Create a per-track note in `Areas/Mixing-DJing/Tracks/`

When the user says "save this track" or "make a note for this", create one note per song under `/Users/agomezu/Claude/Obsidian/Areas/Mixing-DJing/Tracks/` with this layout:

```markdown
---
title: <Artist> — <Title>
date: <YYYY-MM-DD>
tags: [track, dj, <camelot>, bpm-<bpm>]
---

# <Artist> — <Title>

| Attribute | Value |
|---|---|
| Key | <key> |
| Camelot | <camelot> |
| BPM | <bpm> |
| Energy | <energy>/100 |
| Danceability | <danceability>/100 |
| Happiness | <happiness>/100 |
| Popularity | <popularity>/100 |

[View on Tunebat](<url>)
```

Filename: kebab-case `artist-title.md` (e.g. `the-weeknd-blinding-lights.md`). Strip diacritics/punctuation safely.

The `Tracks/` folder may not exist yet — if not, create it on first use, and add a stub `Tracks.md` index there too (following the pattern of `Tracklists/Tracklists.md`).

### C. Just print the result

If the user is exploring (no clear save target) or asks for "just the info", print the JSON in a readable Markdown block and don't write any file:

```markdown
**The Weeknd — Blinding Lights**
- Key: C♯ major · Camelot: 3B · BPM: 171
- Energy 73 · Danceability 51 · Happiness 33 · Popularity 90
- [Tunebat](https://tunebat.com/Info/...)
```

## Workflow examples

**Example 1 — adding to a tracklist, track in user's library**
> User: *"add 'midnight city m83' to the warmup tracklist"*

1. Locate the MP3 in `~/Music/Library/` (use `find` if the path isn't obvious).
2. Run `engine_dj_lookup.py --path "/Users/agomezu/Music/Library/.../Midnight City.mp3"`.
3. **On hit:** show the Engine DJ result, append row to the tracklist, label `✅ Engine DJ` in a Verified column.
4. **On miss:** tell the user *"Not in Engine DJ yet — would you like to analyze it there for accurate key, or accept Tunebat as a rough estimate?"* If they say Tunebat, fall through to `tunebat_fetch.py` and label `❓ tunebat (unverified)`.

**Example 2 — quick lookup, no save, song not in library**
> User: *"what's the BPM and key for blinding lights"*

The user is exploring, not preparing to mix it. Skip Engine DJ (the track isn't there); run `tunebat_fetch.py` and print the readable Markdown block. Note in the response: *"Tunebat value — if you end up mixing this, verify in Engine DJ."*

**Example 3 — building the per-track library**
> User: *"make a track note for strobe by deadmau5"*

1. Try `engine_dj_lookup.py --query "strobe deadmau5"`.
2. If hit, write the per-track note using Engine DJ values; mark `Source: Engine DJ` in the note.
3. If miss, fall back to `tunebat_fetch.py` and write the note with `Source: Tunebat (unverified — analyze in Engine DJ)`.
4. Confirm: *"Saved to `Areas/Mixing-DJing/Tracks/deadmau5-strobe.md` (Engine DJ verified)"*.

**Example 4 — pasted tunebat URL**
> User: *"https://tunebat.com/Info/Strobe-deadmau5/5GjUhwxykUVYCYkiNo4BEM"*

User explicitly pointed at Tunebat — skip Engine DJ, pass the URL verbatim to `tunebat_fetch.py`. Still mention they should verify in Engine DJ before using it in a mix.

## Verified column convention

When a tracklist row gets populated from this skill, add a `Verified` column with one of:
- `✅ Engine DJ` — track was found in `~/Music/Engine Library/Database2/m.db` with `isAnalyzed=1`.
- `❓ tunebat (unverified)` — Tunebat result accepted because Engine DJ had no match. User has been informed.
- `❌ analyze in Engine DJ` — sources disagreed badly or only a low-confidence guess exists.

## Dos and don'ts

**Do**
- Always show the parsed result to the user before writing files.
- Preserve the `url` field somewhere in the vault entry — it's the user's audit link back to the source.
- Use the existing `Tracklists/Tracklists.md` template as the schema reference.
- If `Areas/Mixing-DJing/Tracks/` doesn't exist and the user wants per-track notes, create it + a `Tracks.md` index together.

**Don't**
- Don't write to the vault without showing the user what was fetched.
- Don't overwrite an existing track note silently — if `<artist>-<title>.md` already exists, read it first and ask whether to update or skip.
- Don't run more than one `tunebat_fetch.py` invocation in parallel — they compete for the Chrome instance and timeout. Run sequentially.
- Don't invent values when a field is `null` (occasional fields can be missing for very obscure tracks). Just omit them from the vault entry.

## Known limitations

- **Engine DJ key mapping is partially unverified.** Only `key=1` → A minor / 8A has been user-confirmed. The other 23 values in `ENGINE_KEY_CODES` follow Open Key conventions but should be cross-checked the first time each value comes up. If a returned key contradicts the Engine DJ UI, fix the dict — don't blame the song.
- **Engine DJ DB has stale paths after moves/renames.** Engine DJ stores `path` relative to its DB folder. If you reorganize `~/Music/Library/`, the `--path` lookup may miss until Engine DJ re-scans. The `--query` fuzzy fallback usually still hits.
- **Tunebat search returns the top result for any query**, even nonsense ones. Always confirm artist/title before saving.
- **First Tunebat fetch in a session is slow** (~10–15s) due to Cloudflare challenge clearance. Subsequent fetches in the same hour are faster.
- **Cloudflare may tighten further.** If `tunebat_fetch.py` starts consistently timing out: bump `WAIT_TIMEOUT_MS`, or switch from real Chrome to `channel="chrome-beta"` / Brave.

## Dependencies

Already installed for the user:
- Python 3.11+
- `playwright` (Python package)
- `beautifulsoup4`
- Google Chrome.app (at `/Applications/Google Chrome.app`)

If `playwright` is missing on a fresh setup: `python3 -m pip install --user playwright beautifulsoup4 && python3 -m playwright install chromium`
