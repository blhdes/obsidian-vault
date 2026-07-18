---
title: Progress Log
date: 2026-05-28
tags: [progress, log, learning, music-production]
---

# Progress Log

A dated log of every learning session. **Always read this first** when resuming — it shows what we've covered, key takeaways, and where we left off.

The *detailed knowledge* lives in the topic notes (`Ableton/`, `Theory-Basics/`, `Techniques/`, `Track-Sketches/`). This file is just the trail of breadcrumbs.

## Setup status

- **DAW:** ✅ **Ableton Live Lite installed and working** (2026-07-09). Lite caps projects at 8 tracks and ships a smaller library than Suite — plan sketches within that.
- **Hardware:** ✅ **Akai APC Mini MK2 connected and mapped** (2026-07-09) — 8×8 clip-launch grid + 9 faders, mirroring Session View 1:1. See [[Ableton/apc-mini-mk2-grid|APC Mini MK2 Grid]].
- **Old projects:** 🗑 **All pre-Lite local projects deleted 2026-07-09** at the user's request (`techno-sketch-01` + backups, `test/000`, a Desktop `Untitled` — moved to Trash). `User Library` and `Factory Packs` kept. **2026-07-17:** the vault notes for sketch 01 (its Track-Sketches note + the 10-step deepening folder) were also cleared, keeping only the one applied technique that came out of it ([[Techniques/percussion-layering|Percussion Layering]]). Sessions 1–9 and the general Ableton/Techniques manuals are unaffected.

## 🎯 Active path

**Path 6 — Make a Real Track Sketch**. See [[Roadmap]] for all paths & progress %.

Pulls from paths 1–5 as the track demands. Each pull also bumps that path's % in [[Roadmap]].

**Sketch in progress:** [[Track-Sketches/hardgroove-134|Hardgroove 134]] — 134 BPM, C major. Hardgroove techno, kicked off 2026-07-16 with a stricter hand-built-only workflow. Weeks 1–2 goal (KICK + SUB, interlocked, sidechained, 3 loop variations) is **complete** — next up is PERC/HATS.

