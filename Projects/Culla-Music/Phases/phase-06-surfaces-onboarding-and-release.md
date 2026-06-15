---
title: Phase 6 — New Surfaces, Onboarding & Release Readiness
date: 2026-06-15
tags: [culla-music, phase, history, album, onboarding, localization, app-store, liquid-glass, implemented]
status: implemented (builds clean against iOS 26 SDK; on-device QA pending)
---

# Phase 6 — New Surfaces, Onboarding & Release Readiness

> **Status (2026-06-15):** Merged on `main`. The longest window so far — ~73 commits, `3e9d841` (2026-05-29 queue filter, tail of the post-Phase-5 polish) → `3188d79` (2026-06-14). Where Phase 5 was a pure design-language pass, Phase 6 is **broad**: three new surfaces, a real first-run experience, a deeper iOS 26 glass adoption, data-integrity fixes, and the whole **release-readiness** push — internationalization into 8 languages plus App Store prep. Grouped by theme below, not strictly chronological.

This is the gap the index had left undocumented since 2026-05-28.

---

## 1. Three new surfaces

- **History sheet** (`b963cc4`) — a chronological log of every sort / love / dismissal with **swipe-to-undo per row** and shared skeleton loading. This effectively *replaced* the Phase 4 Dismissed cleanup menu (see §4) as the place to reverse past actions. Fixes followed: loved songs no longer vanish from History (`8fbdbc3`), no unsynced data on first open (`5053223`), and rows **deep-link to the song in Apple Music** (`ea08bc1`).
- **Album liner-notes sheet** (`dce03b5`) — opened from an inline album info button on the now-playing card; surfaces Apple Music `Album.editorialNotes`. The album sleeve was later folded into one cohesive layout (`d334ffa`). Shipped the [[Archive/Culla-Music/Ideas/album-about-editorial-notes|Album "About"]] idea (the bigger "dedicated surface" option). Apple Music **artist** editorial notes also now sit above the Wikipedia bio in the artist hub (`77178c4`, `2596669`).
- **Date jump** (`c9abad9`, `6dbab8d`) — jump to a library-add date from the carousel and sort the session forward from there; an opt-in **date-jump inside swipe sessions** (library / unsorted / artist) via `DateJumpControl` / `DateJumpSheet` (`884f38a`). Carousel date pill kept in sync while scrolling (`548caad`), paging guarded against reentrancy during a jump (`1415d98`).

---

## 2. Onboarding & first-run

- **Brand-forward first-launch screen + gated splash** (`f45efec`, `4bf09d9`) — a splash that waits on real content load instead of flashing empty chrome.
- **One-time swipe guide** (`868d2ec`, `641b503`) — `SwipeGuideOverlay` + `CoachTip`: previews the real next cover in a centre token and **loops a soft drag hint** (lean right toward Add, then up toward Love) so the card reads as the thing you drag; skipped under Reduce Motion. Stronger one-time hero hint + stop replaying tips across sessions (`1f07d0b`). Shipped the [[Archive/Culla-Music/Ideas/onboarding-flow|onboarding]] idea, lighter than the original 3-screen sketch — taught **in place** on the deck.

---

## 3. Deeper iOS 26 Liquid Glass

