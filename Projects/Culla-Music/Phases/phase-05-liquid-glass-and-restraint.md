---
title: Phase 5 — Liquid Glass & the Restraint Pass
date: 2026-05-25
tags: [culla-music, phase, design, liquid-glass, swiftui, minimalism, artist-hub, implemented]
status: implemented (builds clean against iOS 26 SDK; on-device polish ongoing)
---

# Phase 5 — Liquid Glass & the Restraint Pass

> **Status (2026-05-25):** Merged on `main`. This is a pure **design-language** phase, not a feature phase. Two movements: first a bold *Liquid Glass* vocabulary rolled out app-wide, then a deliberate **counter-movement** that disciplined it back toward minimalism. The guiding principle that emerged: _the album covers and the player express everything — extra decoration makes it "over-feel."_

Roughly spans `7932595` (HomeView glass redesign) → `3d3d507` (flush artist sheet). Feature/perf work (source picker, artist-scoped sessions, caching) landed in the same window but is **out of scope** for this note — see §6.

---

## 1. Liquid Glass vocabulary rollout

The founding move: adopt iOS 26's glass surfaces as the app's primary material, with a clean fallback for the 17.0 deployment floor.

- **`glassSurface(in:tint:interactive:)` helper** — one modifier centralises the `if #available(iOS 26)` gate: real `glassEffect` on 26+, `.thinMaterial` + optional tint overlay on 17–25. Every glass surface in the app is a one-liner through it. `GlassPanel` is the section-card primitive built on top.
- **HomeView redesigned + vocabulary propagated app-wide** (`7932595`).
- **Settings and playlist sheets rebuilt on `GlassPanel`** (`b366dda`) — per-section SF-symbol icons, glass cards, `LivingMeshBackground` behind.
- **Modal sheets polished with glass + animated selection** (`67d4c16`).

**Why a helper, not inline gating:** the redesign needed glass at ~8 sites; scattering `#available` blocks would have been unmaintainable. OS gating lives in one file.

**Files:** `Helpers/GlassPanel.swift`, `Helpers/LivingMeshBackground.swift`, `Helpers/AccentEnvironment.swift`, plus most `Views/`.

---

## 2. Home as the centrepiece

Home stopped being a launcher and became the app's hero surface.

- **Art carousel + drag-to-scrub peek deck** (`ac61938`, `0ebd776`, `06dc28b`, `0f1cfb6`, `8635f6a`) — the hero stack previews the next two covers in user-sorted order; a bidirectional scrub gesture springs back on release.
- **Hero morph Home → Swipe deck** (`8ba54b4`, `023ff5a`) — the cover matched-geometry-morphs into the swipe card; the play button reveal syncs to morph completion.
- **Ambient background tinted from hero artwork** (`aa82130`, `3de71df`) — `HomeAmbientBackground` paints a big soft glow keyed to the cover's own dominant colour. This is the layer that later justified *removing* accent halos (the art already glows).
- **Mode picker + drag-anywhere on the carousel** (`b16d06c`).

---

## 3. The restraint pass (the heart of the phase)

After the glass rollout, several screens read as "AI slop" — too much glass, accent, and motion competing for attention. The counter-movement:

- **Scope accent colouring to critical surfaces only** (`f60704d`) — the brand colour marks the CTA and the one primary selection state, not every chevron/icon.
- **Quiet Settings to a calm utility tier** (`50513e3`) — dropped glass + mesh for a private `SettingsCard` on plain `Color(.systemBackground)`; theme picker became a `Menu { Picker }`; palette grid moved behind a disclosure row. Copyright footer added (`42f2c84`).
- **Propagate the calm tier to its sub-sheets** (`6240da4`) and **quiet ManagePlaylistsSheet + fix mesh diagonal cuts** (`1b1d744`).
- **Soften the Manage button so it recedes into the chrome** (`b951e18`).
- **Drop the hairline divider between sidebar rows** (`893de70`).
- **Restrain accent halos to the CTA + selection borders** (`901aefc`) — the big one: album covers shed their accent-tinted shadow blooms for **neutral depth shadows** (the artwork-keyed ambient glow from §2 carries the colour); selection states keep an accent border but lose the radiating bloom; the CTA halo softened `0.55 → 0.30`.

