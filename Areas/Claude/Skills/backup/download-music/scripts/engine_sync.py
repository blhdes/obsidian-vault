#!/usr/bin/env python3
"""Check that the on-disk Library and the monthly library notes are in sync with
the Engine DJ collection.

Engine DJ keeps its collection in a SQLite database (`m.db`). Every track the user
imports lives in the `Track` table as a path relative to the Library
(`../Library/<Artist>/<Album>/<file>`). This script compares three things:

  1. Library on disk   — every audio file under ~/Music/Library/
  2. Engine collection — every row in Track (the m.db)
  3. The month note    — Areas/Mixing-DJing/Library/<month>-YYYY.md

and reports what's out of sync.

Gotchas it handles for you (the reasons doing this by hand is error-prone):
  * Accent normalization — macOS stores filenames decomposed (NFD: e + ´), Engine
    stores them composed (NFC: é). A naive string compare reports identical files
    as both "missing" and "broken". Everything here is NFC-normalized first.
  * Note path typos / deletions — the note sometimes records a folder under
    `<Artist>/Singles/...` when the file actually sits at `<Artist>/...`; deleted
    releases leave a dangling folder reference. Both are surfaced, not crashed on.
  * Intentional holdouts — low-quality / over-compressed tracks kept on disk but
    deliberately NOT imported. List them in `.engine_sync_ignore` (one path per
    line, prefix match) and they move out of the [A] warning into a quiet [D]
    count, so only GENUINE gaps raise the alarm.

Usage:
  engine_sync.py                  # whole-library check + the current month's note
  engine_sync.py june-2026        # whole-library check + the named month's note
  engine_sync.py --no-note        # whole-library check only
  engine_sync.py --show-excluded  # also list the ignore-listed holdouts

Exit status is 0 when every non-excluded Library file is in Engine (and no broken
refs), 1 otherwise — so it can gate a script if ever wanted.
"""
import sqlite3, unicodedata, os, re, sys, datetime

HOME      = os.path.expanduser("~")
ENGINE_DB = os.path.join(HOME, "Music", "Engine Library", "Database2", "m.db")
LIBRARY   = os.path.join(HOME, "Music", "Library")
NOTES_DIR = os.path.join(HOME, "Claude", "Obsidian", "Areas", "Mixing-DJing", "Library")
IGNORE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".engine_sync_ignore")
AUDIO_EXT = {".flac", ".mp3", ".wav", ".aif", ".aiff", ".m4a", ".alac", ".ogg", ".opus", ".aac"}


def nfc(s):
    return unicodedata.normalize("NFC", s)


def engine_tracks():
    """Return (library_rel_paths, other_paths, filetype_counts, total)."""
    if not os.path.exists(ENGINE_DB):
        sys.exit(f"Engine DB not found at {ENGINE_DB}\n"
                 f"(Is Engine DJ installed? The desktop collection lives there.)")
    con = sqlite3.connect(f"file:{ENGINE_DB}?mode=ro", uri=True)  # read-only, no locks
    lib, other, ftypes, total = set(), set(), {}, 0
    for path, ftype in con.execute("SELECT path, fileType FROM Track"):
        total += 1
        ftypes[ftype or "?"] = ftypes.get(ftype or "?", 0) + 1
        if path.startswith("../Library/"):
            lib.add(nfc(path.replace("../Library/", "", 1)))
        else:
            other.add(nfc(path))
    con.close()
    return lib, other, ftypes, total


def disk_files():
    out = set()
    for root, _, files in os.walk(LIBRARY):
        for f in files:
            if os.path.splitext(f)[1].lower() in AUDIO_EXT:
                out.add(nfc(os.path.relpath(os.path.join(root, f), LIBRARY)))
    return out


