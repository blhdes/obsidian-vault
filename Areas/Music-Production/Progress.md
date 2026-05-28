---
title: Progress Log
date: 2026-05-28
tags: [progress, log, learning, music-production]
---

# Progress Log

A dated log of every learning session. **Always read this first** when resuming — it shows what we've covered, key takeaways, and where we left off.

The *detailed knowledge* lives in the topic notes (`Ableton/`, `Theory-Basics/`, `Techniques/`, `Track-Sketches/`). This file is just the trail of breadcrumbs.

## Setup status

- **DAW:** Ableton Live **Suite (30-day trial)** installed — trial ends **~2026-06-27**
- **Hardware:** none yet (mouse + keyboard only)

---

## Session 6 — 2026-05-29

**Topic:** Use **multiple scenes** as **song sections** (Intro / Drop / Break) and jump between them as a live mini-arrangement.

**Covered:**
- [[Ableton/multiple-scenes-and-song-sections|Multiple Scenes & Song Sections]] — why a track has sections, creating scenes (`Cmd+I`), duplicating a scene to make a variation (right-click → Duplicate), copying a single clip with **Option-drag**, the **empty-cell rule** (empty cell in a scene = STOP for that track when scene is launched), a 3-scene Intro/Drop/Break example, and **Global Launch Quantization** (top of Transport, default `1 Bar`) that makes scene jumps land on the beat.

**Key takeaways:**
- **One scene = one song moment.** Multiple scenes = song sections you can jump between.
- **New scene:** `Cmd+I` (or Create → Insert Scene).
- **Duplicate scene** (fast variation): right-click scene name → Duplicate.
- **Copy a single clip:** Option-drag (Mac) / Ctrl-drag (Win) to another cell.
- **Empty cell in a launched scene = stop signal** for that track. If you want a clip to continue, duplicate it into the next scene.
- **Launch Quantization (`1 Bar` default)** makes scene jumps wait for the next bar → clean musical transitions. Lives in the top Transport bar.
- Always **rename scenes** with song-section labels (Intro, Drop, Break, Outro).

**Where we left off:** Can perform a small live arrangement (Intro → Drop → Break) by jumping between scenes. Nothing recorded as a finished song yet.

**Next:** Session 7 — move into **Arrangement View** to commit these scenes onto a real timeline (drag scenes into the timeline OR record a live performance of scene jumps), then learn the basics of the timeline (clips on tracks, locators, loop region).

---

## Session 5 — 2026-05-28

**Topic:** Layer a **second clip** (bassline) on a second MIDI track, and use **scenes** to launch multiple clips in sync.

**Covered:**
- [[Ableton/scenes-and-layering|Scenes and Layering Clips]] — adding a new MIDI track (`Cmd+Shift+T`), loading a bass preset, placing the bass clip on the **same scene** as the drums, drawing a 1-note-per-beat bassline on **C2** with **sustained quarter-note length** (drag the right edge of notes), and using **scene launch buttons** (right of Master) to play all clips in a row simultaneously.

**Key takeaways:**
- **Each row = a scene**. The scene launch button (right of Master) plays **every clip in that row at once, in sync**.
- New MIDI track: **`Cmd+Shift+T`** (Mac) or **Create → Insert MIDI Track**.
- Bass placement: usually around **C2** — adjust to taste (not muddy, not weak).
- **Default pencil draws 1/16 notes.** For sustained sounds (bass, pad), **drag horizontally** while clicking or drag the right edge after to lengthen.
- Scenes can be **renamed** (right-click → Rename) — useful as song-section labels (`Intro`, `Drop`, etc.).

**Where we left off:** Two clips on one scene playing together — first layered groove (drums + bass).

**Next:** Session 6 — build **multiple scenes** (different clip combinations = song sections like Intro / Drop / Break), so we can jump between them and start thinking in song structure. After that, move into Arrangement View to commit a real track timeline.

---

## Session 4 — 2026-05-28

**Topic:** Capture notes into a **MIDI clip** so a loop plays on its own — both by drawing in the piano roll and by recording live.

**Covered:**
- [[Ableton/making-a-midi-clip|Making a MIDI Clip]] — what a MIDI clip is, quick theory of beats/bars/BPM, creating an empty clip (double-click), MIDI Editor anatomy (loop brace, piano roll, grid), Pencil tool (`B`), drawing the classic **four-on-the-floor + backbeat** pattern, recording instead of drawing, **quantize** (`Cmd+U`).