**The two-tier rule that crystallised:** top-level **Settings stays minimal** (consulted *while using* the app, must not compete with the player); **picker/destination sheets keep playfulness** (short-lived focused destinations earn the visual reward).

---

## 4. Artist hub — a new surface, designed twice

A genuinely new screen introduced and then refined within the phase.

- **Artist hub sheet from the swipe card** (`3577d6e`) — photo, genres, top songs (playable via `ApplicationMusicPlayer`), similar artists (recursive drill-in).
- **Official outbound badges** — branded the Google CTA with the official "G" mark (`6d34ef2`); "Listen on Apple Music" badge (`719105b`); play/pause top songs + AM link (`15500a1`). Per vendor identity rules the badges can't be restyled.
- **Robustness** — name-collision fix so the hub stops showing the wrong artist (`f2b1732`); initials fallback for artists without catalog artwork (`53993d6`).
- **"About" bio** (`74bdfe7`) — chained MusicBrainz → Wikipedia lookup with disk cache; idea now archived → [[Archive/Culla-Music/Ideas/artist-bio-from-musicbrainz-wikipedia|Artist bio]].
- **Flush redesign + always-on Apple Music link** (`3d3d507`) — dropped the floating glass-card chrome from About/Top Songs so content sits flush on the sheet (full-width rows, leading-inset hairline dividers); rebuilt the footer as a balanced equal-width pair; made the AM button **unconditional** via a `music.apple.com/search` fallback (library-resolved artists have no catalog `url` — see memory `project_artist_url_resolution`).

---

## 5. Brand & palette

- **Swap the wordmark accent dot for the Culla brand logo** (`93c0698`).
- **8 new accent palette swatches** (`4ae19f0`); **tint monochrome artwork instead of dropping to palette** (`4c83085`).
- **App icon with light / dark / tinted variants** (`28c1875`, `e21b801`) — see [[Phases/phase-app-icon-design|App Icon Design]].

---

## 6. Out of scope (parallel, non-design work)

Landed in the same window but feature/perf, not design language — not detailed here:

- Source picker: pagination, search + sort, per-artist track counts (`5972cda`, `042c7e0`, `514edb2`, `d775bb9`).
- Artist-scoped swipe sessions (`00b7e2b`) — shipped the [[Archive/Culla-Music/Ideas/sort-songs-from-this-artist|Sort from this artist]] idea via the picker's Artists tab.
- Perf: collapsed membership-index snapshots, cancellable cold-start walks, memoized picker filter (`7d30e73`, `02deea5`, `f37a140`).

---

## Design principles that crystallised

1. **Covers + player express everything.** Decoration on top of the artwork double-counts and reads as generic — neutral depth, let the art's own colour glow.
2. **Accent only on critical surfaces** — the CTA and the one primary selection state. A softened halo is reserved for THE primary action per screen.
3. **Two tiers of utility surface** — minimal top-level Settings vs. playful picker sheets. Single-tier-per-flow: a screen and the sheets it presents share one vocabulary.
4. **"AI slop" is the signal to break the vocabulary, not deepen it** — a quieter sibling primitive (`SettingsCard` next to `GlassPanel`) scoped to one screen beats diluting the brand primitive everywhere.

---

## Outstanding / next steps

- **On-device polish** — flush artist-sheet layout and the bare-vs-filled footer pair want an eyeball on small phones (iPhone SE).
- **`Phase 6`** — open. Candidates with a design angle: first-launch onboarding ([[Ideas/onboarding-flow]], eligible for the glass/restraint treatment), stats view ([[Ideas/stats-activity-view]]), album "About" ([[Ideas/album-about-editorial-notes]]).

---

*Phase 4 → [[Phases/phase-04-dismissed-mode-tooling|Phase 4 — Dismissed Mode Tooling]]*
*Project index → [[Projects/Culla-Music/culla-music|Culla Music]]*
