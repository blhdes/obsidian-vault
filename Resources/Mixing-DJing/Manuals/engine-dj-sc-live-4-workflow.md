---
title: Engine DJ → SC Live 4 Workflow
date: 2026-06-03
tags: [dj, manuals, engine-dj, sc-live-4, denon, reference]
---

# Engine DJ → SC Live 4 Workflow

Import tracks, set beatgrids / Hot Cues / Loops, and export to USB/SD so everything shows up on the **Denon SC Live 4**. For **Engine DJ Desktop 5.0** (released May 2026, latest patch 5.0.1). Same steps for any Engine OS unit (Prime 4, SC Live 2, etc.).

> The golden rule: **always move music with Sync Manager, never by drag-copying files in Finder.** Manual copies lose your cues, loops, and beatgrids.

---

## 0. Before you start

- Engine DJ Desktop 5.0 — free from [enginedj.com/downloads](https://enginedj.com/downloads).
- SC Live 4 on **Engine OS 5.0** (update from the unit itself, over Wi-Fi).
- USB stick or SD card formatted **exFAT** (handles big drives; FAT32 works but caps file/drive size).
- Leave ~500 MB free on the drive.

---

## 1. Import tracks

1. Open Engine DJ Desktop.
2. **Settings (gear) → Library →** turn on **Auto Analysis**.
3. Drag folders or audio files (MP3 / WAV / AIFF / FLAC) from Finder into **Collection** (left panel), or use the folder icon to browse.
4. Wait until the bottom bar reads **"No Jobs Running"** — that means BPM, beatgrid, key, and waveform analysis is done.

> Coming from rekordbox, Serato, Traktor, or Apple Music? Use **Import Assistant** (new in 5.0) — a guided import that keeps your existing cues/playlists.

---

## 2. Prep your tracks

Double-click a track to load it into the big waveform.

**Beatgrid** (do this first — cues and loops depend on it)
- Zoom in, then drag the grid lines (or use the grid edit buttons) so the downbeats line up.

**Hot Cues** (up to 8)
- Pads → **Hot Cue** mode (diamond icon).
- Play, then hit a pad **1–8** (or click the waveform) at the spot you want.
- Right-click a pad → rename, recolor, or delete.

**Loops** (up to 8 saved)
- Pads → **Loop** mode.
- Click an empty pad for the **In** point, same pad again for **Out** — or set **Manual** In/Out, or pick an **Auto Loop** length.
- Right-click → rename / color / set **Active Loop** (fires automatically when playback reaches it).

**Also worth setting**
- **Star ratings** (Rating column) — now editable on the SC Live 4 too.
- **Color / comment / key** tags — handy for filtering on the unit.
- **Playlists / Crates** — `+` in the left panel; sub-playlists export too.

Everything saves to the Engine database automatically.

---

## 3. Export to USB/SD (the key step)

1. Plug the drive into the computer.
2. Bottom-left → **SYNC MANAGER**.
3. Left = your Collection playlists/crates; right = your **Drive**.
4. Tick the playlists/folders to send.
5. Click **EXPORT TO DRIVE** and wait for the progress bar.
6. Click **Eject** in the Devices panel before pulling the drive.

The drive now holds an **Engine Library** folder with the database, the audio, and all your cues/loops/grids.

---

## 4. Play on the SC Live 4

1. Power off the unit, insert USB (USB-A ports) or SD.
2. Power on → **Source** screen → pick your drive.
3. Your playlists appear exactly as built — Hot Cues, Loops, waveforms, ratings all intact.

---

## 5. Sync edits back

Made new cues/loops/ratings live on the SC Live 4?

1. Plug the drive back into the computer.
2. Open **Sync Manager** → select the drive → **Sync to Engine DJ** (import from drive).
3. Your changes merge back into the desktop Collection.

---

## What's new in 5.0 (for the SC Live 4)

- **RGB waveforms** — frequencies color-coded (lows/mids/highs); toggle back to classic tri-band anytime.
- **Star ratings on the hardware** — rate tracks mid-set, saved to the drive.
- **32-beat Reverb Rise & Reverb Drop** — longer FX builds (units with built-in FX, which the SC Live 4 has).
- **Import Assistant** — guided import from rekordbox / Serato / Traktor / Apple Music.
- **Redesigned Source screen** + faster database browsing.
- **On-board stems rendering is RANE SYSTEM ONE only** — the SC Live 4 still pre-renders stems on the desktop.

---

## Gotchas

- **Eject** before unplugging, every time.
- **Never drag-copy files onto the drive** — you'll lose cues and loops. Sync Manager only.
- Edited a lot on the hardware? **Sync back** so you don't lose it.
- Big drives (>2 TB) → **exFAT**.
- Only export the playlists you need that night — faster, smaller.

---

## Related

- [[Manuals|Manuals index]]
- [[Areas/Mixing-DJing/Mixing-DJing|Mixing & DJing index]]

## Sources

- [Engine DJ 5.0 Release Notes](https://support.enginedj.com/en/support/solutions/articles/69000878658-engine-dj-5-0-release-notes)
- [Introducing Engine DJ 5.0](https://enginedj.com/news/articles/introducing-engine-dj-5-0)
- [Downloads + Manuals](https://enginedj.com/downloads)
