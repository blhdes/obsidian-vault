#!/usr/bin/env python3
"""
Fetch album art and embed it into an MP3.

Sources tried, in order, until one returns a valid image:
  0. Existing cover image already in the destination folder.
       - Matches common cover filenames (cover/folder/front/album.*) or the
         sole image file in the folder, case-insensitively.
       - Lets multi-track album downloads reuse the cover fetched for track 1
         instead of re-querying the network for every subsequent track.
       - Safe for singles too: each single lives in its own subfolder, so
         there's no shared cover that could leak between unrelated tracks.
  1. Discogs (only when a token is configured — see load_discogs_token).
       - Searches releases by artist + album + track, retries without the
         album filter if needed, and skips Discogs' "spacer" placeholder image.
  2. MusicBrainz + Cover Art Archive
       - Retries without the album filter if the album-filtered query returns 0.
       - Ranks candidate releases (Album/EP/Single > Compilation, skips DJ-mix
         entirely, prefers releases whose title fuzzy-matches the album hint,
         prefers earlier release dates as a tiebreaker).
       - Iterates through every ranked release, not just the first — works
         around CAA/archive.org occasionally 500ing on individual image files
         even when the JSON metadata says art exists.
       - Validates each download (Content-Length match + Pillow decode) so a
         silently-truncated response doesn't get embedded.
  3. iTunes Search API
       - Fallback for new releases not yet indexed on MusicBrainz.
       - Rewrites the thumbnail URL (`100x100bb.jpg`) to `3000x3000bb.jpg`
         to get the original high-res cover.
  4. YouTube thumbnail (only when --youtube-url is passed).
       - Last resort for obscure/niche releases that aren't on MB or iTunes.
       - YouTube Music thumbnails are 1280x720 with the square cover centered
         on grey letterbox bars — we auto-crop to the center square.

PNG covers are converted to JPEG so they embed cleanly into ID3v2 APIC frames.
A `cover.jpg` is also saved next to the MP3 (some players like Mixxx need that to display art).

Usage:
    embed_cover.py <artist> <title> <mp3_path> [album] [--youtube-url URL]
"""

import argparse
import io
import os
import re
import subprocess
import sys
import tempfile
import time

import requests
from mutagen.id3 import ID3, APIC
from mutagen.id3 import error as ID3Error
from PIL import Image

MB_API = "https://musicbrainz.org/ws/2"
CAA_API = "https://coverartarchive.org"
ITUNES_API = "https://itunes.apple.com/search"
DISCOGS_API = "https://api.discogs.com/database/search"
HEADERS = {"User-Agent": "embed-cover-script/2.0 (agomezurrea@gmail.com)"}
TIMEOUT = 30
MAX_CANDIDATES = 10  # how many ranked MB releases to try before giving up

# Where a Discogs personal access token may live (env var wins over the file).
DISCOGS_TOKEN_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".discogs_token")

# Folder-cover detection (source 0).
IMAGE_EXTS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")
COMMON_COVER_NAMES = ("cover", "folder", "front", "album", "albumart", "albumartsmall")


# ---------- MusicBrainz ----------