**Key takeaways:**
- A **MIDI clip** = a container of notes on a MIDI track; loops on its own once you press play.
- **Double-click an empty cell** on a MIDI track → creates an empty 1-bar MIDI clip + opens the MIDI Editor at the bottom.
- Anatomy: **piano keyboard left** (pitch), **horizontal grid** (time), **loop brace top** (what loops).
- **`B`** = Pencil tool (draw/delete notes). **`Shift+Tab`** = toggle between Device chain and Clip view.
- Tiny theory: **120 BPM default**, **4 beats per bar** (4/4), 1 bar at 120 BPM = 2 seconds.
- **Four-on-the-floor** = kick on every beat; **backbeat** = snare on 2 & 4; **hi-hats** on every 1/8.
- **Recording:** arm track → Computer MIDI Kb on → click record on empty clip → play.
- **Quantize:** `Cmd+A` then `Cmd+U` to snap notes to the grid.

**Where we left off:** Can create a MIDI clip and either draw or record a 1-bar pattern that loops on its own.

**Next:** Session 5 — add a **second MIDI clip** (probably a bassline on a different MIDI track with a synth), play it alongside the drums, and learn how scenes let multiple clips run together. After that we can start bringing loops into **Arrangement View** to shape a track.

---

## Session 3 — 2026-05-28

**Topic:** Load a software instrument on a MIDI track and play it with the computer (QWERTY) keyboard.

**Covered:**
- [[Ableton/playing-an-instrument|Playing an Instrument]] — what a software instrument is, loading a preset from `Sounds`, arming a MIDI track, enabling the Computer MIDI Keyboard, the QWERTY layout (A-K white keys, W-U black keys, Z/X octave, C/V velocity), and a note on Drum Racks.

**Key takeaways:**
- A **software instrument** lives on a **MIDI track**; you feed it notes, it makes sound.
- Easiest place to start: **Browser → Sounds → [category] → preset** → double-click onto a MIDI track.
- Loaded devices appear in the **Device chain** at the bottom of the screen.
- **Computer MIDI Keyboard** turns the laptop into a playable piano — toggle with the top-right keyboard icon or `Shift+Cmd+K`. Track must be **armed** (red dot).
- **Drum Racks** use the same flow but map each key to a different drum hit.

**Where we left off:** Can now load a preset and play it live via QWERTY. Nothing recorded or saved as a pattern yet.

**Next:** Session 4 — capture what you play into a **MIDI clip** (either by recording into a Session clip slot, or by drawing notes by hand in the MIDI/piano-roll editor) so a loop plays on its own.

---

## Session 2 — 2026-05-28

**Topic:** Zoom into Session View — what's inside it and how to make a first sound.

**Covered:**
- [[Ableton/session-view-anatomy|Session View Anatomy]] — the 5 parts of the screen (browser, grid, mixer, master, transport), Audio vs. MIDI tracks, clips, scenes, and the "drag a loop and play it" walkthrough.

**Key takeaways:**
- Session View has **5 parts**: Browser (left), Grid (middle), Mixer (bottom of tracks), Master (right), Transport (top).
- **Tracks** are vertical columns; **scenes** are horizontal rows; **clips** are the cells inside.
- Two track types: **Audio** (plays a recording) and **MIDI** (plays notes on a software instrument).
- Clips have a triangular **play** button; the **square** at the bottom of the column stops them. Clips **loop by default** in Session View.
- First sound made: drag an audio loop from the browser → into a clip slot → play.

**Where we left off:** First audio loop playing on a track. Still no MIDI, no own pattern, no arrangement.

**Next:** Session 3 — load a **software instrument** on a MIDI track (e.g. a drum rack or a synth) and play notes via the computer keyboard, so we go from "playing someone else's loop" to "making our own pattern."

---

## Session 1 — 2026-05-28

**Topic:** Tour of the two main views in Ableton Live.

**Covered:**
- [[Ableton/session-vs-arrangement-view|Session View vs. Arrangement View]] — what each view is for and when to use which

**Key takeaways:**
- Ableton has **two views of the same project**: Session (a grid for sketching/looping) and Arrangement (a timeline for finishing tracks).
- **Workflow:** start in Session → sketch ideas → drag the good ones into Arrangement → build the full song.
- Shortcut: **`Tab`** toggles between the two views.

**Where we left off:** Just learned the room layout — no tracks, clips, or sound made yet.

**Next:** Open Live, hit `Tab` a few times to see both views, then session 2 will go deeper into Session View (tracks, scenes, clips).