def load_ignore():
    """Library-relative path prefixes that are intentionally NOT in Engine."""
    pats = []
    if os.path.exists(IGNORE_FILE):
        for line in open(IGNORE_FILE, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#"):
                pats.append(nfc(line.rstrip("/")))
    return pats


def is_excluded(rel, pats):
    return any(rel == p or rel.startswith(p + "/") for p in pats)


def quality(rel):
    """Short codec/bitrate tag for a Library file, so low-quality stragglers stand out."""
    try:
        from mutagen import File as MFile
        info = MFile(os.path.join(LIBRARY, rel)).info
    except Exception:
        return ""
    ext = os.path.splitext(rel)[1].lower().lstrip(".")
    sr = int(getattr(info, "sample_rate", 0) or 0)
    if ext in ("flac", "wav", "aif", "aiff", "alac"):
        bits = getattr(info, "bits_per_sample", 0) or 0
        return f"{ext} {bits}/{sr // 1000}k" if bits and sr else f"{ext} lossless"
    br = int(getattr(info, "bitrate", 0) or 0)
    return f"{ext} {br // 1000}kbps" if br else ext


def check_note(month, eng_lib):
    note_path = os.path.join(NOTES_DIR, f"{month}.md")
    print(f"[C] Month note: {month}.md")
    if not os.path.exists(note_path):
        print(f"     not found at {note_path} — skipping")
        return
    text = open(note_path, encoding="utf-8").read()

    # stated totals line, e.g. "67 releases · 169 tracks · from 54 Soulseek uploaders"
    hdr = re.search(r"(\d+)\s*releases?\s*·\s*(\d+)\s*tracks", text)
    # the Releases (summary) table: sum its Tracks column (3rd col of each dated row)
    rows = re.findall(r"^\|\s*\d{2}-\d{2}\s*\|.*?\|\s*(\d+)\s*\|", text, re.M)
    tbl_rel, tbl_trk = len(rows), sum(int(x) for x in rows)

    if hdr:
        print(f"     header says   : {hdr.group(1)} releases · {hdr.group(2)} tracks")
    print(f"     summary table : {tbl_rel} releases · {tbl_trk} tracks")
    if hdr and (int(hdr.group(1)) != tbl_rel or int(hdr.group(2)) != tbl_trk):
        print(f"     ⚠ header total and summary table disagree — fix the totals line")

    # release folders referenced in the per-release provenance blockquotes
    folders = []
    for line in text.splitlines():
        if line.startswith(">"):
            folders += [nfc(x.rstrip("/")) for x in re.findall(r"`([^`]+/)`", line)]

    def resolve(fol):  # tolerate a stray 'Singles/' the note sometimes records
        for cand in (fol, fol.replace("/Singles/", "/")):
            if os.path.isdir(os.path.join(LIBRARY, cand)):
                return cand
        return None

    resolved = [(f, resolve(f)) for f in dict.fromkeys(folders)]  # de-dup, keep order
    unresolved = [f for f, r in resolved if r is None]

    month_files = set()
    for _, r in resolved:
        if r:
            d = os.path.join(LIBRARY, r)
            for x in os.listdir(d):
                if os.path.splitext(x)[1].lower() in AUDIO_EXT:
                    month_files.add(nfc(os.path.join(r, x)))

    print(f"     on disk       : {len(month_files)} audio files across "
          f"{sum(1 for _, r in resolved if r)} resolved folders")
    if unresolved:
        print(f"     ⚠ {len(unresolved)} note folder(s) not found on disk "
              f"(deleted release, or a path typo in the note):")
        for f in unresolved:
            print(f"        {f}")

    month_missing = sorted(month_files - eng_lib)
    if month_missing:
        print(f"     ⚠ this month's tracks NOT in Engine ({len(month_missing)}):")
        for p in month_missing:
            print(f"        {p}")
    else:
        print(f"     every resolved month track is in Engine ✅")

    print("     note: a month folder can hold files the note deliberately does not")
    print("     count (e.g. a YouTube grab — the note logs Soulseek pulls only), so")
    print("     the note's track number may sit 1–2 below the folder file count.")


def main():
    flags = [a for a in sys.argv[1:] if a.startswith("-")]
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    month = args[0] if args else datetime.date.today().strftime("%B-%Y").lower()

    eng_lib, eng_other, ftypes, total = engine_tracks()
    disk = disk_files()
    ignore = load_ignore()

    broken      = sorted(eng_lib - disk)                                  # in Engine, file gone/moved
    missing_all = sorted(disk - eng_lib)                                  # on disk, not imported
    missing     = [p for p in missing_all if not is_excluded(p, ignore)]  # genuine gaps
    excluded    = [p for p in missing_all if is_excluded(p, ignore)]      # intentional holdouts

    ft = ", ".join(f"{k} {v}" for k, v in sorted(ftypes.items(), key=lambda x: -x[1]))
    print(f"Engine collection : {total} tracks  ({ft})")
    print(f"Library on disk   : {len(disk)} audio files"
          + (f"  ({len(excluded)} intentionally excluded)" if excluded else ""))
    if eng_other:
        print(f"                    ({len(eng_other)} Engine tracks live outside "
              f"~/Music/Library — not checked here)")

    # Loud, leading verdict — based on GENUINE gaps + broken refs only. Ignore-listed
    # holdouts (low-quality on purpose) never raise the alarm; they get the quiet [D] count.
    if missing or broken:
        bits = []
        if missing:
            bits.append(f"{len(missing)} Library track(s) NOT in Engine")
        if broken:
            bits.append(f"{len(broken)} broken ref(s)")
        print(f"\n  ⚠ OUT OF SYNC — {' · '.join(bits)} — see [A]/[B] below.")
    else:
        tail = f" ({len(excluded)} intentionally excluded)" if excluded else ""
        print(f"\n  ✅ IN SYNC — every non-excluded Library file is in Engine.{tail}")
    print()

    print(f"[A] On disk, NOT in Engine, NOT excluded — genuine gaps to import ({len(missing)}):")
    for p in missing:
        q = quality(p)
        print(f"     {p}" + (f"   [{q}]" if q else ""))
    if not missing:
        print("     none — nothing unexpected is missing ✅")
    print()

    print(f"[B] In Engine but the file is missing on disk — broken refs ({len(broken)}):")
    for p in broken:
        print(f"     {p}")
    if not broken:
        print("     none ✅")
    print()

    print(f"[D] Intentionally excluded via .engine_sync_ignore ({len(excluded)}) — not flagged:")
    if "--show-excluded" in flags:
        for p in excluded:
            q = quality(p)
            print(f"     {p}" + (f"   [{q}]" if q else ""))
    elif excluded:
        folders = sorted({os.path.dirname(p) for p in excluded})
        print(f"     {len(excluded)} file(s) across {len(folders)} folder(s); "
              f"run --show-excluded to list. Remove a line from the ignore file when "
              f"you upgrade & import that release.")
    else:
        print("     none")
    # ignore lines that match nothing on disk anymore (release renamed/removed → stale)
    stale = [p for p in ignore if not any(d == p or d.startswith(p + "/") for d in disk)]
    if stale:
        print(f"     ⚠ {len(stale)} ignore line(s) match no file on disk (stale — clean up):")
        for p in stale:
            print(f"        {p}")
    print()

    if "--no-note" not in flags:
        check_note(month, eng_lib)

    sys.exit(0 if not missing and not broken else 1)


if __name__ == "__main__":
    main()
