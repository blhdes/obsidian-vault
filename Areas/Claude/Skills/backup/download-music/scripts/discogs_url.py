#!/usr/bin/env python3
"""
Print the public Discogs release URL for a track or album.

Used by the monthly library note (see the skill doc): each "Tracks by release"
entry ends with a direct Discogs link so a release can be reopened on
discogs.com without re-searching. The URL is resolved from the file's embedded
Discogs release id when present (an exact match — files tagged by a Discogs
tagger carry one), otherwise from the best Discogs search match. Prints
*nothing* when no release is found or no token is configured, so the note
simply omits the link (graceful fallback).

    discogs_url.py <file-or-folder> [--artist A] [--album B] [--title T]

A folder is resolved at the album level (artist + album); a single file also
pins its track title. Needs a Discogs token (see the skill doc).
"""

import argparse
import os
import re
import sys

from embed_cover import load_discogs_token, search_discogs
from cover_folder import infer_from_path, iter_audio_files, read_meta
from fix_metadata import read_discogs_release_id

RELEASE_PAGE = "https://www.discogs.com/release/{}"


def first_audio(folder: str) -> str | None:
    for path, _audio in iter_audio_files(folder):
        return path
    return None


def derive(target: str, args) -> tuple[str | None, str | None, str | None, str | None]:
    """Work out (artist, album, title, release_id) to resolve the release with."""
    artist = album = title = release_id = None

    if os.path.isdir(target):
        sample = first_audio(target)
        if sample:
            artist, album, title = read_meta(sample)
            if not (artist and album):
                ia, ial, _ = infer_from_path(sample)
                artist, album = artist or ia, album or ial
            release_id = read_discogs_release_id(sample)
        title = None  # album-level search — don't pin to one track
    else:
        artist, album, title = read_meta(target)
        if not (artist and title):
            ia, ial, it = infer_from_path(target)
            artist, album, title = artist or ia, album or ial, title or it
        release_id = read_discogs_release_id(target)

    # Explicit overrides always win.
    artist = args.artist or artist
    album = args.album or album
    title = args.title if args.title is not None else title
    return artist, album, title, release_id


def _id_from_resource_url(url: str | None) -> str | None:
    """Pull the numeric release id out of an api.discogs.com/releases/<id> URL."""
    m = re.search(r"/releases/(\d+)", url or "")
    return m.group(1) if m else None


def resolve_url(target: str, args) -> str | None:
    token = load_discogs_token()
    if not token:
        print("(no Discogs token configured — omitting link)", file=sys.stderr)
        return None

    artist, album, title, release_id = derive(target, args)

    # 1. Exact: the file's own embedded Discogs release id.
    if release_id:
        return RELEASE_PAGE.format(release_id)

    # 2. Else: the best-matching Discogs search result (already ranked).
    if not artist or not (album or title):
        print("(couldn't work out artist + album/title to search with)", file=sys.stderr)
        return None
    for cand in search_discogs(artist, album, title, token):
        rid = _id_from_resource_url(cand.get("resource_url"))
        if rid:
            return RELEASE_PAGE.format(rid)
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Print a release's public Discogs URL.")
    parser.add_argument("target", help="Audio file or folder.")
    parser.add_argument("--artist", default=None)
    parser.add_argument("--album", default=None)
    parser.add_argument("--title", default=None)
    args = parser.parse_args()

    target = os.path.expanduser(args.target)
    if not os.path.exists(target):
        print(f"ERROR: no such file or folder: {target}", file=sys.stderr)
        sys.exit(1)

    url = resolve_url(target, args)
    if url:
        print(url)
    # else: nothing on stdout — the note omits the link (fallback).


if __name__ == "__main__":
    main()
