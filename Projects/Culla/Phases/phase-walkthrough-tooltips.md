---
title: In-App Spotlight Tour & Swipe Hints
date: 2026-04-27
tags: [culla, phase, onboarding, tour, tooltips]
---

## What was built

A full first-launch onboarding system for new users. Went through two design iterations in this session:

1. **v1 (discarded):** Full-screen card overlay hiding the app — felt like a separate screen, not native.
2. **v2 (shipped):** In-app spotlight tour overlaid on the real app, plus two sequential swipe-screen hints.

---

## Tour System Overview

The app stays fully visible throughout. Two overlay layers sit on top:

- **Dim canvas** (`allowsHitTesting(false)`) — 58% black with a glowing spotlight cutout over the relevant UI element. Uses `Canvas` + `.drawingGroup()` + `.destinationOut` blend mode to punch the hole.
- **Bubble layer** — A floating card with an arrow tip, icon, title, body text, and a gated Next button. Only the bubble captures touches; everything else passes through to the real app.

Because the dim layer passes touches, the user can tap real UI elements (e.g. the Galleries toolbar icon) through the tour at any point.

---

## Files Created

| File | Purpose |
|---|---|
| `Helpers/OnboardingManager.swift` | `OnboardingKey` enum — 4 static UserDefaults key strings |
| `Helpers/TourEnvironment.swift` | `\.activeTourStep` environment key — injects current step into GalleriesView / GalleryDetailView |
| `Views/TourStep.swift` | `TourStep` enum — step content, spotlight rects, bubble positions, arrow edges |
| `Views/TourContainer.swift` | Main overlay: Canvas dim + pulsing glow ring + `TourBubble` |
| `Views/TourBubble.swift` | Floating card with directional arrow, gate badge, Next/Skip/Let's Go buttons |
| `Views/TourSheetBanner.swift` | `TourSheetBanner` (in GalleriesView) + `TourColorHint` (in GalleryDetailView) |
| `Views/TooltipBubble.swift` | Reusable single-line hint: springs in, auto-dismisses after 4s, tap to dismiss. Uses `.ultraThinMaterial`. |
| `Views/SwipeDirectionsHint.swift` | Cross-layout card showing all 4 swipe directions with colored icon bubbles |

---

## Tour Steps (7)

| # | Spotlight | Type | Gate |
|---|---|---|---|
| 1 | None | Info — Welcome | — |
| 2 | Date wheel (center of screen) | Info — Pick a Date | — |
| 3 | Galleries toolbar icon (top-right) | Info — Your Galleries | — |
| 4 | Galleries toolbar icon | **Gated** — Set Up a Gallery | `galleries.count > 0` |
| 5 | Galleries toolbar icon | **Skippable** — Make It Yours (color) | optional |
| 6 | Galleries toolbar icon | **Gated** — Activate for Swiping | `sidebarGalleryIDs.count > 0` |
| 7 | Start button (bottom) | Info — You're All Set | CTA: "Let's Go!" |

For steps 4–6, the user taps the real Galleries icon through the overlay (dim has `allowsHitTesting(false)`). `GalleriesView` opens as a sheet on top of the tour. When they return, `@Query` reactivity detects the change and unlocks the Next button.

---

## In-Sheet Guidance

Tour guidance follows the user into the sheets where the actual actions happen:

**`GalleriesView`** — `TourSheetBanner` appears at the top of the list for steps 4 (create/import) and 6 (activate). Shows what to tap, updates to "Done! Close to continue." when the condition is met.

**`GalleryDetailView`** — `TourColorHint` appears below the color circle button for step 5. Small banner with an upward arrow: "Tap the circle above to pick a neon color. Close to skip."

Both read `@Environment(\.activeTourStep)` injected by `SplashGate`. Set to `nil` when the tour is inactive — invisible during normal use.

---

## Swipe Screen Hints (SwipeView)

Two hints shown sequentially on the first swipe session, both using `.ultraThinMaterial`:

1. **Zoom tooltip** (`TooltipBubble`) — appears 2s after first photo batch loads, centered on the card. Text: *"Pinch to zoom in or out on any photo."*
2. **Swipe directions hint** (`SwipeDirectionsHint`) — appears 400ms after the zoom tooltip dismisses. Cross layout showing all 4 directions with soft colored icon bubbles (heart yellow ↑, trash red ←, stack accent →, share blue ↓).

**Shared dismissal** — Both hints clear via `dismissHints()` when:
- `actionHistory.count` goes from 0 → 1 (first swipe of any kind)
- Tap-to-dismiss on either hint
- Auto-dismiss timer (4s zoom / 5s swipe directions)

Calendar tooltip was **removed** — tour step 2 already explains the wheel tap, so it was redundant.

---

## Trigger Architecture (SplashGate)

All launch-gate logic lives in `SplashGate` (the window root). The trigger that fixed the "no tour showing" bug:

```swift
// Fires for EVERY paywall dismiss path: X button, swipe, purchase, restore
.onChange(of: showPaywall) { _, isShowing in
    guard !isShowing else { return }
    hasSeenPaywall = true
    scheduleWalkthroughIfNeeded()
}
```

Previously used `onChange(of: hasSeenPaywall)` in `ContentView` — cross-view `@AppStorage` reactivity was silently dropped. Moving everything to `SplashGate` (the root view controller) fixed it. `fullScreenCover` was also moved here for the same reason — child view controllers can't reliably present modals immediately after a parent sheet dismisses.

`sidebarGalleryIDs` was also lifted to `SplashGate` and flows down to `ContentView` + `TourContainer` as bindings.

---

## Other Changes in This Session

**`GalleriesView` delete dialog** — Replaced the custom `DeleteGalleryDialog` full-screen overlay with SwiftUI's native `.confirmationDialog`. Matches the iOS Messages delete pattern: rises from the bottom, pill-shaped buttons, automatic Cancel. 88 lines → 24 lines.

**`OnboardingKey`** now has 4 keys:
```swift
enum OnboardingKey {
    static let walkthroughComplete = "hasCompletedWalkthrough"
    static let calendarTooltipSeen = "hasSeenCalendarTooltip" // legacy
    static let zoomTooltipSeen     = "hasSeenZoomTooltip"
    static let swipeHintSeen       = "hasSeenSwipeHint"
}
```

---

## Key Decisions

- **No arrow on Welcome step** — no spotlight, no arrow needed; bubble is centered.
- **Spotlight positions are approximate** — computed from `GeometryProxy` screen size percentages, not pixel-perfect anchors. Good enough across all iPhone sizes.
- **`drawingGroup()` required** — Canvas blend mode `.destinationOut` only works correctly when the view is composited off-screen first.
- **`GallerySelectionSheet` kept** — still accessible from SwipeView's Manage button as a quick-access shortcut during active sessions.

Related: [[Projects/Culla/Phases/phase-onboarding-gallery-selection]]
See also: [[Projects/Culla/Culla]]
