---
title: Onboarding Walkthrough & Contextual Tooltips
date: 2026-04-27
tags: [culla, phase, onboarding, walkthrough, tooltips]
---

## What was built

Full first-launch onboarding walkthrough (7 steps) and two contextual tooltips.

---

### Files Created

**`Helpers/OnboardingManager.swift`**
Tiny enum `OnboardingKey` with three static `UserDefaults` key strings. Prevents typos and makes key renames a one-line change.

```swift
enum OnboardingKey {
    static let walkthroughComplete = "hasCompletedWalkthrough"
    static let calendarTooltipSeen = "hasSeenCalendarTooltip"
    static let zoomTooltipSeen     = "hasSeenZoomTooltip"
}
```

---

**`Views/TooltipBubble.swift`**
Reusable tooltip component. Springs in on appear, auto-dismisses after 4 seconds, dismisses on tap. Animates out first (0.2s), then fires `onDismiss()` after 250ms so the fade completes before state clears.

---

**`Views/WalkthroughView.swift`**
Full-screen dark overlay (black 0.8 opacity) with a centered card. Steps transition via `.id(currentStep)` + `.transition(.opacity.combined(with: .scale(scale: 0.97)))`. Progress dots animate between 8pt (active) and 5pt (inactive). "Continue" button is grey/disabled until the gate condition is met — lights up automatically via SwiftData `@Query` reactivity. Galleries sheet opens directly from inside the walkthrough (sheet on top of fullScreenCover) so `modelContext`, `SubscriptionManager`, and `appAccent` all inherit correctly.

### 7 Walkthrough Steps

| # | Step | Type | Gate |
|---|---|---|---|
| 1 | Welcome to Culla | Info | — |
| 2 | Pick a Date | Info | — |
| 3 | Your Galleries | Info | — |
| 4 | Set Up a Gallery | **Gated** | `galleries.count > 0` |
| 5 | Make It Yours (color) | **Skippable** | optional |
| 6 | Activate for Swiping | **Gated** | `sidebarGalleryIDs.count > 0` (filtered to existing galleries) |
| 7 | You're Ready! | Info | CTA: "Let's Go!" |

Steps 4, 5, 6 each show an **"Open Galleries →"** button that opens `GalleriesView` as a sheet from within the walkthrough.

---

### Files Edited

**`Views/ContentView.swift`**
- `@AppStorage(OnboardingKey.walkthroughComplete)` + `@AppStorage("hasSeenPaywall")`
- `.fullScreenCover(isPresented: $showWalkthrough)` with `.interactiveDismissDisabled(true)`
- Two triggers with async delays (500–600ms) to avoid conflicting with paywall sheet dismiss animation:
  - `onChange(of: isReady)` — covers app-update users (hasSeenPaywall already true, walkthrough not done)
  - `onChange(of: hasSeenPaywall)` — covers first-timers dismissing the paywall

**`Views/DatePickerView.swift`**
- Calendar tooltip fires only **after** walkthrough completes (step 2 already mentions the calendar tap, so no overlap)
- `.task(id: hasCompletedWalkthrough)` triggers after 1.5s delay
- `TooltipBubble` at `.bottom` of the wheel ZStack, offset 44pt down; hidden in Duplicates mode

**`Views/SwipeView.swift`**
- Zoom tooltip triggers 2s after first photo batch loads (inside existing `.task` block)
- `TooltipBubble` at `.top` of the card stack with horizontal padding

---

## Key decisions

- **Xcode auto-sync**: Project uses `PBXFileSystemSynchronizedRootGroup` (Xcode 15+) — new Swift files in the filesystem are included automatically, no `.xcodeproj` edits needed.
- `trialExpired` check prevents walkthrough from showing when the hard paywall is blocking the app.
- `GallerySelectionSheet` in SwipeView kept as a quick-access shortcut during active sessions — not removed.

Related: [[Projects/Culla/Phases/phase-onboarding-gallery-selection]]
See also: [[Projects/Culla/Culla]]