def mb_search_recordings(artist: str, title: str, album: str | None) -> list[dict]:
    """Query MusicBrainz. Falls back to no-album search if filtered query is empty."""
    def _query(q: str) -> list[dict]:
        resp = requests.get(
            f"{MB_API}/recording",
            params={"query": q, "fmt": "json", "limit": 25},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json().get("recordings", [])

    base = f'recording:"{title}" AND artist:"{artist}"'
    if album:
        results = _query(f'{base} AND release:"{album}"')
        if results:
            return results
        print(f"  (no MB results with album:'{album}', retrying without album filter)")
    return _query(base)


def rank_mb_releases(
    recordings: list[dict],
    album_hint: str | None,
) -> list[tuple[str, str]]:
    """Return [(release_title, mbid), ...] ordered by 'most canonical' first.

    Scoring (higher = better):
      +100  not a Compilation
      +50   release title contains album_hint (case-insensitive)
      +20   primary type is Album/EP/Single
    Tiebreaker: earliest release date.
    DJ-mix releases are skipped entirely (whole-set mixes — never the canonical art).
    """
    seen: set[str] = set()
    scored: list[tuple[int, str, str, str]] = []  # (score, date, title, mbid)
    hint = (album_hint or "").lower().strip()

    for rec in recordings:
        for rel in rec.get("releases", []):
            mbid = rel.get("id")
            if not mbid or mbid in seen:
                continue
            seen.add(mbid)

            rg = rel.get("release-group") or {}
            primary = rg.get("primary-type") or ""
            secondary = set(rg.get("secondary-types") or [])
            if "DJ-mix" in secondary:
                continue

            score = 0
            if "Compilation" not in secondary:
                score += 100
            if hint and hint in (rel.get("title") or "").lower():
                score += 50
            if primary in {"Album", "EP", "Single"}:
                score += 20

            date = rel.get("date") or "9999"
            scored.append((score, date, rel.get("title") or "?", mbid))

    scored.sort(key=lambda r: (-r[0], r[1]))
    return [(title, mbid) for _, _, title, mbid in scored]


def fetch_caa_image(mbid: str) -> bytes | None:
    """Fetch front cover for a release MBID. Returns validated image bytes or None."""
    try:
        meta = requests.get(
            f"{CAA_API}/release/{mbid}", headers=HEADERS, timeout=TIMEOUT
        )
    except requests.RequestException:
        return None
    if meta.status_code != 200:
        return None
    try:
        images = meta.json().get("images", [])
    except ValueError:
        return None
    front = next((img for img in images if img.get("front")), images[0] if images else None)
    if not front:
        return None
    return download_image(front["image"])


# ---------- iTunes ----------

def search_itunes(artist: str, album: str | None, title: str | None) -> str | None:
    """Return a high-res cover URL via iTunes Search API, or None."""
    term = " ".join(t for t in (artist, album, title) if t)
    try:
        resp = requests.get(
            ITUNES_API,
            params={"term": term, "entity": "album", "limit": 5},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        results = resp.json().get("results", [])
    except (requests.RequestException, ValueError):
        return None

    artist_lower = artist.lower()
    candidates = [r for r in results if r.get("artistName", "").lower() == artist_lower]
    if not candidates and results:
        candidates = results  # loose match if artist string differs

    for r in candidates:
        url = r.get("artworkUrl100")
        if not url:
            continue
        # Swap the thumbnail size for max-res original
        return re.sub(r"/\d+x\d+bb\.(jpg|png)$", "/3000x3000bb.jpg", url)
    return None


# ---------- Discogs ----------

def load_discogs_token() -> str | None:
    """Return a Discogs personal access token from $DISCOGS_TOKEN or the token file."""
    env = os.environ.get("DISCOGS_TOKEN")
    if env and env.strip():
        return env.strip()
    if os.path.exists(DISCOGS_TOKEN_FILE):
        try:
            with open(DISCOGS_TOKEN_FILE) as f:
                token = f.read().strip()
            return token or None
        except OSError:
            return None
    return None


def discogs_get(url: str, token: str, params: dict | None = None) -> dict | None:
    """GET a Discogs API URL with auth, retrying once on rate-limit (HTTP 429)."""
    query = {"token": token, **(params or {})}
    for attempt in range(2):
        try:
            resp = requests.get(url, params=query, headers=HEADERS, timeout=TIMEOUT)
        except requests.RequestException as e:
            print(f"    Discogs request failed: {e}")
            return None
        if resp.status_code == 429 and attempt == 0:
            wait = min(int(resp.headers.get("Retry-After", 5) or 5), 60)
            print(f"    Discogs rate-limited, waiting {wait}s...")
            time.sleep(wait)
            continue
        if resp.status_code != 200:
            print(f"    Discogs HTTP {resp.status_code}")
            return None
        try:
            return resp.json()
        except ValueError:
            return None
    return None


def search_discogs(artist: str, album: str | None, title: str | None, token: str) -> list[dict]:
    """Return candidate Discogs releases, best-matching first.

    Each dict carries enough to display *and* resolve full-res art later:
    {title, year, country, format, resource_url, cover_image, thumb, match,
     genre, style}.
    """
    def _params(use_album: bool) -> dict:
        p = {"type": "release", "artist": artist, "per_page": 15}
        if title:
            p["track"] = title
        if album and use_album:
            p["release_title"] = album
        return p

    data = discogs_get(DISCOGS_API, token, _params(use_album=True))
    results = (data or {}).get("results", [])
    if not results and album:
        print(f"  (no Discogs results with album:'{album}', retrying without it)")
        data = discogs_get(DISCOGS_API, token, _params(use_album=False))
        results = (data or {}).get("results", [])

    hint = (album or "").lower().strip()

    def matches(r: dict) -> bool:
        return bool(hint and hint in (r.get("title") or "").lower())

    candidates: list[dict] = []
    for r in sorted(results, key=matches, reverse=True):
        cover = r.get("cover_image") or r.get("thumb") or ""
        if "spacer.gif" in cover:  # Discogs' "no art" placeholder
            continue
        fmt = r.get("format") or []
        candidates.append({
            "title": r.get("title") or "?",
            "year": r.get("year") or "",
            "country": r.get("country") or "",
            "format": ", ".join(fmt) if isinstance(fmt, list) else str(fmt),
            "resource_url": r.get("resource_url") or "",
            "cover_image": cover,
            "thumb": r.get("thumb") or "",
            "match": matches(r),
            "genre": r.get("genre") or [],
            "style": r.get("style") or [],
        })
    return candidates


def discogs_release_images(resource_url: str, token: str) -> list[dict]:
    """A release's images as [{uri, width, height, primary}], largest first."""
    if not resource_url:
        return []
    data = discogs_get(resource_url, token)
    out = []
    for img in (data or {}).get("images") or []:
        uri = img.get("uri")
        if not uri or "spacer.gif" in uri:
            continue
        out.append({
            "uri": uri,
            "width": img.get("width") or 0,
            "height": img.get("height") or 0,
            "primary": img.get("type") == "primary",
        })
    out.sort(key=lambda i: (i["primary"], i["width"] * i["height"]), reverse=True)
    return out


def best_discogs_image(candidate: dict, token: str) -> tuple[str, int, int]:
    """Resolve a candidate's highest-resolution image URL.

    Falls back to the medium search 'cover_image' if the release detail has no
    images. Returns (url, width, height); width/height are 0 when unknown.
    """
    images = discogs_release_images(candidate.get("resource_url", ""), token)
    if images:
        top = images[0]
        return top["uri"], top["width"], top["height"]
    return candidate.get("cover_image", ""), 0, 0


def fetch_discogs_image(artist: str, title: str | None, album: str | None, token: str) -> bytes | None:
    """Return the highest-resolution Discogs cover bytes, or None.

    Resolves the full-size original for the best-matching releases (capped to a
    handful of API calls) and prefers album matches, then the largest image.
    """
    resolved: list[tuple[bool, int, str]] = []
    for cand in search_discogs(artist, album, title, token)[:5]:
        url, w, h = best_discogs_image(cand, token)
        if url:
            resolved.append((bool(cand.get("match")), w * h, url))

    resolved.sort(key=lambda r: (r[0], r[1]), reverse=True)
    for _match, _area, url in resolved:
        data = download_image(url)
        if data:
            return data
    return None


# ---------- YouTube thumbnail ----------

def fetch_youtube_thumbnail(url: str) -> bytes | None:
    """Download YT thumbnail via yt-dlp, auto-crop letterbox to center square, return JPEG bytes."""
    with tempfile.TemporaryDirectory() as tmp:
        out_pattern = os.path.join(tmp, "thumb.%(ext)s")
        try:
            subprocess.run(
                ["yt-dlp", "--write-thumbnail", "--skip-download",
                 "--convert-thumbnails", "jpg", "-o", out_pattern, url],
                check=True, capture_output=True, timeout=60,
            )
        except (subprocess.SubprocessError, subprocess.TimeoutExpired) as e:
            print(f"    yt-dlp failed: {e}")
            return None

        jpgs = [f for f in os.listdir(tmp) if f.endswith(".jpg")]
        if not jpgs:
            print("    no thumbnail file produced")
            return None
        with open(os.path.join(tmp, jpgs[0]), "rb") as f:
            data = f.read()

    # YouTube Music thumbnails are 1280x720 with the square cover centered.
    # Crop to the smaller dimension so we keep just the art.
    img = Image.open(io.BytesIO(data))
    w, h = img.size
    if w != h:
        side = min(w, h)
        left = (w - side) // 2
        top = (h - side) // 2
        img = img.crop((left, top, left + side, top + side))
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=95)
    return buf.getvalue()


# ---------- Existing cover.jpg reuse ----------

def _read_valid_image(path: str) -> bytes | None:
    """Read an image file and confirm Pillow can decode it. Returns bytes or None."""
    try:
        with open(path, "rb") as f:
            data = f.read()
        Image.open(io.BytesIO(data)).load()
    except (OSError, ValueError):
        return None
    return data


def load_existing_folder_cover(mp3_path: str) -> bytes | None:
    """Return bytes of a cover image already sitting in the track's folder, or None.

    Looks for a common cover filename (cover/folder/front/album.*) first, then
    falls back to the sole image file if the folder contains exactly one.
    """
    folder = os.path.dirname(mp3_path)
    if not folder or not os.path.isdir(folder):
        return None
    try:
        names = os.listdir(folder)
    except OSError:
        return None

    images = [n for n in names
              if os.path.isfile(os.path.join(folder, n))
              and os.path.splitext(n)[1].lower() in IMAGE_EXTS]

    # 1. Prioritised common cover filenames (case-insensitive).
    for base in COMMON_COVER_NAMES:
        for name in images:
            if os.path.splitext(name)[0].lower() == base:
                data = _read_valid_image(os.path.join(folder, name))
                if data:
                    return data

    # 2. Sole image in the folder — almost always the release's art.
    if len(images) == 1:
        return _read_valid_image(os.path.join(folder, images[0]))

    return None


# ---------- Download + validate ----------

def download_image(url: str) -> bytes | None:
    """Download an image and verify it's complete. Returns bytes or None."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except requests.RequestException as e:
        print(f"    download failed: {e}")
        return None
    if resp.status_code != 200:
        print(f"    HTTP {resp.status_code}")
        return None

    data = resp.content
    cl = resp.headers.get("Content-Length")
    if cl and len(data) != int(cl):
        print(f"    truncated: got {len(data)}, expected {cl}")
        return None

    # Catches missing JPEG EOI markers, partial PNGs, etc. — verify() only
    # checks the header, so we use load() which actually decodes pixels.
    try:
        Image.open(io.BytesIO(data)).load()
    except (OSError, ValueError) as e:
        print(f"    decode failed: {e}")
        return None
    return data


# ---------- Embed ----------

def normalize_to_jpeg(data: bytes) -> bytes:
    """Convert any input (PNG, etc.) to JPEG so ID3 APIC stays consistent."""
    img = Image.open(io.BytesIO(data))
    if img.format == "JPEG":
        return data
    img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=95)
    return buf.getvalue()


def embed_cover(mp3_path: str, jpg_data: bytes) -> None:
    # Dispatch on the file's real format — writing ID3 onto a FLAC/M4A/OGG
    # prepends a junk ID3 header instead of setting its native picture block.
    from cover_folder import embed_picture

    embed_picture(mp3_path, jpg_data)
    print(f"Embedded into: {mp3_path}")

    cover_path = os.path.join(os.path.dirname(mp3_path), "cover.jpg")
    with open(cover_path, "wb") as f:
        f.write(jpg_data)
    print(f"cover.jpg saved to: {cover_path}")


# ---------- Orchestration ----------

def find_cover(
    artist: str,
    title: str,
    album: str | None,
    mp3_path: str,
    youtube_url: str | None,
) -> tuple[bytes, str] | None:
    """Returns (image_bytes, source_label) or None."""
    existing = load_existing_folder_cover(mp3_path)
    if existing:
        return existing, "existing cover image in folder"

    token = load_discogs_token()
    if token:
        print(f"[Discogs] searching '{title}' by '{artist}'...")
        data = fetch_discogs_image(artist, title, album, token)
        if data:
            return data, "Discogs"
        print("  no Discogs match")

    print(f"[MusicBrainz] searching '{title}' by '{artist}'...")
    try:
        recordings = mb_search_recordings(artist, title, album)
    except requests.RequestException as e:
        print(f"  MusicBrainz request failed: {e}")
        recordings = []

    if recordings:
        ranked = rank_mb_releases(recordings, album)
        print(f"  {len(ranked)} candidate release(s)")
        for rel_title, mbid in ranked[:MAX_CANDIDATES]:
            data = fetch_caa_image(mbid)
            if data:
                return data, f"MusicBrainz / '{rel_title}' ({mbid})"
            print(f"  ✗ '{rel_title}' — no usable art")
    else:
        print("  no MusicBrainz results")

    print("[iTunes] falling back to iTunes Search...")
    url = search_itunes(artist, album, title)
    if url:
        data = download_image(url)
        if data:
            return data, f"iTunes / {url}"
    print("  no iTunes match")

    if youtube_url:
        print(f"[YouTube] last-resort thumbnail fallback from {youtube_url}...")
        data = fetch_youtube_thumbnail(youtube_url)
        if data:
            return data, f"YouTube thumbnail (auto-cropped) / {youtube_url}"
        print("  no usable YouTube thumbnail")

    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch album cover art and embed it into an MP3."
    )
    parser.add_argument("artist")
    parser.add_argument("title")
    parser.add_argument("mp3_path")
    parser.add_argument("album", nargs="?", default=None)
    parser.add_argument(
        "--youtube-url",
        help="YouTube URL to use as a last-resort thumbnail source if MB and iTunes both miss.",
    )
    args = parser.parse_args()

    result = find_cover(args.artist, args.title, args.album, args.mp3_path, args.youtube_url)
    if not result:
        print("ERROR: no cover art found from any source", file=sys.stderr)
        sys.exit(1)

    raw_data, source = result
    print(f"Source: {source}")
    jpg_data = normalize_to_jpeg(raw_data)
    embed_cover(args.mp3_path, jpg_data)


if __name__ == "__main__":
    main()
