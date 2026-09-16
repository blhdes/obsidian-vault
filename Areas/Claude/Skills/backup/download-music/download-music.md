# download-music

A toolkit for building and cleaning up a local music library under `~/Music/Library/`. It does three jobs, each using the database it's best at:

- **Download** — pull audio from **YouTube** at max quality and embed the album art.
- **Covers** — make sure files already on disk display artwork, sourced from **Discogs** (with MusicBrainz / iTunes as fallbacks); fix one by hand when the auto-pick is wrong.
- **Tags** — correct artist / title / album / year from **MusicBrainz**, refine the **genre** from **Discogs** (its granular styles, for DJ crates), and optionally rename files to match.

The cover and tag jobs work on any audio you already have — ripped, imported, or downloaded elsewhere — not just things this skill fetched.

## Commands

### Downloading

- `/download-music <YouTube URL>` — **instant**: resolve, download, and embed the cover in one step. See "Downloading a song".
- `/download-music queue <YouTube URL>` — **collect**: resolve a song's metadata into the queue without downloading. See "Batch queue workflow".
- `/download-music run` — **batch**: download everything pending in the queue. See "Batch queue workflow".

### Covers (artwork)

- `/download-music covers <folder>` — **backfill**: scan a folder (and subfolders) and embed art into every file that's missing it. See "Backfilling covers for a folder".
- `/download-music covers options <file-or-folder>` — **choose**: list the different Discogs cover versions, each with a viewable URL, so you can pick one by hand. See "Choosing a specific cover".
- `/download-music covers set <file-or-folder> <number>` — **apply**: embed the version you picked from `covers options`. See "Choosing a specific cover".

### Tags (metadata)

- `/download-music tags <file-or-folder>` — **fix tags**: correct artist / title / album / year from MusicBrainz *and* refine the genre from Discogs (previews first; writes nothing until confirmed). See "Fixing track metadata".
- `/download-music tags genre <file-or-folder>` — **genre only**: refine just the genre from Discogs, leaving the descriptive fields untouched (for an already-clean library that only needs crate-ready genres). Maps to `--genre-only`. See "Fixing track metadata".
- `/download-music tags rename <file-or-folder>` — **fix tags + rename**: same as `tags`, and also rename each file to its clean title. See "Fixing track metadata".

### Library notes (Obsidian)

- `/download-music library` — **snapshot**: write or refresh **this month's** library-additions note in the Obsidian vault, listing every Soulseek-imported release with its exact on-disk tags (artist / title / album / year / genre / format). `/download-music library <month-year>` (e.g. `june-2026`) targets a specific month. See "Monthly library note".
- `/download-music library check` — **sync check**: compare the Library on disk *and* the month's note against the **Engine DJ** collection — lists any tracks not yet imported, broken file references, and confirms the note's totals line up. `/download-music library check <month-year>` targets a specific month. See "Engine DJ sync check".

### Porting to an external SSD (free up local disk)

- `/download-music port <SSD>` — **preview**: dry-run showing exactly what would move from `~/Music/Library/` onto the SSD, how much space it frees, and any conflicts. Changes nothing. See "Porting the Library to an external SSD".
- `/download-music port <SSD> --apply` — **flush**: actually move the whole Library onto the SSD and delete the local copies. The Library folder itself is kept for future imports. See "Porting the Library to an external SSD".

### Mastering a session recording (for upload)

- `/download-music master <file>` — **master**: loudness-normalize a full DJ-session recording and cap its true peak so it's ready to upload (SoundCloud, etc.). Two-pass EBU R128 via `master_audio.py`; writes `<name>_master.wav` (24-bit) and prints before/after LUFS/TP/LRA. Default target **-14 LUFS** (transparent); `--lufs -10` for club-loud (compresses a quiet source). Feed the lossless file; copy off slow/removable drives first. See the script header for details.

### Packaging a mix for YouTube

- `/download-music youtube <mix-audio> <cover-image-or-URL>` — **package**: render an MP4 (still cover image + mix audio) ready to upload directly to YouTube, then draft the title and description (tracklist) in house style. See "Packaging a mix for YouTube".

> Setup once: the cover commands need a free Discogs token — see "Discogs setup". Everything else works out of the box.

## Downloading a song (step by step)

This is the `/download-music <YouTube URL>` flow. The `queue` / `run` and multi-track sections below reuse these same numbered steps.

### 1. Resolve artist, title, and album

Run yt-dlp in metadata-only mode:

```bash
yt-dlp --print "%(artist|channel)s|||%(album)s|||%(title)s" "<URL>"
```

Split on `|||` to get `artist`, `album`, `title`.

**Cleanup rules — apply before downloading:**

- If `artist` is `channel` (no real artist tag), parse it out of `title` instead. Common separators in YouTube titles:
  - ` - ` → `Artist - Title` (e.g. `Grimes - IDORU`)
  - ` | ` → `ARTIST | TITLE` (e.g. `BICEP | ATLAS`)
- If `album` is `NA` or empty, treat the track as a **single** — it goes into `Singles/<Cleaned Title>/` so each single keeps its own `cover.jpg`. Albums still group their tracks under `<Album>/`.
- Strip noise from the title — these are not part of the song name:
  - `(Official Audio)`, `(Official Music Video)`, `(Official Video)`, `(Visualizer)`, `[Visualiser]`, `(Lyric Video)`
  - Producer credits like `(prod. <name>)`
