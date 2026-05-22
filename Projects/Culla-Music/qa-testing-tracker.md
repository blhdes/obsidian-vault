---
title: QA Testing Tracker
date: 2026-05-22
tags: [culla-music, qa, testing, tracker]
up_to_date_through: 2ce722a (2026-05-22)
---

# Culla Music — QA Testing Tracker

Single source of truth for **all** manual QA on Culla Music. Replaces the three
older per-feature notes (`qa-hero-transition.md`, `qa-dismissed-cleanup-menu.md`,
`qa-loved-up-swipe.md`) — their content lives below, intact.

Reference: [[culla-music|Culla Music — Project Index]]

---

## How to use this tracker

- **One section per shipped change**, ordered newest first.
- Each section header carries the date + commit SHA so it's easy to map back to
  `git log`. When a feature ships across several commits, the section lists them all.
- Checkbox legend:
  - `[ ]` not yet verified on device
  - `[x]` verified working
  - `[!]` issue found — leave a note in the section's **Notes** subheading
- When a feature is fully green and stable, leave the section in place — it
  documents the regression surface for future changes.

## At a glance — what still needs hands-on coverage

Items below are the ones with at least one un-ticked box.

- 2026-05-22 — Settings + playlist sheets glass redesign
- 2026-05-22 — Palette: 8 new swatches + editable while Match Song Artwork is ON
- 2026-05-22 — Solo-artist hero + stable artist picker load
- 2026-05-22 — Home mode tile copy + scrub deck tightening
- 2026-05-22 — Empty-sidebar release opens Manage
- 2026-05-21 — Drag-to-scrub peek deck on Home hero stack
- 2026-05-21 — Wordmark accent dot → Culla brand logo
- 2026-05-21 — Opt-in dismissed surfacing for scoped sessions
- 2026-05-21 — Play button reveal synced to hero morph
- 2026-05-20 — HomeView redesign + Liquid Glass vocabulary app-wide
- 2026-05-20 — Hero stack previews next two covers
- 2026-05-20 — Home ambient background tinted by hero artwork
- 2026-05-20 — Source picker performance pass (paginate artists, memoize, debounce)
- 2026-05-20 — Artist hub: stops showing wrong artist on name collision
- 2026-05-20 — Cancellation correctness (cold-start counts, flyOff hand-off)
- 2026-05-19 — Source picker: search, sort, Artist tab + track counts
- 2026-05-19 — Sort songs from a library artist
- 2026-05-19 — App icon: light/dark/tinted variants
- 2026-05-19 — Home ↔ Swipe hero morph (the older qa-hero-transition checklist)
- 2026-05-18 — Artist hub sheet from the swipe card
- 2026-05-18 — Source-playlist deck shows full collection + UX polish
- 2026-05-18 — Track count next to each playlist row
- 2026-05-16 — Tint monochrome artwork instead of palette drop
- 2026-05-15 — Dismissed-mode cleanup menu (per-playlist removal, Forget, snackbar)
- 2026-05-14 — Loved up-swipe + duplicate Culla Loves fixes (some items already verified)

---

# 2026-05-22

## Settings + playlist sheets glass redesign

**Commits:**
- `b366dda` feat: redesign Settings and playlist sheets with GlassPanel vocabulary
- `67d4c16` feat: polish modal sheets with glass touches and animated selection

### Visual
- [ ] Open **Settings** from Home → sheet uses the new GlassPanel vocabulary
  (translucent material, soft inner highlight, per-section icons), not the old
  `Form` style.
- [ ] Section icons line up with their labels; spacing reads playful, not stock-iOS.
- [ ] Open **Manage Playlists**, **New Playlist**, **Sort From**, **Loved target
  picker** → all four sheets carry the same GlassPanel look.
- [ ] Selected row in any picker animates in (not an instant snap) — gentle
  spring on the chip / checkmark / accent.
- [ ] Light mode + dark mode both read clean — no muddy translucency in dark.

### Behaviour (no regressions)
- [ ] All Settings toggles (haptics, dynamic accent, include curated, match
  song artwork, loved target) still persist across relaunch.
- [ ] Manage Playlists toggles still update sidebar membership.
- [ ] New Playlist creation still calls AM correctly and shows in Manage.

### Notes
_(record observations here)_

---

## Palette — 8 new swatches + editable with Match Song Artwork ON

**Commits:**
- `4ae19f0` feat: add 8 new accent palette swatches
- `2ce722a` fix: keep palette swatches editable when Match song artwork is on

