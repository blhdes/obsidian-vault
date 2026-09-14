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
