---
title: QA — Loved up-swipe + duplicate-playlist fixes
date: 2026-05-14
tags: [culla-music, qa, testing, up-swipe, loved, perf]
---

# QA — Loved up-swipe checklist

Manual tests for the recent fixes + the 2026-05-14 performance pass:

- **Up-swipe transition** (commit `da5b506`) — card now flies fully off-screen instead of stopping mid-screen.
- **Stop duplicating Culla Loves** (commit `728f706`) — first add to a freshly-created loved playlist no longer trashes it on transient failure; 600 ms post-create delay reduces the chance of that first failure.
- **Hide loved from Manage** (commit `728f706`) — the loved target is filtered out of the Manage Playlists sheet.
- **Performance pass** (2026-05-14, pre-commit) — parallel playlist track fetch, deferred membership index, memoized `playlistMemberships`, tighter swipe timing (0.18s fly-off + 0.25s slide-in), accent prefetch for next card, single-pass `AccentExtractor`.

Reference: [[culla-music|Culla Music — Project Index]]

---

## Up-swipe transition (visual)

- [x] Up-swipe a song with enough velocity → the **current card visibly leaves the top of the screen** before the next song appears (no snap-from-the-middle).
- [x] The new card **slides down + fades in** from off-screen — should feel similar in pacing to the right-swipe-to-sidebar transition.
- [x] Total swipe-to-settled-card is **noticeably tighter** than the pre-perf-pass build (~430 ms now vs. ~570 ms before) but still reads as a smooth transition, not a snap.
- [x] Drag up partially (below the threshold) and release → card **springs back** to centre, no Loved action fires.
- [x] Drag up past the threshold → the **pink heart overlay reaches full opacity** before release.
- [x] Right-swipe onto a sidebar playlist still works smoothly (no regression from the y-damping change or the new shorter timings).

## Culla Loves auto-creation

- [x] Fresh install (or after deleting `Culla Loves` in Apple Music + clearing defaults) → first up-swipe creates **exactly one** `Culla Loves` playlist.
- [x] Force-quit the app and relaunch → up-swipe again → **no new playlist** is created; the existing one is reused.
- [x] Repeat for 3 consecutive sessions → still only **one** `Culla Loves` exists in Apple Music.
- [ ] If the first up-swipe surfaces *"Couldn't reach Culla Loves — try again"*, a second up-swipe a few seconds later should succeed **without creating another playlist**.
- [ ] Up-swipe a song that's already in the loved playlist → toast says **"Already loved"**, song is not duplicated.

## Loved target in Settings

- [ ] Pick a normal user playlist as the loved target in Settings → up-swipe adds the song to **that** playlist (not Culla Loves).
- [ ] Pick a known read-only playlist (e.g. *Favorite Songs* / smart Favorites) — if it slips past the name filter, the first up-swipe should still **self-heal**: the picker resets and the playlist is hidden from future pickers.
- [ ] Switching the loved target between Culla Loves and a custom playlist in Settings works without restart.

## Manage Playlists sheet (Swipe view → Manage)

- [ ] The current loved target **does not appear** in the Manage Playlists list.
- [ ] Change the loved target in Settings → reopen Manage → the previously-loved playlist now appears, the newly-loved one is hidden.
- [ ] If no loved target is configured (empty defaults) → **all** editable playlists appear as usual.
- [ ] The **Sort From** picker (Home → "Sort from playlist") still shows the loved target — only Manage hides it.

## Undo + rollback

- [ ] Up-swipe a song → Undo toast appears → tap Undo → song is **removed** from the loved playlist locally and remotely.
- [ ] If the remote add to Culla Loves fails (and we don't see a toast saying success), confirm the **chip** under the song doesn't lie — the loved chip should disappear after the rollback.
- [ ] Sort or love a song → the very next card's **chips reflect reality** for the *previous* card's playlists (membership cache invalidates on every add/remove).
- [ ] Undo a sort → reopen the same card via the queue → previously-added playlist **no longer shows** as a chip.

## Performance pass (2026-05-14)

### Initial load

- [ ] Cold launch → tap **Start Cullaing** in library mode → first card appears within ~1 s on a normal-sized library (was ~6 s with 30+ playlists pre-pass).
- [ ] On the first card in library/dismissed mode, the membership chips may **pop in a beat after the card** itself. This is **expected** — the index is built in the background so the card paints first.
- [ ] Unsorted mode → first card still waits for the playlist scan (it needs the exclusion set), but the wait is much shorter than before because the playlist tracks load in parallel.
- [ ] Toggle **Include curated** in Settings → re-enter unsorted → counts + deck reflect the new scope (parallel fetch returns the right data for both scopes).

### Swipe transitions

- [ ] Left/right/up swipes all feel **snappy but smooth** — no visible micro-stutter mid-transition.
- [ ] During a drag, the card itself never **hitches or pauses** — `playlistMemberships(for:)` memoization should mean SwiftUI isn't re-rendering the card per drag frame.
- [ ] When the new card lands, its **accent gradient is already correct** (no visible color cross-fade). The next card's accent is prefetched while the previous card is visible.
- [ ] Swiping a song without playing the preview first → no audible glitch, no spurious "stop" haptics — `stopPreview()` early-returns when nothing's playing.

### Edge cases / regressions

- [ ] Large library / many playlists (30+) → initial load completes without Apple Music rate-limit errors. If it fails, the parallel TaskGroup should propagate the first error — check for a toast/log entry.
- [ ] Force-quit during initial load → re-launch → state is clean, no half-built membership index leaking from last session.
- [ ] AccentExtractor: artwork that's mostly monochrome (e.g. all-black album cover) → still produces a sensible gradient (falls back to `derivedSecondary`).
- [ ] AccentExtractor: artwork with two distinct dominant colors → gradient now visibly reflects **both** colors (the scoring bugfix means the secondary picker sees correct bucket scores, not last-pixel scores).

---

## Notes

- The 600 ms post-create delay is best-effort — on a slow network Apple Music may still need more time. The fix's safety net is that we no longer trash the playlist on first-attempt failure, so the next up-swipe retries against the same playlist.
- If duplicate `Culla Loves` playlists exist from before this fix shipped, they need to be **deleted manually** in Apple Music — the app won't garbage-collect them.
