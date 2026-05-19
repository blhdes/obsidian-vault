---
title: QA — Home ↔ Swipe matched-geometry hero transition
date: 2026-05-19
tags: [culla-music, qa, testing, transitions, ui, swiftui]
---

# QA — Home ↔ Swipe hero morph checklist

Manual tests for the new matched-geometry transition between Home and Swipe.

**What changed:** The "Start Cullaing" button on Home and the album artwork
on the current `SongCardView` now share a `matchedGeometryEffect(id: "heroStart")`.
Tapping Start morphs the button up into the artwork's rounded rect; tapping
back morphs it back down. Home recedes (~0.92 scale + fade) behind Swipe via
a custom `AnyTransition.parallaxRecede`. Spring: `response 0.55, dampingFraction 0.85`.

**Files touched:**
- `Helpers/Transitions.swift` (new)
- `Views/RootView.swift`
- `Views/HomeView.swift`
- `Views/MusicSwipeView.swift`
- `Views/SongCardView.swift`

Reference: [[culla-music|Culla Music — Project Index]]

---

## Forward morph (Home → Swipe)

- [ ] Tap **Start Cullaing** with the swipe library already warm → the button **visibly stretches upward** and morphs into the album artwork's rounded rect (no cut, no fade-only).
- [ ] During the morph, **Home recedes** behind the incoming Swipe view — scale ~0.92 and dim/fade to invisible.
- [ ] The artwork settles at its final size and position **without a secondary jump** after the morph completes.
- [ ] The morph reads as **one continuous motion**, not two stacked animations.
- [ ] Repeat in **Library**, **Unsorted**, and **Dismissed** modes — same feel in all three.
- [ ] Repeat with a **source playlist selected** (Library + Sort From …) — same feel.

## Back morph (Swipe → Home)

- [ ] Tap the **back chevron** (top-left) → the artwork **shrinks back into the exact position** the Start Cullaing button occupies on Home (full width minus 24pt horizontal padding, near the bottom).
- [ ] Home **springs forward** from 0.92 → 1.0 + fades back in **during** the artwork's shrink, not after.
- [ ] No visible "ghost" of the artwork lingers in the centre of the screen once the morph completes.
- [ ] No flash of system background between the two screens.

## Spring tuning

- [ ] `response: 0.55` — does the morph feel **too fast** (jumpy) or **too slow** (sluggish)? Note your impression.
- [ ] `dampingFraction: 0.85` — any **visible bounce/overshoot** at the end of the morph? Should land cleanly without wobble.
- [ ] Compare forward vs back — do they feel **symmetric**? Forward should not feel snappier than back (or vice versa).

If tuning is needed, edit `RootView.swift` — both `startSession` and `endSession`
wrap their state change in `withAnimation(.spring(response: 0.55, dampingFraction: 0.85))`.

## Loading-window edge case

- [ ] **Cold-start tap test:** Kill the app, relaunch, tap Start Cullaing **immediately** (before the swipe library finishes loading).
  - Does the morph end at an **empty space** (no `SongCardView` rendered yet) before the card fades in?
  - If yes — is it **distracting** or just barely noticeable?
  - Acceptance: the morph element should not appear to "vanish" — even a brief empty target is OK if the card fades in within ~300 ms.
- [ ] Repeat with a slow network (Network Link Conditioner → 3G) — same observation.
- [ ] Tap Start in **Dismissed mode with zero dismissed songs** → `EmptyStateView` shows instead of a card; the morph element terminates at the EmptyStateView (no artwork target). Note whether this looks acceptable or jarring.

## Hero source uniqueness (regression — no warnings)

Two `matchedGeometryEffect` views with the same `id` and both `isSource: true`
in the same hierarchy will print a runtime warning and pick one arbitrarily.

- [ ] Watch the **Xcode console** during a forward + back round-trip — look for `matchedGeometryEffect` or `Multiple inserted views in matched geometry group` warnings. Should be **zero**.
- [ ] In Swipe, swipe a card off-screen so the **next card slides in** → no warning fires. (The next-card preload deliberately receives `heroNamespace: nil` and uses the `matchedHero` helper that no-ops without a namespace.)
- [ ] Trigger the `EmptyStateView` (e.g. dismiss every card in a mode) → exit back to Home → no warnings.

## Interaction with existing chrome / gestures

- [ ] During the forward morph, the **back chevron** does not flash briefly before the swipe content fades in (or if it does, it's not awkward).
- [ ] During the back morph, the **toast / undo banner** (if currently visible) fades out cleanly with the swipe view — no orphan banner left mid-screen.
- [ ] Mid-swipe (card partially dragged) → tap back chevron → morph still works; artwork morphs back from its **dragged offset**, or it snaps to center first (note which).
- [ ] Long-press on a Dismissed card to open the context menu, then dismiss the menu, then tap back → morph still clean.
- [ ] Open the **Manage Playlists** sheet from Swipe, dismiss it, then tap back → morph still clean (no leftover sheet dimming layer).

## Cross-device / mode checks

- [ ] **Light mode** and **dark mode** — both look correct (no color flash during the morph).
- [ ] **Dynamic accent** on vs. off (Settings) — the morph reads the same.
- [ ] **iPhone with home indicator** vs. **older iPhone with bezel** — back chevron position and morph target both look right.
- [ ] iPad (if supported) — same checks.

## Performance

- [ ] No visible **frame drops** during either morph (60fps minimum, ideally 120fps on ProMotion).
- [ ] Memory: round-trip Home ↔ Swipe ~10 times → no obvious memory growth in Xcode's Debug Navigator (the parallax transition adds one extra view briefly during transitions, but it should release).

---

## Notes / things observed

(Capture anything surprising or worth tuning here when you actually run it.)
