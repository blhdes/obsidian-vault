#!/usr/bin/env python3
"""
Fix descriptive tags from two databases (artist / title / album / year from
MusicBrainz, genre from Discogs), and optionally rename files to their clean
title.

MusicBrainz is the canonical tagging database (what MusicBrainz Picard uses),
so its titles and release dates are cleaner than Discogs' pressing-level data.
Discogs, on the other hand, has the granular *styles* electronic music needs
for crate-building (e.g. 'Deep House, Minimal' rather than just 'Electronic') —
so genre is pulled from there. This pairs with the `covers` commands, which
also use Discogs for art.

    fix_metadata.py <file-or-folder>            # PREVIEW tag changes (no writes)
    fix_metadata.py <file-or-folder> --apply    # write the tag changes
    fix_metadata.py <file-or-folder> --rename --apply   # also rename files

It searches MusicBrainz per track using the current artist/title (and the
album as a hint to disambiguate), then proposes artist/title/album/year. For
genre it uses the file's embedded Discogs release id when present (exact),
otherwise searches Discogs, and writes every style comma-joined. By default
nothing is written — you see every old -> new change first. Override a field
with --artist / --album / --title / --year / --genre (handy for a whole
folder); --no-genre skips the Discogs genre step; --genre-only refines just the
genre and leaves the MusicBrainz fields untouched (for an already-clean
library that only needs genres).

Genre needs a Discogs token (see the skill doc); without one it's skipped
silently, like the cover chain. BPM/key/Camelot tags are never touched — those
come from the `tunebat` skill.
"""

import argparse
import difflib
import os
import re
import sys
import time

import mutagen
import mutagen.id3

from embed_cover import (
    mb_search_recordings,
    load_discogs_token,
    search_discogs,
    discogs_get,
)
from cover_folder import infer_from_path, iter_audio_files

FIELDS = ("artist", "title", "album", "year")
DISPLAY_FIELDS = FIELDS + ("genre",)  # genre is sourced from Discogs, not MusicBrainz
MB_MIN_INTERVAL = 1.1  # seconds — MusicBrainz asks for <=1 request/second
_last_mb_call = 0.0

DISCOGS_RELEASE_URL = "https://api.discogs.com/releases/{}"
DISCOGS_TOKEN: str | None = None  # loaded once in main()
DISCOGS_MIN_INTERVAL = 1.1  # Discogs allows ~60 authed requests/min — pace ~1/sec
MAX_SEARCH_STYLES = 8       # a search hit with more styles than this is almost certainly a wrong (VA/label) match
_last_discogs_call = 0.0
_genre_cache: dict = {}     # release-key -> genre string, so an album is looked up once

# AIFF/WAV have no "easy" mutagen wrapper — their tags are raw ID3, which uses
# frame names (TPE1, TCON, ...) instead of easy keys and only accepts Frame objects.
ID3_FRAME_FOR_KEY = {
    "artist": mutagen.id3.TPE1,
    "albumartist": mutagen.id3.TPE2,
    "title": mutagen.id3.TIT2,
    "album": mutagen.id3.TALB,
    "date": mutagen.id3.TDRC,
    "originaldate": mutagen.id3.TDOR,
    "year": mutagen.id3.TDRC,
    "genre": mutagen.id3.TCON,
}


def is_raw_id3(tags) -> bool:
    """True for raw ID3 tags (AIFF/WAV), False for EasyID3 and other formats."""
    return isinstance(tags, mutagen.id3.ID3)


# ---------- read current tags ----------

