#!/usr/bin/env python3
"""Move the whole on-disk Library to an external SSD and free up local space.

This is the *last phase* of the music pipeline. Everything before it is unchanged:
download with Soulseek -> clean tags/covers -> move the release into
`~/Music/Library/` -> import into Engine DJ. This script is the step you run
**only when you say so**: it flushes everything currently in `~/Music/Library/`
onto an external SSD and deletes the local copies, so the internal disk gets its
space back.

It is built to be run again and again, not just once. The Library *folder* itself
is kept (only its contents move), so new Soulseek imports keep landing in
`~/Music/Library/` exactly as before, and the next time the disk fills up you run
this again to flush them onto the SSD too. A re-run just merges the new releases
into the SSD library.

How it stays safe (it deletes local files, so safety IS the point):

  * Dry-run by default. It only previews and counts. Nothing is copied or deleted
    until you add `--apply` (same convention as `fix_metadata.py`).
  * It refuses to run unless the destination is a *real external drive*: the
    target volume must be mounted AND sit on a different physical disk than the
    source. This is the macOS data-loss trap it guards against -- if the SSD isn't
    plugged in, `/Volumes/<name>` can silently be an ordinary folder on the
    internal disk, and a naive "move" would copy your library a few millimetres to
    the left and then delete the original. The different-disk check makes that
    impossible.
  * Copy -> verify -> delete, one file at a time. Each file is copied, then the
    copy on the SSD is re-read and its SHA-256 checksum compared to the original.
    The local original is deleted **only** after its copy is proven
    byte-identical. A mismatch leaves both files untouched and is reported.
  * Resumable & repeatable. If a file is already on the SSD (same size, same
    checksum), the copy is skipped and only the local original is removed -- so a
    re-run after an interruption picks up where it left off.
  * Everything moves, not just audio. `cover.jpg`, vinyl-rip lineage `.txt` /
    `.nfo` files and sleeve scans travel with their release.

Engine DJ -- READ THIS: Engine DJ stores each track as a path *relative to the
internal disk* (`../Library/<Artist>/...`). Once the files live on the SSD, Engine
will show them as missing/relocated until you point Engine at the new location
(add the SSD as a drive in Engine DJ, or relink the collection). This script does
NOT touch the Engine database -- it only moves files -- so re-linking Engine is a
separate, manual step. The script prints a reminder when it finishes.

Usage:
  port_library.py /Volumes/<SSD>                 # dry-run preview (default)
  port_library.py /Volumes/<SSD> --apply         # actually move + delete locals
  port_library.py /Volumes/<SSD> --no-verify     # size-only, no checksum (faster, less safe)
  port_library.py --target /Volumes/<SSD>/MyPath # custom destination folder
                                                 #   (default: <SSD>/Music/Library)
"""
import argparse
import hashlib
import os
import shutil
import sys

HOME = os.path.expanduser("~")
SOURCE = os.path.join(HOME, "Music", "Library")   # what we flush onto the SSD
CHUNK = 1024 * 1024                                # 1 MiB read/write blocks
SKIP_NAMES = {".DS_Store"}                         # macOS junk: never copied


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------
def human(n):
    """Bytes -> a short human string, e.g. 9.9 GB."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def mount_point_of(path):
    """The volume `path` lives on (walks up to the nearest real mount point)."""
    p = os.path.abspath(path)
    while p != "/" and not os.path.ismount(p):
        p = os.path.dirname(p)
    return p


# ---------------------------------------------------------------------------
# the destination must be a genuine external drive
# ---------------------------------------------------------------------------
def resolve_target(args):
    """Return (target_dir, volume_mount). Exits with a clear message if the
    destination isn't a real, mounted, *different-disk* external drive."""
    if args.target:
        target = os.path.abspath(args.target)
    elif args.volume:
        target = os.path.join(os.path.abspath(args.volume), "Music", "Library")
    else:
        sys.exit("Give the SSD to move to, e.g.:\n"
                 "  port_library.py /Volumes/<SSD>            (dry-run preview)\n"
                 "  port_library.py /Volumes/<SSD> --apply    (move for real)")

    volume = mount_point_of(target)

    if volume == "/":
        sys.exit(f"Refusing: '{target}' resolves to the boot disk, not an external "
                 f"drive.\nPlug in the SSD and pass its /Volumes/<name> path.")

    if not os.path.exists(volume):
        sys.exit(f"Refusing: the volume '{volume}' does not exist. Is the SSD "
                 f"plugged in and mounted?")

    # The decisive check: source and destination must be on DIFFERENT physical
    # disks. If they share a device, the "external" path is really a folder on the
    # internal disk (drive not mounted) -- moving there then deleting the source
    # would destroy data. Better to stop now.
    if os.stat(SOURCE).st_dev == os.stat(volume).st_dev:
        sys.exit(f"Refusing: '{volume}' is on the SAME disk as your Library.\n"
                 f"That means the SSD isn't actually mounted there -- if I moved "
                 f"files now and deleted the originals, you'd lose them.\n"
                 f"Plug the SSD in, confirm it shows under /Volumes/, and retry.")

    return target, volume