**Paused:** [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — 128 BPM, A minor. Club techno with strong Detroit-style influence. Full 5-layer loop stack done (drums/bass/stab/pad/lead); still needs FX/arrangement/mix/export whenever it resumes.

**Side sketch (self-driven, started 2026-07-12):** [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — 138 BPM, A minor. The user's first track built alone, no lesson plan — 🎉 **completed and exported 2026-07-16**.

---

## Sketch — 2026-07-18 — Hardgroove 134 (Drift Deep-Dive — LFO as a Second Transient)

**Topic:** Free exploration session on the KICK's Drift patch — used the LFO as a second, independent modulation source (Filter Freq) alongside the existing pitch envelope, and hit a real synthesis principle: LFO Rate decides whether modulation reads as *movement* or as *tone*.

**Covered:**
- [[Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] — new section 7: Retrigger mode, Sine vs Saw Down shape (symmetric wobble vs one-directional decay), and the ~20Hz audio-rate threshold, with this build's A/B result (999Hz = texture/buzz, 30–80Hz = a shaped hit — the latter preferred)

**Key takeaways:**
- The LFO tab's own local "Amount/Mod" pair is just an internal send level — the actual destination assignment (Source → Target → Amount) lives in the separate **"Mod" tab**, Drift's real Mod Matrix.
- **Sine LFO shape swings both above and below center** — modulating a filter with it doesn't just brighten, the below-center half also darkens, which can read as the sound getting more grave/dark rather than a clean pop. **Saw Down** only falls once per trigger, behaving more like an actual decay envelope.
- **Any LFO's Rate has an audible threshold, not just a fast/slow dial:** below ~20Hz it's felt as shaped movement (a sweep/snap with contour); at/above ~20Hz it enters audio rate and starts to sound like its own texture/tone (a subtle buzz), because the ear hears the modulation frequency itself. This is a general Drift/synthesis principle, not kick-specific — relevant to any future patch with modulation (pads, risers, etc.).
- Explored purely by ear/experimentation rather than a fixed lesson plan — a genuine "keep playing with the synth" session.

**Where we left off:** KICK now has two independent transient layers — the original pitch-envelope click, plus an LFO-driven filter snap at 30–80Hz (Saw Down, Retrigger on).

**Next:** Open — more Drift/chain experiments queued if wanted (Noise-oscillator click layer, a rawer Saturator curve, a non-sidechain Compressor on KICK for glue, EQ Three's unused Mid band for presence), or move on to PERC/HATS.

---

## Sketch — 2026-07-17 — Hardgroove 134 (3 Loop Variations — Weeks 1–2 Goal Complete 🎉)

**Topic:** Built the final piece of the original workflow — **3 distinct 8-bar kick+sub loops**, each with its own character, derived from one base pattern using only placement/velocity edits.

**Covered:**
- [[Techniques/loop-character-variations|Loop Character Variations (Placement-Only)]] — new technique note: derive several loop personalities from one pattern via small targeted edits (leave alone / add a phrase-boundary anticipation / remove one hit periodically) rather than writing unrelated patterns
- [[Track-Sketches/hardgroove-134|Hardgroove 134]] — Loop 1 (Straight Roller, unedited), Loop 2 (Rolling Push — added anticipation note in bars 4/8), Loop 3 (Stripped/Hypnotic — removed one hit in bars 2/4/6/8) all built and confirmed

**Key takeaways:**
- **Three *unrelated* patterns feel like three different songs; three *variations of one pattern* feel like the same idea breathing differently.** Small, targeted edits to specific bars beat inventing new patterns from scratch.
- The **anticipation-note push** (Loop 2) directly exploits the sidechain groove tool from the previous session — the added note lands close enough to the kick that it catches the compressor's release/recovery and audibly swells in, confirmed by ear ("feels rolling").
- The **skip-a-note strip** (Loop 3) needs only one removed hit per alternating bar to read as meaningfully sparser — over-removing would have undercut the effect.
- **This closes the entire original Weeks 1–2 goal from kickoff:** KICK, SUB, interlock, sidechain, and 3 character loops — all hand-built, no programmatic control, taught one parameter/concept at a time with confirmation before advancing.

**Where we left off:** Low end (KICK + SUB) fully built and grooving in 3 distinct flavors, nothing else in the mix yet.

**Next:** Open-ended — move into the rest of the 8-track budget (**PERC** via Drum Rack, then **HATS**), building outward from the kick/sub foundation.

---

## Sketch — 2026-07-17 — Hardgroove 134 (SUB Built, Interlock + Sidechain Done)

**Topic:** Finished the Weeks 1–2 core workflow: **SUB** patch mirroring KICK, the kick/sub interlock pattern placed, and the sidechain wired up and confirmed.

**Covered:**
- [[Track-Sketches/hardgroove-134|Hardgroove 134]] — SUB built, interlock pattern in, sidechain confirmed; all of steps 1–4 of the original plan done
- [[Techniques/kick-sub-interlock-sidechain|Kick/Sub Interlock as a Sidechain Groove Tool]] — new technique note: when the ducked element never overlaps the kick (already interlocked), sidechain Release becomes a pure groove/motion tool — tuned right, the sub swells into its own hit instead of sounding static

**Key takeaways:**
- **SUB's Envelope 1 is the mirror-opposite of KICK's:** Sustain 100% (holds while the note plays) instead of 0% (self-terminating). This flips which parameter controls duration — for the kick, note length barely matters (the envelope decays to silence on its own); for the sub, **note length is the only thing controlling how long it rings**, since there's no decay to cut it short.
- Ableton's bar.beat.sixteenth notation: an 8th note = 2 sixteenths. As a Length/duration value that's `0.0.2`; as an end position computed from a start of `X.X.1`, the correct end is `X.X.3` (not `X.X.2`, which is only a 16th note and would leave a gap).
- **This project's groove rule (no swing/FX, placement + velocity only)** was respected — the interlock is a straight 8th-note grid, unlike Ticket to Detroit's swung hats.
- **Sidechain as a groove tool, not just cleanup:** since KICK and SUB are already time-separated (never overlapping), the duck isn't preventing a frequency clash — Release timing (137ms here) is tuned so the sub is still recovering/swelling as its own note begins, producing the "rolling" motion this genre is built on.
- SC Filter (~80Hz) on the sidechain's trigger input — filters *what triggers the compressor*, not the compressed audio, so only the kick's low thump fires the duck, ignoring saturation edge on top.

**Where we left off:** KICK + SUB interlocked and sidechained, sounding like a real rolling low end with nothing else in the mix. Weeks 1–2 core workflow (steps 1-4) complete.

**Next:** Build the **3 distinct 8-bar kick+sub loops**, each with its own character — the final target for this phase, using velocity variation and placement as the differentiation tools (not swing/FX).

---

## Sketch — 2026-07-17 — Hardgroove 134 (KICK Patch Complete)

**Topic:** Finished the KICK's full signal chain in Drift — **Drift → Saturator → EQ Three** — built entirely from a blank patch, one parameter at a time.

**Covered:**
- [[Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] — the full recipe: oscillator isolation, Pitch Mod vs Freq Mod, Envelope 1 as the hardwired Amp Envelope, killing hidden LFO/Drift-macro wobble, Saturator, EQ Three
- [[Track-Sketches/hardgroove-134|Hardgroove 134]] — KICK chain complete; session log has the full debugging trail

**Key takeaways:**
- **Pitch Mod and Freq Mod are separate controls that both default to "Env 2"** — easy to raise the wrong one. The first "click" heard was actually the filter popping open (Freq Mod), not a real pitch drop, since Pitch Mod's own amount was still at 0%.
- **Envelope 1 is Drift's hardwired Amp Envelope** — always controls volume, no Mod Matrix assignment needed (unlike Envelope 2, which needs an explicit Pitch Mod / Freq Mod slot).
- Debugging a "periodic" volume drift ruled out fixed-value parameters first (a static Attack time can't create a multi-beat cycle — it's identical on every note), then found real candidates: **LFO Rate in Hz** (drifts out of phase with the tempo grid unless synced to `1:1`), the **global Drift macro** (deliberate per-note randomness), and finally the **Mod tab's** actual Mod Matrix — an LFO→Volume routing at low amount, sine-shaped, producing a slow loudness swell across many loop repeats.
- **Saturator** (new device this session): drives a waveshaping curve for harmonic weight, not obvious distortion. Added brightness/edge is a normal side effect of the added harmonics, not a mistake — EQ Three is the next stage specifically for taming it if needed.
- **EQ Three** recipe for a kick sharing space with a separate sub: narrow the Low band via the Low/Mid crossover Freq (~50-60Hz) and trim Gain a couple dB, rather than killing the band outright — the kick keeps some low body, just doesn't encroach on SUB's territory.
- This directly completes Path 2's flagged first step (from-scratch Drift patch) — first genuinely deep sound-design session of this project.

**Where we left off:** KICK is fully built and sounding right ("groovier"). Nothing else on the track yet.

**Next:** Mirror the process for **SUB** — pure sine, no pitch envelope, full sustain, EQ Three killing everything above ~180Hz, offbeat pattern interlocked with the kick. Then sidechain SUB to KICK, then the 3 target 8-bar loop variations.

---

## Sketch — 2026-07-16 — Hardgroove 134 (Kickoff)

**Topic:** Third track sketch kicked off — **hardgroove techno at 134 BPM**, rebuilding the low end from zero in Drift. A deliberate fresh start, not a continuation: [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] is paused (Solo Sketch 138 also wrapped the same day — see below).

**Covered:**
- [[Track-Sketches/hardgroove-134|Hardgroove 134]] — new sketch: 134 BPM, C major, 8-track budget (KICK/SUB/PERC/HATS/STAB-LEAD/ATMOS/FX-RISER/RETURN), stock-devices-only rule (Drift/EQ Three/Saturator/Compressor/Drum Rack/Simpler), Weeks 1–2 goal (KICK + SUB only, three distinct 8-bar loops)
- KICK track started: Drift loaded, oscillator isolated to a single plain sine (Osc 2/Sub/Noise off) — checkpoint before the pitch envelope

**Key takeaways:**
- New house rule for this project: **100% hand-built in Ableton's UI** — no Producer Pal, no MCP, no programmatic control. The point is learning the interface directly, not the fastest path to a finished loop.
- Live Lite's 8-track ceiling now forces a **pre-committed instrument budget** up front (KICK/SUB/PERC/HATS/STAB-LEAD/ATMOS/FX-RISER/RETURN) rather than adding tracks ad hoc as the sketch grows.
- Drift is the sound-design workhorse here (no Operator/Wavetable/EQ Eight allowed) — building "from a blank preset" means actively zeroing Drift's default pre-routing (recall: Env 2 → Freq Mod ships at 80% out of the box), not just loading the device and assuming it's silent/neutral.
- This directly picks up Path 2's flagged first step (Roadmap: "Open Drift with all presets cleared, build a bass from a single sine wave") — now literally underway on the kick patch.

**Where we left off:** KICK track created, Drift loaded, oscillator isolated to a single plain sine — waiting on user confirmation before wiring the pitch envelope.

**Next:** Pitch envelope on the kick (short decay routed to pitch → the thump/click transient), then the amp envelope, Saturator, EQ Three. Then mirror the whole process for SUB.

---

## Sketch — 2026-07-16 — Solo Sketch 138 (Exported — Sketch Complete 🎉)

**Topic:** Rendered the final WAV. **Solo Sketch 138 is done, start to finish** — the user's first fully self-driven track, from the original drum loop through export.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — marked complete; full State summary added
- [[Ableton/exporting-your-track|Exporting Your Track]] — corrected for this Live version: "Master" renamed to **Main** in the Rendered Track field, and the standalone **Render Tail** field is gone — pad **Render Length** a couple bars past the last clip instead so Reverb/Delay tails have room

**Key takeaways:**
- Live 12's Export dialog is leaner than what was originally documented — no dedicated tail control, Spanish-localized labels for this user (Pista renderizada, Duración de renderización, etc.), both now reflected in the vault note.
- This sketch's arc covered nearly every mixing topic in Path 3 (interlock → clip envelopes → rumble → sidechain ducking → riser stacked envelopes → EQ carving → limiter) plus Path 4's opener (sampling) — a genuinely full production cycle, independently driven.
- Real value came from working through non-obvious Ableton debugging (Loop vs. End fields, note length vs. clip length, Session/Arrangement clip independence, default device modulation) rather than from any single lesson.

**Where we left off:** Track exported. Solo Sketch 138 closed as a complete, finished piece.

**Next:** Open — could return focus to [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] (still needs FX/arrangement/mix/export), start a fresh self-driven sketch, or dive into Path 2 (sound design from scratch) / Path 1 (chord progressions), both flagged earlier as things the user wants more of.

---

## Sketch — 2026-07-16 — Solo Sketch 138 (Mix Pass — EQ + Limiter)

**Topic:** The mix pass. Two new closing concepts for Path 3: **EQ carving** (subtractive EQ — cut, don't boost; high-pass anything that isn't the kick/rumble/bass) and the **Master Limiter** (a hard ceiling as the last device on Master, safety net against clipping).

**Covered:**
- [[Techniques/eq-carving|EQ Carving (Subtractive EQ)]] — the cut-don't-boost philosophy, the high-pass-everything-else rule, applied per-track to the sketch's 6 tracks
- [[Ableton/master-limiter|Master Limiter (Mix Safety Net)]] — Ceiling ~-0.3dB, small Gain, why this isn't full mastering
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — homework queued: high-pass Polymeter perc + Stab Dub Direct, add the Limiter, verify Build 2 doesn't clip

**Key takeaways:**
- Subtractive EQ: when two elements clash in the same frequency range, cut the one that doesn't need it there, rather than boosting the other to compete.
- The single highest-value move for a beginner: high-pass everything except the kick/rumble/bass, since almost nothing else needs true low end.
- A Limiter is an extreme compressor with a hard ceiling — catches summed peaks across 6 tracks that no individual track's level would predict.
- This closes out Path 3's remaining topics (EQ, limiter) — sidechain and automation were already done.

**Where we left off:** Concepts covered; sketch itself unchanged pending homework.

**Next:** Homework — apply the EQ carving + Limiter, confirm the Master meter behaves on Build 2. Then: export, the finish line for this sketch.

---

## Sketch — 2026-07-16 — Solo Sketch 138 (Riser Debugging Resolved)

**Topic:** Closed out the riser debugging chain: rebuilt the riser clean in Session View (Freq Mod zeroed, envelopes redrawn), verified it solo, cleared every stale/duplicate riser block from Arrangement, then re-recorded. Confirmed working.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — full debugging saga logged under "Riser debugging saga — resolved 2026-07-16"

**Key takeaways:**
- The real fix wasn't any single tweak — it was **removing accumulated stale state** (old Session clip, leftover duplicate Arrangement blocks) and rebuilding from one verified source, then re-recording once.
- General debugging order for "my automation isn't working" in Live: clip End vs. Loop-section Length, note length vs. clip length, which physical clip copy is actually playing (Session vs. Arrangement), then any of the device's own internal modulation already routed to that parameter.
- Drift's default patch ships with **Env 2 → Freq Mod at 80%** already routed — worth zeroing on any fresh Drift instance where a clean, externally-automated filter sweep is wanted.

**Where we left off:** Riser confirmed working correctly in Arrangement. Structure layer is genuinely done.

**Next:** Mix pass, then export.

---

## Sketch — 2026-07-16 — Solo Sketch 138 (Session vs Arrangement Clip Debugging)

**Topic:** Tracked down why the extended 8-bar riser "still sounded like the original": the Session View clip slot and its recorded Arrangement copy are **independent objects** once captured — editing one doesn't touch the other. Soloing/playing from the Session clip slot played the old, unedited version.

**Covered:**
- [[Ableton/arrangement-view-basics|Arrangement View Basics]] — new addendum: Session clip vs. its Arrangement copy are separate after Capture; always audition fixes from the Arrangement timeline itself, not the Session slot

**Key takeaways:**
- This was a multi-step debug chain: Loop-off clip's End vs. Loop-section Length (fixed) → note not extended with the clip (fixed) → finally, testing via the *wrong* clip entirely (the stale Session copy).
- Resolution: play back via the Arrangement timeline (`Spacebar` with playhead there) to judge the real, fixed automation.
- Open decision: the original Session clip is still stale — matters only if the user wants to keep performing this track live from Session/APC later.

**Where we left off:** Root cause found; riser automation confirmed correct once tested from the right place.

**Next:** Confirm the Arrangement playback now sounds right, then the mix pass, then export.

---

## Sketch — 2026-07-15 — Solo Sketch 138 (Arrangement Rearranged)

**Topic:** Follow-up: the arrangement now has a two-act shape — Build 1 (riser → Polymeter+Rumble enter + one Stab hit) → breakout/thin back to drums+bass → riser → Build 2, a bigger climax where the Stab sample became a repeated rhythmic run instead of one hit.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — updated Observations with the "Arrangement take v2" read

**Key takeaways:**
- Turning a single one-shot into a repeated run for the second pass is a real escalation device — the climax gets its own identity instead of just repeating Build 1.
- The riser retrigger question from the first take is now partially resolved: Build 2's riser is a single clean hit, Build 1's is still the back-to-back double — worth confirming whether that asymmetry (longer first build, shorter second) is deliberate.
- Track 7 confirmed intentionally empty — only 6 MIDI/Sample tracks in use, no action needed.

**Where we left off:** Two-act arrangement in place. One open question (Build 1's riser doubling) before moving to the mix pass.

**Next:** Resolve the riser question, then the mix pass, then export.

---

## Sketch — 2026-07-15 — Solo Sketch 138 (Recorded to Arrangement)

**Topic:** Homework check-in: the performance is recorded into Arrangement. Applied the "mixed scene + individual clip launches" addendum from [[Ableton/arrangement-view-basics|Arrangement View Basics]] — drums/bass ran continuously, Polymeter perc + Rumble entered together partway through, the Stab Dub Direct sample fired once, and the Riser fired twice back-to-back around the new-layer entrance.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — full take recorded; see the sketch note's Observations for the arrangement read and two open questions (riser double-trigger intent, unused Audio track)

**Key takeaways:**
- Staggering track entrances (rather than only whole-scene launches) reads as real arrangement dynamics — a valid, more granular alternative to the Intro/Build/Drop/Break scene model.
- **A retriggered clip resets its envelopes.** Firing the same riser clip twice in a row gives two short re-attacks, not one longer continuous swell — if a longer build is wanted, extend the clip (and its envelope lengths) instead of repeating it.
- Riser placement (right before a new layer enters, not only before a "drop") generalizes the technique correctly.

**Where we left off:** Take recorded. Two open questions before the mix pass: is the double riser intentional, and is the empty Audio track (7) meant to be used or freed up.

**Next:** Resolve the riser question, then the mix pass, then export.

---

## Sketch — 2026-07-14 — Solo Sketch 138 (FX/Riser Applied)

**Topic:** Homework check-in: the riser is built and working — Noise generator enabled on Drift (Osc 1/2 off), Filter Freq and Track Volume both automated rising across the clip as two stacked lanes in the Envelopes tab, Loop off.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — riser track complete, all 8 planned layers now in place (drums, rumble, bass, sample accent, riser + the 4-scene structure)
- [[Ableton/clip-envelopes|Clip Envelopes]] — corrected: the Envelopes tab sits top-right of Clip View (not a small "E" button), and its Device/Control dropdowns live at the *bottom* of the pane, not the top — fixed after two rounds of screenshots. Also documented: each Device/Control pair's automation is stored independently, which is *how* stacking two envelopes on one clip actually works.

**Key takeaways:**
- Live's UI for this (Live 12) differs from the vault's original 2026-05-30 description — Envelopes is a tab, not an icon button. Vault corrected to match the real interface.
- The sketch's layering stage is now fully closed: every item from the original 8-track plan is built.

**Where we left off:** All planned layers built. Nothing left to *add* — remaining work is finishing/polish.

**Next:** Record the performance into Arrangement, then mix pass, then export — the home stretch for this sketch.

---

## Sketch — 2026-07-13 — Solo Sketch 138 (FX/Riser)

**Topic:** The tension-tool layer: a **riser** built from Drift's **Noise oscillator** with two stacked clip envelopes (Filter Cutoff + Track Volume) rising together on one non-looping clip.

**Covered:**
- [[Techniques/riser-fx|Riser FX (Noise Build-Up)]] — Noise as a pitch-free source, the stacked-envelope build recipe, Loop off, launching by hand before the Drop
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — homework queued: build the Riser track (slot 6 of the 8-track budget)

**Key takeaways:**
- A riser = brightness (filter opening) + loudness (volume rising) compounding together over 1–2 bars — reads as one "build" event, not two separate sweeps.
- **Noise** (new oscillator type on Drift, alongside the sine/triangle used before) has no clear pitch, so it never clashes with the track's key — ideal raw material for transition FX.
- This is the first time **two envelope lanes stack on the same clip** — every earlier automation move (acid lead, etc.) only touched one parameter at a time.
- **Loop off** matters — a riser that repeats turns into a siren; it should fire once and stop.
- It isn't tied to a scene — it gets launched by hand a bar or two before the Drop pad, the same performance instinct already used for scene jumps.

**Where we left off:** Concept covered; sketch itself unchanged pending homework.

**Next:** Homework — build the Riser track and try launching it into the Drop. Then: record the performance into Arrangement, mix pass, export.

---

## Sketch — 2026-07-13 — Solo Sketch 138 (Sampling Applied)

**Topic:** Homework check-in: the **Stab Dub Direct** sample loaded into Simpler on a new track, trimmed, and set to **One-Shot** — first real use of the sampling lesson.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — sample-based accent added, dub-techno-flavored texture layer

**Key takeaways:**
- One-Shot was the right call for a stab-as-texture: it fires the whole hit once per trigger, no held-note behavior to manage.
- Using a sampled stab as an accent (not a repeated harmonic hook) keeps it in the "texture" role — consistent with the earlier decision to skip a written stab/bleep for this sketch.

**Where we left off:** Sampling layer in; drums, rumble, bass (both ducked), 4-scene structure, and now a dub-flavored one-shot accent all in the sketch.

**Next:** FX/riser for transitions, record the performance into Arrangement, mix pass, export.

---

## Sketch — 2026-07-13 — Solo Sketch 138 (Sampling — Simpler Basics)

**Topic:** Path 4 opener: **sampling** in Simpler — key/pitch-mapped playback (Classic mode) vs. **One-Shot mode** for percussive/texture hits, and trimming a sample's Start/Length.

**Covered:**
- [[Ableton/sampling-with-simpler|Sampling with Simpler]] — dragging audio in, key/pitch mapping, Classic vs One-Shot vs Slice, Start/Length trimming
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — homework queued: add a one-shot texture/hit as an accent

**Key takeaways:**
- Simpler plays back *your* audio the same way Drift plays an oscillator — familiar shape (MIDI track, arm, play), new source material. Already used once, hidden inside the Acid Bass preset on Sketch 01.
- Key mapping: root key (default C3) plays the sample at original speed; every semitone away transposes it, same mechanism as a synth oscillator.
- **Classic** = plays/loops while the key is held (tonal/sustained material). **One-Shot** = plays the full sample once regardless of key length — the right fit for percussive/texture hits, matching the sketch's drums-first direction. **Slice** auto-chops across keys — flagged for a later session (e.g. chopping a drum break).
- **Start/Length** markers trim dead air so a hit fires exactly on the beat.

**Where we left off:** Concept covered; sketch itself unchanged pending homework.

**Next:** Homework — drag a short one-shot texture or hit into Simpler on a new track, trim it, set to One-Shot, place it as a bar-end accent alongside the existing Tamb Chop/Triangle Build hits. Then: FX/riser, record the performance to Arrangement, mix pass, export.

---

## Sketch — 2026-07-13 — Solo Sketch 138 (Sidechain Applied)

**Topic:** Homework check-in: sidechain ducking applied — the Compressor sidechains the rumble to the kick (the essential case), and the user also chose to duck the bass the same way (the "optional" case from [[Techniques/sidechain-ducking|the note]]).

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — rumble and bass both duck against the kick now

**Key takeaways:**
- Rumble ducking is the essential case — continuous low end has to get out of the kick's way on every hit.
- Bass ducking is the optional case — the offbeat bass already dodges the kick in time, so sidechaining it stacks an extra rhythmic pump on top of that existing manual [[Techniques/kick-bass-interlock|interlock]], rather than fixing a clash.
- Both ducks pulling from the same kick chain keeps the pump locked together musically.

**Where we left off:** 4-scene structure (Intro/Build/Drop/Break) built and performed from the APC; rumble + bass both sidechained to the kick. The sound-design/mixing layers for this sketch are essentially closed out.

**Next:** Structure + polish stage — record the performance into Arrangement, FX/riser for transitions, sampling (Path 4 opener) for texture, mix pass, export.

---

## Sketch — 2026-07-12 — Solo Sketch 138 (Kickoff)

**Topic:** The user's first **self-driven** sketch (138 BPM, A minor, Cashon Kit): built a drum loop + break variation alone, then asked "what would a pro do next?". New technique queued: the **rumble** — a reverb-generated low-end layer under the kick.

**Covered:**
- [[Track-Sketches/solo-sketch-138|Solo Sketch 138]] — the new sketch: stats, state, observations, next-steps list
- [[Techniques/rumble-bass|Rumble (Reverb Low-End Layer)]] — kick copy → 100%-wet reverb → EQ out the highs → quiet fader
- [[Techniques/techno-production-arc|Techno Production Arc]] — the 7-stage high-level map, few-elements principle, 8-bar rule, Lite track budget
- [[Techniques/stab-vs-bleep|Stab vs Bleep]] — comparison reference; neither is required — user chose a drums-focused direction
- [[Techniques/ghost-notes-and-fills|Ghost Notes & Fills]] — vel 20–40 hits on `e`/`a` + phrase-end fills every 4/8 bars via the clip Duplicate button
- [[Techniques/polymeter-percussion|Polymeter Percussion]] — 3-beat perc clip rotating against the 4-beat bar; one static pattern = 3 bars of variation
- [[Techniques/sidechain-ducking|Sidechain Ducking]] — Compressor + sidechain from the kick pad's chain; duck the rumble 6–10 dB, Release = the groove knob

**Key takeaways:**
- Built unprompted: four-on-the-floor kicks, offbeat rides (open-hat job, darker color), bar-end accents, velocity ramp, swing groove, and a no-kick break clip — all known concepts, self-applied. Solid.
- **Swing 16ths had nothing to move** — every hit sat on quarters/`&`s (the known "swing needs 16ths" rule, caught in the wild). Fix: low-velocity `e`/`a` hits.
- **The rumble** = low end generated *from the kick* via reverb, on a separate track so the dry kick keeps its punch. Style-specific: raw/hypnotic techno at 130–145.
- Priority order for a bare drum loop: low end first, then one hypnotic mid element, then variations/structure.

**Where we left off:** 4-scene structure built and performed from the APC (Intro/Build/Drop/Break). Sidechain ducking lesson delivered as homework — Compressor on the rumble, sidechained to the kick pad's chain.

**Next:** Hear the ducked loop. Then queued: **sampling** (Path 4 opener), FX/riser for transitions, record the performance to Arrangement, mix pass, export.

---

## Sketch — 2026-07-10 — Ticket to Detroit (Bleep Lead)

**Topic:** Layer 5: the **bleep lead** — the first *written melody* (motif craft: call-and-response, space, variation) and the first **from-scratch synth patch** (a plain bleep on Drift, using only known dials).

**Covered:**
- [[Techniques/bleep-lead-motif|Bleep Lead & Motif Writing]] — the 2-bar call/response motif, three craft rules, the register-lanes map, the bleep recipe
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — lead track added; the full loop stack (drums/bass/stab/pad/lead) now plays

**Key takeaways:**
- **A club melody = a motif**: a 3–5 note cell + space, repeated with small variations — not a vocal line.
- **Call and response:** bar 1 rises away from home (A4 C5 E5), bar 2 falls back and lands on the root (G5 E5 A4). Ending on A closes the breath.
- **Change one dimension at a time** — both bars share the same `e/&/e` rhythm; only the pitches vary.
- **Silence is a note:** beat 4 stays empty in both bars. Sparse = hypnotic.
- **Register lanes:** kick/bass low, stab+pad mid (A3–B4), lead on top (octave 5), hats above — nobody fights.
- First hand-built patch: **sine/triangle + fast attack + short release + mono** on Drift = a bleep. Every dial was already known (ADSR, mono, osc).
- Lead clip gets the swing groove — its `e` hits must move with the hats.

**Where we left off:** The full 5-track loop stack — swung drums, syncopated bass, Am9 stab, string pad, bleep motif — playing as one groove at 128 BPM from the APC row. The loop is *done*; what remains is structure.

**Next:** Either the **FX/riser layer** or straight to **arranging scenes** (Intro/Build/Drop/Break on the APC grid — known from sketch 01, now with 5 real layers).

---

## Sketch — 2026-07-10 — Ticket to Detroit (String Pad)

**Topic:** Layer 4: the **string pad** — one held Am9 as a dark bed under everything. New concept: the **ADSR amplitude envelope**, taught through the stab/pad contrast (same chord, opposite envelope = opposite instrument).

**Covered:**
- [[Techniques/adsr-envelopes|ADSR Envelopes (Stab vs Pad)]] — the four dials, the envelope diagram, the pad recipe
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — pad track added; also logged the user's own Channel EQ on the stab + the three stab A/B clips

**Key takeaways:**
- **ADSR = the loudness shape of a note:** Attack (time to full volume), Decay (time to fall to sustain), Sustain (a *level*, not a time), Release (fade after key-up).
- The acid lead's filter envelope was the same mechanism aimed at cutoff instead of volume.
- **Stab vs pad = the same chord at opposite envelope settings** — fast A/short R = percussion, slow A/long R = atmosphere. The envelope decides the instrument.
- Pad rules: darken with the low-pass, mix quiet (felt, not heard) — the mute test should reveal an emptier room, not a stopped instrument.
- **Grooves only apply to rhythmic clips** — a held whole note has nothing on the swung positions.
- Clips of different lengths loop independently (2-bar pad over 1-bar drums/bass/stab) — known from sketch 01, reapplied.

**Where we left off:** Four tracks — drums, bass, stab (+Channel EQ), pad — looping as one swung groove at 128 BPM from the APC row.

**Next:** The **bleep lead** — a sparse pentatonic Detroit melody on top; melody-writing rules of thumb over a fixed groove.

---

## Sketch — 2026-07-10 — Ticket to Detroit (Chord Stab)

**Topic:** The Detroit signature: the **minor 9th chord stab**. New theory: **chord extensions** — stacking past the triad to the 7th and 9th. First polyphonic clip in the sketch.

**Covered:**
- [[Theory-Basics/sevenths-and-ninths|Sevenths and Ninths (Chord Extensions)]] — the 1-3-5-7-9 stacking pattern, why "9" not "2", triad vs 7th vs 9th character
- [[Techniques/detroit-chord-stab|Detroit Chord Stab]] — poly voices, fast attack + filtered dark, mid-range voicing, sparse weak-position rhythm, Option-drag for stacked notes
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — stab track added; drums + bass + Am9 stab now loop together

**Key takeaways:**
- **Chords stack every other scale note:** A→C→E→G→B. Triad = 1-3-5 (Am), add 7 (G) = Am7, add 9 (B, the 2nd an octave up) = Am9.
- More extensions = more color: triad states the key plainly, the 9th *floats* in it. The m7/m9-as-stab is the Detroit-specific use of a universal concept.
- A **stab is a rhythm instrument** — one chord repeated on syncopated weak positions; the rhythm is the interest, not chord changes.
- **Voices ≥ 5 on the stab synth** — the exact opposite of the mono-bass rule; five notes must ring at once.
- Voice it mid-range (A3–B4), above bass / below hats; optionally drop the root since the bass owns A.
- Same swing groove file on every rhythmic clip — the stab's `a`-of-2 hit must move with the hats.
- Drawing chords: draw the 5-note stack once, lasso it, **Option-drag** copies to the other hits.

**Where we left off:** Drums + syncopated bass + Am9 stab looping as one swung groove at 128 BPM, launchable as a row from the APC.

**Next:** The **string pad** — same chord knowledge stretched into a long sustained bed (slow attack, the anti-stab), filtered to sit under everything.

---

## Sketch — 2026-07-10 — Ticket to Detroit (Syncopated Bassline)

**Topic:** Second layer: a **syncopated bassline** in A minor pentatonic. New concept: **syncopation** — accenting the weak positions (`e`/`a`, offbeats) so the line pulls forward instead of stamping. Extends the known kick/bass interlock from "avoid the kick" to "actively push around it".

**Covered:**
- [[Techniques/syncopated-bassline|Syncopated Bassline (Detroit Bass)]] — syncopation, the anchor/push/turnaround pattern anatomy, design rules, matching grooves across clips
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — bass track added; drums + bass now swing together

**Key takeaways:**
- **Syncopation = emphasis on weak positions.** The ear expects weight on the beats; accents between them create the forward pull.
- Pattern anatomy: **anchor** (offbeat root hits — the known interlock), **push** (a 16th anticipation, e.g. the `a` of 3), **turnaround** (C→G at bar's end resolving to A).
- Extra notes come from **A minor pentatonic** (A C D E G) — guaranteed to fit; root-heavy keeps it Detroit.
- New hits go on `e`/`a`/offbeats only — never on the kick's quarters. Interlock still rules.
- Short staccato 1/16 lengths, mono voice, ~A1 — all known settings, reapplied.
- **The bass clip gets the SAME swing groove as the drums** — mismatched swing between rhythmic clips makes them flam. One groove file for the whole project.

**Where we left off:** Drums + syncopated bass looping together at 128 BPM, both on the Swing 16ths 59 groove, launchable as a row from the APC.

**Next:** The **Detroit chord stab** — a minor 7th/9th chord as a short rhythmic hit. First real chord work (Path 1 territory: what a 7th/9th actually is).

---

## Sketch — 2026-07-10 — Ticket to Detroit (Hat Swing)

**Topic:** Put the *Detroit* into the drums: **swing/groove**. Fill the closed hats to a 16th stream, then push the offbeat 16ths late with a groove from Live's **Groove Pool** — the DAW version of the 909's shuffle function.

**Covered:**
- [[Techniques/swing-and-groove|Swing & Groove (The Detroit Shuffle)]] — swing %, why swing needs 16th content, Groove Pool mechanics (Base/Timing/Random/Velocity/Amount, Commit)
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — 16th closed hats added, swing groove applied

**Key takeaways:**
- **Swing = the offbeat 16ths (`e`/`a`) land late.** 50% = straight; 54–58% = subtle classic house/Detroit roll; 66% ≈ triplet shuffle.
- **Swing needs 16ths to act on** — quarters, 2 & 4, and `&`s don't move. An all-8ths pattern sounds identical with swing on.
- Closed hats fill to 16ths but **skip the `&`** so they don't choke the ringing open hat; new `e`/`a` hits sit at low velocity.
- **Grooves are non-destructive**: drag from Browser onto a clip; notes on screen don't move. Groove Pool (wave button, bottom-left of Browser) holds the dials; **Commit** prints it into the notes.
- The kick stays straight even in the same clip — swing only moves notes on `e`/`a`, so one drum clip is fine.
- Salt rule: set swing higher than feels right, back it off, and A/B against Groove = None.

**Where we left off:** Foundation loop now rolls — 16th hats with velocity variation + a ~54–58% swing groove, still launchable from the APC pads.

**Next:** The **syncopated Detroit bassline** — A minor pentatonic notes pushing around the kick (reuses kick/bass interlock, adds real syncopation).

---

## Sketch — 2026-07-09 — Ticket to Detroit (Kickoff)

**Topic:** Fresh start on Live Lite. Deleted all old local projects, then kicked off the new sketch **Ticket to Detroit** (128 BPM, A minor, club techno with Detroit influence): rebuilt the foundation drum loop as a repeat of the first-track exercise, and learned the **APC Mini MK2 → Session View mapping** — first hardware lesson.

**Covered:**
- [[Track-Sketches/ticket-to-detroit|Ticket to Detroit]] — the new sketch: stats, the Detroit production reference map, the 8-track plan, kickoff log
- [[Ableton/apc-mini-mk2-grid|APC Mini MK2 Grid]] — pads = clip slots, right column = scenes, faders = volumes, pad colors, the red frame

**Key takeaways:**
- **Detroit-style, in production terms:** 909 palette + four-on-the-floor, **swing on the hats**, syncopated moving bassline, the **minor 7th/9th chord stab**, string-machine pads, raw velocity variation, DJ-friendly layered structure.
- **128 BPM**, staying in **A minor** — known note vocabulary, fits the minor-key Detroit palette.
- The foundation loop is the same known skeleton: kick on quarters, clap on 2 & 4, closed hats on beats, open hats on the `&`s.
- The APC's 8×8 grid **is** Session View: pad = clip slot, right column = scene launch, faders 1–8 = track volumes, fader 9 = Master.
- Pads obey the same **1-Bar Launch Quantization** as mouse clicks — hardware presses land musically for free.
- Lite's 8-track cap ↔ the APC's 8-wide grid: the whole project stays visible on the hardware, and the track plan was budgeted to fit.

**Where we left off:** Old projects deleted; `ticket to detroit.als` exists with the foundation drum loop on a 909-style kit at 128 BPM, launchable from the APC pads.

**Next:** **Swing/groove on the hats** — the Detroit shuffle (Path 5 territory) — then the syncopated bassline.

---

## Status — 2026-07-08 — Ordered Akai APC Mini MK2 (ships with Live Lite)

**What happened:** Ordered an **Akai Professional APC Mini MK2** — an 8×8 grid controller with 8 faders. It bundles an **Ableton Live Lite** license, so this is how we get onto Lite (no separate download hunt needed). Waiting on delivery.

**Why it fits:** The MK2's 8×8 pad grid mirrors Session View's clip grid exactly — the same grid every sketch session has used. Faders map to track volumes. First hardware in the setup: we shift from clicking clips with a mouse to **launching scenes/clips by hand**, which is the whole point of Session View.

**Next:** When it arrives → use the included code to install **Ableton Live Lite** → confirm it opens and the MK2 lights up → then start fresh (likely `techno-sketch-02` on Lite). First hands-on lesson candidate: **mapping the APC grid to Session View + launching clips from the pads.**

---

## Status — 2026-07-07 — Suite trial expired → uninstalled, moving to Lite

**What happened:** The Ableton Live **Suite** 30-day trial expired (~2026-06-27) and has now been **uninstalled** (app + all system data moved to Trash). Every project file was left untouched in `~/Music/Ableton/` — `techno-sketch-01` and its 11 backups, the `test/000` project, the User Library, and the Factory Packs.

**Plan:** Install **Ableton Live Lite** (the free tier) and restart the hands-on journey from scratch on the smaller set. Lite is a good fit — everything covered so far (Sessions 1–9 + the sketch work) is core workflow that Lite fully supports.

**What changes on Lite:**
- Lite caps the number of tracks/scenes and ships a **smaller device + sound library** than Suite — some Suite-only instruments/effects won't exist.
- Opening `techno-sketch-01` in Lite may show **missing or greyed-out devices** (anything that was Suite-only). That's expected, not a broken file — the notes and structure survive. Keep the old sketch as a **reference** and start a **fresh sketch** on Lite.

**Where the deepening plan stands:** ⏸ **Paused** at candidate #2 (**Pad / atmosphere**) — #1 (Percussion layer) is done. Resume the list once Lite is in, or fold the remaining ideas into a clean Lite sketch.

**Next:** Install Ableton Live Lite → confirm it opens → decide: continue `techno-sketch-01` (repairing any missing devices) *or* start `techno-sketch-02` fresh on Lite. Then pick the learning thread back up.

---

## Session 9 — 2026-05-29

**Topic:** **Export** the finished track as a WAV/MP3 audio file to use in Mixxx, on the SC Live 4, or share online.

**Covered:**
- [[Ableton/exporting-your-track|Exporting Your Track]] — setting the **render range** (selection on timeline ruler vs. full arrangement default), **`Cmd+Shift+R`** to open Export Audio/Video, **Render Tail** (2–4s for reverb/delay), file formats (**WAV** for DJ/archive, **MP3 320 kbps** for sharing), **44.1 kHz sample rate**, **16-bit** for DJ use / **24-bit** for archive, why to leave **Normalize OFF**, naming + saving, and dropping the file into Mixxx or onto USB for the SC Live 4.

**Key takeaways:**
- Export = render whatever's on the **Arrangement timeline** through the **Master** to a single audio file.
- Define range first: **drag on the timeline ruler** for a specific section, or **deselect** for full arrangement. Verify in dialog (Render Start / Length).
- **Always set Render Tail to 2–4 sec** if reverb/delay is used — otherwise tails get cut off.
- **WAV 44.1 kHz / 16-bit** = universal DJ-ready default. **24-bit** for archive.
- Tick **both WAV and MP3** to render both at once — Live handles it in one pass.
- **Normalize OFF** — trust your mix. Real loudness comes from mastering (limiter on Master), a later topic.
- Filename in **kebab-case** (e.g. `first-beat-2026-05-29.wav`) plays nicely with DJ software libraries.

**Where we left off:** Full end-to-end first-track workflow complete: scene → arrangement → mix → effects → export → DJ-ready file. 🎉

**Next:** With the basic loop closed, the path forks. Possible next threads (user picks):
- **Theory-Basics:** notes/scales/keys/chords — unlocks melody writing
- **Sound design:** how synths/drums actually make sound (oscillators, filters, envelopes)
- **Deeper mixing:** EQ, compression, sidechain ducking, automation, basic mastering
- **Sampling:** chopping audio with Simpler/Sampler
- **Drum-pattern depth:** variations, fills, swing/groove
- **First real track-sketch:** apply everything to make a fuller original piece in [[../Track-Sketches/Track-Sketches]]

---

## Session 8 — 2026-05-29

**Topic:** **Mixing basics** (volume, pan, mute/solo, meters, headroom) + **first effects** (Reverb, Delay) via the Device chain.

**Covered:**
- [[Ableton/mixing-basics-and-effects|Mixing Basics & First Effects]] — the mixer strip (volume fader, pan knob, mute/solo, meters), reading **dB** levels and avoiding **clipping** (red = bad), **headroom** targets (tracks −12 to −6 dB, Master −6 to −3 dB), panning rules of thumb (kick/bass center, hats can drift), Mute (`M`) / Solo (`S`), the **Device chain** at the bottom and left-to-right signal flow, **MIDI vs Audio effects**, loading from Browser → Audio Effects → preset, **Reverb** (Dry/Wet, "space" — avoid on kick/bass), **Delay** (Ping Pong, BPM-synced 1/4 or 1/8), reorder by drag, bypass with device on/off LED.

**Key takeaways:**
- Mix targets: individual tracks peak **−12 to −6 dB**, Master **−6 to −3 dB**, never red on Master.
- **Kick & bass always centered.** Width comes from hats / percussion / pads, gently.
- **Mute (`M`)** and **Solo (`S`)** are your A/B tools — non-destructive.
- The **Device chain** (bottom panel) shows everything loaded on the selected track; effects flow left → right after the instrument.
- **Always start with presets** when adding an effect — way faster than building from scratch.
- **Reverb Dry/Wet** sweet spot for most things: 15–35%. Keep it OFF kick & bass.
- **Delay** sync to 1/4 or 1/8 to lock with the BPM; Ping Pong = bounces L/R.
- Bypass via the small LED at top-left of any device for instant A/B.

**Where we left off:** Track is mixed (balanced volumes, sensible pans, small reverb on drums) — ready to be exported as an audio file.

**Next:** Session 9 — **Exporting** the track. Set the export range (loop brace), `Cmd+Shift+R` Export Audio dialog, WAV vs MP3, sample rate / bit depth, then drop the finished file into Mixxx or play it on the SC Live 4. After that we'll start branching into **deeper theory** and **sound design** as separate threads.

---

## Session 7 — 2026-05-29

**Topic:** Move into **Arrangement View** — record the Session performance onto a real timeline, edit clips, and play back the track.

**Covered:**
- [[Ableton/arrangement-view-basics|Arrangement View Basics]] — `Tab` to switch, Arrangement anatomy (timeline ruler, horizontal tracks, clip blocks, playhead, loop brace), the **Session-to-Arrangement record workflow** (Global Record + scene launch), basic editing (move/trim/duplicate `Cmd+D` / split `Cmd+E` / delete), the **Loop region** for working on a section, **Locators** (named timeline markers), and the yellow "back to Arrangement" override icon.

**Key takeaways:**
- **Arrangement View = the song timeline.** Same tracks, now stacked horizontally; clips are blocks positioned in time.
- **Capture flow:** Stop everything → hit **Global Record** (red circle in Transport) → launch a Session scene → perform → Stop → `Tab` to Arrangement = your performance is now on the timeline.
- **Launch Quantization still applies during recording** — scene jumps land on bars.
- **Editing:** drag body = move, drag edge = trim, `Cmd+D` = duplicate, `Cmd+E` = split at playhead, `Delete` = delete.
- **Loop region** (bracket above ruler) + loop toggle in Transport = focus playback on a section.
- **Locators** = named markers (Intro, Drop, Break) — click name to jump.
- If Session takes over a track during Arrangement playback, the **yellow icon** at the top returns control to Arrangement.

**Where we left off:** First real song timeline captured — performed Intro/Drop/Break into Arrangement and can play it back.

**Next:** Session 8 — basics of **mixing** (track volume balance, panning, mute/solo) + first taste of **effects** (reverb / delay on a track), then **exporting** the track to a WAV/MP3 file you can share or DJ with.

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
