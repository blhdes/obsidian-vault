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
- This is wired into the `[[../Claude/Skills/download-music|/download-music]]` skill: **`tags genre`** (genre-only) refines just the genre from Discogs and leaves the descriptive tags alone — the right tool for a library that's already cleanly tagged.
- Obscure bootlegs / white-labels often won't match Discogs — set those by hand.

## 5. The thing that beats any folder scheme: track prep

For smoothness, **cue points and loops** do more than any organising system. In Engine, drop a few hot cues per track (intro, first downbeat, breakdown, the drop, outro) and maybe a loop. Live, you're not hunting — you hit a cue and you're in. Prioritise this over an elaborate structure.

## 6. Concrete starting plan

1. **Tag the library** — Engine handles BPM/key on import; we add **genre** (Discogs styles) and an **energy** number (comment/rating).
2. **In Engine:** 3–4 genre crates · 2–3 Smart Lists (BPM band + energy) · one `Set – <date>` playlist you're actively building and will export.
3. **Hot-cue the 10–15 tracks** you most want to mix first.

The trap at this stage is over-building the system while the library is tiny. Tags + a couple of Smart Lists scale far better than a folder tree.

---

## Related

- [[Mixing-DJing]] — area index
- [[../Claude/Skills/download-music|/download-music skill]] — now refines genre from Discogs styles (`tags genre`)
- [[Genre-Studies/Genre-Studies|Genre Studies]] — genre breakdowns & BPM/key cheatsheets
- [[Tracklists/Tracklists|Tracklists]] — where prepared sets live

> **Gear:** Denon DJ **SC LIVE 4** (standalone, Engine OS) + **Engine DJ desktop** for library prep and USB/SD export.
