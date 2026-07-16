---
title: Exporting Your Track
date: 2026-05-29
tags: [ableton, export, render, wav, mp3, mastering]
---

# Exporting Your Track

Your track plays inside Ableton — now turn it into a **standalone audio file** (`.wav` / `.mp3`) you can share, upload, or DJ with.

"Exporting" and "rendering" mean the same thing in Live: take everything you hear (all tracks, mixed through the Master) and save it as a single audio file.

## Step 0 — be in Arrangement View

Export captures **what's on the Arrangement timeline**, not what's loaded in Session. If your performance is still only in Session, do the Session-to-Arrangement record from [[arrangement-view-basics|Session 7]] first.

Press **`Tab`** to make sure you're in Arrangement.

## Step 1 — define what to export (the "render range")

Live needs to know *which part* of the timeline to render. Two ways:

| Situation | How to set the range |
|---|---|
| **Whole arrangement** | Click on empty space in the timeline to **deselect everything**. Live defaults to "bar 1 → end of last clip." |
| **Specific section** | **Click and drag** on the timeline ruler to highlight the bars you want (e.g. drag from bar 1 to bar 17 for a 16-bar loop). Only that highlighted region exports. |

> 💡 You'll see the chosen **Render Start** and **Render Length** at the top of the Export dialog — always verify there before hitting OK.

## Step 2 — open the Export dialog

- **Mac:** `Cmd + Shift + R`
- **Win/Linux:** `Ctrl + Shift + R`
- Or: top menu → **File → Export Audio/Video**

A dialog opens with a long list of options. Most you can ignore. Focus on these:

## Step 3 — the settings that matter

### Rendered Track

Leave it on **"Main"** (renamed from "Master" in Live 12) — that renders the whole mix (all tracks combined). You *can* also render individual tracks separately (called "stems"), but for a finished track you want Main.

### Render Start / Render Length

Should reflect the range you defined in Step 1. **Double-check** before exporting.

### Render Tail

⚠️ **Important if you used Reverb or Delay.** Without a tail, the reverb's last "ring" gets cut off at the end of your track.

- For a track with reverb: set Render Tail to **2.0 seconds** (or 4.0 if your reverb is very long).
- For a totally dry track: 0 is fine.

### File Type — WAV or MP3?

| Format | When to use it | Size (4-min track) |
|---|---|---|
| **WAV** | DJ use (Mixxx, SC Live 4), masters, archive, sending to mastering | ~40 MB |
| **AIFF** | Same as WAV but Apple-flavored. Functionally equivalent. | ~40 MB |
| **FLAC** | Lossless compression — half the size of WAV, identical quality. Less universal. | ~20 MB |
| **MP3** | Casual sharing, SoundCloud, emailing | ~9 MB |

**Rule of thumb:** export **WAV** for archive + DJ use. Then optionally also export MP3 for sharing.

### Sample Rate

**44100 Hz** (a.k.a. "44.1 kHz") is the standard for music. CDs and most DJ libraries use this. Leave it there.

(48 kHz is for video. Higher rates exist but aren't useful for a beginner.)

### Bit Depth

For WAV:
- **16-bit** → CD quality, universally compatible → **safe default for DJ use**.
- **24-bit** → more headroom and detail; great for archive or further mixing.
- 32-bit float → for sending to a mastering engineer; overkill otherwise.

**Pick 16-bit** if you're going straight into Mixxx / SC Live 4. **24-bit** if you might come back and remix later.

### MP3 settings (if exporting MP3)

When you tick the **MP3** box, set:
- **Bit Rate: 320 kbps** — highest MP3 quality. Anything lower is noticeably worse.

You can tick **both WAV and MP3** and Live renders both at once. Handy.

### Normalize

A checkbox that boosts the final file's loudest peak to **0 dB** (maximum).

- **Off (recommended for now):** keeps the mix you balanced. Good practice.
- **On:** can be useful if your mix is quiet, but it doesn't make the song *louder-sounding* — just maxes the peak. For real loudness you want a **[[master-limiter|Limiter]]** on Main instead.

Leave **Normalize OFF** for now. Trust your mix.

### Convert to Mono

Leave **OFF**. You want stereo.

## Step 4 — Save

1. Click **Export**.
2. Choose the **folder** (e.g. `~/Music/My-Tracks/` or `~/Documents/Ableton/Exports/`).
3. Choose a **filename** — kebab-case helps if it'll end up in Mixxx later: `first-beat-2026-05-29.wav`.
4. Hit Save.

Live renders the file. A small progress bar shows up. For a 4-bar loop this takes a fraction of a second; for a full 4-minute track, a few seconds.

## Step 5 — drop it into Mixxx / SC Live 4

### Mixxx

1. Open Mixxx.
2. Drag the exported WAV (or MP3) into the **library** area.
3. Mixxx analyzes BPM/key automatically. Verify the BPM matches what you set in Live (it should — 120 BPM = 120 BPM).

### SC Live 4

1. Copy the WAV onto your **USB stick** (the one used by the SC Live 4).
2. The SC Live 4 will pick it up next time you boot it standalone — your own track in the deck. 🎛

## Quick sanity checks after export

- **Open the file in any media player** (QuickTime, VLC) and listen end-to-end.
- **No clipping** at the start or end?
- **Reverb / delay tail not cut off** at the end (this is where Render Tail saves you).
- **Track length** matches what you expected.

## What's *not* here yet

This is **exporting**, not **mastering**. A "mastered" track has had compression + EQ + limiting applied to the Master to make it loud and competitive with commercial releases. That's a whole skill of its own — covered in future sessions if you're interested.

For now, an unmastered export is **plenty** to share, DJ with, and feel proud of. 🎉
