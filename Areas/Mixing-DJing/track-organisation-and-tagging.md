---
title: Track Organisation & Tagging (my approach for Engine DJ)
date: 2026-06-07
tags: [dj, mixing, organisation, tagging, engine-dj, genre, crates]
---

# Track Organisation & Tagging

My honest, considered opinion on how to organise a DJ library to optimise mixing sessions — written for a **small, eclectic, just-starting** library played on a **Denon controller via Engine DJ**, exporting to USB/SD. Captured from a working session on 2026-06-07 so I can come back to it.

> TL;DR: **Tags first, not mood folders.** Get BPM, key, genre and energy right, then let Engine's *Smart Lists* do the sorting. Don't build a "build / drop" folder tree — it's premature and you'll outgrow it.

---

## 1. Why I'd skip "build / drop / vibe" folders

It's a tempting idea, but I wouldn't do it — at least not now:

- **A track isn't one mood.** Most tracks contain an intro, a build, a breakdown, a drop and an outro *inside the same file*. Filing the whole thing under "drop" throws that away, and you'll second-guess every track.
- **It doesn't scale and it's subjective.** With a small library, mood bins are half-empty and arbitrary. In a year you'd be fighting the folder tree.
- **The thing it's reaching for — "how energetic is this, where in a set does it belong" — belongs as a *number on the track*, not a folder.** As a number you can filter it flexibly; as a folder it's a one-way box.

## 2. What actually makes a session smoother

The two things that decide whether two tracks *can even be mixed* are **BPM** (tempo) and **key** (harmonic compatibility — the Camelot wheel). An eclectic library is all over the map on both, so the #1 job isn't mood — it's **making compatible pools easy to find**. Mood/energy is a refinement you apply *after* you've got tracks that fit together at all.

**Foundation, in order:**

1. **BPM** — Engine analyses this itself on import. ✅ Don't hand-tag it.
2. **Key (musical + Camelot)** — Engine analyses this too. ✅ Set Engine to display Camelot for harmonic mixing.
3. **Genre** — Engine does **not** generate or refine this; it only *reads* the `genre` tag. ⚠️ **This is the one we own.** See §4.
4. **Energy (1–10)** — there's no native Engine field, so store it in the **comment** (e.g. `E7`) or repurpose the **star rating**. Then Smart Lists can filter on it.

## 3. How to use Engine DJ (tool by tool)

Use each tool for what it's good at, and **don't try to organise the Collection itself**:

| Tool | Use it for |
|---|---|
| **Collection** | The whole `~/Music/Library`, imported. The flat archive. Don't organise here. |
| **Smart Lists** | The workhorse — rule-based, auto-updating. e.g. *"House · 120–125 · energy ≥ 7"* hands you peak-time house instantly and maintains itself. **This is the flexible version of a "drop folder."** |
| **Playlists** (manual, ordered) | A *set*. Warmup → peak → cooldown. Order matters. **This is what you export to USB/SD.** |
| **Crates** (a few, broad) | Digging bins by vibe you flip through live — e.g. `Deep/Minimal`, `Trance/Prog`, `Leftfield/Bass`. Three or four, not twenty. |

## 4. Genre — the part Engine can't do for you

Engine only reads the `genre` tag, so good genre crates depend entirely on what's written into the files. Decisions made:

- **Source: Discogs *styles***, not MusicBrainz (whose genres are weak for electronic music). Discogs styles are the granular sub-genres crates need.
- **Format: all styles, comma-joined**, e.g. `House, Deep House, Minimal`. Richest for filtering — a Smart List with `genre contains "Minimal"` *or* `contains "Deep House"` both catch it.
- This is wired into the `[[../Claude/Skills/Docs/download-music|/download-music]]` skill: **`tags genre`** (genre-only) refines just the genre from Discogs and leaves the descriptive tags alone — the right tool for a library that's already cleanly tagged.
- Obscure bootlegs / white-labels often won't match Discogs — set those by hand.

## 5. The thing that beats any folder scheme: track prep

For smoothness, **cue points and loops** do more than any organising system. In Engine, drop a few hot cues per track (intro, first downbeat, breakdown, the drop, outro) and maybe a loop. Live, you're not hunting — you hit a cue and you're in. Prioritise this over an elaborate structure.

## 6. Concrete starting plan

1. **Tag the library** — Engine handles BPM/key on import; we add **genre** (Discogs styles) and an **energy** number (comment/rating).
2. **In Engine:** 3–4 genre crates · 2–3 Smart Lists (BPM band + energy) · one `Set – <date>` playlist you're actively building and will export.
3. **Hot-cue the 10–15 tracks** you most want to mix first.

The trap at this stage is over-building the system while the library is tiny. Tags + a couple of Smart Lists scale far better than a folder tree.

---

## 2026-06-30 — The system I actually built

Put the plan above into practice on the real Engine collection (~277 tagged tracks). Reference for how it's set up so I don't have to rederive it.