- [ ] Settings → Accent → 8 new swatches are visible and selectable.
- [ ] Toggle **Match song artwork** ON → swatches **remain tappable** (not greyed).
  Picking a swatch updates the manual fallback even while Match is ON.
- [ ] With Match ON: app tint reads from artwork; Match OFF: app tint reverts
  to the last-picked swatch.
- [ ] Quickly toggle Match ON/OFF a few times → no flicker, no stale tint.

### Notes

---

## Solo-artist hero + stable artist picker load

**Commit:** `a0ee236` fix: solo artist hero + stable artist picker load

- [ ] Pick an artist with **only one library track** in the source picker → the
  hero preview renders that single artwork (no empty stack, no crash).
- [ ] Open the source picker → Artists tab → list loads **once** and stays
  stable; no jitter, no thumbnails swapping after settle.
- [ ] Close and reopen the picker → no full re-fetch; counts and artwork are
  remembered.
- [ ] Background → foreground the app → re-open picker → still stable.

### Notes

---

## Home mode tile copy + scrub deck tightening

**Commits:**
- `0bf5be8` fix: shorten Home mode tile descriptions
- `06dc28b` refactor: tighten the Home scrub deck
- `0f1cfb6` tune: shorten scrub deck reveal distance to 80pt
- `8635f6a` fix: let the scrub gesture start anywhere in the hero section

- [ ] Home → mode tiles (Library / Unsorted / Dismissed) show the new shorter
  descriptions; nothing wraps awkwardly on iPhone SE or Pro Max.
- [ ] Drag down on the hero section → scrub deck reveals at **~80 pt** drag
  distance (used to need more travel).
- [ ] Start the scrub gesture from **any point inside the hero**, not just the
  artwork — it should pick up the drag.
- [ ] Release the drag → deck snaps closed cleanly; no overshoot or stuck state.

### Notes

---

## Empty-sidebar release opens Manage

**Commit:** `7869bf9` feat: empty-sidebar release opens Manage + polish pass

- [ ] Drag a card onto the sidebar area when the sidebar has **zero playlists
  enabled** → on release, the **Manage Playlists sheet** opens automatically
  instead of silently dropping the gesture.
- [ ] Toast or onboarding hint communicates the redirect (no silent failure).
- [ ] Configure at least one sidebar playlist → drag-to-drop works as before.
- [ ] Other "polish pass" items mentioned in the commit body still feel right
  (re-check commit if anything else looks off).

### Notes

---

# 2026-05-21

## Drag-to-scrub peek deck on Home hero stack

**Commit:** `ac61938` feat: drag-to-scrub peek deck on Home hero stack

- [ ] Vertically drag the Home hero artwork → adjacent covers (next + previous
  in the user-sorted order) **scrub into view**, like a deck peeking.
- [ ] The currently-centered cover changes as you scrub.
- [ ] Release mid-scrub → snaps to the **nearest cover** with a gentle spring.
- [ ] The scrub gesture does NOT conflict with the Start-Cullaing tap — a tap
  still launches the deck cleanly.
- [ ] Counts (Library / Unsorted / Dismissed) update to match the cover-in-focus
  if relevant to the mode.

### Notes

---

## Wordmark accent dot → Culla brand logo

**Commit:** `93c0698` feat: swap wordmark accent dot for the Culla brand logo

- [ ] Home wordmark shows the **Culla brand logo** in place of the small accent dot.
- [ ] Logo tints correctly under all accent palettes (including the new 8 swatches).
- [ ] Match Song Artwork ON → logo follows the artwork tint.

### Notes

---

## Opt-in dismissed surfacing for scoped sessions

**Commit:** `124de50` feat: opt-in dismissed surfacing for scoped sessions

- [ ] Open the source picker → start a session scoped to one playlist / artist →
  a toggle / opt-in lets dismissed songs re-surface **within that scope** only.
- [ ] With the opt-in OFF (default) → scoped session excludes dismissed songs as before.
- [ ] With the opt-in ON → previously-dismissed songs from that scope appear in
  the deck again; swiping right resolves the dismissal correctly.
- [ ] Leaving the scoped session and starting a non-scoped one → the opt-in
  state does not bleed across.

### Notes

---

## Play button reveal synced to hero morph

**Commit:** `023ff5a` fix: sync play button reveal to hero morph completion

- [ ] Tap **Start Cullaing** → during the hero morph, the play button on
  `SongCardView` is **hidden**, then fades in **after** the morph settles.
- [ ] No early flash of the play button during the morph.
- [ ] Tap back → morph back; play button fades out in sync with the morph start.

