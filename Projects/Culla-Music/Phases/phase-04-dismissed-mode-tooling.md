---
title: Phase 4 — Dismissed Mode Tooling
date: 2026-05-15
tags: [culla-music, phase, dismissed, undo, haptics, long-press, snackbar, implemented]
status: implemented (compiles; on-device testing in progress)
---

# Phase 4 — Dismissed Mode Tooling

> **Status (2026-05-15):** All features merged on `main`. Builds clean against iOS 26 SDK. On-device validation tracked in [[qa-dismissed-cleanup-menu|QA — Dismissed-mode cleanup menu]].

Phase 3 left the Dismissed deck as a one-trick view: see what you'd rejected, optionally un-dismiss by right-swiping into a playlist. Phase 4 turns it into a real cleanup workspace — old rejections resurface for reconsideration, each gesture means something different, and a long-press exposes surgical playlist tools with full undo coverage.

Covers commits `2414cda` (2026-05-14) → `fb9d6f1` (2026-05-15).

---

## 1. Resurface stale dismissals in Unsorted (`2414cda`)

Dismissals older than **30 days** now reappear in the Unsorted deck so the user can revisit old rejections as taste shifts. Recent dismissals (≤ 30 days) and the Library deck are unchanged — the resurface logic is scoped to the Unsorted exclusion set.

- A red **"Dismissed"** pill on the card (later replaced by the age chip in §2) makes the prior state visible at a glance — there's no ambiguity about why a song you "rejected" is back on screen.
- **Left-swipe on a resurfaced track** updates `DismissedSong.dismissedAt` in place instead of inserting a duplicate row, so the dismissed table stays clean and the resurface window math stays correct.
- Undo for that path is `.redismissed(song:record:originalDismissedAt:)` — restores the original timestamp on undo, not "now".

**Why 30 days?** Short enough that taste-shift drift is visible, long enough that a quick dismiss doesn't haunt the user the next day. Single constant in the view model — easy to tune from data later.

**Files touched:** `ViewModels/MusicSwipeViewModel.swift` (heaviest), `Views/MusicSwipeView.swift`, `Views/PlaylistMembershipChips.swift`, `Views/SongCardView.swift`.

---

## 2. Gesture rework + dismissed-age chip (`d48a75f`)

Each gesture in the Dismissed deck is now a deliberate decision instead of a leftover from Library mode's swipe vocabulary:

| Gesture | Effect | Notes |
|---|---|---|
| **Left-swipe** | Re-confirm the dismissal — bumps `dismissedAt`, reorders the deck by recency next session. | Same code path as the resurfaced-track case in §1. |
| **Right-swipe** | Un-dismiss + sort into the chosen sidebar playlist. | Unchanged from Phase 1; was already the canonical "rescue" gesture. |
| **Up-swipe** | Love AND un-dismiss; toast reads **"Loved & restored"**. | New `.lovedFromDismissed` undo case restores the prior dismissed timestamp. |
| **Double-tap** | Skip (session-only). | Unchanged. |

The red "Dismissed" pill from §1 is replaced by a **"Dismissed Xmo ago"** chip driven by an in-memory `dismissedDates: [String: Date]` map on the view model. Compact relative-age scale: `just now / Nh / Nd / Nw / Nmo / Ny`. The same chip appears in Unsorted for resurfaced dismissals, where the age is the prompt for reconsidering.

**Why an in-memory map?** Looking up the dismissed date from SwiftData on every drag frame would re-query for nothing — the data is stable for the session. The map is populated alongside SwiftData mutations so the chip lookup stays O(1).

**Files touched:** `ViewModels/MusicSwipeViewModel.swift`, `Views/MusicSwipeView.swift`, `Views/PlaylistMembershipChips.swift`, `Views/SongCardView.swift`.

---

## 3. Long-press menu for cross-playlist cleanup (`9a3d607`)

A destructive long-press affordance lets the user strip a stale track from every Apple Music playlist it lives in, without leaving the Dismissed deck.

