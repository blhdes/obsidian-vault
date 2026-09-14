#!/usr/bin/env python3
"""
Pick a specific Discogs cover for a track or album, by hand.

Discogs lists every pressing/edition as its own release, so one album can have
many different covers. This tool lets you see them and choose:

    cover_picker.py list <file-or-folder> [--artist A] [--album B] [--title T]
        Print a numbered list of Discogs cover versions for the target, each
        with its release info, resolution, and a URL you can open in a browser
        to view it live. The list is cached so you can `set` by number next.

    cover_picker.py set <file-or-folder> <number>
        Embed the chosen cover (its highest-resolution version) into the target
        and write a cover.jpg beside it. A folder target covers every audio
        file inside it.

Search terms come from the target's tags (or folder layout); override any of
them with --artist / --album / --title. Needs a Discogs token (see the skill
doc); `set` with no prior `list` will re-run the search automatically.

Note: the Discogs API caps served images at ~600px on the long edge — the
giant original scans on the website aren't exposed through the API.
"""

import argparse
import json
import os
import sys

from embed_cover import (
    best_discogs_image,
    download_image,
    load_discogs_token,
    normalize_to_jpeg,
    search_discogs,
)
from cover_folder import embed_picture, infer_from_path, iter_audio_files, read_meta

CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cover_options.json")


# ---------- search terms ----------

def first_audio(folder: str) -> str | None:
    for path, _audio in iter_audio_files(folder):
        return path
    return None


def derive_terms(target: str, args) -> tuple[str | None, str | None, str | None]:
    """Figure out (artist, album, title) to search Discogs with."""
    artist = album = title = None

    if os.path.isdir(target):
        sample = first_audio(target)
        if sample:
            artist, album, title = read_meta(sample)
            if not (artist and album):
                ia, ial, _ = infer_from_path(sample)
                artist, album = artist or ia, album or ial
        title = None  # album-level search — don't pin to one track
    else:
        artist, album, title = read_meta(target)
        if not (artist and title):
            ia, ial, it = infer_from_path(target)
            artist, album, title = artist or ia, album or ial, title or it

    # Explicit overrides always win.
    artist = args.artist or artist
    album = args.album or album
    title = args.title if args.title is not None else title
    return artist, album, title


# ---------- cache ----------

def load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_cache(cache: dict) -> None:
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=2)
    except OSError as e:
        print(f"  (couldn't write options cache: {e})")


# ---------- list ----------

def build_options(target: str, args) -> list[dict]:
    """Resolve a numbered list of cover options (with full-res URLs) for target."""
    token = load_discogs_token()
    if not token:
        print("ERROR: no Discogs token configured — see the skill doc.", file=sys.stderr)
        sys.exit(1)

    artist, album, title = derive_terms(target, args)
    if not artist or not (album or title):
        print("ERROR: couldn't work out an artist + album/title to search with.\n"
              "       Pass --artist / --album / --title explicitly.", file=sys.stderr)
        sys.exit(1)

    print(f"Searching Discogs for: {artist} / {album or '—'} / {title or '—'}\n")
    options = []
    for cand in search_discogs(artist, album, title, token)[:args.limit]:
        url, w, h = best_discogs_image(cand, token)
        if not url:
            continue
        options.append({
            "title": cand["title"],
            "year": cand["year"],
            "country": cand["country"],
            "format": cand["format"],
            "width": w,
            "height": h,
            "url": url,
        })
    return options


def cmd_list(target: str, args) -> None:
    options = build_options(target, args)
    if not options:
        print("No Discogs cover versions found. Try --artist/--album/--title overrides.")
        return

    for i, o in enumerate(options, 1):
        res = f"{o['width']}x{o['height']}" if o["width"] else "?"
        meta = " · ".join(p for p in (o["year"], o["country"], o["format"]) if p)
        print(f"[{i}] {o['title']}")
        print(f"     {meta}   ({res})")
        print(f"     {o['url']}\n")

    cache = load_cache()
    cache[os.path.abspath(target)] = options
    save_cache(cache)
    print(f"Open the URLs to compare, then: cover_picker.py set \"{target}\" <number>")


# ---------- set ----------

def cmd_set(target: str, number: int, args) -> None:
    abspath = os.path.abspath(target)
    options = load_cache().get(abspath)
    if not options:
        print("(no cached options for this target — re-running the search)")
        options = build_options(target, args)
        cache = load_cache()
        cache[abspath] = options
        save_cache(cache)

    if not options:
        print("ERROR: no cover options to choose from.", file=sys.stderr)
        sys.exit(1)
    if not 1 <= number <= len(options):
        print(f"ERROR: pick a number between 1 and {len(options)}.", file=sys.stderr)
        sys.exit(1)

    chosen = options[number - 1]
    print(f"Setting [{number}] {chosen['title']} ({chosen['width']}x{chosen['height']})")
    raw = download_image(chosen["url"])
    if not raw:
        print("ERROR: couldn't download the chosen image.", file=sys.stderr)
        sys.exit(1)
    jpg = normalize_to_jpeg(raw)

    targets = [target] if os.path.isfile(target) else [p for p, _ in iter_audio_files(target)]
    if not targets:
        print("ERROR: no audio files at the target.", file=sys.stderr)
        sys.exit(1)

    written_covers: set[str] = set()
    done = 0
    for path in targets:
        try:
            embed_picture(path, jpg)
        except Exception as e:
            print(f"  ✗ {os.path.basename(path)} — {e}")
            continue
        folder = os.path.dirname(path)
        if folder not in written_covers:
            with open(os.path.join(folder, "cover.jpg"), "wb") as f:
                f.write(jpg)
            written_covers.add(folder)
        done += 1
        print(f"  ✓ {os.path.relpath(path, os.path.dirname(abspath))}")

    print(f"\nDone — embedded into {done} file(s); wrote {len(written_covers)} cover.jpg.")


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(description="Pick a Discogs cover by hand.")
    sub = parser.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--artist", default=None)
    common.add_argument("--album", default=None)
    common.add_argument("--title", default=None)
    common.add_argument("--limit", type=int, default=8, help="Max versions to list.")

    p_list = sub.add_parser("list", parents=[common], help="List cover versions.")
    p_list.add_argument("target", help="Audio file or folder.")

    p_set = sub.add_parser("set", parents=[common], help="Embed a chosen version.")
    p_set.add_argument("target", help="Audio file or folder.")
    p_set.add_argument("number", type=int, help="Which version (from `list`).")

    args = parser.parse_args()
    target = os.path.expanduser(args.target)
    if not os.path.exists(target):
        print(f"ERROR: no such file or folder: {target}", file=sys.stderr)
        sys.exit(1)

    if args.cmd == "list":
        cmd_list(target, args)
    else:
        cmd_set(target, args.number, args)


if __name__ == "__main__":
    main()
