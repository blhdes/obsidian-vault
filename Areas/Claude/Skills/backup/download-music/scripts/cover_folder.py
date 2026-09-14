#!/usr/bin/env python3
"""
Backfill cover art for every audio file in a folder (recursively).

For each audio file that has NO embedded cover art, find one and embed it.
Sources are tried in this order (the search/ranking logic is shared with
embed_cover.py — this script just drives it over a whole folder):

  0. A cover image already sitting in the track's own folder
       (cover/folder/front/album.*, or the sole image in the folder).
  1. Discogs            (only if a token is configured — see embed_cover.py).
  2. MusicBrainz + Cover Art Archive.
  3. iTunes Search API.

Files that ALREADY have embedded art are skipped, unless --overwrite is given.
A cover.jpg is also written into each track's folder so file-based players
(Mixxx, Finder previews) display the art too.

Artist / album / title come from each file's own tags; if those are missing,
they're inferred from the folder layout (<Artist>/<Album>/<Title>, with the
<Artist>/Singles/<Title>/ layout handled too).

Works across every format mutagen can open (MP3, FLAC, M4A/MP4, OGG Vorbis,
Opus, WAV/AIFF, ...).

Usage:
    cover_folder.py <folder> [--overwrite]
"""

import argparse
import base64
import io
import os
import sys

import mutagen
from mutagen.flac import FLAC, Picture
from mutagen.id3 import ID3, APIC
from mutagen.mp4 import MP4, MP4Cover
from mutagen.oggopus import OggOpus
from mutagen.oggvorbis import OggVorbis
from PIL import Image

# Shared search + normalisation logic (same directory).
from embed_cover import find_cover, normalize_to_jpeg

# Skip obvious non-audio files fast, before paying for a mutagen probe.
SKIP_EXTS = {
    ".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".pdf", ".txt", ".md",
    ".nfo", ".cue", ".log", ".m3u", ".m3u8", ".db", ".ini", ".ds_store",
    ".json", ".xml", ".html", ".zip", ".rar",
}


# ---------- reading existing state ----------

def has_embedded_art(audio: mutagen.FileType) -> bool:
    """True if the file already carries embedded cover art."""
    if isinstance(audio, FLAC):
        return len(audio.pictures) > 0
    if isinstance(audio, MP4):
        return bool(audio.tags and audio.tags.get("covr"))
    if isinstance(audio, (OggVorbis, OggOpus)):
        tags = audio.tags
        return bool(tags and (tags.get("metadata_block_picture") or tags.get("coverart")))
    # ID3-based (MP3, WAV, AIFF, ...).
    tags = getattr(audio, "tags", None)
    if tags is None:
        return False
    try:
        return len(tags.getall("APIC")) > 0
    except AttributeError:
        return any(str(k).startswith("APIC") for k in tags.keys())


def read_meta(path: str) -> tuple[str | None, str | None, str | None]:
    """Return (artist, album, title) from the file's tags, or Nones."""
    try:
        audio = mutagen.File(path, easy=True)
    except Exception:
        audio = None
    if audio is None or audio.tags is None:
        return None, None, None

    def first(*keys: str) -> str | None:
        for key in keys:
            val = audio.tags.get(key)
            if val:
                text = str(val[0]).strip()
                if text:
                    return text
        return None

    return first("artist", "albumartist"), first("album"), first("title")


def infer_from_path(path: str) -> tuple[str | None, str | None, str | None]:
    """Best-effort artist/album/title from the folder layout when tags are missing.

    Handles both  <Artist>/<Album>/<Title>.ext  and
                  <Artist>/Singles/<Title>/<Title>.ext.
    """
    stem = os.path.splitext(os.path.basename(path))[0]
    folder = os.path.dirname(path)
    album = os.path.basename(folder) or None
    artist = os.path.basename(os.path.dirname(folder)) or None

    # Single: track sits in its own folder named after the song.
    if album and album.lower() == stem.lower():
        album = None
    # ...inside a Singles/ bucket, so the real artist is one level higher.
    if artist and artist.lower() == "singles":
        artist = os.path.basename(os.path.dirname(os.path.dirname(folder))) or None

    return artist, album, stem


# ---------- embedding (format dispatch) ----------

