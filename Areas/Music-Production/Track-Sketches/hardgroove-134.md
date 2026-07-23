---
title: Hardgroove 134
date: 2026-07-16
tags: [ableton, track-sketch, techno, hardgroove, drift, live-lite]
---

# Hardgroove 134

The third track sketch. [[ticket-to-detroit|Ticket to Detroit]] is **parked** (not abandoned) — this is a deliberate fresh start with a different aesthetic and a stricter build discipline: everything hand-built in Ableton's UI, no programmatic DAW control of any kind for this project.

## Stats

| | |
|---|---|
| **Project** | *(to be saved — new .als, Live Lite)* |
| **BPM** | 134 |
| **Key** | C major *(nominal for now — kick/sub don't care about key; matters once STAB/LEAD and ATMOS arrive)* |
| **Goal** | Hardgroove techno — rolling, percussive, relentless low end; tight and dry, no reverb wash |
| **Setup** | Live Lite (8-track cap) + hardware controller — parts played in, not drawn, wherever it makes sense |
| **Build rule** | 100% hand-built in Ableton's UI. No Producer Pal, no MCP, no programmatic control — the point is to learn the interface directly |

## Track budget (fits Lite's 8 tracks)

| # | Track | Role |
|---|---|---|
| 1 | **KICK** | Drift → Saturator → EQ Three |
| 2 | **SUB** | Drift → EQ Three |
| 3 | **PERC** | Drum Rack — all percussion lives here |
| 4 | **HATS** | — |
| 5 | **STAB/LEAD** | — |
| 6 | **ATMOS** | — |
| 7 | **FX/RISER** | — |
| 8 | **RETURN** | shared return track |

## Devices allowed

Stock Lite only: **Drift, EQ Three, Saturator, Compressor, Drum Rack, Simpler**. No Operator, no Wavetable, no EQ Eight, no third-party plugins.

**Confirmed 2026-07-22 against Ableton's official Live 12 Lite Features page:** this is a deliberate creative subset, not Lite's actual technical ceiling. Lite genuinely also includes Impulse (instrument) plus Channel EQ, Reverb, Delay, Auto Filter, Auto Pan, Beat Repeat, Chorus-Ensemble, Gate, Limiter, Looper, Phaser-Flanger, Tuner, Utility (effects) — all left out of this project on purpose. Operator/Wavetable/EQ Eight, however, are genuinely absent from Lite (Standard/Suite only) — that part of the rule reflects a real limitation, not a choice.

## Weeks 1–2 goal

Rebuild the low end from zero in Drift — **just KICK and SUB, nothing else yet**. The point is understanding Drift's synthesis parameters deeply, not finishing a track. Target: **3 distinct 8-bar kick+sub loops**, each with its own character, that groove on their own with nothing else in the mix.

- **KICK:** single sine, short pitch envelope for the thump/click, amp envelope tuned for punch. Four-on-the-floor, C1, velocity 120.
- **SUB:** pure sine, no pitch envelope, full sustain, EQ Three killing everything above ~180Hz. Offbeat pattern interlocked with the kick, C1, 8th-note duration.
- **Sidechain:** SUB ducks against KICK via Compressor.

## Session log

### 2026-07-16 — Kickoff

- Pivoted from Ticket to Detroit to a fresh sketch with new constraints: hardgroove techno at 134 BPM, strict hand-built-only workflow.
- New project set up: 134 BPM, C major, Session view.
- Track 1 renamed **KICK**, Drift loaded, oscillator isolated to a single plain sine (Osc 2 / Sub / Noise off) — first checkpoint before touching the pitch envelope.

**What's next:** the pitch envelope on the kick (short decay routed to pitch → the thump/click transient), then the amp envelope, Saturator, EQ Three. Then mirror the process for SUB.

### 2026-07-17 — KICK patch complete

- Full recipe documented in [[../Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] — worth reading in full; summary below.
- Debugged a real mix-up: Drift's **Pitch Mod** (oscillator pitch) and **Freq Mod** (filter cutoff) both default to sourcing "Env 2" and look similar — the first "click" heard was actually the filter popping (Freq Mod), not a true pitch drop, since Pitch Mod's amount was still 0%. Fixed by raising Pitch Mod instead and zeroing Freq Mod.
- Chased a subtle periodic volume drift down through: Envelope 1 Attack (ruled out — a fixed value can't be periodic) → LFO Rate in Hz vs. tempo-synced (switched to `1:1`) → the global **Drift** macro (zeroed) → finally the **Mod tab**'s actual Mod Matrix, likely an LFO→Volume routing at a tiny amount (sine-shaped, hence the "sine wave" loudness swell across loop repeats).
- **Envelope 1** confirmed as Drift's hardwired Amp Envelope (no Mod Matrix routing needed) — Attack ~0.5ms, Decay 175ms, Sustain 0%, Release 600ms (irrelevant since Sustain is 0).
- **Envelope 2** final shape (drives Pitch Mod): Attack 0ms, Decay 30ms, Sustain 0%.
- **Saturator** added: Analog Clip, Drive ~4dB — result: thicker but noticeably sharper (added harmonics extend upward as well as adding low-mid weight — expected, not a mistake).
- **EQ Three** added: FreqLow 50Hz, GainLow -1.81dB, Slope 48, Mid/High untouched — cleaned up sub-rumble below what the kick needs (reserving deep low end for SUB) without losing punch. Confirmed sounding "groovier."
- **KICK chain is now complete: Drift → Saturator → EQ Three.**

**What's next:** Mirror the whole process for **SUB** — pure sine, no pitch envelope, full sustain, EQ Three killing everything above ~180Hz, offbeat pattern interlocked with the kick. Then sidechain SUB to KICK, then build out the 3 target 8-bar loop variations.

### 2026-07-17 — SUB built, interlock + sidechain done

- **SUB** patch built mirroring KICK: Drift isolated to a single sine, no Pitch/Freq Mod, Envelope 1 set for full sustain (Attack ~0-5ms, Decay irrelevant, Sustain 100%, Release ~50-100ms), EQ Three killing Mid+High bands entirely (crossover at 180Hz) — pure sub tone confirmed.
- **Kick/sub interlock pattern** placed — straight 8th-note grid, **no swing** (this project's groove comes from placement/velocity only, per the original brief):

```
         1 & 2 & 3 & 4 &
Kick   : ● · ● · ● · ● ·
Sub    : · ● · ● · ● · ●
```

- Kick notes: 8th-note length (doesn't matter much — Sustain 0% self-terminates). Sub notes: 8th-note length is *load-bearing* here (Sustain 100% means note length is the only thing controlling duration). Velocity 120 on both for now.
- **Sidechain** wired: Compressor on SUB, sidechained from KICK (Post FX), SC Filter ~80Hz to focus the trigger on the kick's thump. Threshold -28.8dB, Ratio 8.4:1, Attack 0.01ms, Release 137ms, RMS detection. Confirmed by ear: the sub swells up into each hit rather than sounding static or choked — see [[../Techniques/kick-sub-interlock-sidechain|Kick/Sub Interlock as a Sidechain Groove Tool]] for why this works (Release timing shapes the swell since the two never actually overlap).
- **All of the Weeks 1–2 workflow (steps 1–4) is now done.**

**What's next:** Build out the **3 distinct 8-bar kick+sub loops**, each with its own character — the final target for this phase, using velocity variation and placement tweaks (not swing/FX) as the differentiation tools.

### 2026-07-17 — 3 loop variations done — Weeks 1–2 goal complete 🎉

- Built all three target loops from one duplicated 8-bar clip — see [[../Techniques/loop-character-variations|Loop Character Variations (Placement-Only)]] for the general technique:
  - **Loop 1 — Straight Roller:** the base interlock, unedited, all 8 bars — its character is the unwavering repetition.
  - **Loop 2 — Rolling Push:** added sub hit on the `a` of beat 3 in bars 4 and 8 — a 16th-note anticipation into the phrase-ending kick. Confirmed: swells audibly via the sidechain, reads as "rolling."
  - **Loop 3 — Stripped/Hypnotic:** removed the sub hit on beat 3's `&` in bars 2, 4, 6, 8 — sparser, more space, clear contrast against Loop 1.
- **This closes out the entire original Weeks 1–2 goal:** KICK ✅, SUB ✅, interlock ✅, sidechain ✅, 3 distinct 8-bar loops ✅ — all built entirely by hand, no programmatic control, one parameter/concept at a time.

**What's next:** Open — the low end is done and grooving on its own. Next phase moves into the rest of the 8-track budget: **PERC** (Drum Rack, all percussion), then **HATS**, building outward from the kick/sub foundation.

### 2026-07-18 — Free Drift exploration on KICK

- Explored the LFO as a **second, independent transient layer** on top of the existing pitch-envelope click, routed to Filter Freq via the Mod tab (not the LFO tab's local Amount/Mod, which is just an internal send). Retrigger on, tried Sine vs. **Saw Down** (chose Saw Down — behaves like an actual one-shot decay rather than a symmetric up/down wobble). Rate tested at 999Hz (read as texture/buzz — audio-rate) vs. **30–80Hz** (read as a shaped hit) — the latter preferred. Full writeup: [[../Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] §7.
- Continued experimenting further down the chain: added a **non-sidechain Compressor** after EQ Three (Peak detection, Attack ~3-10ms to let the transient spike through before clamping, fast Release, moderate ratio, Makeup to restore level) for glue/punch. Also tried a **+2-3dB boost on EQ Three's Mid band** for presence — flagged that this band spans a wide range (50Hz–2.5kHz on this build), so it's a broad thickening move, not a surgical "click" boost; Saturator/Drive is the better tool if a narrower click is wanted instead.
- Both applied; sonic verdict not yet logged in detail — pick up from here next time if refinement is wanted.
- **Depth fix:** dropped Osc 1's **Oct to -2** — confirmed noticeably deeper, the direct fix for "too high" (EQ/Saturator alone can't add a missing fundamental).
- **Debugged inconsistent hit-to-hit sound** (uneven Compressor GR curves, kick audibly "kicking differently" each hit): ruled out Drift's instability macro (0%), Auto Release (off), external sidechain (off), and velocity (confirmed uniform across all notes) one by one. Concluded the likely remaining cause is **Drift's oscillator phase not resetting per note** — a separate mechanism from the LFO's own Retrigger (which only resets the LFO, not the oscillator) — consistent with Drift being an analog-modeled oscillator that free-runs continuously, like real hardware. **Decision: kept as-is** — this reads as raw/alive character fitting the hardgroove aesthetic rather than a bug to fix. Full diagnostic trail: [[../Techniques/drift-kick-from-scratch|Building a Kick From Scratch in Drift]] §8.
- Confirmed: Ableton Live (any edition) has no native autotune/pitch-correction device, and **Live Lite doesn't support third-party VST/AU plugins at all** — moot for this project anyway given the stock-devices-only rule, but worth knowing for future reference.

**What's next:** Continue outward into the rest of the 8-track budget — **PERC** (Drum Rack) is the next planned layer, then **HATS**.

### 2026-07-21 — PERC — Drum Rack basics + placement plan

- New concept: [[../Ableton/drum-rack-anatomy|Drum Rack Anatomy]] — building the rack from **empty** (not a preset kit), each pad a nested Simpler, why one Drum Rack track solves the Lite 8-track squeeze for a multi-sound percussion layer. Choke groups flagged for later (HATS, where open/closed hat actually needs one).
- Worked out where PERC's hits go: **KICK (quarter beats) + SUB (the "&" 8ths) already claim every 8th-note pulse between them** — the two interlock so tightly there's no 8th-note gap left. PERC's whole role is the leftover **16th-note `e`/`a` slots**:

```
              1 e & a 2 e & a 3 e & a 4 e & a
Kick        : ● · · · ● · · · ● · · · ● · · ·
Sub         : · · ● · · · ● · · · ● · · · ● ·
Perc (opt A): · ● · ● · ● · ● · ● · ● · ● · ●    ← continuous 16th shimmer
Perc (opt B): · · · · · · · ● · · · · · · · ●    ← sparse accent (a-of-2, a-of-4 only)
```

- Two starter placement options given, genre-neutral: **Option A** (continuous 16th, shaker-style, reuses the exact logic from [[../Techniques/percussion-layering|Percussion Layering]]) vs. **Option B** (sparse 2-hit accent, rim/clave-style punctuation). Homework is to pick one (or build both on separate pads) and judge by ear.

**What's next:** Homework — build the PERC track: empty Drum Rack, drag 1-2 one-shot samples onto separate pads, trim Start/Length, place hits per Option A or B above. Confirm the groove, then move to **HATS**.

### 2026-07-22 — PERC built + HATS kicked off

- **PERC built:** Rim DMX Lo Fi on C1 (Option B — sparse accent), a Shaker layered in via a second pad + a simultaneous note in the piano roll (not a shared key — direct drag onto an occupied pad was confirmed to **replace**, not layer, so two separate pads triggered at the same clip position is the reliable layering method). EQ Three high-pass added (FreqLow ~150-200Hz + the **"L"** cut button — FreqHi was a dead end, it's the Mid/High crossover and can't reach low enough) plus a touch of Saturator for grit.
- Debugged along the way: found the **Key Range** editor lives behind the **I/O** toggle in the Chain List (not a dedicated "Zone Editor" as first guessed) — see [[../Ableton/drum-rack-anatomy|Drum Rack Anatomy]] for the corrected writeup.
- **HATS kicked off:** new concept, **Choke Groups** — makes two independent one-shot chains (closed/open hi-hat) replicate the real physical constraint of a hi-hat (only one can ring at a time). Pattern handed off as homework: closed hat doubles KICK's quarter-note positions, open hat doubles SUB's `&` positions — safe to overlap in time since hats live in a totally different frequency register (reapplies [[../Techniques/open-vs-closed-hihat|the known offbeat-hat pattern]], now proven-safe to stack on already-occupied beats via frequency separation rather than needing a free time slot like PERC did).

**What's next:** Homework — build the HATS track (new Drum Rack, closed + open hat one-shots, same Choke Group), draw the pattern, confirm the open hat's tail gets cut cleanly. This closes out the full rhythmic skeleton (KICK/SUB/PERC/HATS) — **STAB/LEAD** next.

- **Confirmed working:** Choke Group cuts the open hat's tail cleanly against the next closed hat hit. Full rhythmic skeleton (KICK/SUB/PERC/HATS) now built and playing together.
- **Deliberate pause before STAB/LEAD:** rather than moving straight on to the next track, the user wants a deeper sound-design pass on the layers already built — going for more depth/character before adding anything new.
- **Simpler's internal Filter applied to both hats:** Low Pass, Frequency swept down to just before losing the "tss", a touch of Resonance for color. Confirmed working on both closed and open hat.
- **Caught mid-session, by the user:** the Filter/Vol "< Vel" modulation amounts only do anything if velocity actually varies note-to-note — a flat velocity input means the modulation multiplies by the same constant every hit, nothing audible changes. Applied velocity groove to the HATS pattern (closed hats varied ~90-110, open hat accents boosted ~115-120) so the Vel-modulation actually has something to work with.
- **Full ensemble listening pass** — KICK/SUB/PERC/HATS heard together for the first time with all this layer-depth work applied: checked pan spread, level balance, and frequency masking via solo/mute A-B. **Confirmed sounding great — the best-sounding sketch of the project so far.**

### 2026-07-22 — Sampling detour: capturing a found-audio fragment

- Before moving to STAB/LEAD, a deliberate side-experiment: sampling a short dialogue+music fragment from an external video source, to try Simpler's **Slice** mode on real found material rather than a clean library one-shot.
- **New capture method learned:** recording external/system audio directly into Live via a **BlackHole** loopback + Multi-Output Device (Mac), landing as a normal Audio track clip — see [[../Ableton/sampling-with-simpler|Sampling with Simpler]] for the full setup. Confirmed working; captured into Arrangement (via the transport Record button, not a Session clip slot).
- Clip successfully dragged into a **Simpler** on a new MIDI track. **Slice mode** (transient-based vs. equal-division chopping) was introduced as the next tool but **not yet applied** — the user chose to pause here and pick this back up later rather than continue now.
- Open question for next time: slice the dialogue+music mix as-is ("found" character), or separate voice from music first (Live 12 Suite/Standard's native stem-extraction, unconfirmed on Lite; otherwise a web-based stem separator) for cleaner individual slices.

**Where we left off:** Sampling experiment proven end-to-end (capture → Simpler) but parked before the creative chopping stage. Rhythmic skeleton (KICK/SUB/PERC/HATS) remains the finished, confirmed-good part of the sketch.

### 2026-07-22 — Key reconsidered to C Phrygian + STAB built from scratch

- **Key changed:** C major (nominal) → **C Phrygian** — a darker/more tense mode fitting the raw/industrial direction, deliberately chosen now that a tonal layer (STAB) finally makes key matter. Root stays C, consistent with kick/sub's existing C1. New theory: [[../Theory-Basics/phrygian-mode|The Phrygian Mode]].
- **Device-list correction:** confirmed against Ableton's official Live 12 Lite page that this project's "stock devices only" list was a deliberate creative subset, not Lite's real ceiling — see the updated "Devices allowed" section above. Also set a new **4-month goal** (through ~Nov 2026, tracked in [[../Roadmap|Roadmap]]) to explore everything Lite actually offers before upgrading.
- **STAB built from scratch in Drift** — full recipe: Voices 32, Osc 1 Square (isolated), Envelope 1 shaped for a stab (not pad), Low Pass filter **Type I** (12dB/oct, grittier DFM-1 circuit) at ~900Hz. Chord: **Cm(b9), no root, no 7th** — Eb3-G3-Db4, the leanest of four voicings compared. Placed at the `a` of beat 3 (one hit per bar), the only genuinely free slot left once kick/sub/perc/hats were accounted for. Full recipe: [[../Techniques/drift-stab-from-scratch|Drift Stab From Scratch]].
- **Confirmed sounding good** by the user on first listen.

**Where we left off:** STAB built and confirmed. Rhythmic skeleton + STAB now playing together. LEAD (the other half of this track's shared "STAB/LEAD" slot) intentionally deferred.

**Next:** Open — refine/add a second stab hit if it feels sparse, consider the LEAD half of this track slot, resume the sampling detour, or move to **ATMOS**.

### 2026-07-22 — STAB FX exploration — Auto Filter movement

- Before adding a second STAB hit or moving to LEAD, a deliberate detour: layering movement/texture effects onto the STAB chain, starting with a genuinely new device.
- **Auto Filter** introduced — an effects-chain filter (separate from Drift's own internal Low Pass) with its own LFO section, able to add rhythmic cutoff *movement* on top of the STAB's already-set static tone. Full recipe: [[../Techniques/auto-filter-movement|Auto Filter Movement]].
- Recipe handed off: Auto Filter after Drift in the STAB chain, Low Pass type, Frequency centered near Drift's own ~900Hz cutoff, LFO Sync on at 1/16 or 1/8, moderate Amount, Sine wave to start — A/B against Amount at 0.
- Flagged, not yet taught: **Chorus-Ensemble** (width via modulated delays) and **Phaser-Flanger** (sweeping comb-filter movement) as further options to compare in this same exploration arc.

**Where we left off:** Auto Filter recipe handed off as homework — not yet added/confirmed in the project.

**Next:** Homework — add and tune Auto Filter on STAB, confirm by ear. Once the movement layer feels settled (possibly after also trying Chorus-Ensemble/Phaser-Flanger), move to the STAB variation (second hit) — then **LEAD**.

### 2026-07-22 — STAB FX round 2 — Chorus-Ensemble + Phaser-Flanger

- **Auto Filter confirmed sounding good** on STAB. Side question answered: it's called "Auto" because the filter moves *by itself* via its own internal LFO, as opposed to hand-automating a knob or drawing a clip envelope (the riser technique) — same destination, different mechanism.
- Two more movement effects introduced in the same exploration arc: [[../Techniques/chorus-ensemble-width|Chorus-Ensemble Width]] (pitch/time thickening — a different axis than Auto Filter's cutoff movement) and [[../Techniques/phaser-flanger-sweep|Phaser-Flanger Sweep]] (notch sweep vs. delay+feedback sweep).
- **Stacking discussed directly:** three independent LFO-driven effects (Auto Filter + Chorus-Ensemble + Phaser-Flanger) on one STAB voice risks mush against this project's "tight and dry" goal. Recommendation given: keep Chorus-Ensemble alongside Auto Filter on STAB (complementary axis), reserve Phaser-Flanger's more dramatic sweep for **LEAD** instead — not yet decided/confirmed by the user.

**Where we left off:** Chorus-Ensemble and Phaser-Flanger recipes handed off; not yet auditioned in the project.

**Next:** Homework — try both on STAB (A/B'd solo against Auto Filter alone), decide what stays vs. what's reserved for LEAD. Then the STAB variation (second hit) — then **LEAD**.

### 2026-07-23 — STAB FX decision — Chorus-Ensemble kept

- Both effects auditioned. **Decision: Chorus-Ensemble stays** on STAB, confirmed by ear. Phaser-Flanger tried but not kept here — reserved for **LEAD** instead, per the earlier trade-off discussion (its more dramatic sweep suits an exposed melodic line better than a background chord stab).
- **STAB chain finalized for now: Drift → Auto Filter → Chorus-Ensemble.**

**Where we left off:** STAB fully done — chord, tone, and two confirmed movement layers.

**Next:** A second STAB hit if it still feels sparse — otherwise straight to **LEAD**, where Phaser-Flanger is already queued as a first thing to try.

### 2026-07-23 — LEAD kickoff — solving the shared STAB/LEAD track

- STAB variation (second hit) explicitly **deferred** — the user wants to hold all such variations until building out more tracks and preparing the full Arrangement, rather than doing it now. Moving straight to **LEAD**.
- Real constraint surfaced: track 5 was budgeted **STAB/LEAD** together from kickoff, and Lite's 8-track cap is already fully spent — LEAD can't get its own track.
- **Solution: Instrument Rack + Key Zones**, new concept: [[../Ableton/instrument-rack-key-zones|Instrument Rack Key Zones]] — a plain Instrument Rack is the general form of a Drum Rack (already known), letting several distinct melodic chains share one track split by note range via the same I/O Key Range editor.
- Plan handed off: group STAB's existing Drift → Auto Filter → Chorus-Ensemble into Chain 1 (key-zoned to its current register, ~C1–B4); build a new Drift patch → Phaser-Flanger as Chain 2, key-zoned above it (C5+), reusing the known "lead sits on top" register-lane rule.
- LEAD patch/motif itself reuses already-known building blocks (mono voice, ADSR shaping, call-and-response motif writing from [[../Techniques/bleep-lead-motif|Bleep Lead & Motif Writing]]) rather than re-teaching them — the new content this session is entirely the *track-sharing* mechanism, not melody-writing basics.

**Where we left off:** Concept + plan handed off; Instrument Rack not yet built.

**Next:** Homework — build the Instrument Rack (2 chains, key-zoned), the LEAD Drift patch, and a short motif in C Phrygian.

**Update, same day — `Cmd+G` gotcha on step 1:** selecting the Drift *track header* and pressing `Cmd+G` created a **Track Group** (track-list folder), not a Rack — confirmed directly (new "Group" track appeared, Drift unchanged on its own track, no space saved). Corrected: a Rack only forms when the *devices* are selected inside the track's Device View first. [[../Ableton/instrument-rack-key-zones|Instrument Rack Key Zones]] updated with this distinction.

**Where we left off:** Track Group needs undoing; correct device-selection method handed off, not yet executed.

**Next:** Ungroup the Track Group, select Drift + Auto Filter + Chorus-Ensemble in the Device View, `Cmd+G` there to form Chain 1, then build Chain 2 (LEAD).

**Update, same day — Chain 1 confirmed:** Drift + Auto Filter + Chorus-Ensemble successfully grouped into an Instrument Rack via the corrected method (devices selected in Device View, not the track header) — this is Chain 1 (STAB), on the original track, no new track spent.

**Next:** Open the Rack's Chain List, drag in a second instrument to form Chain 2 (LEAD), set both chains' Key Ranges via I/O, then build the LEAD Drift patch.

**Update, same day — Chain 2 created, Key Range mechanic corrected:** second Drift dropped into the Chain List, forming Chain 2 (LEAD) alongside Chain 1 (STAB). Real gotcha: unlike Drum Rack, a plain Instrument Rack's Chain List has **no I/O button** — Key Range is exposed directly via the **Key** toggle (next to Vel / Chain / Hide). Confirmed on this Live 12 Lite build. [[../Ableton/instrument-rack-key-zones|Instrument Rack Key Zones]] corrected in place.

**Where we left off:** Both chains exist; Key Ranges not yet dragged into place.

**Next:** Click Key, drag STAB's chain low and LEAD's chain high (non-overlapping), then build the LEAD Drift patch inside Chain 2.
