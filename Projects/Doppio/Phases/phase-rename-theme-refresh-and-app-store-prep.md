---
title: Rename, Theme & Motion Refinement, and App Store Prep
date: 2026-06-22
tags: [doppio, phase, rename, themes, accessibility, app-store, done]
status: shipped
---

# Rename, Theme & Motion Refinement, and App Store Prep

Schematic record — reconstructed retroactively from git history (no phase note
existed for this cluster). Commits `ab669c9..69f6eca`, June 10–22, on top of the
[[Projects/Doppio/Dev-Insights/themes-and-motion-polish|Themes & Motion Polish]]
pass (2026-06-04). This is the work that took the app from "well past scaffold"
to feature-complete and App-Store-submission-ready — but **the app has not been
submitted yet**; the manual distribution steps in `store/CHECKLIST.md` (publish
the website, capture screenshots, archive & upload, create the App Store Connect
record) are still outstanding.

## What shipped

- **Renamed HalfTime → beatmch → Doppio** (`ab669c9`, `dd0d2fb`, 2026-06-10) —
  bundle id, repo folder, and Xcode project all renamed; see the naming note at
  the top of [[Projects/Doppio/Doppio|the index]].
- **Theme set grown to 22** (`7e4b14f`, 2026-06-11) — from the 12 cross-hue
  themes documented in the 2026-06-04 dev-insight to **11 dark + 11 light**,
  every palette refined. (The vault index and the repo's own README both still
  said "12 themes" before this audit — corrected 2026-09-14.)
- **HALF/DOUBLE redesigned as a two-position switch** (`4065f8c`, `1cd728d`,
  `e64b1a4`) — both words now sit on screen at once (live side bold/accent-lit,
  idle side dim/scaled) instead of a single flipping label; centred by ink, not
  by slot.
- **App icon shipped** (`908a1cd`, `439631f`) — light/dark/tinted variants,
  first a red "pp" mark (2026-06-14), then replaced by the magenta "dd"
  doubled-letterform mark (2026-06-21). This is the concept from **Prompt 3 —
  Doubled letterform** in the logo-prompt idea note, which has now been deleted
  since the decision shipped.
- **Orbit & Ripple slowed to one gesture per bar** (`e240bdc`, 2026-06-21) —
  already documented in [[Projects/Doppio/Beat-Styles|Beat-Styles]].
- **Accessibility**: VoiceOver support for the tempo dial (`2f20eff`,
  2026-06-22) — the orb is an adjustable element (swipe = ±1 BPM, announces
  result + source), rotor actions switch beat style/theme, the mode row is a
  button, decorative elements are hidden from the accessibility tree.
- **App Store prep**: privacy manifest + export-compliance flag (`58703dc`),
  bundle id finalized to `app.doppio` (`c2903ef`), marketing/privacy/support
  website in `docs/` (`247e226`), full + short + Spanish listing copy in
  `store/` (`247e226`, `3afb15d`, `69f6eca`), and screenshot captions
  (`5dbe551`).

## Since this phase

Nothing further in git history as of this audit (2026-09-14) — `69f6eca`
(2026-06-22) is still the latest commit, working tree clean. The app is
feature-complete and submission-ready per `store/CHECKLIST.md`, but the actual
App Store submission (website publish, screenshots, archive/upload, App Store
Connect listing) hasn't happened yet.

## Related

- [[Projects/Doppio/Doppio|Doppio]] — project index
- [[Projects/Doppio/Dev-Insights/themes-and-motion-polish|Themes & Motion Polish]] — the phase this builds on
- [[Projects/Doppio/Beat-Styles|Beat-Styles]] — per-bar Orbit/Ripple detail