- Keep intentional artistic stylings (leetspeak, lowercase, punctuation like `Fred again..`).
- If still ambiguous, ask the user before continuing.

### 2. Download the audio

Pick the output folder based on whether this is an album track or a single:

- **Album track:** `~/Music/Library/<Artist>/<Album>/<Cleaned Title>.mp3`
- **Single:** `~/Music/Library/<Artist>/Singles/<Cleaned Title>/<Cleaned Title>.mp3`

```bash
yt-dlp -f "bestaudio/best" \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  -o "<output path>.%(ext)s" \
  "<URL>"
```

Build the output path explicitly from the cleaned values rather than relying on `%(artist|channel)s` etc. — the YouTube template often produces messy folder names. Note the exact mp3 path for step 3.

### 3. Embed the album cover art

Always pass `--youtube-url` so the YouTube thumbnail fallback is available for obscure releases:

```bash
python3 ~/.claude/skills/download-music/embed_cover.py "<Artist>" "<Song Title>" "<path/to/file.mp3>" "<Album>" --youtube-url "<URL>"
```

The script tries sources in order until one returns a valid image:

0. **Existing cover image in the destination folder**
   - Matches common cover filenames (`cover` / `folder` / `front` / `album`.*) or the sole image in the folder, case-insensitively.
   - Lets multi-track album downloads reuse the cover fetched for track 1 — no network call needed for tracks 2+.
   - Singles each live in their own subfolder, so this rule is safe: there's nothing else in the folder to clash with.
1. **Discogs** (only when a token is configured — see "Discogs setup")
   - Searches releases by artist + album + track, retries without the album filter if needed, and skips Discogs' grey "spacer" placeholder image.
   - Resolves each release's **highest-resolution** image (the original, not the small search thumbnail) and, among the best-matching releases, picks the largest. Discogs' API caps served images at ~600px on the long edge — the giant website scans aren't exposed through the API.
   - To eyeball the different pressings and pick one yourself, use `covers options` (see "Choosing a specific cover").
   - Skipped silently when no token is set, so the chain still works without one.
2. **MusicBrainz + Cover Art Archive**
   - Retries without the `release:` filter if the album-filtered query returns 0 results (handles album-name typos like `"Formula EP"` vs `"Formula - EP"`).
   - Ranks candidate releases: skips DJ-mixes entirely, prefers non-compilations, prefers releases whose title fuzzy-matches the album hint, then earliest release date.
   - Iterates through every ranked release — works around archive.org's CDN occasionally returning HTTP 500 on individual cover files.
   - Validates each download: rejects truncated responses (Content-Length mismatch) and undecodable images (Pillow `load()` failure). Prevents broken JPEGs from being embedded.
3. **iTunes Search API**
   - Fallback for new releases that MusicBrainz hasn't indexed yet.
   - Uses the `100x100bb` → `3000x3000bb` URL trick to get max-res originals.
4. **YouTube thumbnail** (only when `--youtube-url` is passed)
   - Last-resort fallback for niche/old releases neither database indexes.
   - YouTube Music thumbnails are 1280x720 with the actual square art centered on grey letterbox bars — the script auto-crops to the center square.
   - Often correct for label-uploaded music videos and YT Music auto-generated channels.

PNG covers (e.g. some Cover Art Archive releases) are auto-converted to JPEG. A `cover.jpg` is also written next to the MP3 (some players like Mixxx need that to display art).

### 4. Confirm success

Report back with:
- Final file path (e.g. `~/Music/Library/Grimes/Miss Anthropocene/IDORU.mp3`)
- Where the cover came from — the script prints a `Source:` line (e.g. `MusicBrainz / 'Atlas' (8942fa1f...)`, `iTunes / <url>`, `YouTube thumbnail (auto-cropped) / <url>`, or `existing cover.jpg in folder`)

If even the YouTube thumbnail fails (rare), tell the user — they may want to re-run with corrected metadata or supply art manually.

## Batch queue workflow

Use this when you want to collect songs over time and download them all at once later. The queue lives at `~/.claude/skills/download-music/queue.md` — a plain markdown file the user can open and hand-edit.

### Queue file format

Two sections. **Pending** holds songs waiting to be downloaded; **Downloaded (history)** is an append-only log of what's already been fetched.

```markdown
# Download queue

## Pending
- <Artist> · <Album or (single)> · <Title> · <URL>

## Downloaded (history)
- [YYYY-MM-DD] <Artist> · <Album or (single)> · <Title> · <URL>
```

Fields are separated by ` · ` (space-middot-space). For a single (no album), put `(single)` in the album slot — that's the signal to use the single folder layout at download time.

### `/download-music queue <URL>` — add to the queue

1. Run **section 1** above to resolve and clean artist / album / title. Do **not** download.
2. If this URL is already present in Pending or in history, tell the user it's a duplicate and stop.
3. Append one line under `## Pending`:
   `- <Artist> · <Album or (single)> · <Title> · <URL>`
4. Confirm briefly: the cleaned name you stored, and how many songs are now pending. If the user passes a playlist or full-album URL, resolve and append every track (see "Multi-track albums and playlists" for how to list them).

### `/download-music run` — download the batch

