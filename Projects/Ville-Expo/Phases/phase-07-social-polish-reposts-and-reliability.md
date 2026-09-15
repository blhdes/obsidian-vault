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

## 2026-09-15 — comment_likes migration confirmed applied

The one open question from this phase was whether `supabase/migrations/20260717_create_comment_likes_table.sql` (shipped in the same commit as this phase's item 7, comments likeable/repostable) had actually been pasted into the Supabase SQL Editor and run, since — unlike earlier migrations — it was never logged in `docs/changelog.md` with a "Migrations to run" note.

Verified live: queried the `comment_likes` table via the project's Supabase REST API (`.../rest/v1/comment_likes`) and got `200 []` — table exists, RLS active, no rows yet. **Migration was already applied.**

Side note: the Supabase project (`zmrrepjysejkixwruksj.supabase.co`) had auto-paused from free-tier inactivity — it's been dormant since 2026-07-17 — so the first check that day came back as DNS `NXDOMAIN`. User reactivated it from the Supabase dashboard, then the check above passed.

**No DB migrations are pending on this project.** Everything still open is product work (the 5-item "Remaining Items" list above), not database work.

## 2026-09-15 — Clipping & repost social parity (built this session)

While re-testing the app on the physical iPhone for the first time in ~2 months, found that Clippings (highlighted review quotes) and reposted Letterboxd reviews had **no like or comment UI at all** — only swipe-to-repost, unlike Takes and Comments. Root cause: `ClippingCard`/`ReviewCard` were simply never built with `TakeInteractionBar`'s heart/comment/repost bar.

Built full parity, in `ville-du-cinema-mobile` commits `af975f4` (dependency bump — see below), `775d29c` (the feature), `779dd1e` (docs) — pushed to `feature/tos-compliant-rebuild`:

- New `clipping_likes` + `clipping_comments` tables, both **keyed by `original_url`, not a row id** — every repost of a Clipping inserts a brand-new `user_clippings` row rather than referencing the original, so a like/comment has to key off the same `original_url` already used to dedupe repost counts. This means liking any repost of a quote hits the same shared thread as the original.
- New `ClippingInteractionBar` (mirrors `TakeInteractionBar`), wired into `ClippingCard`, `ClippingRepostCard`, and — since a plain Letterboxd repost (`type: 'repost'`) is *also* just a `Clipping` row — into `RepostCard` too, for free.
- New `ClippingDetailScreen` (comment thread), registered as `ClippingDetail` on all three tab stacks.
- UI polish while in there: `ReviewCard` gained an optional `footer` prop so the interaction bar shares a row with the Letterboxd source-link logo instead of stacking below it (was generating an extra line of vertical space per repost card); icon gap in all three interaction bars tightened 24px → 8px; added `utils/formatCount.ts` for compact counts (1600 → "1.6k") — didn't find any pre-existing rounding utility despite recalling one, built fresh.
- Scoped out: Clipping comments are flat, no like/repost on the comment itself (matches Takes' original pre-Phase-7 shape) — a deliberate smaller scope, not a gap.

Also updated dependencies first (`af975f4`): `expo-doctor` found 17 packages behind their SDK 55 patch version and a **missing `react-native-worklets` peer dependency** that reanimated 4 requires outside Expo Go — flagged as a real crash risk for the dev-client build, not just noise. Also downgraded jest 30→29.7 (SDK-expected) and added `ts-node` (needed for jest to parse `jest.config.ts`, which broke immediately after the jest downgrade).

Repo docs updated to match: `docs/changelog.md` (new dated section, not slotted into the Phase-N numbering since Phase 7 itself was never added there) and `README.md` feature list.

**Next up (user's ask, not yet started):** comment-on-comment replies for Takes, single-level nesting (per user's explicit choice over infinite Reddit-style nesting). Note the original plan doc (`docs/village-social-layer.md` §3) explicitly said "no nested threads for now" — this will be a deliberate deviation from the original plan, worth flagging when picking it up.

## 2026-09-15 (same session, later) — Reply threading built, NOT yet verified — pick up here next time

Built single-level comment replies (the item above), committed and pushed as `0345059` on `feature/tos-compliant-rebuild`. **Session ended before it could be tested on device** — three things still need doing, in order:

1. **Apply the migration**: paste `supabase/migrations/20260915_add_comment_replies.sql` into the Supabase SQL Editor (adds `parent_comment_id` to `take_comments`). Confirmed via REST API it wasn't applied as of session end.
2. **Get the dev-client build onto the iPhone**: the wireless install (`npx expo run:ios --device "Alejandro"`, no cable) kept hanging indefinitely on `- Connecting to: Alejandro` — build itself succeeded both times (0 errors), it's specifically the device-transfer step over Wi-Fi that stalled. Killed the stuck process at session end. **Try USB next time** — the cheatsheet's wireless-pairing note ([[Projects/Ville-Expo/Dev-Insights/expo-build-and-run-cheatsheet|cheatsheet]]) may need a caveat added once this is confirmed as a real wireless-specific flakiness, not a one-off.
3. **Test the reply flow live**: reply button on a top-level comment → banner appears above the compose bar → post → renders indented under the parent → counts (badge + "Comments (N)" label) include replies.

Code-reviewed against the existing patterns myself while building (mirrors `useComments`/`CommentInteractionBar`/`TakeDetailScreen` conventions throughout) and `tsc --noEmit` + `jest` were both clean, but that's not the same as it actually working on a phone — don't assume it's done.

Also from earlier in this same session: [[Projects/Ville-Expo/Ville-Expo|Clipping/repost like-comment parity]] (commits `af975f4`/`775d29c`/`779dd1e`/`2ee8f8f`) — that part *was* fully tested live and confirmed working, unlike this reply-threading piece.

---
Repo docs: `docs/changelog.md` (Phases 0–6) · `docs/village-social-layer.md` (original plan + remaining items) · `docs/letterboxd-compliance-audit.md`
Project index: [[Projects/Ville-Expo/Ville-Expo|Ville Expo]]
