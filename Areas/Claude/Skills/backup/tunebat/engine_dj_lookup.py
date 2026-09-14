#!/usr/bin/env python3
"""Engine DJ database lookup — the ground truth for the /tunebat skill.

Engine DJ is the canonical source for key/BPM (the user mixes on it). This
script queries the local Engine DJ SQLite database and returns the same JSON
shape as `tunebat_fetch.py`, with `source: "engine-dj"`.

Usage:
    engine_dj_lookup.py --path "/Users/agomezu/Music/Library/.../Song.mp3"
    engine_dj_lookup.py --query "Message of Love St David"

Exits non-zero (with a JSON error on stderr) when no match is found, so the
caller can fall back to tunebat_fetch.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

ENGINE_DB = Path.home() / "Music" / "Engine Library" / "Database2" / "m.db"
LIBRARY_ROOT = Path.home() / "Music"

# Engine DJ key integer → (key name, Camelot code).
#
# Derived from one confirmed data point (key=1 → A minor / 8A, per the user on
# 2026-05-23) and Open Key notation (1m–12m, 1d–12d). The mapping is consistent
# with the publicly documented Engine SDK ordering but has NOT been fully
# verified across all 24 values. If a future track in the DB returns a key that
# disagrees with what Engine DJ shows in its UI, fix the offending row here.
ENGINE_KEY_CODES: dict[int, dict[str, str]] = {
    # Minor keys (1–12 = Open Key 1m–12m)
    1:  {"key": "A minor",  "camelot": "8A"},   # confirmed 2026-05-23
    2:  {"key": "E minor",  "camelot": "9A"},
    3:  {"key": "B minor",  "camelot": "10A"},
    4:  {"key": "F♯ minor", "camelot": "11A"},
    5:  {"key": "C♯ minor", "camelot": "12A"},
    6:  {"key": "G♯ minor", "camelot": "1A"},
    7:  {"key": "E♭ minor", "camelot": "2A"},
    8:  {"key": "B♭ minor", "camelot": "3A"},
    9:  {"key": "F minor",  "camelot": "4A"},
    10: {"key": "C minor",  "camelot": "5A"},
    11: {"key": "G minor",  "camelot": "6A"},
    12: {"key": "D minor",  "camelot": "7A"},
    # Major keys (13–24 = Open Key 1d–12d)
    13: {"key": "C major",  "camelot": "8B"},
    14: {"key": "G major",  "camelot": "9B"},
    15: {"key": "D major",  "camelot": "10B"},
    16: {"key": "A major",  "camelot": "11B"},
    17: {"key": "E major",  "camelot": "12B"},
    18: {"key": "B major",  "camelot": "1B"},
    19: {"key": "F♯ major", "camelot": "2B"},
    20: {"key": "D♭ major", "camelot": "3B"},
    21: {"key": "A♭ major", "camelot": "4B"},
    22: {"key": "E♭ major", "camelot": "5B"},
    23: {"key": "B♭ major", "camelot": "6B"},
    24: {"key": "F major",  "camelot": "7B"},
}


def fail(msg: str) -> None:
    print(json.dumps({"error": msg}), file=sys.stderr)
    sys.exit(1)


def normalize_path_for_engine(abs_path: str) -> str:
    """Engine DJ stores paths relative to its database folder (e.g.
    `../Library/Artist/Album/Track.mp3`). Convert an absolute path into that
    relative form for matching."""
    db_dir = ENGINE_DB.parent
    try:
        return os.path.relpath(abs_path, db_dir)
    except ValueError:
        return abs_path


def lookup_by_path(conn: sqlite3.Connection, abs_path: str) -> dict | None:
    rel = normalize_path_for_engine(abs_path)
    basename = os.path.basename(abs_path)
    # Try exact relative-path match first; fall back to filename suffix match.
    for sql, args in [
        ("SELECT id, title, artist, album, filename, path, bpm, bpmAnalyzed, key, isAnalyzed FROM Track WHERE path = ?", (rel,)),
        ("SELECT id, title, artist, album, filename, path, bpm, bpmAnalyzed, key, isAnalyzed FROM Track WHERE filename = ?", (basename,)),
    ]:
        row = conn.execute(sql, args).fetchone()
        if row:
            return dict(row)
    return None


def _tokens(s: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", (s or "").lower()))


def lookup_by_query(conn: sqlite3.Connection, query: str) -> dict | None:
    """Fuzzy match by tokenizing the query and scoring against title + artist +
    path. Cheap because Engine DJ libraries are usually small (hundreds of
    tracks, not millions)."""
    query_tokens = _tokens(query)
    if not query_tokens:
        return None

    rows = conn.execute(
        "SELECT id, title, artist, album, filename, path, bpm, bpmAnalyzed, key, isAnalyzed FROM Track"
    ).fetchall()

    best, best_score = None, 0
    for r in rows:
        row = dict(r)
        haystack = _tokens(" ".join([
            row.get("title") or "",
            row.get("artist") or "",
            row.get("album") or "",
            row.get("filename") or "",
            row.get("path") or "",
        ]))
        score = len(query_tokens & haystack)
        if score > best_score:
            best, best_score = row, score
    # Require at least half the query tokens to match — guards against
    # returning a random track for an unrelated query.
    if best and best_score >= max(1, len(query_tokens) // 2):
        return best
    return None


def to_output(row: dict) -> dict:
    key_code = row.get("key")
    key_info = ENGINE_KEY_CODES.get(key_code, {}) if key_code else {}
    bpm = row.get("bpmAnalyzed") or row.get("bpm")
    return {
        "source": "engine-dj",
        "artist": row.get("artist") or None,
        "title": row.get("title") or None,
        "album": row.get("album") or None,
        "filename": row.get("filename"),
        "path": row.get("path"),
        "key": key_info.get("key"),
        "camelot": key_info.get("camelot"),
        "engine_key_code": key_code,
        "bpm": round(bpm, 2) if isinstance(bpm, (int, float)) else None,
        "isAnalyzed": bool(row.get("isAnalyzed")),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Engine DJ database lookup")
    parser.add_argument("--path", help="Absolute path to the MP3 file")
    parser.add_argument("--query", help="Free-text query (artist + title)")
    args = parser.parse_args()

    if not args.path and not args.query:
        fail("Pass --path <abs-path> or --query '<artist title>'")

    if not ENGINE_DB.exists():
        fail(f"Engine DJ database not found at {ENGINE_DB}")

    conn = sqlite3.connect(f"file:{ENGINE_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row

    row = lookup_by_path(conn, args.path) if args.path else lookup_by_query(conn, args.query)
    if not row:
        fail("No matching track in Engine DJ database — fall back to tunebat_fetch.py")

    if not row.get("isAnalyzed"):
        fail(f"Track found (id={row['id']}, {row.get('filename')}) but not analyzed in Engine DJ yet")

    print(json.dumps(to_output(row), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
