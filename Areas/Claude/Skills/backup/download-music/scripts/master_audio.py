#!/usr/bin/env python3
"""Master a full DJ-session recording for upload (loudness + true-peak safety).

Two-pass EBU R128 loudness normalization via ffmpeg's `loudnorm` (measure, then
apply as a single transparent gain with `linear=true`), plus a true-peak ceiling
so it never clips when SoundCloud transcodes to lossy. Writes a 24-bit WAV next to
the input as `<name>_master.wav`.

    python3 master_audio.py "session.wav"                 # default -14 LUFS (transparent, streaming-safe)
    python3 master_audio.py "session.wav" --lufs -10      # louder, club level (compresses a quiet source)
    python3 master_audio.py "session.wav" -o "/path/out.wav"

Notes:
- Feed the LOSSLESS recording (WAV/AIFF/FLAC), not an MP3; upload the result lossless.
- Reaching a loud target (e.g. -10) from a quiet source forces heavy limiting and
  squashes dynamics — the tool prints before/after LUFS/TP/LRA so you can see it.
- If the source is on a slow/removable drive, copy it local first (drive naps abort ffmpeg).
"""
import argparse, json, re, subprocess, sys
from pathlib import Path


def measure(path, I, TP, LRA):
    """Pass 1: return loudnorm's measured stats for `path` as a dict."""
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path),
         "-af", f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    blob = re.search(r"\{[^{}]+\}", out[out.rfind("{"):] if "{" in out else out)
    if not blob:
        sys.exit("could not read loudness stats (is this a valid audio file?)")
    return json.loads(blob.group(0))


def show(tag, m):
    print(f"  {tag}: {m['input_i']} LUFS / {m['input_tp']} dBTP / LRA {m['input_lra']}")


def main():
    ap = argparse.ArgumentParser(description="Master a DJ-session recording (loudness + true-peak).")
    ap.add_argument("input")
    ap.add_argument("--lufs", type=float, default=-14.0, help="target integrated loudness (default -14)")
    ap.add_argument("--tp", type=float, default=-1.0, help="true-peak ceiling in dBTP (default -1)")
    ap.add_argument("--lra", type=float, default=11.0, help="target loudness range (default 11)")
    ap.add_argument("-o", "--output", help="output path (default <name>_master.wav)")
    a = ap.parse_args()

    src = Path(a.input)
    if not src.exists():
        sys.exit(f"no such file: {src}")
    out = Path(a.output) if a.output else src.with_name(f"{src.stem}_master.wav")

    print("Pass 1: measuring…")
    m = measure(src, a.lufs, a.tp, a.lra)
    show("IN ", m)

    print("Pass 2: applying (linear, 24-bit)…")
    af = (f"loudnorm=I={a.lufs}:TP={a.tp}:LRA={a.lra}"
          f":measured_I={m['input_i']}:measured_TP={m['input_tp']}"
          f":measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}"
          f":offset={m['target_offset']}:linear=true")
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
         "-af", af, "-ar", "44100", "-c:a", "pcm_s24le", str(out)],
    )
    if r.returncode != 0:
        sys.exit("ffmpeg failed while writing the master")

    show("OUT", measure(out, a.lufs, a.tp, a.lra))
    print(f"→ {out}")


if __name__ == "__main__":
    main()