def read_discogs_release_id(path: str) -> str | None:
    """Find an embedded Discogs release id across FLAC/MP3/MP4 tag styles.

    Files tagged by a Discogs tagger carry the exact release id, which gives a
    precise genre lookup with no guessing. Read from the non-easy tags because
    EasyID3 doesn't expose custom frames.
    """
    try:
        audio = mutagen.File(path)
    except Exception:
        return None
    if audio is None or audio.tags is None:
        return None
    tags = audio.tags
    # Vorbis comments (FLAC, OGG): case-insensitive lowercase keys.
    try:
        val = tags.get("discogs_release_id")
        if val:
            return str(val[0]).strip() or None
    except Exception:
        pass
    # ID3 (MP3): a TXXX:DISCOGS_RELEASE_ID frame.
    getall = getattr(tags, "getall", None)
    if callable(getall):
        for frame in getall("TXXX"):
            if (getattr(frame, "desc", "") or "").upper() == "DISCOGS_RELEASE_ID" and frame.text:
                return str(frame.text[0]).strip() or None
    # MP4: a freeform ----:com.apple.iTunes:DISCOGS_RELEASE_ID atom.
    try:
        val = tags.get("----:com.apple.iTunes:DISCOGS_RELEASE_ID")
        if val:
            raw = val[0]
            text = raw.decode("utf-8", "ignore") if isinstance(raw, bytes) else str(raw)
            return text.strip() or None
    except Exception:
        pass
    return None


def read_current(path: str) -> dict:
    """Return the file's current {artist, title, album, year, genre, ...}."""
    try:
        audio = mutagen.File(path, easy=True)
    except Exception:
        audio = None
    tags = audio.tags if audio is not None else None

    def first(*keys: str) -> str | None:
        if tags is None:
            return None
        for key in keys:
            if is_raw_id3(tags):
                frame_cls = ID3_FRAME_FOR_KEY.get(key)
                frame = tags.get(frame_cls.__name__) if frame_cls else None
                val = frame.text if frame else None
            else:
                val = tags.get(key)
            if val:
                text = str(val[0]).strip()
                if text:
                    return text
        return None

    return {
        "artist": first("artist", "albumartist"),
        "title": first("title"),
        "album": first("album"),
        "year": (first("date", "originaldate", "year") or "")[:4] or None,
        "genre": first("genre"),
        "discogs_release_id": read_discogs_release_id(path),
    }


# ---------- MusicBrainz lookup ----------

def _artist_credit(rec: dict) -> str | None:
    parts = []
    for ac in rec.get("artist-credit") or []:
        if isinstance(ac, dict):
            parts.append(ac.get("name") or (ac.get("artist") or {}).get("name", ""))
            parts.append(ac.get("joinphrase", ""))
    return "".join(parts).strip() or None


# Words marking a non-canonical version — penalised unless the query asked for them.
_NOISE = re.compile(
    r"\b(remix|rmx|edit|version|mix|live|instrumental|demo|acoustic|"
    r"remaster(?:ed)?|mono|karaoke|cover|tribute|re-?recorded|bootleg)\b",
    re.IGNORECASE,
)


def _n(s: str | None) -> str:
    """Lowercase + collapse punctuation to spaces, for fuzzy comparison."""
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _ratio(a: str | None, b: str | None) -> float:
    return difflib.SequenceMatcher(None, _n(a), _n(b)).ratio()


def _year(date: str) -> int:
    m = re.match(r"\d{4}", date or "")
    return int(m.group()) if m else 9999


def _release_bonus(rel: dict, hint_n: str) -> float | None:
    """How canonical a single release is, as album/year source. None = skip it."""
    rg = rel.get("release-group") or {}
    secondary = set(rg.get("secondary-types") or [])
    if "DJ-mix" in secondary:
        return None
    bonus = 0.0
    if hint_n and _n(rel.get("title")) == hint_n:
        bonus += 2.0                                    # exact match to the file's album
    if (rel.get("status") or "") == "Official":
        bonus += 0.4
    if "Compilation" in secondary:
        bonus -= 0.5
    if "Live" in secondary:
        bonus -= 0.5
    bonus += {"Album": 0.4, "EP": 0.3, "Single": 0.2}.get(rg.get("primary-type") or "", 0.0)
    date = rel.get("date") or rg.get("first-release-date") or ""
    bonus += (2100 - _year(date)) / 10000.0             # nudge toward the earliest pressing
    return bonus