### Notes

---

# 2026-05-20

## HomeView redesign + Liquid Glass vocabulary

**Commits:**
- `7932595` feat: redesign HomeView and propagate Liquid Glass vocabulary app-wide
- `f60704d` refactor: scope accent colouring to critical surfaces only
- `301cf86` chore: drop dead RootView.activeConfig

- [ ] Home reads as a single Liquid Glass surface — translucent panels, layered
  highlights, no leftover stock-form chrome.
- [ ] Accent tint shows only on **critical surfaces** (CTA, chips, active drop
  targets). Background panels stay neutral material.
- [ ] Mode cards, Sort-From row, Start button all share the new vocabulary.
- [ ] Dark mode + light mode both legible (no muddy contrast).
- [ ] No visual regression on iPhone SE.
- [ ] Cold launch → Home renders without flashing default colours before the
  ambient tint settles.

### Notes

---

## Home ambient background tinted by hero artwork

**Commits:**
- `aa82130` feat: tint Home background with hero artwork and clamp ArtworkImage sizes
- `3de71df` fix: stop HomeAmbientBackground from inflating HomeView past screen edges

- [ ] Home background subtly takes the **hero artwork's dominant color** without
  drowning out content.
- [ ] HomeView does not get pushed past screen edges (no horizontal/vertical
  overflow under the ambient layer).
- [ ] Switch the hero cover (via scrub deck) → background tint cross-fades in
  step with the new cover.
- [ ] Monochrome artwork → background falls back to a sensible derived palette
  (see also: tint-monochrome QA below).

### Notes

---

## Hero stack previews next two covers in user-sorted order

**Commit:** `0ebd776` feat: hero stack previews the next two covers in user-sorted order

- [ ] Home hero shows the current cover front-and-center with **two more covers
  peeking behind** in the user-sorted order.
- [ ] Order matches the sort selected on Home (alpha asc / desc / shuffle etc.).
- [ ] Solo-artist edge case (only one track) → see `a0ee236` checklist above.
- [ ] Empty library → no crash; falls back to placeholder hero.

### Notes

---

## Swipe back button — full-rectangle hit area

**Commit:** `2dc2e7b` fix: make swipe back button's hit area the full rectangle

- [ ] In Swipe view, tap the back chevron **anywhere inside its bounding rect**
  (not just the glyph) → returns to Home.
- [ ] No accidental triggers when dragging cards.

### Notes

---

## Source picker performance + polish pass

**Commits:**
- `5972cda` fix: paginate library artists and drop misleading zero counts
- `737ed70` refactor: collapse source-picker sort UI into an inline chip
- `560ea63` fix: stop refetching artist counts on every picker open
- `2805334` perf: skip the duplicate library walk on picker open
- `fb40c86` fix: stop flickering artist thumbnails during library-artist refresh
- `6e356e7` fix: artist-source loader stops spinning after a failed fetch
- `f37a140` perf: memoize source-picker filter and sort
- `27b8224` fix: MembershipIndex.trackCount stops collapsing unknown into 0

- [ ] Open the source picker → Artists tab → **paginates** in batches; no
  hang on a 500+ artist library.
- [ ] Artists with **unknown counts** show "—" (or equivalent), not "0".
- [ ] Sort UI is an **inline chip**, not a stacked control.
- [ ] Reopen the picker → counts and thumbnails are remembered (no re-fetch flicker).
- [ ] Force-quit + relaunch → first open triggers a fetch; subsequent opens are instant.
- [ ] Trigger a library-artist refresh while the picker is open → thumbnails
  **do not flicker** between placeholders and real art.
- [ ] Disconnect network → fail the fetch → loader **stops spinning** and shows
  a sensible empty/error state (no infinite spinner).
- [ ] Type fast in the search box → filter is memoized; no per-keystroke jank.
- [ ] Browse playlists with both known and unknown track counts → row counts
  match Apple Music; unknowns are never silently shown as 0.

### Notes

---

## Artist hub — stops showing the wrong artist on name collision

**Commit:** `f2b1732` fix: artist hub stops showing the wrong artist on name collision

- [ ] Pick a song whose artist shares a name with another (different MusicKit
  IDs) → opening the **Artist hub sheet** shows the artist whose ID matches
  the song, not a name-collision sibling.
- [ ] Top tracks shown in the hub belong to the right artist.
- [ ] Apple Music link opens the correct artist page.

### Notes

---

## Cancellation correctness — cold-start counts & flyOff hand-off