- **Context menu** with: `Remove from all playlists (N)` (only when N > 0) → confirmation dialog listing the playlist names → fires `removeFromAllPlaylists()`. Plus `Open in Apple Music` → SwiftUI `openURL` so the user can do a true library-delete in Apple's app (MusicKit doesn't expose that to third parties).
- **`PlaylistRemovalSnapshot`** captures each playlist plus the existing `SortedSong.sortedAt` so undo restores rows with their original timestamps instead of resetting to "now".
- The `DismissedSong` row is **untouched** — the song stays dismissed, just stops surfacing across the library.
- Apple Music removals run **sequentially**; the toast reports partial failures.
- The 0.3 s sidebar-preview `LongPressGesture` is **suppressed in Dismissed mode** so the system context menu's recognizer can claim the touch first. Right-swipe-to-sort still reveals the sidebar — the preview is the only thing lost.

This phase originally shipped with the all-or-nothing confirmation. §4 replaces it.

**Files touched:** `ViewModels/MusicSwipeViewModel.swift`, `Views/MusicSwipeView.swift`.

---

## 4. Per-playlist removal sheet + forget dismissal + snackbar undo (`fb9d6f1`)

Reworks §3's destructive flow so it's **surgical, reversible, and discoverable**. Same long-press affordance; everything downstream changed.

### 4a. `RemoveFromPlaylistsSheet`

Replaces the system confirmation dialog with a custom sheet listing the song's playlist memberships as toggleable rows, all selected by default.

- Filled red checkmark = will be removed; empty circle = spared.
- Toolbar button label updates live: `Remove (N)`.
- Empty selection disables the button — no accidental no-ops.
- Footer reminds the user: _"The song stays dismissed. These playlists are also updated in Apple Music."_
- Tracking is stored as an **excluded** set internally (`Set<String>` of AM IDs), so the default "all selected" is the empty set — no per-row init dance.

The underlying API was generalized:

```swift
// before:
func removeFromAllPlaylists()
case removedFromAllPlaylists(song:, removals:)

// after:
func removeFromPlaylists(_ playlists: [Playlist])
case removedFromPlaylists(song:, removals:)
```

Caller passes the explicit subset. The membership index now **prunes only the affected AM IDs** instead of dropping the whole entry; undo **merges** restored IDs back in so playlists the user left checked stay in the index throughout.

### 4b. Context menu preview

The system `.contextMenu(menuItems:preview:)` form now renders a preview view above the menu — artwork, title, artist, **"IN N PLAYLISTS"** header, and a dot-joined wrapping list of names. Empty case shows _"Not in any of your playlists"_. The user sees what they're about to act on before any tap.

### 4c. Inline-snackbar undo for cross-playlist removal

The top toast becomes a **snackbar** for the destructive action: message + inline `↶ Undo` button in the same capsule, persisted for **6 s** instead of the standard 1.4 s. The bottom undo button is suppressed while the snackbar is up — no duplicate Undos.

The snackbar's Undo **cancels the in-flight Apple Music removal task** before issuing the re-adds, eliminating the prior remove/add race on the same playlist. The Task handle lives on a new `pendingPlaylistRemovalTask` slot for cancellation.

### 4d. "Forget dismissal" menu item

A new menu item (`tray.and.arrow.up` icon) deletes the `DismissedSong` row without touching playlist memberships:

- If the song was in 0 playlists → it becomes Unsorted on next refresh.
- If it was in any playlists → it stays there, just no longer dismissed.

Standard 2.5 s bottom-button undo restores the row with its **original `dismissedAt`**, so the dismissed-age chip reads the same value as before the forget.

### 4e. Discoverability tip

Long-press is invisible. A one-time pill banner — _"Long-press a card for cleanup options"_ — appears in Dismissed mode, gated by `@AppStorage("hasSeenDismissedLongPressTip")`. Self-dismisses on the first successful long-press, or via an X button.

### 4f. Haptics

- `Haptics.contextMenuOpen()` (heavy impact) fires via a `simultaneousGesture(LongPressGesture(0.45))` alongside the system menu opening — same gesture also flips the tip flag.
- `Haptics.undo()` (selection feedback) ticks on every Undo tap, both snackbar inline and the bottom button.
- Gating now reads `UserDefaults.standard.object(forKey: "hapticsEnabled") as? Bool ?? true` — defaults to **on** when never set, so feedback works on first launch before `RootView.seedDefaults` runs.

