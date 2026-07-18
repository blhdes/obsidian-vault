---
title: Content Sources — Letterboxd vs Native Village
date: 2026-05-19
tags: [architecture, content-model, letterboxd, takes, clippings, dev-insight]
---

# Content Sources — Letterboxd vs Native Village

Ville du Cinéma has **two content sources**. Letterboxd is the original (read-only, TOS-compliant RSS); the Native Village layer is the newer in-app social layer (takes, clippings, comments, likes). Source for this doc: code on `feature/tos-compliant-rebuild` at `/Users/agomezu/Claude/ville-du-cinema-mobile/`.

## Source 1 — Letterboxd (RSS, read-only)

Pulled live from public Letterboxd RSS feeds of users the viewer follows. Nothing is cached in our DB — every feed open re-fetches and merges. TOS-compliant: no GraphQL, no scraping, no API keys.

**Entities** (`Review` in `types/database.ts`, parsed in `services/feed.ts`):

| Type | What it is | Fields of note |
|---|---|---|
| `review` | A written Letterboxd review | `review` (HTML body), `rating` (★ string), `movieTitle`, `link`, `pubDate`, `creator`, `avatarUrl` |
| `watch` | A bare "watched on X" log entry, no body | Same shape; `review` is empty string |

**What the user can do with a Letterboxd review/watch:**

| Action | How | Output |
|---|---|---|
| Read full review | Long-press the ReviewCard | Opens `ReviewReaderScreen` with word-by-word text selection |
| Save a quote | Select text in reader → preview | Creates a clipping (`type: 'quote'`) in `user_clippings` |
| Repost the whole review | Swipe-left on ReviewCard | Creates a clipping (`type: 'repost'`) — full Review JSON stored in `review_json` |
| View the author profile | Tap name/avatar | `ExternalProfileScreen` (Letterboxd read-only view) |
| Open on Letterboxd | Tap Letterboxd icon | External browser to `review.link` |

**What you CANNOT do on Letterboxd content:** like, comment, edit. Those interactions only exist on native Village objects. Letterboxd content is consumable and quotable, never editable inside Village.

