---
title: QA — Loved up-swipe + duplicate-playlist fixes
date: 2026-05-14
tags: [culla-music, qa, testing, up-swipe, loved]
---

# QA — Loved up-swipe checklist

Manual tests for the three recent fixes:

- **Up-swipe transition** (commit `da5b506`) — card now flies fully off-screen instead of stopping mid-screen.
- **Stop duplicating Culla Loves** (commit `728f706`) — first add to a freshly-created loved playlist no longer trashes it on transient failure; 600 ms post-create delay reduces the chance of that first failure.
- **Hide loved from Manage** (commit `728f706`) — the loved target is filtered out of the Manage Playlists sheet.

Reference: [[culla-music|Culla Music — Project Index]]

---

## Up-swipe transition (visual)

- [ ] Up-swipe a song with enough velocity → the **current card visibly leaves the top of the screen** before the next song appears (no snap-from-the-middle).
- [ ] The new card **slides down + fades in** from off-screen — should feel similar in pacing to the right-swipe-to-sidebar transition.
- [ ] Drag up partially (below the threshold) and release → card **springs back** to centre, no Loved action fires.
- [ ] Drag up past the threshold → the **pink heart overlay reaches full opacity** before release.
- [ ] Right-swipe onto a sidebar playlist still works smoothly (no regression from the y-damping change).

## Culla Loves auto-creation

- [ ] Fresh install (or after deleting `Culla Loves` in Apple Music + clearing defaults) → first up-swipe creates **exactly one** `Culla Loves` playlist.
- [ ] Force-quit the app and relaunch → up-swipe again → **no new playlist** is created; the existing one is reused.
- [ ] Repeat for 3 consecutive sessions → still only **one** `Culla Loves` exists in Apple Music.
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

---

## Notes

- The 600 ms post-create delay is best-effort — on a slow network Apple Music may still need more time. The fix's safety net is that we no longer trash the playlist on first-attempt failure, so the next up-swipe retries against the same playlist.
- If duplicate `Culla Loves` playlists exist from before this fix shipped, they need to be **deleted manually** in Apple Music — the app won't garbage-collect them.