### 4g. `setToast(_:undoable:)` helper (internal)

A new private helper on `MusicSwipeViewModel` pairs `toastMessage` with `toastUndoable` so the snackbar flag can't leak from a destructive action into a later, unrelated toast. **All 26** toast-set sites route through it; three opt into `undoable: true` (the snackbar path). `toastUndoable` is written **before** `toastMessage` so the view's `onChange(of: toastMessage)` reads the correct snackbar mode when picking its timer duration.

**Files touched:** `Helpers/Haptics.swift`, `ViewModels/MusicSwipeViewModel.swift`, `Views/MusicSwipeView.swift`. New: `Views/RemoveFromPlaylistsSheet.swift`.

---

## New files

- `Views/RemoveFromPlaylistsSheet.swift` — selection sheet for partial cross-playlist removal.

## Edited files

- `ViewModels/MusicSwipeViewModel.swift` — heaviest churn across the phase. Resurface logic, `redismissed` undo case, gesture rework, `lovedFromDismissed`, dismissed-date map, long-press cleanup action, per-playlist generalization, `forgetCurrentDismissal`, `setToast` helper + 26-site rewrite, snackbar-aware toast flag.
- `Views/MusicSwipeView.swift` — context-menu wiring (preview + sheet), one-time tip pill, simultaneous-gesture haptic, `setToast`-aware top-toast capsule with inline Undo, suppressed bottom undo while snackbar is up.
- `Helpers/Haptics.swift` — `contextMenuOpen`, `undo`, robust gating default.
- `Views/SongCardView.swift` — dismissed-age chip rendering.
- `Views/PlaylistMembershipChips.swift` — dismissed-state pill (later removed in favor of the age chip).

---

## Implementation notes

- **Why a sheet instead of toggles in the context-menu preview?** iOS context-menu previews aren't reliably interactive — tapping inside the preview generally dismisses the menu. The sheet route gives breathing room for the toggleable rows and keeps the menu's preview as a glance-only summary.
- **`setToast` ordering matters.** `toastUndoable` is written before `toastMessage` so the view's `onChange(of: toastMessage)` observer, which runs after the @Observable update settles, reads the correct snackbar flag for its timer duration calculation.
- **In-flight cancellation in `removeFromPlaylists`.** The Apple Music removal Task checks `Task.isCancelled` inside the loop and before publishing the final toast. Undo cancels first, then re-adds — no chance of a concurrent remove on the same playlist racing the re-add.
- **Membership-index merging on undo.** With per-playlist subsets, the old "overwrite the entry on undo" approach was wrong — it would clobber any membership the user left checked. The new code dedup-merges restored AM IDs into whatever's currently in the index.
- **Pill banner placement.** 60 pt top padding clears the back chevron on standard devices. Worth a manual check on iPhone SE.
- **Pre-existing concurrency warning unaffected.** `MusicLibraryService.startClipPositionObserver` still has the same main-actor warning pattern (see memory: `project_avplayer_concurrency_warnings`). Not touched here.

---

## Outstanding / next steps

- **Cross-song multi-select** — explicitly deprioritized. Belongs in a future Manage surface, not bolted onto the swipe deck. Open shelf item.
- **Full accessibility pass for the long-press menu** — VoiceOver users can't easily trigger a long-press; would want a parallel entry point (swipe-revealed "More" button or detail view). Cross-cutting, not scoped to Dismissed mode.
- **Manual on-device QA** — see [[qa-dismissed-cleanup-menu|QA — Dismissed-mode cleanup menu]] for the full checklist (tip banner on iPhone SE, mid-flight undo cancellation timing, haptic gating on a fresh install).
- **`Phase 5`** — open. Likely candidates: stats view ([[Ideas/stats-activity-view]]), smart-playlist suggestion chip ([[Ideas/smart-playlist-suggestion]]), or first-launch onboarding ([[Ideas/onboarding-flow]]).

---

*Phase 3 → [[Phases/phase-03-source-sorting-player-and-settings|Phase 3 — Source Sorting, Player Polish & Settings]]*
*QA checklist → [[qa-dismissed-cleanup-menu|QA — Dismissed-mode cleanup menu]]*
*Related ideas → [[Ideas/swipe-and-player-enhancements]]*