**Commits:**
- `0cf73b1` perf: don't await the cold-launch membership rebuild on Home
- `02deea5` fix: cold-start count walk is now cancellable on toggle flip
- `a216824` fix: flyOff hand-off is cancellable on rapid re-swipes
- `7d30e73` perf: collapse N membership-index snapshots into one per debounce burst
- `4eb8f56` fix: mark ArtistCountsSnapshot nonisolated so detached decode can return it

- [ ] Cold launch → Home appears immediately; counts populate **after** the
  hero renders (not blocking it).
- [ ] On Home, flip **Include curated** while the cold-start count walk is
  in flight → walk **cancels and restarts** with the new scope; no double-set
  of counts.
- [ ] In Swipe, rapid-swipe 5+ cards in quick succession → no hung "flyOff"
  animation, no orphan card stuck mid-fly. Each new swipe **cancels the
  previous hand-off**.
- [ ] During a burst of membership changes (e.g. multi-playlist removal undo)
  → membership index emits **one snapshot per debounce window**, not N.
- [ ] No `data race` warnings in Xcode Thread Sanitizer for ArtistCountsSnapshot
  decodes.

### Notes

---

# 2026-05-19

## Home ↔ Swipe matched-geometry hero morph

**Commit:** `8ba54b4` feat: hero morph transition from Home to Swipe deck

Original notes preserved from `qa-hero-transition.md` (2026-05-19). Tap-target
overlap with `023ff5a` (play button sync) and `2dc2e7b` (back button hit area)
above — keep an eye on both during this checklist.

**Files touched (original):**
- `Helpers/Transitions.swift` (new)
- `Views/RootView.swift`, `Views/HomeView.swift`, `Views/MusicSwipeView.swift`, `Views/SongCardView.swift`

### Forward morph (Home → Swipe)
- [ ] Tap **Start Cullaing** with the library warm → button visibly stretches
  into the album artwork's rounded rect (no cut, no fade-only).
- [ ] Home recedes (scale ~0.92, fades) behind incoming Swipe view.
- [ ] Artwork settles without a secondary jump.
- [ ] Reads as **one continuous motion**.
- [ ] Repeat in Library / Unsorted / Dismissed modes — same feel.
- [ ] Repeat with a source playlist selected (Sort From …) — same feel.

### Back morph (Swipe → Home)
- [ ] Tap the back chevron → artwork shrinks back into the Start button's
  position (full width minus 24pt horizontal padding, near bottom).
- [ ] Home springs 0.92 → 1.0 + fades **during** shrink, not after.
- [ ] No ghost of the artwork lingers centre-screen.
- [ ] No flash of system background between screens.

### Spring tuning
- [ ] `response: 0.55` — feels right? Note if too fast/slow.
- [ ] `dampingFraction: 0.85` — any bounce/overshoot? Should land cleanly.
- [ ] Forward vs back feel **symmetric**.

### Loading-window edge case
- [ ] Cold-start tap test — kill app, relaunch, tap Start immediately. Morph
  ends at empty space before card fades in — acceptable if card appears
  within ~300 ms.
- [ ] Slow network (3G via Network Link Conditioner) — same observation.
- [ ] Dismissed mode with zero dismissed songs → morph terminates at
  EmptyStateView; note if acceptable or jarring.

### Hero source uniqueness (no console warnings)
- [ ] Forward + back round-trip → **zero** `matchedGeometryEffect` warnings.
- [ ] Swipe a card off-screen so the next card slides in → no warning. (Next-
  card preload uses `heroNamespace: nil` and the `matchedHero` no-op helper.)
- [ ] Trigger EmptyStateView (dismiss every card in a mode) → exit back to
  Home → no warnings.

### Interaction with existing chrome / gestures
- [ ] Forward morph: back chevron doesn't flash before content fades in.
- [ ] Back morph: visible toast/undo banner fades cleanly with the swipe view
  — no orphan banner mid-screen.
- [ ] Mid-swipe (card partially dragged) → tap back → morph still works
  (note if it morphs from dragged offset or snaps to center first).
- [ ] Long-press Dismissed card → context menu → dismiss menu → tap back →
  morph still clean.
- [ ] Open Manage Playlists sheet from Swipe → dismiss → tap back → morph
  still clean (no leftover sheet dimming).

### Cross-device / mode checks
- [ ] Light + dark mode — both correct (no colour flash).
- [ ] Dynamic accent on vs off — morph reads the same.
- [ ] iPhone with home indicator vs older bezel — back chevron position
  and morph target both look right.
- [ ] iPad (if supported) — same checks.

