---
title: download-music skill
date: 2026-06-03
tags: [claude, skill, music, dj, yt-dlp, discogs]
---

# 🎵 `download-music` skill

A toolkit for building and cleaning up my local DJ library under `~/Music/Library/`. It does **three jobs**, each using the database it's best at:

- **Download** — pull audio from YouTube at max quality and embed the album art.
- **Covers** — make sure files already on disk show artwork (Discogs first, MusicBrainz / iTunes as fallbacks). Works on *any* audio, not just things this skill downloaded.
- **Tags** — fix artist / title / album / year from MusicBrainz **and** refine the genre from Discogs styles, optionally renaming files to match.
- **Library notes** — snapshot what's actually *in* the Library each month (Soulseek imports + their on-disk tags) into the Obsidian vault.
- **Port** — the last phase: flush the whole Library onto an external SSD and delete the local copies, to free up the internal disk.

Implemented as a **slash command** (not a `SKILL.md`): typing `/download-music …` loads `~/.claude/commands/download-music.md` and Claude follows it.

## Commands

| Command | What it does |
|---|---|
| `/download-music <URL>` | Download + embed cover in one step |
| `/download-music queue <URL>` | Resolve metadata into the queue, don't download yet |
| `/download-music run` | Download everything pending in the queue |
| `/download-music covers <folder>` | Backfill art into every file in a folder that's missing it |
| `/download-music covers options <file-or-folder>` | List the different Discogs cover versions (with viewable URLs) |
| `/download-music covers set <file-or-folder> <n>` | Embed the version `n` you picked |
| `/download-music tags <file-or-folder>` | Fix artist/title/album/year from MusicBrainz **and** refine genre from Discogs (previews first, writes nothing) |
| `/download-music tags genre <file-or-folder>` | Refine **only** the genre from Discogs styles — for an already-clean library |
| `/download-music tags rename <file-or-folder>` | Same as `tags`, plus rename files to the clean title |
| `/download-music library [month-year]` | Snapshot this month's Soulseek imports + their on-disk tags into the vault (`Areas/Mixing-DJing/Library/`) |
| `/download-music port <SSD>` | **Preview** moving the whole Library onto an external SSD (dry-run, changes nothing) |
| `/download-music port <SSD> --apply` | **Flush** the Library onto the SSD and delete the local copies (frees disk) |

Accepts a single track, a playlist URL, or "grab the rest of the EP too" from one track.

## Options (flags)

Mostly relevant when running the scripts directly. The big one: **`tags` previews by default and only writes with `--apply`** — there is no `--write`.

| Flag | Where | What it does |
|---|---|---|
| `--apply` | `tags` | **The write switch.** Without it, `tags` only previews — nothing is saved |
| `--rename` | `tags` | Also rename each file to its clean title |
| `--artist` `--album` `--title` `--year` | `tags` | Force a field when the auto-match is wrong |
| `--overwrite` | `covers <folder>` | Re-fetch and replace art even on files that already have it |
| `--artist` `--album` `--title` | `covers options` / `set` | Override the Discogs search terms when tags are messy |
| `--limit N` | `covers options` | How many cover versions to list (default 8) |
| `--youtube-url` | download | Last-resort YouTube-thumbnail source (the download flow passes it automatically) |

## Where files land

```
~/Music/Library/
└── <Artist>/
    ├── <Album>/
    │   ├── cover.jpg          ← one per album folder
    │   └── track.mp3
    └── Singles/
        └── <Single Title>/
            ├── cover.jpg      ← belongs to this single only
            └── <Single Title>.mp3
```

