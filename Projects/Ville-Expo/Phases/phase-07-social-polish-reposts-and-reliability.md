---
title: "Phase 7 — Social Layer Polish, Reposts & Reliability"
date: 2026-04-18
tags: [ville-expo, ville-du-cinema, phase, mobile, react-native, done]
status: shipped
---

# Phase 7 — Social Layer Polish, Reposts & Reliability

Schematic record, reconstructed retroactively (2026-09-14) from `git log` — no vault phase note existed for this cluster. Picks up right after the repo's own **Phase 6 — Film-Anchored Clippings** (`3ec1691`, 2026-03-27), which along with Phases 0–6 is fully documented in the repo itself at `docs/changelog.md` (that file is the authoritative build history for the TOS-compliant rebuild through Phase 6 — this note only covers what came *after* it and isn't duplicated there).

**~90 commits, 2026-03-29 → 2026-04-18**, plus one isolated follow-up commit on **2026-07-17**. The branch (`feature/tos-compliant-rebuild`) has been dormant since — no commits in the ~2 months since.

## 1. FilmCard interaction polish

Tap-to-search (Google, in-app browser) wired up on film title, director, and cast names; poster taps to a fullscreen fade modal; takes/clippings paginated (3 default, "show more" up to 15); IMDb + Letterboxd inline badge links after genre tags; skeleton loading state while the TMDB fetch resolves.

## 2. Unified profile overhaul

`ProfileScreen` and `NativeProfileScreen` rewritten to mirror each other and merge takes + clippings into one filtered feed per profile, with an author row and Instagram-style profile-picture blur. `FilmCard`'s takes and clippings merged into a single "From the Village" section.

## 3. Universal repost system

Reposting extended from reviews-only to **Takes and Clippings** (`40a6bdf`), with author/user metadata preserved through reposts (including legacy records), shared `TakeInteractionBar` + `RepostHeader` components, and a run of counter-correctness fixes (double-repost prevention, re-repost inflation, duplicate `actionColor` prop).

## 4. Branding & visual polish

The official Letterboxd 3-dot logo replaced an earlier approximation, went through several sizing/theme iterations before settling as a subtle 22px signature; a Village "V" logo added to Discover's "In Your Network" header; teal accent replaced with black (light) / near-white (dark); card typography (font sizes, body scale) unified across `ReviewCard`/`ClippingCard`/`TakeCard` via a shared `useTypography`.

## 5. Reliability & feed stabilization

Feed scroll stabilized (eliminated header/tab-bar overscroll bounce, fixed-height footer, `FeedDivider` full-bleed rendering fixes); `TakeInteractionBar` jitter eliminated by warming pub/sub caches before render and publishing batch social data instead of per-item fetches; skeleton-gating race fixed so takes don't render before social data is ready; take/clipping fetch limits added (50 takes, 50/30 clippings) for load performance.

## 6. Smart relative timestamps

A relative-timestamp utility ("2h", "3d") wired into take/comment views (`d3a38db`), later tightened to more compact abbreviations (`c902724`).

## 7. Isolated follow-up — comments likeable & repostable

**`75ff4ff` (2026-07-17)** — comments gained their own like/repost affordance, matching Takes and Clippings. The only commit on the branch since April; nothing since.

---

## Current status (as of this audit, 2026-09-14)

- Branch `feature/tos-compliant-rebuild`, working tree clean, **dormant since 2026-07-17** (~2 months).
- `docs/village-social-layer.md`'s "Remaining Items" table (not re-verified line-by-line here, but nothing in the git history since suggests otherwise) still lists as **not built**: "because you saved X" TMDB-recommendation surfacing, unified film+people search, RSS reviews on Film Cards, Take-as-image sharing, and visual lanes distinguishing RSS vs. Village content in the feed.

---
Repo docs: `docs/changelog.md` (Phases 0–6) · `docs/village-social-layer.md` (original plan + remaining items) · `docs/letterboxd-compliance-audit.md`
Project index: [[Projects/Ville-Expo/Ville-Expo|Ville Expo]]