### Performance
- [ ] No frame drops (60fps min, 120fps on ProMotion).
- [ ] Round-trip Home ↔ Swipe ~10 times → no obvious memory growth.

### Notes
_(capture surprises here)_

---

## Sort songs from a library artist (scope by artist)

**Commits:**
- `00b7e2b` feat: scope swipe sessions by library artist
- `53993d6` feat: initials fallback for artists without catalog artwork
- `35f3d68` feat: warm membership snapshot on Home so source counts work on first launch
- `d1f8a71` fix: tighten Home count flows — source-aware, race-safe, flicker-free
- `43c72d0` fix: correct unsorted exclusion and dismissed loading state

- [ ] Open the source picker → Artists tab → pick an artist → start session
  → deck shows **only that artist's library tracks**.
- [ ] Right-swipe adds to the chosen playlist (the artist scope does not
  block normal sorting).
- [ ] Counts on Home reflect the artist scope (Library/Unsorted/Dismissed
  within that artist's tracks).
- [ ] An artist with no catalog artwork → **initials fallback** renders
  (no broken-image icon).
- [ ] Cold launch → enter artist source for the first time → counts populate
  without flicker (membership snapshot warms on Home).
- [ ] Toggle scope between two artists rapidly → counts settle to the
  correct one (no race).

### Notes

---

## Source picker — search, sort + track counts for artist rows

**Commits:**
- `042c7e0` feat: search and sort for the source picker
- `514edb2` feat: track counts for artist rows in source picker

- [ ] Source picker has a **search field** that filters playlists + artists
  live.
- [ ] Sort options (alpha asc/desc, track count, recent) work for both
  Playlist and Artist tabs.
- [ ] Each **artist row** shows its track count next to the name.
- [ ] Counts match the deck length when the scope is started.

### Notes

---

## App icon — light, dark, tinted variants

**Commits:**
- `28c1875` feat: add app icon with light, dark, and tinted variants
- `e21b801` fix: show full vinyl in dark and tinted app icons

- [ ] Default icon (light) renders correctly on the Home Screen.
- [ ] Toggle iOS appearance to **Dark** → icon swaps to dark variant.
- [ ] Toggle to **Tinted** → icon respects the chosen home-screen tint.
- [ ] In both dark and tinted variants, the **full vinyl** is visible
  (no cropping/clipping).
- [ ] App icon shows correctly in Settings, Spotlight, Notification Center.

### Notes

---

## Artist hub CTAs — Apple Music + Google + play

**Commits:**
- `15500a1` feat: play/pause top songs in artist hub and add Apple Music link
- `719105b` feat: use official "Listen on Apple Music" badge for artist hub CTA
- `6d34ef2` feat: brand the artist-hub Google CTA with the official "G" mark

- [ ] Open artist hub → top-songs list has a **play/pause** button per row.
- [ ] Tap play → ApplicationMusicPlayer plays the song (or 30s preview for
  non-subscribers).
- [ ] Tap pause → playback stops.
- [ ] "**Listen on Apple Music**" CTA uses the **official badge** (Apple's
  styling, not a custom button).
- [ ] Google CTA shows the **official multicolor "G" mark**.
- [ ] Both CTAs deep-link correctly (Apple Music opens to the artist; Google
  opens a relevant search).

### Notes

---

# 2026-05-18

## Artist hub sheet from the swipe card

**Commit:** `3577d6e` feat: artist hub sheet from the swipe card

- [ ] On a swipe card, tap the artist name → **Artist Hub sheet** opens.
- [ ] Sheet shows artist artwork, top tracks, a short bio area, and CTAs
  (see the CTA checklist under 2026-05-19).
- [ ] Dismiss the sheet → returns to the card without disturbing the deck.
- [ ] Open the hub for an artist already covered by the name-collision fix
  (`f2b1732`) → correct artist is shown.

### Notes

---

## Source-playlist deck shows the full collection + UX polish

**Commits:**
- `b7f9086` feat: source-playlist deck shows the full collection
- `cd1d597` feat: polish source-playlist picker UX
- `bf40cc2` fix: surface freshly-loved songs when sorting from their playlist

- [ ] Sort From a playlist → deck contains the **full playlist** (not just
  the unsorted subset).
- [ ] Source picker UX feels polished (clear row separators, consistent
  spacing, no janky reload).
- [ ] Up-swipe a song into Culla Loves, then start a Sort-From session on
  the Culla Loves playlist → the just-loved song appears in the deck.

### Notes

---

## Track count next to each playlist row

**Commit:** `d775bb9` feat: show track count next to each playlist row

- [ ] Manage Playlists sheet — each row shows a track count.
- [ ] Source picker → Playlists tab — same.
- [ ] Counts match Apple Music's count for that playlist.

### Notes

---

# 2026-05-16

## Tint monochrome artwork instead of palette drop

**Commit:** `4c83085` feat: tint monochrome artwork instead of dropping to palette

- [ ] All-black / all-white artwork → app tint becomes a **subtle tint of the
  monochrome value**, not the default palette accent.
- [ ] Mixed-mono artwork still produces a sensible gradient via AccentExtractor.
- [ ] Cards switch covers → tint cross-fades smoothly, no harsh swap.

### Notes

---

## Cached playlist memberships (perf-only)

**Commits:**
- `9583912` perf: cache playlist memberships so chips render instantly
- `b951e18` style: soften Manage button so it recedes into the chrome

_No user-visible behaviour change; mainly a perf + look-and-feel item._

- [ ] Membership chips on cards appear **immediately** (no one-beat delay).
- [ ] Manage button reads as recessive chrome, not a primary CTA.
- [ ] Add/remove a song from a playlist (via context menu) → chip updates
  on the next card without a full re-render.

### Notes

---

# 2026-05-15

## Dismissed-mode cleanup menu

**Commit:** `fb9d6f1` feat: per-playlist removal sheet + forget dismissal + undo snackbar

Original notes preserved from `qa-dismissed-cleanup-menu.md`.

**What this covers:**
- **Per-playlist removal sheet** — replaces the all-or-nothing "Remove from
  all playlists" dialog from `9a3d607` (now removed).
- **Context menu preview** — long-press shows song + memberships above menu items.
- **Inline-snackbar undo** — cross-playlist removal offers a 6 s in-toast Undo
  that cancels in-flight AM removals before re-adding.
- **Forget dismissal** — new menu item un-dismisses without sorting.
- **Discoverability tip** — one-time pill in Dismissed mode.
- **Haptics polish** — heavy on context-menu open, light tick on Undo.

### Per-playlist removal sheet
- [ ] In Dismissed mode, long-press a card in multiple playlists → context
  menu shows **"Remove from playlists… (N)"** with N = real count.
- [ ] Tap it → sheet slides up with artwork (80pt) + title + artist, then a
  list of playlist rows.
- [ ] Every row starts with a **filled red checkmark** (all selected).
- [ ] Top-right toolbar reads **"Remove (N)"** with live count.
- [ ] Untoggle one → checkmark becomes an empty circle; button updates to
  **"Remove (N-1)"**.
- [ ] Untoggle every row → **Remove** button disabled (greyed).
- [ ] Confirm with one unchecked → song removed from **checked** only;
  verify in Apple Music that the unchecked one still has the song.
- [ ] Song in 1 playlist → single row; can confirm with N = 1.
- [ ] Song in 5+ playlists → list scrolls; toggling stays responsive.
- [ ] Footer reminder is visible (stays-dismissed + AM update note).
- [ ] After confirming, dismissed deck **does not advance** — same card.
- [ ] Cancel button dismisses sheet without change.

### Context menu preview
- [ ] Long-press dismissed card → preview appears **above** the menu items.
- [ ] Shows 140pt artwork, song title, artist, **"IN N PLAYLISTS"** header
  (uppercase, caption), dot-joined list (e.g. `Workout · Roadtrip · Late Nights`).
- [ ] Wraps when many; layout balanced (max 320pt wide).
- [ ] **Empty case:** song in 0 playlists → preview reads **"Not in any of
  your playlists"**; Remove item hidden (only Forget + Open-in-AM shown).

### Inline-snackbar undo (cross-playlist removal)
- [ ] After Remove → top toast is a capsule with message + inline **↶ Undo** button.
- [ ] Snackbar persists ~6 s (longer than normal 1.4 s toasts).
- [ ] Bottom undo button **not** shown while snackbar is up.
- [ ] Tap Undo → membership chips reappear; AM confirms song restored.
- [ ] **Mid-flight Undo:** confirm Remove on 4+ playlists, tap Undo within
  ~1 s → no playlist ends up missing the song after dust settles. (In-flight
  removal Task is cancelled before the re-adds fire.)
- [ ] Toast text transitions **"Removing from N playlists…"** →
  **"Removed from N playlists"** when AM finishes; 6 s window resets.
- [ ] Partial failure → reads **"Removed from X, Y failed"**; Undo still tappable.
- [ ] Snackbar auto-dismisses after 6 s → next non-snackbar toast uses
  standard 1.4 s with **no inline Undo** (the `setToast` leak fix).

### Forget dismissal
- [ ] Long-press dismissed card → menu shows **"Forget dismissal"** with
  **tray.and.arrow.up** icon, between Remove and Open-in-AM.
- [ ] Always shown (unlike Remove, which hides on empty memberships).
- [ ] Tap → toast **"Dismissal forgotten"**, card flies off, deck advances.
- [ ] **Bottom** Undo button (not snackbar) flashes for ~2.5 s.
- [ ] Tap Undo → song goes back to the front; dismissed-age chip matches
  the original ("Dismissed Xmo ago").
- [ ] Forget a song in 0 playlists → next refresh of Unsorted shows it.
- [ ] Forget a song in 1+ playlists → song stays in those; verify on next
  swipe or in Apple Music.
- [ ] Repeat forget + undo → no SwiftData write errors in console.

### Discoverability tip
- [ ] First entry to Dismissed mode after install (or after clearing
  `hasSeenDismissedLongPressTip` in UserDefaults) → pill **"Long-press a
  card for cleanup options"** with hand-tap icon under back-button row.
- [ ] Tap **X** on pill → fades, stays gone next time.
- [ ] Without manual dismiss, perform a successful long-press → pill auto-
  fades; `hasSeenDismissedLongPressTip` = true; no re-appear next time.
- [ ] iPhone SE: pill doesn't overlap back chevron at top-leading.
- [ ] Right-drag (sidebar reveal): pill fades with chrome via `chromeOpacity`.

### Haptics
- [ ] Long-press dismissed card → **heavy haptic** at ~0.45 s, aligned with
  context menu opening.
- [ ] Tap Undo in snackbar → **light selection tick**.
- [ ] Tap Undo in bottom button → same light tick.
- [ ] Settings → Haptics OFF → repeat — no feedback fires.
- [ ] Fresh install (or clear `hapticsEnabled`) → haptics fire by default
  on the first long-press (gating defaults to ON unless explicitly disabled).

### Notes
- `removeFromAllPlaylists()` → `removeFromPlaylists(_:)` and
  `.removedFromAllPlaylists` → `.removedFromPlaylists` (SwipeAction case).
  Payload unchanged; `PlaylistRemovalSnapshot` still captures `sortedAt`
  per playlist so Undo restores local rows with original timestamps.
- Undo branch for `.removedFromPlaylists` **merges** restored AM IDs into
  the membership index instead of overwriting. Spared playlists stay in
  the index throughout, so Undo only re-adds the removed ones.
- `setToast(_:undoable:)` is the single entry point for toast updates.
  Direct `toastMessage = …` assignments would re-introduce the
  `toastUndoable` leak — keep all writes routed through the helper.
- The pre-existing AVPlayer main-actor warning in
  `MusicLibraryService.startClipPositionObserver` is unaffected by this
  change (see project memory for the planned fix the next time that file
  is touched).

---

# 2026-05-14

## Loved up-swipe + duplicate Culla Loves fixes + perf pass

Original notes preserved from `qa-loved-up-swipe.md`. Some items already
verified before this tracker existed — keep their `[x]` state.

**What this covers:**
- **Up-swipe transition** (`da5b506`) — card flies fully off-screen.
- **Stop duplicating Culla Loves** (`728f706`) — first add to a freshly-
  created loved playlist no longer trashes it on transient failure; 600 ms
  post-create delay reduces first-failure odds.
- **Hide loved from Manage** (`728f706`) — loved target filtered out of
  Manage Playlists sheet.
- **Performance pass** (pre-`728f706`) — parallel playlist track fetch,
  deferred membership index, memoized `playlistMemberships`, tighter swipe
  timing (0.18s fly-off + 0.25s slide-in), accent prefetch for next card,
  single-pass `AccentExtractor`.

### Up-swipe transition (visual)
- [x] Up-swipe with enough velocity → current card visibly leaves the top
  before the next song appears (no snap-from-the-middle).
- [x] New card slides down + fades in from off-screen — similar pacing to
  right-swipe-to-sidebar.
- [x] Total swipe-to-settled is noticeably tighter than the pre-perf-pass
  build (~430 ms now vs ~570 ms before) but still smooth, not a snap.
- [x] Drag up below threshold + release → springs back to centre, no Loved
  action fires.
- [x] Drag up past threshold → pink heart overlay reaches full opacity
  before release.
- [x] Right-swipe onto a sidebar playlist still works (no regression from
  the y-damping change or shorter timings).

### Culla Loves auto-creation
- [x] Fresh install (or after deleting `Culla Loves` in AM + clearing
  defaults) → first up-swipe creates **exactly one** `Culla Loves`.
- [x] Force-quit + relaunch → up-swipe again → **no new playlist**;
  existing one is reused.
- [x] Repeat for 3 sessions → still only **one** `Culla Loves`.
- [ ] If first up-swipe surfaces *"Couldn't reach Culla Loves — try again"*,
  a second up-swipe a few seconds later succeeds **without** creating another.
- [ ] Up-swipe a song already in the loved playlist → toast **"Already loved"**;
  song not duplicated.

### Loved target in Settings
- [ ] Pick a normal user playlist as loved target → up-swipe adds to **that**
  playlist (not Culla Loves).
- [ ] Pick a known read-only playlist (e.g. *Favorite Songs* / smart Favorites)
  — if it slips past the name filter, the first up-swipe should **self-heal**:
  picker resets, playlist hidden from future pickers.
- [ ] Switch loved target between Culla Loves and a custom playlist in
  Settings → works without restart.

### Manage Playlists sheet (Swipe → Manage)
- [ ] Current loved target **does not appear** in Manage list.
- [ ] Change loved target → reopen Manage → previously-loved playlist
  appears; newly-loved one is hidden.
- [ ] If no loved target configured (empty defaults) → **all** editable
  playlists appear as usual.
- [ ] **Sort From** picker (Home → "Sort from playlist") still shows the
  loved target — only Manage hides it.

### Undo + rollback
- [ ] Up-swipe → Undo toast → tap Undo → song removed from loved playlist
  locally and remotely.
- [ ] If remote add to Culla Loves fails (no success toast), chip under
  the song doesn't lie — loved chip disappears after rollback.
- [ ] Sort/love a song → next card's chips reflect reality for the *previous*
  card's playlists (membership cache invalidates on every add/remove).
- [ ] Undo a sort → reopen the same card via the queue → previously-added
  playlist **no longer shows** as a chip.

### Performance pass — initial load
- [ ] Cold launch → tap Start in library mode → first card appears within
  ~1 s on a normal-sized library (was ~6 s with 30+ playlists pre-pass).
- [ ] On first card in library/dismissed mode, membership chips may **pop
  in a beat after the card** — this is **expected** (background index).
- [ ] Unsorted mode → first card still waits for playlist scan (needs the
  exclusion set), but the wait is much shorter than before (parallel fetch).
- [ ] Toggle **Include curated** in Settings → re-enter unsorted →
  counts + deck reflect new scope (parallel fetch returns correct data
  for both scopes).

### Performance pass — swipe transitions
- [ ] Left/right/up swipes feel **snappy but smooth** — no micro-stutter.
- [ ] During drag, the card never **hitches or pauses** — `playlistMemberships(for:)`
  memoization should prevent SwiftUI from re-rendering per drag frame.
- [ ] When the new card lands, its **accent gradient is already correct**
  (no visible color cross-fade). Next card's accent is prefetched.
- [ ] Swipe without playing the preview first → no audio glitch, no spurious
  "stop" haptics (`stopPreview()` early-returns when nothing's playing).

### Performance pass — edge cases / regressions
- [ ] Large library / 30+ playlists → initial load completes without AM
  rate-limit errors. If it fails, parallel TaskGroup propagates the first
  error — check for a toast/log entry.
- [ ] Force-quit during initial load → re-launch → state is clean; no
  half-built membership index leaking.
- [ ] AccentExtractor: mostly-monochrome artwork (e.g. all-black cover) →
  still produces a sensible gradient (falls back to `derivedSecondary`).
- [ ] AccentExtractor: two distinct dominants → gradient visibly reflects
  **both** colors (scoring bugfix means the secondary picker sees correct
  bucket scores).

### Notes
- 600 ms post-create delay is best-effort — on slow networks AM may need
  more. The safety net: we no longer trash the playlist on first-attempt
  failure, so next up-swipe retries against the same playlist.
- Duplicate `Culla Loves` playlists from before the fix shipped need to be
  **deleted manually** in Apple Music — the app won't GC them.

---

## Maintenance — when adding a new section

1. Bump the `up_to_date_through` field in the frontmatter to the newest
   commit included.
2. Put the new section under the right date header at the top.
3. Add a one-line entry to **At a glance — what still needs hands-on coverage**.
4. When every box in a section is `[x]`, remove that section's bullet from
   the At-a-glance list (but leave the section in place as regression doc).
