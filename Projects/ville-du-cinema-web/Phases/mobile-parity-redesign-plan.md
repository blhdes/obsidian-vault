---
title: Mobile Parity + Redesign — Kickoff Plan
date: 2026-04-25
tags: [ville-du-cinema, phase, planning, kickoff]
---

# Mobile Parity + Redesign — Kickoff Plan

Captured so we can pick this up in a new session. Branch created, no code written yet — planning phase.

## State on save

- **Branch created**: `feat/mobile-parity-redesign` on local clone of web repo
- **Web repo path**: `/Users/agomezu/Claude/ville-du-cinema-app/`
- **Mobile repo path**: `/Users/agomezu/Claude/ville-du-cinema-mobile/`
- **Remote**: currently HTTPS (`https://github.com/blhdes/ville-du-cinema-app.git`). SSH rejected — see "Open questions" below.
- **No commits yet** on the branch.

## What the web app currently is

A Letterboxd RSS aggregator. You follow Letterboxd usernames and see their reviews as an editorial magazine feed. That's the whole product. Stack:

- Next.js 16 App Router + React 19 + TypeScript
- Tailwind v4, Lucide icons
- Supabase (auth + `user_data` table)
- next-intl with `fr` (default) / `en` / `es`
- Cahiers du Cinéma brutalist aesthetic (sepia/cream/editorial red, Playfair Display + EB Garamond)

## What the mobile app has that web doesn't

| Feature | Mobile | Web |
|---|---|---|
| Takes (short film posts) | ✅ | ❌ |
| Clippings (quote snippets) | ✅ | ❌ |
| Comments on takes/clippings | ✅ | ❌ |
| Likes | ✅ | ❌ |
| Reposts (takes + clippings) | ✅ | ❌ |
| In-app follow graph (follow users, not just Letterboxd names) | ✅ | ❌ |
| User search | ✅ | ❌ |
| Rich external profile pages | ✅ | ⚠ basic `/u/[username]` |
| Favorite films grid | ✅ | ❌ |
| Saved films | ✅ | ❌ |
| Discover (trending posters, network films) | ✅ | ❌ |
| Film cards (TMDB) | ✅ | ❌ |
| Letterboxd RSS feed | — | ✅ (keep) |

Mobile already has `supabase/migrations/` that defines the social tables — port these first.

Mobile services to port (framework-agnostic, easy wins): `services/takes.ts`, `clippings.ts`, `comments.ts`, `likes.ts`, `favoriteFilms.ts`, `savedFilms.ts`, `tmdb.ts`, `feed.ts`.

Mobile hooks to port: `useTakes`, `useClippings`, `useLike`, `useComments`, `useRepostCount`, `useFavoriteFilms`, `useSavedFilm`, `useClippingRepostCount`.

## Proposed 4-phase plan

Ship each phase as its own PR off `feat/mobile-parity-redesign`.

### Phase 0 — Foundation
- Port mobile's `supabase/migrations/` into web's `supabase-schema.sql` + migration files. Tables: `takes`, `clippings`, `comments`, `likes`, `reposts`, `follows`, `favorite_films`, `saved_films`.
- Port `services/tmdb.ts` — needs `TMDB_API_KEY` env var.
- **Decide design direction** (see open question #1 below). This shapes everything after.

### Phase 1 — Social primitives (backbone)
- API routes: `app/api/takes/`, `app/api/clippings/`, `app/api/likes/`, `app/api/comments/`, `app/api/reposts/`, `app/api/follows/`, `app/api/users/search/`.
- Hooks: port the mobile ones listed above.

### Phase 2 — Feed + Discover
- Rebuild `app/[locale]/page.tsx` as a blended feed (takes + clippings + RSS reviews).
- Components: `TakeCard`, `ClippingCard`, `RepostCard`, `TakeInteractionBar`.
- New `app/[locale]/discover/page.tsx` + `components/discover/` (trending posters, network films).

### Phase 3 — Profile + Films
- Rich `app/u/[username]/page.tsx` with FavoriteFilmsGrid, tabs for takes/clippings/reviews.
- `app/[locale]/films/[id]/page.tsx` (film card view, TMDB-backed).
- `app/[locale]/saved/page.tsx`.

### Phase 4 — Create flows + Design pass
- `app/[locale]/takes/new/page.tsx`, `app/[locale]/clippings/new/page.tsx`.
- Global redesign pass applying the visual direction decided in Phase 0.

## Open questions — pending user answer

1. **Design direction** — evolve the current Cahiers-du-cinéma editorial feel, or go fully radical? If radical, do you have a reference (site / mockup / mood)?
2. **Scope start** — go all-in on Phase 0+1 (DB + APIs) first, or start with a visible design prototype on one page so you can react to the look early?
3. **SSH** — `~/.ssh/blhdes` key exists but `~/.ssh/config` does not, so `git@github.com:blhdes/...` was rejected. HTTPS fallback is working. Want an SSH config entry added so SSH remote works?

## Gotchas / things to know before resuming

- **Existing `MOBILE_MIGRATION.md` in the web repo is the opposite direction** — it planned web → mobile. Don't confuse it with this project. Also `PRE_MIGRATION_TERMINAL_GUIDE.md` and the remote branches `feature/expo-migration` / `feature/pre-migration-hardening` relate to that earlier migration.
- The web app has an existing "guest mode" (localforage → Supabase migration via `MigrationModal`). Any new social features need to decide: guest-mode-allowed or auth-required? Likely auth-required for takes/comments/likes.
- `lib/storage.ts` and `lib/auth.ts` are already abstracted as swap points — takes/clippings logic should route through similar abstractions where possible.
- i18n is in place (`fr`/`en`/`es`). All new UI strings need entries in `messages/*.json`. Mobile app doesn't have i18n yet — strings will need translation work.
- Global user rules that apply when resuming:
  - Beginner-friendly plain language, skip preamble/summaries.
  - For >3 files, provide `[File Path] -> [Action]` checklist before generating code.
  - Refactors touching >200 line files → suggest logic extraction first.
  - Conventional Commits (`feat:`, `fix:`, `refactor:`).
  - Functional components, Tailwind utility classes, no `any`, Zod for validation.

## How to resume

In the next session, open this note and say:
> _"Resume the Ville du Cinéma web redesign — context in `Projects/ville-du-cinema-web/Phases/mobile-parity-redesign-plan.md`. I'm ready to answer the open questions."_