- **Liquid Glass morphing across Home, Swipe, Settings** (`588125d`) and **extended to sheets** — soft scroll-edge effects + the History toast *materializing* in place (`6e42c7a`).
- **SortChip** collapsed to an icon-only native-glass circle (`9d6085e`) after a press-chrome cropping fix (`d536c02` → see [[Dev-Insights/SortChip Menu Press Chrome Crops Capsule Glass 2026-05-30|write-up]]).
- **Per-cover accent transitions** — soft lockstep accent cross-fades in the swipe deck (`dfed19a`); the deck now opens on the cover tint, not the palette accent (`55cfa35`).
- **Contrast-aware CTA text + breathing Home glow** (`0757534`).
- Settings sheet reliably restyles on a live theme change (`82db384`, building on Phase-5's `9ee8c3b`).

---

## 4. Sorting, filtering & playlist management

- **Per-playlist library queue filter** (`3e9d841`, tail of post-Phase-5) and **filter the Library swipe by artist, not just playlist** (`700f560`).
- **Sort chips on the Playlists sheet + a shared sort chip** (`dffb7f2`), menus collapsed to one row per field, Filter-queue scope switch reworked (`c0cbff2`), filter count surfaced up top + a **"Selected first"** sort toggle (`7ad33ef`).
- **Swipe-to-rename** Culla-created playlists in the Sidebar list (`2196580`).
- **33-color accent palette** with contrast-aware labels (`008ceb2`) — up from the Phase-5 set.
- **ManagePlaylistsSheet rebuilt** on a plain grouped List (`dbcc7f6`); **NewPlaylistSheet** rebuilt as a compact creation card (`e3c71b3`); swipe toast slimmed to a status pill with consolidated undo (`042804f`).
- **Dropped the Phase 4 Dismissed cleanup menu** (`436ed74`) — `RemoveFromPlaylistsSheet`, the `removedFromPlaylists` / `forgotDismissal` undo cases, and `PlaylistRemovalSnapshot` all removed. Rationale: its headline "remove from playlists" only worked on Culla-made playlists, so it was misleading on Apple-made ones. Undo now lives in the **History sheet** (§1). *(Phase 4 note annotated accordingly.)*

---

## 5. Catalog auditioning & data integrity

- **Surface catalog tracks** in playlist-scoped + dismissed decks (`b649738`) — audition songs not yet in the library.
- **Reconcile sorts against live playlists** (`ed68950`) — a shared `SortedSongReconciler` keeps deck exclusion + History phantom rows in sync with real playlist membership; reconcile is refused against an empty/failed membership map (`083e3df`), and runs off the membership rebuild rather than a re-fetch (`ec508fa`). *(See memory `project_sortedsong_voided_reconciliation`.)*
- **Bug fixes:** clear a phantom dismissed song carried across sessions (`924cd21`); stop the Library deck skipping ~half the library (`fbb61f3`); stop duplicate cards from concurrent deck refills (`cde8953`); **cold-launch freeze** fixed by isolating `HomeViewModel` to the main actor (`30d3550`).

---

## 6. Swipe-down to share + now-playing liner

- **Swipe down = Share** the current song (`31353ba`) — the last unbound gesture (down was reserved since Phase 3).
- **Now-playing liner row** — shared carousel/swipe playback chrome with a **marquee** for the centred title (`b8b08b8`), with width measured from `UIFont` not a hidden SwiftUI copy (`069a8bd`, `0940154`; see memory `project_marquee_text_width_measurement`); tiny-trail titles shrink to fit instead of scrolling (`46f9b93`).

---

## 7. Internationalization (the headline release item)

- **Full localization via String Catalogs** (`618ca12`) — the entire UI ships translated into **8 languages**: English (source) + Spanish, German, French, Italian, Japanese, Brazilian Portuguese, Simplified Chinese. Counts and relative-time strings use each locale's plural rules; the Apple Music permission prompt (`InfoPlist.xcstrings`) is localized too.
- **Audited 2026-06-15** — every translatable key (213 in `Localizable.xcstrings` + 1 in `InfoPlist.xcstrings`) is fully translated in all 7 target languages; every compiler-extracted string is covered; plain-`String` UI copy is wrapped in `String(localized:)`. Done via the `/swift-localize` skill.

---

## 8. App Store readiness

- **Bundle identifier set to `app.culla.music`** (`c80910d`); privacy manifest comment uses CullaMusic (`854f3b1`).
- **Target iPhone only** so App Store Connect stops requiring iPad screenshots (`b129783`).
- **Settings footer** shows version only, build number dropped (`a27c34d`); `CURRENT_PROJECT_VERSION` bumped (`507ac6a`).

---

## 9. Dev tooling

- **Portfolio-screenshot mode** (`eef441a`, `c6a0136`, `3188d79`) — a single `cullaScreenshotMode` flag (`PlaylistSidebarView.swift`, default off) swaps the right-drag sidebar for dressed-up sample playlists **and** guards `MusicSwipeView` so no swipe can mutate the library while framing a shot. Demo images are not bundled (re-add on demand). Documented in the repo README.
- **`DebugFlags.forceLegacyUI`** (`a5082a9`) — preview the pre-glass UI on device.

---

## 10. Perf / refactor

- Scope playback-position reads to leaf cards in swipe & carousel (`61d7ee2`); scan the carousel's centred song once per body pass (`7b1764d`); drop a per-tick allocation in the hero scrub gate (`84a614c`); tidy the HomeView count-cache — name keys, one fingerprint, static formatter (`cb1cd53`).

---

## Outstanding / next steps

- **On-device QA is well behind** — [[qa-testing-tracker|QA Testing Tracker]]'s last logged pass is 2026-05-22; this entire phase (History, album sheet, date jump, onboarding, glass morphing, localization, App Store prep) is unverified on device. Biggest pre-TestFlight risk.
- **Localized layout check** — non-English strings are longer (German especially); eyeball Settings rows, chips, and the swipe-guide copy on a small phone.
- **Still-open ideas:** [[Ideas/stats-activity-view|Stats / activity view]], [[Ideas/smart-playlist-suggestion|Smart playlist suggestion chip]], [[Ideas/artist-count-name-fallback|Name-based artist-count fallback]].
- **Next:** likely a TestFlight push, then the eventual merge into [[Projects/Culla/Culla|Culla]].

---

*Phase 5 → [[Phases/phase-05-liquid-glass-and-restraint|Phase 5 — Liquid Glass & the Restraint Pass]]*
*Project index → [[Projects/Culla-Music/culla-music|Culla Music]]*