# ---------------------------------------------------------------------------
# scan: figure out what each file's fate is, without touching anything
# ---------------------------------------------------------------------------
def scan(target, verify):
    """Walk the source Library and bucket every file. Returns four lists of
    (src, dst, size) tuples: to_move, already (identical copy on SSD), conflict
    (different file already at dst), plus the running byte totals."""
    to_move, already, conflict = [], [], []
    for root, _, files in os.walk(SOURCE):
        for name in files:
            if name in SKIP_NAMES:
                continue
            src = os.path.join(root, name)
            rel = os.path.relpath(src, SOURCE)
            dst = os.path.join(target, rel)
            size = os.path.getsize(src)

            if not os.path.exists(dst):
                to_move.append((src, dst, size))
            elif os.path.getsize(dst) == size and (not verify or sha256(src) == sha256(dst)):
                already.append((src, dst, size))   # safe to just delete the local copy
            else:
                conflict.append((src, dst, size))  # a DIFFERENT file is already there
    return to_move, already, conflict


# ---------------------------------------------------------------------------
# the actual move: copy -> verify -> delete, per file
# ---------------------------------------------------------------------------
def copy_verify_delete(src, dst, verify):
    """Copy src to dst, prove the copy is intact, then delete src.
    Returns True on success. On any doubt the local original is kept."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)

    h = hashlib.sha256()
    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
        for chunk in iter(lambda: fsrc.read(CHUNK), b""):
            h.update(chunk)
            fdst.write(chunk)
    shutil.copystat(src, dst)   # keep the original mod.time / permissions

    ok = os.path.getsize(dst) == os.path.getsize(src)
    if ok and verify:
        ok = sha256(dst) == h.hexdigest()

    if not ok:
        # the copy is bad -- throw IT away, never the original
        try:
            os.remove(dst)
        except OSError:
            pass
        return False

    os.remove(src)   # original is now safely on the SSD
    return True


def prune_empty_dirs(root):
    """Remove empty subfolders left behind (the Library root itself is kept, so
    new Soulseek imports still have somewhere to land). A folder holding only a
    `.DS_Store` counts as empty."""
    removed = 0
    for dirpath, _, _ in os.walk(root, topdown=False):
        if os.path.abspath(dirpath) == os.path.abspath(root):
            continue
        entries = os.listdir(dirpath)
        if all(e in SKIP_NAMES for e in entries):
            for e in entries:
                os.remove(os.path.join(dirpath, e))
            os.rmdir(dirpath)
            removed += 1
    return removed


# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Move ~/Music/Library to an external SSD and free local space.")
    ap.add_argument("volume", nargs="?",
                    help="the SSD mount, e.g. /Volumes/<SSD> "
                         "(library goes to <SSD>/Music/Library)")
    ap.add_argument("--target", help="custom destination folder (overrides <volume>/Music/Library)")
    ap.add_argument("--apply", action="store_true",
                    help="actually move + delete locals (default is a dry-run preview)")
    ap.add_argument("--no-verify", action="store_true",
                    help="skip the checksum and compare sizes only (faster, less safe)")
    args = ap.parse_args()
    verify = not args.no_verify

    if not os.path.isdir(SOURCE):
        sys.exit(f"No Library found at {SOURCE} -- nothing to move.")

    target, volume = resolve_target(args)
    to_move, already, conflict = scan(target, verify)

    move_bytes = sum(s for _, _, s in to_move)
    free = shutil.disk_usage(volume).free

    print(f"Source : {SOURCE}")
    print(f"Target : {target}   (volume {volume})")
    print(f"Verify : {'SHA-256 checksum' if verify else 'size only (--no-verify)'}")
    print()
    print(f"  to move        : {len(to_move):>4} files   {human(move_bytes)}")
    print(f"  already on SSD : {len(already):>4} files   (local copy will be removed)")
    print(f"  conflicts      : {len(conflict):>4} files   (different file already on SSD -- skipped)")
    print(f"  SSD free space : {human(free)}")
    print()

    if conflict:
        print("⚠ Conflicts (a DIFFERENT file already exists at the destination -- left untouched):")
        for src, dst, _ in conflict:
            print(f"     {os.path.relpath(src, SOURCE)}")
        print()

    if move_bytes > free:
        sys.exit(f"⚠ Not enough room on the SSD: need {human(move_bytes)}, "
                 f"have {human(free)}. Free some space and retry.")

    if not args.apply:
        print("DRY-RUN -- nothing was changed. Re-run with --apply to move for real.")
        _engine_reminder()
        return

    # --- apply ---------------------------------------------------------------
    print("Moving...")
    total = len(to_move) + len(already)
    done = failed = 0
    for src, dst, _ in already:
        os.remove(src)               # verified-identical copy already on SSD
        done += 1
    for i, (src, dst, _) in enumerate(to_move, 1):
        rel = os.path.relpath(src, SOURCE)
        if copy_verify_delete(src, dst, verify):
            done += 1
            print(f"  [{i}/{len(to_move)}] {rel}")
        else:
            failed += 1
            print(f"  [{i}/{len(to_move)}] ✗ VERIFY FAILED, kept local: {rel}")

    pruned = prune_empty_dirs(SOURCE)

    print()
    print(f"Done. {done}/{total} files now on the SSD, {failed} kept local (verify failed), "
          f"{len(conflict)} conflicts skipped.")
    print(f"Removed {pruned} empty folder(s). The Library root {SOURCE} is kept for "
          f"future imports.")
    if failed or conflict:
        print("⚠ Some files were NOT moved -- see above. Nothing was lost; re-run after "
              "investigating.")
    _engine_reminder()


def _engine_reminder():
    print()
    print("── Engine DJ ──────────────────────────────────────────────────────────")
    print("Engine DJ points at the INTERNAL disk (../Library/...). After this move it")
    print("will show those tracks as missing until you point Engine at the SSD")
    print("(add it as a drive in Engine DJ, or relink the collection). This script")
    print("only moved files -- it did not touch Engine's database.")


if __name__ == "__main__":
    main()