def mb_lookup(artist: str, title: str, album_hint: str | None) -> dict | None:
    """Return proposed {artist, title, album, year, matched, score} or None.

    Scores every (recording × release) pair so an earlier studio album on one
    recording can beat a later live/comp release on another — the two-step
    "best recording then best release" can't see that.
    """
    global _last_mb_call
    recordings = None
    for attempt in range(2):  # one retry for MusicBrainz's transient 503/429s
        wait = MB_MIN_INTERVAL - (time.monotonic() - _last_mb_call)
        if wait > 0:
            time.sleep(wait)
        try:
            recordings = mb_search_recordings(artist, title, album_hint)
            break
        except Exception as e:
            if attempt == 0:
                print(f"    MusicBrainz hiccup ({e}); retrying...")
                time.sleep(2)
            else:
                print(f"    MusicBrainz lookup failed: {e}")
        finally:
            _last_mb_call = time.monotonic()

    if not recordings:
        return None

    hint_n = _n(album_hint)
    best = None  # (score, recording, release)
    for rec in recordings:
        rtitle, rartist = rec.get("title") or "", _artist_credit(rec) or ""
        base = 3.0 * _ratio(rtitle, title) + 2.0 * _ratio(rartist, artist)
        if _NOISE.search(rtitle) and not _NOISE.search(title):
            base -= 1.5                                 # query wanted the plain track
        try:
            base += float(rec.get("score", 0)) / 1000.0
        except (TypeError, ValueError):
            pass

        pairs = [(rel, _release_bonus(rel, hint_n)) for rel in rec.get("releases") or []]
        pairs = [(rel, b) for rel, b in pairs if b is not None] or [(None, 0.0)]
        for rel, bonus in pairs:
            cand = (base + bonus, rec, rel)
            if best is None or cand[0] > best[0]:
                best = cand

    _score, rec, rel = best
    date = (rel or {}).get("date") or rec.get("first-release-date") or ""
    ym = re.match(r"\d{4}", date)
    return {
        "artist": _artist_credit(rec),
        "title": (rec.get("title") or "").strip() or None,
        "album": (rel or {}).get("title") or None,
        "year": ym.group() if ym else None,
        "matched": f"{_artist_credit(rec)} – {rec.get('title')}",
        "score": rec.get("score"),
    }


# ---------- Discogs genre/style lookup ----------

def _combine_genre(genres: list, styles: list) -> str | None:
    """Comma-join Discogs styles (the granular sub-genres) for crate-building.

    Falls back to the broad genre when a release has no styles. De-duplicates
    case-insensitively and keeps Discogs' order, e.g. 'House, Deep House,
    Minimal'.
    """
    seen, out = set(), []
    for s in (styles or genres or []):
        s = (s or "").strip()
        if s and s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return ", ".join(out) or None


def _discogs_pace() -> None:
    """Keep Discogs requests ~1/sec apart so a big folder doesn't get 429'd.

    In a normal run MusicBrainz's per-track pacing covers this, but --genre-only
    makes no MusicBrainz calls, so genre would otherwise hammer Discogs.
    """
    global _last_discogs_call
    wait = DISCOGS_MIN_INTERVAL - (time.monotonic() - _last_discogs_call)
    if wait > 0:
        time.sleep(wait)
    _last_discogs_call = time.monotonic()


def _within_cap(genre: str | None) -> bool:
    """A genre with too many styles is unusable for crates and almost always a
    wrong (various-artists/label) match — reject it whatever the source."""
    return bool(genre) and genre.count(",") + 1 <= MAX_SEARCH_STYLES