1. Read every line under `## Pending`. If there are none, say the queue is empty and stop.
2. For each entry, run **section 2** (download) and **section 3** (embed cover), reusing the stored Artist / Album / Title — `(single)` in the album slot means use the single folder layout. Download tracks in parallel (one tool-call batch); embed covers sequentially so same-album tracks reuse one `cover.jpg`.
3. As each song finishes successfully, move its line from `## Pending` to `## Downloaded (history)`, prefixing today's date: `- [YYYY-MM-DD] ...`. Leave any song that **failed** in `## Pending` so it can be retried next run.
4. Report a short summary: how many downloaded and where, plus any that failed and why.

## Multi-track albums and playlists

When the user provides a playlist URL, or asks to download a full album/EP from a single track URL:

1. **List the tracks** — if you have a playlist URL:
   ```bash
   yt-dlp --flat-playlist --print "%(id)s|||%(title)s" "<playlist URL>"
   ```
   If you only have one track URL but need to find others from the same EP/album, get the uploader's channel and list its uploads:
   ```bash
   yt-dlp --print "%(channel_url)s" --playlist-items 1 "<track URL>"
   yt-dlp --flat-playlist --print "%(id)s|||%(title)s" "<channel URL>"
   ```
   Then verify candidates share the same `%(album)s` field.
2. **Download all tracks in parallel** — multiple yt-dlp invocations in one tool-call batch.
3. **Embed covers sequentially** — run `embed_cover.py` once per track. The first call hits the network; the rest pick up the saved `cover.jpg` from the album folder automatically (source 0 above). This means at most one network lookup per album.

## Backfilling covers for a folder

Use this when you already have audio files on disk (ripped, imported, or downloaded elsewhere) and just want to make sure they all *display* a cover. It downloads nothing from YouTube — it only finds and embeds art into the files that are missing it.

```bash
python3 ~/.claude/skills/download-music/cover_folder.py "<folder>"
```

What it does, per audio file found under `<folder>` (recursively):

1. **Skips files that already have embedded art** — only the missing ones are touched. (Pass `--overwrite` to re-fetch and replace art on *every* file, e.g. to upgrade low-res or wrong covers.)
2. Reads `artist` / `album` / `title` from the file's own tags. If those are missing, it infers them from the folder layout (`<Artist>/<Album>/<Title>` and the `<Artist>/Singles/<Title>/` layout are both handled).
3. Finds a cover using the same source chain as section 3 — **folder image → Discogs → MusicBrainz → iTunes** (no YouTube step, since there's no URL).
4. Embeds the art into the file and writes a `cover.jpg` next to it. Works across every format mutagen can open (MP3, FLAC, M4A/MP4, OGG, Opus, WAV/AIFF, …).

At the end it prints a summary: how many were embedded, how many already had art (skipped), and any that failed and why.

> Because covers are found per *folder* first, a multi-track album folder only does one network lookup: track 1 fetches the art and writes `cover.jpg`, and the rest of the album reuses it.

### Discogs setup

Discogs needs a free **personal access token** to search and download images. Without one, the Discogs step is simply skipped and the chain falls back to MusicBrainz / iTunes.

1. Log in at <https://www.discogs.com/settings/developers>.
2. Click **Generate new token** and copy the token string.
3. Save it where the script looks for it (either works; the env var wins):
   ```bash
   # Option A — a token file (gitignored, read automatically)
   printf '%s' '<your-token>' > ~/.claude/skills/download-music/.discogs_token
   chmod 600 ~/.claude/skills/download-music/.discogs_token

   # Option B — an environment variable
   export DISCOGS_TOKEN='<your-token>'
   ```

Once set, both this command **and** the normal YouTube download flow gain Discogs as their second source (right after the folder image).

## Choosing a specific cover

Discogs lists every pressing/edition of a release separately, so one album often has many different covers (original vs. reissue, regional variants, etc.). When the automatic pick isn't the one you want, choose by hand. This is Discogs-only and needs a token.

**1. List the versions:**

```bash
python3 ~/.claude/skills/download-music/cover_picker.py list "<file-or-folder>"
```

Search terms come from the target's own tags (or the folder layout). For a **folder** it searches at the album level; for a single **file** it includes the track title. Override any of them with `--artist`, `--album`, `--title` when the tags are messy, and `--limit N` to show more/fewer.

It prints a numbered list — each entry shows the release (year · country · format), its resolution, and a URL you can open in a browser to see the cover live:

```
[1] Daft Punk - Discovery
     2014 · Europe · Vinyl, LP, Album, Reissue   (600x600)
     https://i.discogs.com/.../R-5835447-...jpeg

[2] Daft Punk - Discovery
     2002 · Europe · CD, Album, Reissue   (500x496)
     https://i.discogs.com/.../R-213409-...jpeg
```

**2. Set the one you want:**

```bash
python3 ~/.claude/skills/download-music/cover_picker.py set "<file-or-folder>" 2
```

This embeds version `2` (its highest-resolution image) into the target and writes a `cover.jpg` beside it. A **folder** target applies the cover to every audio file inside it — handy for fixing a whole album at once. (The list from step 1 is cached, so the numbers stay valid; `set` will re-run the search on its own if you skipped `list`.)

## Fixing track metadata

Use this when files have messy or missing tags — wrong capitalisation, no album, no year, no real genre. It corrects four descriptive fields — **artist, title, album, year** — from **MusicBrainz** (the canonical tagging database; cleaner titles and release dates than Discogs), and refines the **genre** from **Discogs**. MusicBrainz genres are weak for electronic music, so genre comes from Discogs' **styles** — the granular sub-genres that make DJ crates useful (e.g. `House, Deep House, Minimal` instead of a bare `Electronic`). This is the half of organising Engine DJ can't do for you: Engine analyses BPM and key itself on import, but it only ever *reads* the genre tag — so good genre crates depend on what's written here.

It does **not** touch BPM / key / Camelot tags — those come from the `tunebat` skill.

**Genre needs a Discogs token** (the same one the cover commands use — see "Discogs setup"). Without a token the genre step is skipped silently and only the MusicBrainz fields are corrected. The genre lookup uses the file's embedded Discogs **release id** when present (an exact, single-request match — files tagged by a Discogs tagger have one), otherwise it searches Discogs by artist/album/title. Every style is written, de-duplicated and comma-joined. The lookup is **resolved once per release and cached**, so a whole album is tagged consistently (and a track that fails its own search inherits a sibling's genre); Discogs calls are **paced** (~1/sec) so a big folder isn't rate-limited; and an **over-broad match is rejected** (more than ~8 styles almost always means a wrong various-artists/label release) so it falls back to a cleaner result or to none. Obscure bootlegs and white-labels often won't match — set those by hand with `--genre`.

