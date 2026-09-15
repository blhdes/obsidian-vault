---
title: Ville Expo — Ville du Cinéma Mobile
date: 2026-05-19
tags: [project, mobile, expo, react-native, ville-du-cinema]
---

# 🎬 Ville Expo

Index note for the **Ville du Cinéma mobile app** — the Expo / React Native version. This is the source-of-truth project for the mobile build; the [[Projects/ville-du-cinema-web/ville-du-cinema-web|web redesign]] mirrors features from here.

## Repo

- **Path:** `/Users/agomezu/Claude/ville-du-cinema-mobile/`
- **Remote:** `git@github.com:blhdes/ville-du-cinema-mobile.git`
- **Working branch:** `feature/tos-compliant-rebuild`
- **Stack:** Expo SDK 55 · React 19 · React Native · React Navigation v7 · Supabase · TypeScript · Jest

## Related projects

- [[Projects/ville-du-cinema-web/ville-du-cinema-web|Ville du Cinéma — Web Redesign]] — Next.js 16 web app mirroring this app's social features.
- [[Projects/village-swift/village-swift|village-swift (VILLE)]] — **separate, paused** pure-Swift/SwiftData reading-only distillation of this app (no auth, no social, no RN/Expo/JS). Not a fork of this codebase, just references it when porting logic. (Absorbed the old `Ville-Native-App` planning note on 2026-09-14 — same project, now archived as a duplicate.)

## Sections

- **[[Ideas]]** — product ideas, UX experiments, feature sketches.
- **[[Dev-Insights]]** — lessons learned: bugs, patterns, decisions, and *why*.
- **[[Phases]]** — milestones and the phased plan.

## How to use this space

When working on the mobile app, ask Claude things like:
- _"New Phase note for the TOS-compliant rebuild milestone"_
- _"Save this dev-insight — [what I learned wiring up Expo SecureStore with Supabase]"_
- _"New idea in Ideas/ — [feature sketch]"_

## Status (updated 2026-09-14, was 4 months stale)

The "just (re)started 2026-05-19" note below was inaccurate even at the time — the branch already had ~170 commits of real work behind it by then (started 2026-03-01). Checked against the actual repo:

- **Branch:** `feature/tos-compliant-rebuild`, working tree clean, **171 commits total**, most recent **2026-07-17** — dormant since (~2 months).
- **Build history, Phases 0–6** (ToS-compliant scraping removal → TMDB Film Cards → Takes/Likes/Comments → Discovery → Watchlist/Favorites → Film-Anchored Clippings): fully documented in the repo's own `docs/changelog.md` — that's the authoritative source, not reproduced here.
- **Phase 7** (undocumented until this audit — social-layer polish, universal reposts, Letterboxd/Village branding, feed-reliability fixes, relative timestamps, through the isolated 2026-07-17 comment-likes/reposts commit): now recorded in [[Projects/Ville-Expo/Phases/phase-07-social-polish-reposts-and-reliability|the new phase note]].
- **Known open items** (per the repo's own `docs/village-social-layer.md` "Remaining Items" table, not independently re-verified here): TMDB-based "because you saved X" recommendations, unified film+people search, RSS reviews surfaced on Film Cards, Take-as-image sharing, visual lanes distinguishing RSS vs. Village content in the feed.
- App is a mature, feature-complete social layer per its own `README.md` (feed, Takes, Clippings, Reposts, TMDB film pages, watchlist/favorites, discovery, Google OAuth + guest mode) — this is well past an early rebuild, whatever "current focus" means next is a real product decision, not a resume-from-scratch one.

> Original 2026-05-19 placeholder (kept for history): *"Project just (re)started 2026-05-19. Soon picking back up on the `feature/tos-compliant-rebuild` branch. Fill in current focus here as work resumes."*

## 2026-09-15 — DB check-in

Confirmed the last outstanding question from the dormancy audit: the `comment_likes` migration (`20260717_create_comment_likes_table.sql`) was already applied to the live Supabase DB — verified via the REST API after reactivating the project (it had auto-paused from free-tier inactivity). **No DB migrations pending.** Details in [[Projects/Ville-Expo/Phases/phase-07-social-polish-reposts-and-reliability|Phase 7 note]]. Remaining open work is the 5-item product list (TMDB recommendations, unified search, RSS reviews on Film Cards, Take-as-image sharing, RSS/Village feed lanes), not database work.

## 2026-09-15 — First on-device test in ~2 months, Clipping/repost parity shipped

Rebuilt and installed on the physical iPhone (`Alejandro`) for the first time since the July dormancy — found dependency drift (17 packages behind SDK 55 patch, missing `react-native-worklets` peer dep) and fixed it first. Live testing then surfaced a real gap: Clippings and reposted Letterboxd reviews had no like/comment UI, only repost. Built full parity (new `clipping_likes`/`clipping_comments` tables keyed by `original_url`, `ClippingInteractionBar`, `ClippingDetailScreen`) plus UI polish (interaction bar now shares a row with the Letterboxd logo instead of stacking, tighter icon spacing, compact "1.6k"-style counts). Shipped in commits `af975f4`/`775d29c`/`779dd1e` on `feature/tos-compliant-rebuild`, pushed. Full writeup in [[Projects/Ville-Expo/Phases/phase-07-social-polish-reposts-and-reliability|Phase 7 note]].

**Queued next:** comment-on-comment replies for Takes (single-level, user's explicit choice) — a deliberate deviation from the original plan doc, which said no nested threads.

## 2026-09-15 (later) — Reply threading built but unverified, session cut short

Built and pushed (`0345059`) before the session had to end — **not tested on device**. The wireless install hung indefinitely on "Connecting to Alejandro" (build succeeded fine, it's specifically the Wi-Fi device-transfer step). Next session: apply the new migration, retry over USB, then actually test the reply flow. Full detail in [[Projects/Ville-Expo/Phases/phase-07-social-polish-reposts-and-reliability|Phase 7 note]] — read that "pick up here" section first.