def _discogs_genre_lookup(artist, title, album_hint, release_id) -> str | None:
    """One Discogs lookup (no cache): exact via release id, else search."""
    if release_id:
        _discogs_pace()
        data = discogs_get(DISCOGS_RELEASE_URL.format(release_id), DISCOGS_TOKEN)
        if data:
            genre = _combine_genre(data.get("genres") or [], data.get("styles") or [])
            if _within_cap(genre):
                return genre
            # else: the embedded id is over-broad (likely wrong) — fall through to search
    if not artist or not (album_hint or title):
        return None
    _discogs_pace()
    cands = search_discogs(artist, album_hint, title, DISCOGS_TOKEN)
    if not cands:
        return None
    genre = _combine_genre(cands[0].get("genre") or [], cands[0].get("style") or [])
    return genre if _within_cap(genre) else None


def discogs_genre(artist, title, album_hint, release_id) -> str | None:
    """A refined genre string from Discogs, or None.

    Caches by release so a whole album is looked up once and tagged
    consistently: keyed on the Discogs release id when present, else
    artist+album, else artist+title for a single. Only successful results are
    cached, so a track that fails its own search still inherits a sibling's
    genre once any track on the album resolves.
    """
    if not DISCOGS_TOKEN:
        return None
    if release_id:
        key = ("rid", release_id)
    elif album_hint:
        key = ("aa", (artist or "").lower(), album_hint.lower())
    else:
        key = ("at", (artist or "").lower(), (title or "").lower())

    if _genre_cache.get(key):
        return _genre_cache[key]
    result = _discogs_genre_lookup(artist, title, album_hint, release_id)
    if result:
        _genre_cache[key] = result
    return result


# ---------- proposing changes ----------

def propose(path: str, args) -> dict | None:
    """Build {field: (old, new)} of changes for one file, plus 'matched'/'rename'."""
    current = read_current(path)
    artist = current["artist"]
    title = current["title"]
    album_hint = current["album"]
    if not (artist and title):
        ia, ial, it = infer_from_path(path)
        artist, title, album_hint = artist or ia, title or it, album_hint or ial
    if not (artist and title):
        return {"error": "no artist/title to search with"}

    mb_result = None if args.genre_only else mb_lookup(artist, title, album_hint)
    proposed = dict(mb_result or {})  # MB may miss — overrides and genre can still apply

    # Explicit overrides win over MusicBrainz.
    for field, override in (("artist", args.artist), ("album", args.album),
                            ("title", args.title), ("year", args.year)):
        if override is not None:
            proposed[field] = override

    changes = {}
    for field in FIELDS:
        new = (proposed.get(field) or "").strip()
        old = current.get(field) or ""
        if new and new != old:
            changes[field] = (old or None, new)

    # Genre is sourced from Discogs (its styles are the granular sub-genres),
    # independent of the MusicBrainz match above.
    if args.genre is not None:
        new_genre = args.genre.strip() or None
    elif args.no_genre:
        new_genre = None
    else:
        new_genre = discogs_genre(artist, title, album_hint, current.get("discogs_release_id"))
    if new_genre and new_genre != (current.get("genre") or ""):
        changes["genre"] = (current.get("genre") or None, new_genre)

    if not changes and new_genre is None:
        if args.genre_only:
            return {"error": "no Discogs genre found"}
        if mb_result is None:
            return {"error": "no MusicBrainz match"}

    result = {
        "changes": changes,
        "matched": proposed.get("matched"),
        "score": proposed.get("score"),
    }

    if args.rename:
        new_title = changes["title"][1] if "title" in changes else current["title"]
        if new_title:
            new_name = _sanitize(new_title) + os.path.splitext(path)[1]
            if new_name != os.path.basename(path):
                result["rename"] = new_name
    return result


# ---------- writing ----------

def _sanitize(name: str) -> str:
    name = re.sub(r'[/\\:*?"<>|]', "_", name.strip()).rstrip(". ")
    return name or "untitled"


def write_tags(path: str, changes: dict) -> None:
    audio = mutagen.File(path, easy=True)
    if audio is None:
        raise ValueError(f"unsupported file: {path}")
    if audio.tags is None:
        audio.add_tags()
    for field, (_old, new) in changes.items():
        key = "date" if field == "year" else field
        if is_raw_id3(audio.tags):
            frame_cls = ID3_FRAME_FOR_KEY[key]
            audio.tags.setall(frame_cls.__name__, [frame_cls(encoding=3, text=[new])])
        else:
            audio[key] = new
    audio.save()