**Always previews first — nothing is written without `--apply`:**

```bash
# 1. Preview the proposed old -> new changes (writes nothing)
python3 ~/.claude/skills/download-music/fix_metadata.py "<file-or-folder>"

# 2. Write the tag changes once you're happy
python3 ~/.claude/skills/download-music/fix_metadata.py "<file-or-folder>" --apply

# Also rename each file to its clean title (e.g. 01.mp3 -> One More Time.mp3):
python3 ~/.claude/skills/download-music/fix_metadata.py "<file-or-folder>" --rename --apply

# Genre ONLY — refine just the genre, leave artist/title/album/year alone:
python3 ~/.claude/skills/download-music/fix_metadata.py "<file-or-folder>" --genre-only --apply
```

How it matches, per track:

1. Searches MusicBrainz using the file's current artist + title, with the current album as a disambiguating hint.
2. Scores every (recording × release) pairing, so it prefers the **plain** track over remixes/live/compilation versions, the release that matches the file's existing album, and otherwise the earliest official studio album. Each proposal shows the matched `Artist – Title` and MusicBrainz score so you can sanity-check it.
3. Refines the genre from Discogs (release-id lookup, else search) — shown as a `genre` line in the same `old -> new` preview.
4. Only fields that actually differ are listed as `old -> new`; identical values are left alone.