**Only ever writes under `~/Music/Library/`** — never into the sibling app folders in `~/Music/` (Mixxx, Apple Music's `Music Library.musiclibrary`, Engine Library).

## How covers are found

The script walks a fallback chain, stopping at the first valid image:

1. **Existing cover image** already in the folder → lets a multi-track album reuse track 1's art (no extra network calls).
2. **Discogs** — best art, but needs a token (see setup). Picks the highest-res image among the best-matching pressings.
3. **MusicBrainz + Cover Art Archive** — validates each download (rejects truncated / undecodable files).
4. **iTunes** — catches brand-new releases the others haven't indexed.
5. **YouTube thumbnail** — last resort (download flow only); auto-crops the square art out of the letterboxed 1280×720.

Every embed also drops a `cover.jpg` next to the file, since some players (Mixxx) need it to display art. The script prints a `Source:` line so I know where the art came from.

## One-time setup: Discogs token

The cover commands need a free Discogs personal access token; everything else works out of the box. Without it, the Discogs step is silently skipped and the chain falls back to MusicBrainz / iTunes.

1. Generate one at <https://www.discogs.com/settings/developers>.
2. Save it where the script looks (env var wins over file):
   ```bash
   printf '%s' '<token>' > ~/.claude/skills/download-music/.discogs_token
   chmod 600 ~/.claude/skills/download-music/.discogs_token
   # or: export DISCOGS_TOKEN='<token>'
   ```

## Dependencies

| Tool | Install |
|---|---|
| `yt-dlp`, `ffmpeg` | `brew install yt-dlp ffmpeg` |
| `mutagen`, `requests`, `Pillow` | `pip install mutagen requests Pillow` |

## Where everything lives

```
~/.claude/commands/download-music.md        ← full manual (source of truth)
~/.claude/skills/download-music/
├── embed_cover.py    ← cover for one downloaded file
├── cover_folder.py   ← backfill covers across a folder
├── cover_picker.py   ← list / set a specific Discogs version
├── fix_metadata.py   ← MusicBrainz tags + Discogs genre fixer (+ rename)
├── port_library.py   ← move the Library → external SSD, then delete locals
├── queue.md          ← the download queue
└── .discogs_token    ← optional Discogs token
```

For the step-by-step bash and edge-case rules, read the command file above — this note is just the map.

## Monthly library note

`/download-music library` keeps a human-readable record of what's actually **in** the Library, in the vault at `Areas/Mixing-DJing/Library/`. One note per month (`june-2026.md`, …) lists every release moved in from Soulseek that month with its **exact on-disk tags** — artist / title / album / year / genre / format — so I can audit genres (the tag Engine DJ reads but never fixes) without opening files.

- **Source of truth for *what* to include:** the Soulseek log (`~/Soulseek Downloads/_downloaded-sources.md`). Anything not logged there is skipped.
- **Source of truth for the *tags*:** the files on disk.
- Each release gets a provenance line (uploader · quality · move date) + a per-track table, plus a "tag-check notes" section flagging missing/weak genres.

See [[../../Mixing-DJing/Library/Library|the Library index]].

## Porting the Library to an external SSD

The **last phase** of the pipeline, for when the internal disk fills up. `port_library.py` moves everything in `~/Music/Library/` onto an external SSD and deletes the local copies. Run it **only when I say so** — it's a deliberate flush, not automatic. It's **repeatable**: the Library *folder* is kept (only its contents move), so new Soulseek imports keep landing there and the next flush just merges them in.

```bash
python3 ~/.claude/skills/download-music/port_library.py /Volumes/<SSD>          # dry-run preview (default)
python3 ~/.claude/skills/download-music/port_library.py /Volumes/<SSD> --apply  # move + delete locals
```

Default destination is `<SSD>/Music/Library/` (mirrors the local layout). It moves **everything** — audio, `cover.jpg`, and vinyl-rip lineage `.txt`/`.nfo` files + scans travel with their release.

**Why it's safe** (it deletes local files, so this is the whole point):

- **Dry-run by default** — nothing moves until `--apply`.
- **Refuses anything but a real external drive** — destination must be mounted *and* on a different physical disk than the source. Blocks the macOS trap where an unplugged SSD's `/Volumes/<name>` is silently a folder on the internal disk (a naive move would then delete the originals off the boot drive).
- **Copy → checksum-verify → delete, per file** — a local file is deleted only after its SSD copy is proven byte-identical (SHA-256). A mismatch leaves both files in place.
- **Resumable / idempotent** — a file already on the SSD (same size + checksum) is skipped and only its local copy removed.

> ⚠ **Engine DJ caveat:** Engine stores track paths relative to the internal disk (`../Library/…`), so after the move it shows those tracks as missing until I point Engine at the SSD (add it as a drive, or relink). The script does **not** touch Engine's database — re-linking is a separate manual step, and it prints this reminder when it finishes. See [[../../Mixing-DJing/Manuals/engine-dj-sc-live-4-workflow|Engine DJ → SC Live 4 Workflow]].

## Related notes

- [[_index]] — Claude skills index
- [[../claude-config-files|claude-config-files]] — how Claude's config layering works
- [[../../Mixing-DJing/Mixing-DJing|Mixing & DJing area]] — main consumer of this skill
- [[../../Mixing-DJing/Library/Library|Library notes]] — the monthly snapshots this skill writes
</content>
</invoke>