**Where it appears:** `FeedScreen` (merged with native content), `ExternalProfileScreen` (a Letterboxd user's reviews only).

## Source 2 — Native Village (Supabase-backed)

Four native object types. **Takes** and **Clippings** are the user-generated content; **Comments** and **Likes** are interactions on top.

### Takes — short-form posts (`takes` table)

- 280 chars, anchored to a TMDB film.
- Created in `CreateTakeScreen`: search TMDB → write → post.
- Immutable once posted (no edit).

### Clippings — saved/reposted content (`user_clippings` table)

A clipping has a `type` field with 5 variants — this is the key to understanding the data model:

| `type` | Source | How it's created |
|---|---|---|
| `quote` | Letterboxd review excerpt | `ReviewReaderScreen` → select text → `QuotePreviewScreen` → save |
| `repost` | Full Letterboxd review | Swipe-left on ReviewCard → `saveRepost()` |
| `take-repost` | Native Village take | Repost action on TakeCard / TakeInteractionBar → `saveRepostTake()` |
| `clipping-repost` | Another user's clipping | Repost action on a clipping → `saveRepostClipping()` |
| `comment-repost` | A comment on a take | Repost action on a comment row (`CommentInteractionBar`) → `saveRepostComment()` — added 2026-07-17 |

The original object is preserved as JSON in `clipping.review_json` for rich rendering when reposted in someone else's feed.

### Comments (`take_comments` table)

- 280 chars, replies to a take.
- **Flat thread** — no nested replies, oldest-first.
- Created in `TakeDetailScreen`.
- Author can delete; no edit.
- **Likeable + repostable since 2026-07-17** — each comment row shows a `CommentInteractionBar` (heart + repeat). A repost becomes a `comment-repost` clipping rendered by `CommentRepostCard` in the feed/profiles.

### Likes (`take_likes` + `comment_likes` tables)

- 1-per-user toggle on a take (`take_likes`) or a comment (`comment_likes`, cascade-deletes with the comment).
- That's it — likes are not entities you interact with further.

## 🟢 Master table — what's possible on native content

This is the answer to "what is commentable and repostable and what is not":

| Object | Create how | 👍 Likeable | 💬 Commentable | 🔁 Repostable | ✏️ Editable | 🗑️ Deletable |
|---|---|:-:|:-:|:-:|:-:|:-:|
| **Take** | `CreateTakeScreen` (TMDB film + 280-char text) | ✅ | ✅ (flat) | ✅ → `take-repost` clipping | ❌ | ✅ (author) |
| **Clipping — `quote`** | Select text in `ReviewReaderScreen` → preview → save | ❌ | ❌ | ✅ → `clipping-repost` | ❌ | ✅ (author) |
| **Clipping — `repost`** (LB review) | Swipe-left on ReviewCard | ❌ | ❌ | ✅ → `clipping-repost` | ❌ | ✅ (author) |
| **Clipping — `take-repost`** | Repost action on a Take | ❌ | ❌ | ✅ → `clipping-repost` | ❌ | ✅ (author) |
| **Clipping — `clipping-repost`** | Repost action on a Clipping | ❌ | ❌ | ✅ → `clipping-repost` | ❌ | ✅ (author) |
| **Clipping — `comment-repost`** | Repost action on a Comment | ❌ | ❌ | ✅ → `comment-repost` (same comment, re-shared) | ❌ | ✅ (author) |
| **Comment** | Reply in `TakeDetailScreen` | ✅ (`comment_likes`) | ❌ | ✅ → `comment-repost` clipping | ❌ | ✅ (author) |
| **Like** | Heart toggle on a Take or Comment | n/a | n/a | n/a | n/a | toggle off |

**Key asymmetry to remember:** only **Takes** are commentable. Clippings can only be reposted — never liked or commented on. Comments (since 2026-07-17) can be liked and reposted, but not replied to — the thread stays flat.

## Cross-source interaction model

```
Letterboxd review ──quote──▶ Clipping (quote)
Letterboxd review ──repost─▶ Clipping (repost)
                              │
                              └──repost──▶ Clipping (clipping-repost)

Take ──repost──▶ Clipping (take-repost) ──repost──▶ Clipping (clipping-repost)
 │
 ├──like──▶ take_likes row
 └──comment──▶ Comment ──like──▶ comment_likes row
                │
                └──repost──▶ Clipping (comment-repost) ──repost──▶ Clipping (comment-repost)
```

- **One-way flow Letterboxd → Village**: a Letterboxd review becomes Village content only via quote or repost. It cannot be commented or liked at its origin.
- **All reposts collapse to a clipping** — there isn't a separate "repost" table. The `type` field on `user_clippings` is what tells the renderer how to display it.
- **Anchoring via TMDB**: takes and clippings can store `tmdb_id` for film-centric discovery (e.g. `FilmCardScreen` aggregates all takes about a single film).

## Schema reality-check

Tables that exist on `feature/tos-compliant-rebuild`:

| Table | Holds |
|---|---|
| `takes` | Native short-form posts |
| `take_likes` | Like toggles (composite PK `user_id` + `take_id`) |
| `take_comments` | Replies on takes |
| `comment_likes` | Like toggles on comments (composite PK `user_id` + `comment_id`, cascade on comment delete) |
| `user_clippings` | All five clipping variants (`type` discriminator + nullable `review_json`) |

**No table caches Letterboxd reviews** — they're always live-fetched. This is what keeps the app TOS-compliant.

## Where each source surfaces

| Screen | Letterboxd content | Native content |
|---|:-:|:-:|
| `FeedScreen` | ✅ merged | ✅ merged |
| `FilmCardScreen` | ❌ | ✅ takes for that TMDB id |
| `NativeProfileScreen` | ❌ | ✅ user's takes + clippings |
| `ExternalProfileScreen` | ✅ reviews | ❌ |
| `ReviewReaderScreen` | ✅ (full read view) | ❌ |
| `TakeDetailScreen` | ❌ | ✅ take + comments |
| `SavedFilmsScreen` | ✅ via saves | ✅ via clippings/takes |

## Source files (for verification / future edits)

- `services/feed.ts` — RSS parsing + feed merge
- `services/takes.ts`, `services/clippings.ts`, `services/comments.ts`, `services/likes.ts` — CRUD per native type
- `types/database.ts` — `Review`, `Take`, `Clipping`, etc.
- `screens/CreateTakeScreen.tsx`, `screens/QuotePreviewScreen.tsx`, `screens/ReviewReaderScreen.tsx`, `screens/TakeDetailScreen.tsx`
- `components/TakeCard.tsx`, `components/TakeInteractionBar.tsx`, `components/ReviewCard.tsx`
- `components/CommentInteractionBar.tsx`, `components/feed/CommentRepostCard.tsx`, `hooks/useCommentLike.ts` — comment likes + reposts (2026-07-17)

## Related

- [[Ville-Expo]] — project index.
- [[expo-build-and-run-cheatsheet]] — how to run/rebuild the app on iPhone.
