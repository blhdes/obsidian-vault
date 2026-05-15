---
title: QA — Dismissed-mode cleanup menu
date: 2026-05-15
tags: [culla-music, qa, testing, dismissed, long-press, undo, haptics]
---

# QA — Dismissed-mode cleanup menu

Manual tests for the long-press cleanup rework on Dismissed cards (commit `fb9d6f1`, _"feat: per-playlist removal sheet + forget dismissal + undo snackbar"_):

- **Per-playlist removal sheet** — replaces the all-or-nothing "Remove from all playlists" confirmation from `9a3d607` with a toggleable list. That older dialog is gone.
- **Context menu preview** — long-press shows the song + its playlist memberships above the menu items.
- **Inline-snackbar undo** — cross-playlist removal now offers a 6 s in-toast Undo that cancels any in-flight Apple Music removals before re-adding.
- **Forget dismissal** — new menu item un-dismisses a song without sorting it.
- **Discoverability tip** — one-time "Long-press a card for cleanup options" pill in Dismissed mode.
- **Haptics polish** — heavy impact on context-menu open, light tick on Undo. Gating now defaults to ON when never set.

Reference: [[culla-music|Culla Music — Project Index]]

---

## Per-playlist removal sheet

- [ ] In Dismissed mode, long-press a card that's in multiple playlists → context menu shows **"Remove from playlists… (N)"** with N matching the actual membership count.
- [ ] Tap it → sheet slides up with the song's artwork (80 pt) + title + artist at the top, then a list of playlist rows below.
- [ ] Every row starts with a **filled red checkmark** by default (all selected).
- [ ] Top-right toolbar button reads **"Remove (N)"** with the live count.
- [ ] Untoggle one row → checkmark becomes an empty circle, button updates to **"Remove (N-1)"**.
- [ ] Untoggle every row → **"Remove"** button is disabled (greyed).
- [ ] Confirm with one playlist unchecked → song is removed from the **checked** playlists only; verify in Apple Music that the unchecked one still contains the song.
- [ ] Song in only **1** playlist → sheet shows a single row; can still confirm with N = 1.
- [ ] Song in **5+** playlists → list scrolls cleanly; toggling stays responsive.
- [ ] Footer reminder ("The song stays dismissed. These playlists are also updated in Apple Music.") is visible.
- [ ] After confirming, the dismissed deck **does not advance** — same card stays on screen (the action is on memberships, not on the dismissed mark).
- [ ] Cancel button in the toolbar dismisses the sheet without any change.

## Context menu preview

- [ ] Long-press a dismissed card → preview view appears **above** the menu items.
- [ ] Preview shows 140 pt artwork, song title, artist name, **"IN N PLAYLISTS"** header (uppercase, caption), and a dot-joined list of names (e.g. `Workout · Roadtrip · Late Nights`).
- [ ] Names wrap to multiple lines when many; layout stays balanced (max 320 pt wide).
- [ ] Empty case: long-press a dismissed song that's in 0 playlists → preview reads **"Not in any of your playlists"** and the Remove menu item is hidden (only Forget + Open-in-Apple-Music are shown).

## Inline-snackbar undo (cross-playlist removal)

- [ ] After confirming Remove → top toast is a capsule with the message on the left and an inline **↶ Undo** button on the right.
- [ ] Snackbar persists ~6 s (longer than normal toasts at ~1.4 s).
- [ ] Bottom undo button is **not** shown while the snackbar is up (no duplicate Undos).
- [ ] Tap Undo → local membership chips reappear; verify in Apple Music that the song is back in all previously-removed playlists.
- [ ] **Mid-flight Undo**: confirm Remove on a song in 4+ playlists, tap Undo within ~1 s → no playlist ends up missing the song after the dust settles. The in-flight removal Task is cancelled before the re-adds fire.
- [ ] Toast text transitions from **"Removing from N playlists…"** → **"Removed from N playlists"** when the AM task finishes; the 6 s window resets to a fresh 6 s.
- [ ] If some AM removals fail → toast reads **"Removed from X, Y failed"** and Undo is still tappable.
- [ ] Snackbar auto-dismisses after 6 s → next non-snackbar toast (e.g. swipe a song) uses the standard 1.4 s timer with **no inline Undo** (the leak fix via `setToast`).

## Forget dismissal

- [ ] Long-press a dismissed card → menu shows **"Forget dismissal"** with a **tray.and.arrow.up** icon, positioned between Remove and Open-in-Apple-Music.
- [ ] Always shown (unlike Remove, which requires non-empty memberships).
- [ ] Tap → toast **"Dismissal forgotten"**, card flies off, dismissed deck advances to the next song.
- [ ] **Bottom** Undo button (not the snackbar) flashes for ~2.5 s.
- [ ] Tap Undo → song goes back to the front of the deck **and the dismissed-age chip matches the original** ("Dismissed Xmo ago" reads the same value as before forgetting).
- [ ] Forget a song that's in 0 playlists → next refresh of Unsorted shows it there.
- [ ] Forget a song that's in 1+ playlists → song stays in those playlists; verify via chips on a later swipe or via Apple Music.
- [ ] Repeat forget + undo a few times → no SwiftData write errors in the Xcode console.

## Discoverability tip

- [ ] First entry to Dismissed mode after install (or after clearing `hasSeenDismissedLongPressTip` in UserDefaults) → pill **"Long-press a card for cleanup options"** with a hand-tap icon appears under the back-button row.
- [ ] Tap the **X** on the pill → it fades out and stays gone (re-enter Dismissed mode → no pill).
- [ ] Without dismissing manually, perform a successful long-press → pill auto-fades; `hasSeenDismissedLongPressTip` flips to true; doesn't reappear next time.
- [ ] iPhone SE (small screen): pill doesn't visually overlap the back chevron at top-leading.
- [ ] During a right-drag (sidebar reveal): pill fades along with the rest of the chrome via `chromeOpacity`.

## Haptics

- [ ] Long-press a dismissed card → **strong (heavy) haptic** at ~0.45 s, lined up with the system context-menu actually opening.
- [ ] Tap Undo in the snackbar → **light selection tick**.
- [ ] Tap Undo in the bottom button (non-snackbar action) → **same light selection tick**.
- [ ] Settings → toggle Haptics **OFF** → repeat all of the above; no haptic feedback fires.
- [ ] Fresh install (or clear `hapticsEnabled` in UserDefaults) → haptics fire by default on the very first long-press, even before opening Settings (the gating defaults to ON unless explicitly disabled).

---

## Notes

- `removeFromAllPlaylists()` → `removeFromPlaylists(_:)`, and the matching `.removedFromAllPlaylists` SwipeAction case → `.removedFromPlaylists`. Payload unchanged; the `PlaylistRemovalSnapshot` mechanism still captures `sortedAt` per playlist so Undo restores local rows with original timestamps.
- The undo branch for `.removedFromPlaylists` now **merges** restored AM IDs into the membership index instead of overwriting. Spared playlists stay in the index throughout, so Undo only re-adds the removed ones.
- `setToast(_:undoable:)` is the new single entry point for toast updates. Direct `toastMessage = …` assignments would re-introduce the `toastUndoable` leak — keep all toast writes routed through the helper.
- The pre-existing AVPlayer main-actor warning in `MusicLibraryService.startClipPositionObserver` is unaffected by this change (see global memory for the planned fix the next time that file is touched).