def _flac_picture(jpg_bytes: bytes) -> Picture:
    pic = Picture()
    pic.type = 3          # front cover
    pic.mime = "image/jpeg"
    pic.desc = "Cover"
    pic.depth = 24
    try:
        pic.width, pic.height = Image.open(io.BytesIO(jpg_bytes)).size
    except (OSError, ValueError):
        pass
    pic.data = jpg_bytes
    return pic


def embed_picture(path: str, jpg_bytes: bytes) -> None:
    """Embed JPEG cover art into an audio file of any mutagen-supported type."""
    audio = mutagen.File(path)
    if audio is None:
        raise ValueError(f"unsupported file: {path}")

    if isinstance(audio, FLAC):
        audio.clear_pictures()
        audio.add_picture(_flac_picture(jpg_bytes))
        audio.save()
        return

    if isinstance(audio, MP4):
        if audio.tags is None:
            audio.add_tags()
        audio.tags["covr"] = [MP4Cover(jpg_bytes, imageformat=MP4Cover.FORMAT_JPEG)]
        audio.save()
        return

    if isinstance(audio, (OggVorbis, OggOpus)):
        b64 = base64.b64encode(_flac_picture(jpg_bytes).write()).decode("ascii")
        audio["metadata_block_picture"] = [b64]
        audio.save()
        return

    # ID3-based (MP3, WAV, AIFF, ...): drive it through the file's own tags.
    if audio.tags is None:
        audio.add_tags()
    tags = audio.tags
    if isinstance(tags, ID3):
        tags.delall("APIC")
        tags.add(APIC(encoding=3, mime="image/jpeg", type=3, desc="Cover", data=jpg_bytes))
        audio.save()
        return

    raise ValueError(f"don't know how to embed art into {type(audio).__name__}: {path}")


# ---------- walk ----------

def iter_audio_files(root: str):
    """Yield (path, mutagen_object) for every real audio file under root."""
    for dirpath, _dirs, files in os.walk(root):
        for name in sorted(files):
            if name.startswith("."):
                continue
            if os.path.splitext(name)[1].lower() in SKIP_EXTS:
                continue
            path = os.path.join(dirpath, name)
            try:
                audio = mutagen.File(path)
            except Exception:
                audio = None
            if audio is None or getattr(audio, "info", None) is None:
                continue  # not an audio stream mutagen understands
            yield path, audio


# ---------- main ----------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Backfill embedded cover art for every audio file in a folder."
    )
    parser.add_argument("folder", help="Folder to scan (recurses into subfolders).")
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-fetch and replace art even on files that already have it.",
    )
    args = parser.parse_args()

    root = os.path.abspath(os.path.expanduser(args.folder))
    if not os.path.isdir(root):
        print(f"ERROR: not a folder: {root}", file=sys.stderr)
        sys.exit(1)

    embedded = skipped = failed = 0
    failures: list[tuple[str, str]] = []

    for path, audio in iter_audio_files(root):
        rel = os.path.relpath(path, root)

        if not args.overwrite and has_embedded_art(audio):
            print(f"• {rel} — already has art, skipping")
            skipped += 1
            continue

        artist, album, title = read_meta(path)
        if not (artist and title):
            ia, ial, it = infer_from_path(path)
            artist, album, title = artist or ia, album or ial, title or it
        if not (artist and title):
            print(f"✗ {rel} — no artist/title to search with")
            failed += 1
            failures.append((rel, "missing metadata"))
            continue

        print(f"→ {rel}  ({artist} / {album or '—'} / {title})")
        result = find_cover(artist, title, album, path, None)
        if not result:
            print(f"✗ {rel} — no cover found from any source")
            failed += 1
            failures.append((rel, "no cover found"))
            continue

        raw, source = result
        try:
            jpg = normalize_to_jpeg(raw)
            embed_picture(path, jpg)
            with open(os.path.join(os.path.dirname(path), "cover.jpg"), "wb") as f:
                f.write(jpg)
        except Exception as e:
            print(f"✗ {rel} — embed failed: {e}")
            failed += 1
            failures.append((rel, f"embed failed: {e}"))
            continue

        print(f"  ✓ embedded ({source})")
        embedded += 1

    print("\n=== Summary ===")
    print(f"  embedded:                  {embedded}")
    print(f"  already had art (skipped): {skipped}")
    print(f"  failed:                    {failed}")
    for rel, why in failures:
        print(f"    - {rel}: {why}")

    if failed and embedded == 0 and skipped == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
