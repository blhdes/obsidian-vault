---
title: First-launch onboarding flow
date: 2026-05-12
tags: [culla-music, idea, feature, onboarding, ux, shipped]
---

> **✅ Shipped — Phase 6 (2026-06-05 → 2026-06-10).** Landed as a lighter-weight design than the 3-screen walkthrough sketched below: a brand-forward first-launch screen + gated splash (`f45efec`, `4bf09d9`), then a **one-time, looping swipe-guide overlay** (`SwipeGuideOverlay` + `CoachTip`) that previews the real next cover and animates the drag hints (`868d2ec`, `641b503`, `436ed74`), plus a stronger one-time hero hint (`1f07d0b`). The mental model is taught *in place* on the deck rather than in a separate paged flow. See [[Projects/Culla-Music/Phases/phase-06-surfaces-onboarding-and-release|Phase 6]]. Original reasoning kept below.

# First-launch onboarding flow

After Apple Music auth, run a short 3-screen walkthrough explaining the core mental model. Skippable, persisted via a `hasOnboarded` flag in `@AppStorage`.

Mirrors photo Culla's `phase-onboarding-gallery-selection.md` pattern.

## Screens

1. **Three modes.** *"Sort your library, focus on unsorted songs, or revisit dismissals."* Visual: the three Home mode cards in miniature.
2. **Swipe.** *"Right to file. Left to dismiss. Tap to listen."* Visual: a ghost card with arrows. Mention undo lives at the bottom of every swipe screen.
3. **Membership chips.** *"Chips show where a song already lives. Avoid re-sorting."* Visual: a song card with two example chips.

After screen 3 → land on Home with `hasOnboarded = true`.

## Notes

- Skippable at any step (top-right *Skip*). Skip also sets `hasOnboarded`.
- Re-runnable from Settings (*"Show onboarding again"*) — useful for the user when they show the app to someone else.
- Up-swipe / Heart should get a fourth screen **only if** [[up-swipe-heart-loved]] ships first. Otherwise keep it to three.

## Open questions

- **When to fire.** After auth resolves on first launch — before Home appears.
- **Visual style.** Reuse Home's typography and card surfaces; don't introduce a separate onboarding design language.
- **Apple Music subscription nuance.** Should we surface "you'll get 30s previews without an AM subscription, full songs with one" on screen 2? Probably yes — sets expectations.

## Size / risk

Medium. Risk: none functional, just polish. Worth doing before a wider release / TestFlight push.