def rename_file(path: str, new_name: str) -> str:
    folder = os.path.dirname(path)
    stem, ext = os.path.splitext(new_name)
    new_path = os.path.join(folder, new_name)
    i = 2
    while os.path.exists(new_path) and os.path.abspath(new_path) != os.path.abspath(path):
        new_path = os.path.join(folder, f"{stem} ({i}){ext}")
        i += 1
    if os.path.abspath(new_path) != os.path.abspath(path):
        os.rename(path, new_path)
    return new_path


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fix artist/title/album/year tags from MusicBrainz."
    )
    parser.add_argument("target", help="Audio file or folder (recurses).")
    parser.add_argument("--apply", action="store_true", help="Actually write changes (default: preview only).")
    parser.add_argument("--rename", action="store_true", help="Also rename files to their clean title.")
    parser.add_argument("--artist", default=None)
    parser.add_argument("--album", default=None)
    parser.add_argument("--title", default=None)
    parser.add_argument("--year", default=None)
    parser.add_argument("--genre", default=None,
                        help="Force this genre on every file (skips the Discogs lookup).")
    parser.add_argument("--no-genre", action="store_true",
                        help="Don't refine the genre from Discogs.")
    parser.add_argument("--genre-only", action="store_true",
                        help="Only refine the genre — skip the MusicBrainz artist/title/album/year step.")
    args = parser.parse_args()

    target = os.path.expanduser(args.target)
    if not os.path.exists(target):
        print(f"ERROR: no such file or folder: {target}", file=sys.stderr)
        sys.exit(1)

    global DISCOGS_TOKEN
    DISCOGS_TOKEN = load_discogs_token()
    if not DISCOGS_TOKEN and not args.no_genre and args.genre is None:
        print("(no Discogs token — genre refinement skipped; see the skill doc to enable)\n")

    files = [target] if os.path.isfile(target) else [p for p, _ in iter_audio_files(target)]
    if not files:
        print("No audio files found.")
        return

    mode = "APPLYING" if args.apply else "PREVIEW (no changes written)"
    print(f"=== {mode} — {len(files)} file(s) ===\n")

    changed = renamed = unchanged = failed = 0
    base = os.path.dirname(os.path.abspath(target))

    for path in files:
        rel = os.path.relpath(path, base)
        result = propose(path, args)

        if result.get("error"):
            print(f"✗ {rel} — {result['error']}")
            failed += 1
            continue

        changes, rename_to = result["changes"], result.get("rename")
        if not changes and not rename_to:
            unchanged += 1
            continue

        if result.get("matched"):
            print(f"{rel}    [match: {result['matched']}, MB score {result['score']}]")
        elif args.genre_only:
            print(f"{rel}    [genre only]")
        else:
            print(f"{rel}    [genre via Discogs — no MusicBrainz match]")
        for field in DISPLAY_FIELDS:
            if field in changes:
                old, new = changes[field]
                print(f"     {field:<6}: {old or '(none)'!r} -> {new!r}")
        if rename_to:
            print(f"     rename: {os.path.basename(path)!r} -> {rename_to!r}")
        print()

        if args.apply:
            try:
                if changes:
                    write_tags(path, changes)
                if rename_to:
                    rename_file(path, rename_to)
            except Exception as e:
                print(f"     ✗ failed to apply: {e}\n")
                failed += 1
                continue
        if changes:
            changed += 1
        if rename_to:
            renamed += 1

    print("=== Summary ===")
    verb = "changed" if args.apply else "would change"
    print(f"  {verb}: {changed} file(s)" + (f", renamed: {renamed}" if args.rename else ""))
    print(f"  already correct: {unchanged}")
    print(f"  no match / failed: {failed}")
    if not args.apply and (changed or renamed):
        print("\nRe-run with --apply to write these changes.")


if __name__ == "__main__":
    main()
