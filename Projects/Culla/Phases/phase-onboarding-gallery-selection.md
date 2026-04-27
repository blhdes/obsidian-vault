---
title: Onboarding Walkthrough & Gallery Selection
date: 2026-04-27
tags: [culla, phase, onboarding, galleries, freemium]
---

## What was built

Two related features planned and partially implemented this session.

---

### Gallery Selection in GalleriesView ✅ Shipped

Users can now activate/deactivate galleries for their swipe session directly from `GalleriesView`, without going into SwipeView first.

**How it works:**
- The color dot on each gallery row is now an interactive 24pt selection toggle
- **Not selected:** colored ring outline
- **Selected:** filled neon circle with white checkmark + soft glow shadow
- Smooth 0.18s animation between states
- A status line sits between the stats header and the list:
  - Orange → `"Tap a circle to activate galleries for swiping"` (nothing active)
  - Gray → `"2 of 10 active for swiping"` (X selected out of Y total galleries)
  - Gray → `"3 active · Upgrade to select more"` (free cap hit)
- In **edit mode**, the plain decorative 10pt dot returns — no interference with rename/reorder

**Freemium cap:**
- Free users: max 3 selected (`freeGalleryLimit = 3`) — paywall fires on 4th attempt
- Pro users: max 10, silently ignored if somehow exceeded

**Key pattern used:** `Button` inside `NavigationLink` with `.buttonStyle(.plain)` — circle tap intercepts before navigation fires, row tap still goes to `GalleryDetailView`.

**Only file changed:** `culla/Views/GalleriesView.swift`

---

### App Walkthrough + Tooltips 📋 Planned (not yet implemented)

**Files to create:**
- `Helpers/OnboardingManager.swift` — `@AppStorage` flags for walkthrough + tooltip state
- `Views/Onboarding/WalkthroughView.swift` — 8-step full-screen overlay
- `Views/Tooltips/TooltipBubble.swift` — reusable hint bubble (auto-dismisses in 4s)

**Files to edit:**
- `Views/DatePickerView.swift` — trigger walkthrough on first launch, show calendar tooltip
- `Views/SwipeView.swift` — show zoom tooltip

**Walkthrough steps:**

| # | Type | Title | Gated by |
|---|---|---|---|
| 1 | Info | Welcome to Culla | — |
| 2 | Info | Pick a Date | — |
| 3 | Info | What Are Galleries? | — |
| 4 | **Action** | Create or Import a Gallery | `galleries.count > 0` |
| 5 | **Skippable** | Change a Gallery Color | optional |
| 6 | **Action** | Select Your Galleries | `sidebarGalleryIDs.count > 0` |
| 7 | Info | You're Ready! | — (CTA: Get Started) |

Step 6 now opens `GalleriesView` — the gallery selection feature above makes this work without a separate sheet.

**Two contextual tooltips:**
- `DatePickerView` → *"Tap the wheel to open a full calendar"* (shown once, `@AppStorage` flag)
- `SwipeView` → *"Pinch to zoom in or out"* (shown once, `@AppStorage` flag)

---

## Key decisions

- No "Manage" mode — selection always visible inline
- `activeGalleryCount` filters against `galleries` array to gracefully handle deleted gallery IDs
- `GallerySelectionSheet` in SwipeView stays as a quick-access shortcut during active sessions
- Color change flow unchanged — tap gallery row → `GalleryDetailView` → tap color circle at top

Related: [[Projects/Culla/Culla]]