**The key principle (don't forget this):** two separate layers.
- **Disk (`~/Music/Library/<Artist>/…`) = storage only.** Kept by artist on purpose — stable, multi-genre-safe, keeps the verbatim label/catalog folder names, and Engine stores paths relative to it. **Never reorganise the disk by genre/mood** (genre is multi-valued, it'd break Engine paths and split artists). The "too many artist folders" feeling is a Finder problem, and I almost never browse in Finder.
- **Engine DJ = the finding layer.** All mood/genre/energy browsing lives here, in Smart Playlists driven by the tags — non-destructive, and a track can sit in many lists at once.

**Cleanup done:** Engine had auto-created ~215 playlists that just mirrored the artist/release folders (and 0 smart playlists) — the folder sprawl copied inside Engine. Deleted the ~82 top-level artist playlists (children went with them). **Deleting a playlist never touches the tracks or files** — everything stays in *Collection*. Engine has no multi-select for playlists, so it's one-by-one (or edit the DB with a backup).

### Layer 1 — Genre families (Smart Playlists, automatic)

Rule = `Genre · contains · <word>`; for two-word ones set **Match ANY**. Counts as of 2026-06-30. Built once, every future import self-files the moment its genre tag is written. Overlap between lists is fine and intended (e.g. *Progressive House* shows in both House and Trance-adjacent).

| Smart Playlist | Rule | ~Tracks |
|---|---|---|
| **Techno** | contains `Techno` | 173 |
| **Techno — Dub** | contains `Dub Techno` | 10 |
| **Techno — Minimal** | contains `Minimal` | 21 |
| **Techno — Hard / Industrial** | ANY: `Hard Techno` / `Industrial` / `Raw` / `Hard Groove` / `EBM` / `Peak Time` | ~25 |
| **House** | contains `House` | 93 |
| **Trance** | contains `Trance` | 34 |
| **Ambient / Downtempo** | ANY: `Ambient` / `Downtempo` | ~24 |
| **Hip-Hop / Cloud Rap** | ANY: `Cloud Rap` / `Trap` | 19 |
| **Dubstep / Bass** | contains `Dubstep` | 19 |
| **Experimental** | contains `Experimental` | 16 |
| **Electro** | contains `Electro` | 14 |
| **Acid** | contains `Acid` | 13 |
| **Soul & Pop** | ANY: `Soul` / `Synth-pop` | 3 (classics — will grow; for mixing with techno) |
| **New** *(utility)* | `Date Added · in the last · 30 days` | — |

`Techno` (173) is the bulk; the `Techno — …` names keep the sub-textures grouped next to the parent. The remaining ~123 are "straight" techno, still findable under the parent.

**Coverage check (2026-06-30):** 274 of 277 tagged tracks land in a family, 0 tracks have an empty genre. The only 3 outside were non-dance (Johnnie Mae Matthews ×2 *Northern Soul, Soul*; Sophia Stel *Synth-pop*) → grouped into **Soul & Pop** rather than misfiled into a dance list.

### Layer 2 — Mood / texture / energy (manual, the part genre can't do)

Genre can't say "dark / hypnotic / emotional". A small controlled vocabulary goes in the **Comment** field as hashtags → Smart Playlist rule `Comment · contains · #tag`. (Checked first: the Comment field only held low-value scene notes like "24/48 Vinyl Recording" — no key/energy data, safe to use; append works fine for "contains".)

| Energy (1 per track) | Texture / feel (1–2 per track) |
|---|---|
| `#warmup` · `#peak` · `#closer` | `#dark` `#hypnotic` `#emotional` `#dubby` `#vocal` `#tool` |

**This is manual and gradual** — mood is heard, not deduced. Tag tracks while auditioning / prepping a set, not all at once. **Start small:** make `#peak`, `#dark`, `#hypnotic`, `#emotional` first and tag a batch of tracks I know well; add the rest once the habit sticks.

---

## 2026-07-01 — Collect vs. play, and hot cues

### Collect ≠ play — the working set

The trap once the library grows: loving a track isn't a reason to play it in a set. Pros play from a small selection they know cold, not the whole library. Separate the two:

- **Collect freely → `New`.** Everything that grabs me lands in the `New` smart playlist (Date Added · last 30 days). No decision here, just capture — 300+ is fine.
- **Promote by auditioning *in the mix*.** A track only earns a spot once I've actually mixed it and it does a job nothing else does (this energy / this key bridge / this moment). If two do the same job, the better one wins for that set.
- **`Current` — the working crate.** Make it as a **normal Playlist in Engine** (not a smart one): 40–60 tracks I'm actively playing and know cold (where it breaks, what it mixes into). Sets come from here. Refresh ~monthly; everything else stays in the library ready for its turn.
- **⭐ rating = floor-tested.** Star the ones that have worked on a real floor, so the cream rises to the top of any list.

Rule that frees you: **you'll play ~10% of the library 90% of the time** — that depth beats a big pile.

**Flow:** `New` (capture) → audition in the mix → `Current` (working crate) → per-set playlist (e.g. `Set – <date>`).

### Hot cues — where to place them

Cues only work if the **beatgrid is correct first** (bad grid → cues drift, fix it before cueing). **Golden rule:** put every cue on the **first beat of a phrase** (the "1" of an 8- or 16-bar section), snapped to the grid — so when I drop or jump, both tracks' phrases line up.

The 3–4 that actually earn their place (house/techno):

1. **Intro / first solid kick** — where the beat truly starts; for dropping in time with the track already playing.
2. **Breakdown** — where it strips back / drops the kick; to anticipate it or jump there.
3. **Drop / groove return** — where the energy comes back after the breakdown.
4. **Mix-out** — the phrase where I start pulling this track and bringing in the next.

Don't over-cue: 3–4 on the "1" beat 8 messy ones. Start with just **intro + breakdown** — the two that save you live.

---

## Related

- [[Mixing-DJing]] — area index
- [[../Claude/Skills/Docs/download-music|/download-music skill]] — now refines genre from Discogs styles (`tags genre`)
- [[Resources/Mixing-DJing/Genre-Studies/Genre-Studies|Genre Studies]] — genre breakdowns & BPM/key cheatsheets
- [[Tracklists/Tracklists|Tracklists]] — where prepared sets live

> **Gear:** Denon DJ **SC LIVE 4** (standalone, Engine OS) + **Engine DJ desktop** for library prep and USB/SD export.