Force any field with `--artist` / `--album` / `--title` / `--year` / `--genre` (handy to pin a whole folder's album, year, or genre). Two genre switches: **`--genre-only`** skips the MusicBrainz step and refines just the genre — the right choice for a library that's already descriptively clean (e.g. Discogs-tagged) and only needs crate-ready genres, and it's much faster since it makes no MusicBrainz calls; **`--no-genre`** does the opposite, leaving genre alone. MusicBrainz asks for ≤1 request/second, so a big folder is paced accordingly (with one automatic retry on its occasional `503`s).

> Auto-matching can still be wrong — that's exactly why it previews. Read the `old -> new` list before adding `--apply`, especially for obscure tracks or ones with no existing album tag.

## Vinyl rips — treat as handicraft

A vinyl rip is a hand-made artifact, not a throwaway web release. The person who ripped it documents their gear and process and encodes the pressing/quality in the folder name. **Honour that work** — give vinyl rips more respectful handling than scene/web releases.

**How to spot one:** the folder name contains `(Vinyl)` / `Vinyl` / a sample-rate tag like `24-48` / `24bit,48khz`, **or** there's a lineage/info file inside (a `.txt`/`.nfo` describing the turntable, cartridge, phono stage, cleaning, declicking and FLAC-encode chain — e.g. `Lineage (Aug 2022).txt`).

**Rules:**

- **Never rename the rip's folder.** The name carries the pressing and quality info (`Burial-UNTRUE.-24bit,48khz (Vinyl)`). Keep it exactly as-is, even when moving into the Library.
- **Never delete the human-authored files** — lineage `.txt`, info `.nfo`, ripping logs, the ripper's own label/sleeve scans. These ARE the craft. (This is the opposite of throwaway scene junk like `.m3u` / `.sfv`, which is fine to drop.)
- **Carry those files along** when moving the rip under `~/Music/Library/`: move the audio *and* the lineage/info/scan files together, preserving the original folder name.
- **Covers:** when the user is *deliberately* choosing art via `covers options` / `covers set`, replacing `cover.jpg` is the whole point — go ahead. The protection above is about the folder name and the documentation files, **not** the cover. Only avoid *silently* overwriting a ripper's own cover scan when they haven't asked you to.
- Tag fixes (`tags`) on the audio are still fine when asked — the rule guards the folder name and the documentation, not the music files' own metadata.

## Folder structure

```
~/Music/Library/
└── <Artist>/
    ├── <Album>/
    │   ├── cover.jpg               ← one per album folder
    │   ├── track1.mp3
    │   └── track2.mp3
    └── Singles/
        ├── <Single A Title>/
        │   ├── cover.jpg           ← belongs to this single only
        │   └── <Single A Title>.mp3
        └── <Single B Title>/
            ├── cover.jpg
            └── <Single B Title>.mp3
```

> Every single gets its own subfolder, so its `cover.jpg` is never overwritten by a later download.
>
> **Only write under `~/Music/Library/`.** The parent `~/Music/` also contains folders owned by other software (Mixxx, Apple Music's `Music Library.musiclibrary`, Engine Library, etc.) — never put downloads there.

## Moving a Soulseek folder into the Library (+ source log)

When a downloaded folder (typically from `~/Soulseek Downloads/complete/<user>/<release>/`) is cleaned up — tags fixed, cover set — and the user asks to move it into their Library:

1. **Move it** under `~/Music/Library/<Artist>/`:
   - Normal release: **keep the original Soulseek folder name verbatim** (it shows the label and/or year, e.g. `Alvar - 2025 - Moon Ritual [Junction Forest] [FLAC]`) — do *not* rename it to a bare `<Album>/`. File names inside can stay as the uploader had them when already clean (e.g. `01. I Need.flac`); no need to force-rename to bare titles.
   - **Single-track release whose folder name carries label/catalog info** (e.g. `[WAP 449D] Evian Christ - Ultra (2020)`): **keep the original folder name verbatim**, filed directly under `<Artist>/` like a normal release — do **not** flatten it into `Singles/<Title>/`. The user values seeing the label + catalog number (e.g. the Warp record number) on disk: it's how they remember releases and discover more. The `Singles/<Cleaned Title>/` layout is only for tracks that arrive *without* a meaningful folder name — YouTube/`download` grabs, and loose tracks pulled out of a compilation or dump folder. (If the single's source folder name is just a bare `Artist - Title` with no label/catalog, the `Singles/` layout is still fine.)
   - **Vinyl rip:** keep the original folder name exactly (see "Vinyl rips" above) and move the audio + all lineage/info/scan files together.
   - **Bootleg / white-label / special-catalog release** (e.g. `XXX (2008) [MP3] {Remerge Records-RE-XXX}`): also keep the original folder name exactly. These have no clean cover or canonical tags, so the label + catalog number in the folder name is the only reliable way to re-identify them.
2. **Clean the original** Soulseek folder: delete leftover scene junk (`.m3u` / `.nfo` / `.sfv`) and the now-empty release/user folders. (Never delete a vinyl rip's lineage/info files — those move *with* the rip in step 1.)
3. **Log the source** — append the move to `~/Soulseek Downloads/_downloaded-sources.md`, grouped by Soulseek **user**, recording the **original folder name** verbatim, a short type/quality note, and the date:
   ```
   ## <soulseek-user>
   - <original folder name>  — <type / quality e.g. "vinyl rip · 24/48 FLAC">  [moved YYYY-MM-DD]
   ```
   Add a new `## <user>` heading only if that user isn't already in the file; otherwise append under their existing heading. This log is how we find good uploaders again in the app later (especially quality vinyl rippers) — once a folder is moved out, it's the only remaining trace of who it came from.

   **Keep it to one scannable line.** The job of this log is *re-finding the uploader*, not retelling the release. Type/quality + format is the core; add at most a short parenthetical (≤ ~15 words) only when the folder name alone doesn't identify the music (e.g. `(Burial vs Basic Channel mashup)`). **Do not** narrate tag fixes, Discogs ids, catalog numbers, or decisions here — that belongs in the monthly note's tag-check, and only if it's genuinely worth flagging. If in doubt, shorter.
4. **Update the monthly library note** — add the moved release(s) to the current month's Obsidian note (see "Monthly library note" below): summary-table row, per-release tracks section with Discogs link, updated totals, and a tag-check note if anything was off or set by hand.
5. **Check for an incomplete-album gap** — if the folder is filed under its real album/EP name (not `Singles/`) and holds only *some* of the release's tracks, update `Areas/Mixing-DJing/Library/incomplete-albums.md` (see "Incomplete albums tracker" below). Skip this for VA-comp single-track pulls and for a missing track that's already owned under a different release — neither is a real gap.

> Do steps 2–5 **every time** a folder is moved/cleaned through the skill, not just when asked — the log, the monthly note, and the gap tracker are only useful if they're complete.

## Monthly library note (Obsidian)

A running, human-readable record of what's actually **in** `~/Music/Library/`, kept in the Obsidian vault so the genre/quality of every imported release can be audited without opening files. One note per month — the counterpart to the Soulseek source log (that log tracks *who* I pulled from; this tracks *what tags* landed on disk).

- **Where:** `Areas/Mixing-DJing/Library/<month>-YYYY.md` (e.g. `june-2026.md`), indexed by `Areas/Mixing-DJing/Library/Library.md`.
- **Scope:** only releases recorded in `~/Soulseek Downloads/_downloaded-sources.md` with a `[moved YYYY-MM-…]` in that month — i.e. things actually moved into the Library through this skill. **Ignore anything not in that log** (YouTube grabs, hand-added files, etc.).
- **Why genre-first:** Engine DJ analyses BPM/key on import but only ever *reads* the `genre` tag, so the Discogs styles written by `tags genre` are what crates depend on. This note is where that genre is eyeballed per release.

### Building / refreshing the note

1. **Pick the month** and read the Soulseek log; take every entry whose `[moved YYYY-MM-DD]` falls in that month.
2. **Map each logged folder to its Library location.** The log records the *original Soulseek folder name*, not the Library path — use judgement: a normal release lives under `<Artist>/<Album>/`, a vinyl/bootleg keeps its verbatim folder name (see "Vinyl rips"), a single-track release whose folder name carries label/catalog info keeps that verbatim folder name under `<Artist>/`, and a bare single (YouTube grab or loose track) lives under `<Artist>/Singles/<Title>/`. A "loose track" log entry maps to that one file, not a whole folder.
3. **Read the on-disk tags** of each audio file in those folders — artist, title, album, year, genre — plus the codec/format (e.g. `FLAC 24/96`, `MP3 320`). Read the files directly (mutagen); to quickly eyeball just the genres, `fix_metadata.py "<folder>" --genre-only` (preview, no `--apply`) prints each track's current → proposed genre. Also grab each release's **Discogs link** with `python3 ~/.claude/skills/download-music/discogs_url.py "<folder>"` — it prints the public `discogs.com/release/<id>` URL (from the embedded release id, else a search) or nothing if unmatched.
4. **Write the note** with this layout:
   - Frontmatter — `title`, `date`, `tags: [library, soulseek, imports, <month-year>, dj]`.
   - A one-line total: releases · tracks · uploaders.
   - A **Releases (summary)** table: `Moved | Artist — Release | Tracks | Format | Genre | Soulseek user`.
   - A **Tracks by release** section: one `###` heading per release with a provenance blockquote (uploader · quality · move date · Library path) and a table `# | (Artist) | Title | Year | Genre | Format`. Add the Artist column only when it varies within the release (splits, features, mashups); otherwise put the artist in the heading. **End each release's section** (right after its track table) **with a direct Discogs release link** — a `[Discogs ↗](https://www.discogs.com/release/<id>)` line — so the release can be reopened on Discogs without re-searching. Get the URL with `discogs_url.py "<folder>"` (resolves the embedded Discogs release id when present, else the best search match). **Fallback:** if it prints nothing — no match, or no token — first try an **official substitute link** for a release with no Discogs/MusicBrainz entry (brand-new or non-DB release): the label/artist's streaming smart link (e.g. an A24 `ffm.to` link), Bandcamp, or the official video. Use the same `[A24 Music ↗](url)` / `[Bandcamp ↗](url)` style. **Verify it resolves to the right release** (WebFetch) before linking — never invent or guess a URL; if you can't confirm one, **omit the link** entirely. **Sanity-check search-based matches:** an embedded-id hit is exact, but a *search* match can land on the wrong release (a compilation, a different artist, the wrong pressing) — open it, or confirm the artist/title/year/catalog via the Discogs API, before trusting it. Prefer the release that matches the on-disk version (right year/format/pressing).
   - A **Tag-check notes** section flagging anything off: a missing album/year, a broad/weak genre (e.g. a bare `Electronic`), an over-broad bootleg genre. **One short line per flag (≤ ~25 words) — a glance, not a story.** Only list releases that genuinely need a second pass or where something was *set by hand* (genre/year/cover invented because the DBs had nothing, a wrong auto-match overridden, a missing-DB release). **A clean arrival that needed no fixing gets no bullet at all** — silence means it was fine. Write the *result* (`genre set by hand: Synth-pop, Dream Pop, Alt-Pop — no DB match`), not the reasoning, sources, or play-by-play.
5. **Append, don't duplicate:** if the month's note already exists, add the new releases to its tables rather than rewriting it (vault rule), and update the index's monthly list.

> Run this **as part of every Library move** (step 4 of "Moving a Soulseek folder") — not just on request. `/download-music library` exists to rebuild or audit a month after the fact. The Soulseek log is the source of truth for *what* to include; the files on disk are the source of truth for the *tags*.

## Incomplete albums tracker (Obsidian)

A single running list — `Areas/Mixing-DJing/Library/incomplete-albums.md`, indexed from `Library.md` — of releases sitting in the Library with only *some* of their tracks, so it's easy to check "what's left" and go hunt for the rest. The monthly notes record what *is* on disk; this file records what's *missing* from it.

**What qualifies:** a release folder filed under its real album/EP name (not `Singles/<Title>/`) that holds fewer tracks than the official release. **What doesn't:**
- A single-track pull from a **various-artists compilation** (e.g. `VA — Shades Part 2`, `Airod — Exhale VA001`) — the goal was only ever that one track, not the rest of the comp.
- A "missing" track that's **already owned** under a different release (e.g. Basic Channel's `BCD-2` skips *Phylyps Trak* on purpose — it's filed separately as the 1993 single).
- Anything in `Singles/` — that layout itself signals the pull was deliberately just the one track.

**Building/updating a row:**

1. Get the release's **full official tracklist** — the Discogs API returns it directly (more reliable than scraping the site, which blocks WebFetch):
   ```bash
   TOKEN=$(cat ~/.claude/skills/download-music/.discogs_token)
   curl -s -H "User-Agent: download-music-skill/1.0" "https://api.discogs.com/releases/<id>?token=$TOKEN" \
     | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['position'],'-',t['title']) for t in d['tracklist']]"
   ```
   Get `<id>` from `discogs_url.py "<folder>"` — but **verify it's the right release first** (same rule as the monthly note: a search match can land on the wrong pressing or even the wrong album entirely — this is what caught KiCk i vs Kick II). No usable Discogs entry (unmatched or too new)? Use the label/artist's Bandcamp tracklist instead (WebFetch works fine there, unlike Discogs).
2. **Diff** the official tracklist against the on-disk tracks' titles/positions to get the exact missing track names — not just a count.
3. **Add/update the row**: `Artist — Release | Have/Total | Missing tracks (names) | Library path | Source link · [[<month>-2026]]`. Keep the missing-tracks cell as plain comma-separated names.
4. **Got more tracks later?** Update Have/Missing. **Now complete?** Delete the row entirely — this file only tracks gaps, not history.

## Engine DJ sync check

The monthly note records what was *moved into the Library*; Engine DJ is what you actually *play from*. They drift apart when a release is imported into the Library (and logged in the note) but never added to Engine — or when a file Engine knows about gets moved/deleted on disk. This check compares all three (disk ↔ note ↔ Engine) and says exactly what's out of step.

Engine keeps its desktop collection in a SQLite database — `~/Music/Engine Library/Database2/m.db` — with one row per track in a `Track` table, each storing the file's path relative to the Library (`../Library/<Artist>/…`). The script opens that database **read-only**, so it never writes to Engine and is safe to run with the app open or closed.

```bash
python3 ~/.claude/skills/download-music/engine_sync.py                 # current month
python3 ~/.claude/skills/download-music/engine_sync.py june-2026       # a specific month
python3 ~/.claude/skills/download-music/engine_sync.py --no-note       # disk ↔ Engine only
python3 ~/.claude/skills/download-music/engine_sync.py --show-excluded # list the ignore-listed holdouts
```

It prints four blocks plus a one-line verdict (`⚠ OUT OF SYNC` / `✅ IN SYNC`) up top:

- **[A] On disk, NOT in Engine, NOT excluded — this is the main result.** Every audio file under `~/Music/Library/` that has no matching Engine row *and* isn't on the ignore-list. **Anything here is a genuine gap — import it.** It covers the *whole* Library, not just one month, and it does **not** matter whether an entry is in a monthly note or the Soulseek log: a loose single (a YouTube grab, a hand-added `.wav` edit) is just as out of sync as a logged release. Each line shows the file's format/bitrate so a low-quality straggler is obvious. The verdict and exit status key off this block (plus [B]) — **not** off [D].
- **[B] In Engine but missing on disk** — broken references: Engine has a row but the file was moved or deleted. Relink or remove these in Engine.
- **[C] Month note** — reads `Areas/Mixing-DJing/Library/<month>-YYYY.md`, checks the header total matches the summary table, resolves each release's folder on disk, and confirms every one of that month's tracks is in Engine.
- **[D] Intentionally excluded** — files matched by `.engine_sync_ignore` (see below). Shown as a quiet count, never as an alarm. `--show-excluded` lists them with their bitrate.

Two things it normalizes so the comparison can be trusted (both tripped up the by-hand version):

- **Accents.** macOS stores filenames decomposed (`é` = `e` + combining ´), Engine stores them composed. Without normalizing, the *same* file shows up as both missing **and** broken. Everything is compared NFC-normalized, so accented titles (`L'Éternité`, `Premià de Mar`) match correctly.
- **Scope vs. count.** A month's folder can hold a file the note intentionally doesn't count — e.g. the Grimes `IDORU` YouTube grab sits in `Grimes/Miss Anthropocene/` next to the Soulseek `New Gods`, but the note logs Soulseek pulls only. So Engine (which holds everything) can legitimately sit 1–2 above the note's number; the script notes this instead of flagging it as an error.

**The ignore-list (`~/.claude/skills/download-music/.engine_sync_ignore`).** Not everything in the Library belongs in Engine — low-quality / over-compressed sources are often kept on disk on purpose until a better rip turns up. Without a way to record that, the check would flag those holdouts on every run, and that constant noise is exactly what once led to a *real* gap (a missing `.wav` edit) being waved off. So intentional holdouts go in this file — one Library-relative path per line, `#` for comments, **prefix match** (a trailing-`/` line excludes a whole folder; a full file path excludes just that file). Matched files drop out of [A] into [D]. **When you upgrade one to a better version and import it, delete its line** so the folder is audited normally again; the check also warns about ignore lines that no longer match anything on disk (stale entries to clean up).

Run it after a Library import session, or whenever Engine's count and a month note disagree. **Format matters on import:** Engine reads the `genre` tag but won't pick up a format it doesn't ingest — if a whole release is missing from [A] and shares one unusual extension (it once silently skipped an **AIFF** EP until it was re-imported), that format is the likely cause; converting those files to FLAC/WAV and re-importing fixes it.

## Porting the Library to an external SSD

The **last phase** of the pipeline, run **only when the user says so**. Everything earlier is unchanged: download → clean tags/covers → move the release into `~/Music/Library/` → import into Engine DJ. When the local disk fills up, this step flushes everything currently in `~/Music/Library/` onto an external SSD and deletes the local copies, reclaiming the space. It's repeatable: the Library *folder* is kept (only its contents move), so new Soulseek imports keep landing there, and the next flush just merges them into the SSD library.

```bash
python3 ~/.claude/skills/download-music/port_library.py /Volumes/<SSD>           # dry-run preview (default)
python3 ~/.claude/skills/download-music/port_library.py /Volumes/<SSD> --apply   # move + delete locals
python3 ~/.claude/skills/download-music/port_library.py /Volumes/<SSD> --no-verify  # size-only, faster, less safe
python3 ~/.claude/skills/download-music/port_library.py --target /Volumes/<SSD>/Custom/Path  # custom destination
```

By default the Library lands at `<SSD>/Music/Library/` (mirroring the local layout, which keeps a future Engine re-link natural). It moves **everything**, not just audio — `cover.jpg`, vinyl-rip lineage `.txt`/`.nfo` files and scans travel with their release.

How it protects against data loss (it deletes local files, so this matters):

- **Dry-run by default** — only `--apply` moves anything (same convention as `fix_metadata.py`).
- **Refuses anything but a real external drive** — the destination volume must be mounted *and* on a different physical disk than the source. This blocks the macOS trap where an unplugged SSD's `/Volumes/<name>` is silently a folder on the internal disk; the different-disk check makes a "move then delete" onto your own boot drive impossible.
- **Copy → verify → delete, per file** — each file is copied, the copy is re-read and SHA-256-compared to the original, and the local original is deleted **only** once the copy is proven byte-identical. A mismatch leaves both files in place and is reported.
- **Resumable & idempotent** — a file already on the SSD (same size + checksum) is skipped and only its local copy removed, so a re-run continues where it left off.

> **Engine DJ caveat — always mention this when running `--apply`.** Engine DJ stores each track's path relative to the internal disk (`../Library/<Artist>/…`). Once files live on the SSD, Engine shows them as missing until the user points Engine at the new location (add the SSD as a drive in Engine DJ, or relink). The script does **not** touch Engine's database — re-linking is a separate manual step — and it prints this reminder when it finishes.

## Packaging a mix for YouTube

YouTube only accepts video uploads — a WAV/MP3 file can't be uploaded directly, and it makes no difference if the audio already has embedded cover art (ID3/RIFF artwork): YouTube never reads audio metadata. The fix is to render a video where the cover image sits as a single still frame for the whole length of the mix.

### 1. Get the cover image

A square (1:1) image works best. Download it if it's a URL:

```bash
curl -sL -o "cover.jpg" "<image URL>"
```

### 2. Render the video

```bash
ffmpeg -y -loop 1 -i "<cover.jpg>" -i "<mix.wav>" \
  -c:v libx264 -tune stillimage -c:a aac -b:a 320k -pix_fmt yuv420p -shortest \
  "<mix>.mp4"
```

- `-loop 1 -i cover.jpg` holds the image as a static video frame.
- `-c:a aac -b:a 320k` re-encodes the audio to a format YouTube accepts, at high quality.
- `-shortest` stops the video exactly when the audio ends (otherwise the looping image has no natural end point).

Output lands next to the source file. Confirm the file exists and report its size/duration before handing it off.

### 3. Draft the title and description

House style, artist alias **cookiedeal**:

- **Title:** `<artist alias> - <series name> <NNN>` — e.g. `cookiedeal - solitaire mixes 001`, zero-padded to 3 digits.
- **Description:** all lowercase, no em dashes (use commas or plain hyphens instead), numbered tracklist as `artist - title`. No timestamps unless the user supplies exact cue times (e.g. from an Engine DJ session export) — never estimate them.
- Tracklist order follows the actual play order in the mix, not a library view's row numbers — a session often includes tracks that got mixed out before the final recording started. Confirm with the user which rows actually made it into the mix, and drop any accidental duplicate plays.

### Vault: the solitaire mixes series

Each mix's source file, cover, tracklist, and YouTube link are logged at `Areas/Mixing-DJing/Tracklists/solitaire-mixes.md` in the Obsidian vault, so numbering and style stay consistent across the series without re-deriving them each time. Check it before drafting a new mix's title, and add/update the entry (including the YouTube link once it's actually published).

## Notes

- Music library root: `~/Music/Library/`
- Raw DJ session/mix recordings (source for YouTube packaging): `~/Music/dj mixes <year>/`
- Solitaire mixes series tracker (Obsidian vault): `Areas/Mixing-DJing/Tracklists/solitaire-mixes.md`
- Cover art script (single file): `~/.claude/skills/download-music/embed_cover.py`
- Folder backfill script: `~/.claude/skills/download-music/cover_folder.py`
- Cover picker (Discogs versions): `~/.claude/skills/download-music/cover_picker.py`
- Metadata fixer (MusicBrainz tags + Discogs genre): `~/.claude/skills/download-music/fix_metadata.py`
- Discogs release-URL resolver (for the monthly note's per-release links): `~/.claude/skills/download-music/discogs_url.py`
- Discogs token (optional): `~/.claude/skills/download-music/.discogs_token` or `$DISCOGS_TOKEN`
- Download queue file: `~/.claude/skills/download-music/queue.md`
- Soulseek source log: `~/Soulseek Downloads/_downloaded-sources.md`
- Monthly library notes (Obsidian vault): `Areas/Mixing-DJing/Library/` (index `Library.md`, one `<month>-YYYY.md` per month)
- Incomplete albums tracker (Obsidian vault): `Areas/Mixing-DJing/Library/incomplete-albums.md`
- Engine DJ desktop collection (SQLite, read-only by the sync check): `~/Music/Engine Library/Database2/m.db` (`Track` table)
- Engine sync checker (Library ↔ month note ↔ Engine): `~/.claude/skills/download-music/engine_sync.py`
- Engine sync ignore-list (intentional low-quality holdouts): `~/.claude/skills/download-music/.engine_sync_ignore`
- Library porter (Library → external SSD, then delete locals): `~/.claude/skills/download-music/port_library.py`
- Session masterer (loudness + true-peak for upload): `~/.claude/skills/download-music/master_audio.py`
- Skill definition: `~/.claude/commands/download-music.md`
- Dependencies:
  - `yt-dlp` (Homebrew)
  - `ffmpeg` (Homebrew)
  - `mutagen`, `requests`, `Pillow` (pip)
- Platform: YouTube for now, expandable to other yt-dlp-supported platforms later.
