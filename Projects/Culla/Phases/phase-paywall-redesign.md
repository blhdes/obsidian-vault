---
title: "Phase: Custom Paywall & Pre-Release Polish"
date: 2026-04-25
tags: [culla, paywall, revenuecat, phase, pre-release, app-store]
status: in-progress
---

# Phase: Custom Paywall & Pre-Release Polish

Pre-release phase focused on replacing the RevenueCatUI dependency with a fully custom paywall, wiring up trial logic, and polishing the UI to match Culla's visual identity before App Store submission.

## What shipped

### 1. RevenueCatUI removed — custom paywall built from scratch
**Commit:** `b190515`

Dropped the `RevenueCatUI` package entirely from `project.pbxproj`. Replaced `PaywallView` + `CustomerCenterView` with:
- A hand-rolled `PaywallSheet.swift` that loads `Offerings.current` via `Purchases.shared`, renders all active packages, and handles purchase / restore / loading / error states manually.
- `SettingsView.swift` now uses SwiftUI's native `.manageSubscriptionsSheet(isPresented:)` in place of `CustomerCenterView`.
- All RC identifiers, entitlement IDs (`Culla Pro`), and API keys untouched.

### 2. Trial eligibility + disclosure
- Calls `Purchases.shared.checkTrialOrIntroDiscountEligibility(productIdentifiers:)` after loading offerings — hides trial copy only when the user is **definitively ineligible**, shows it optimistically for `.unknown`.
- Trial-eligible package cards show a "7-day free trial" subtitle; CTA reads "Start 7-day free trial".
- A disclosure pill (outlined `RoundedRectangle(12)` + shield icon + accent stroke) appears below the CTA for trial-eligible users: *"Free for 7 days, then [price] [period]. Cancel anytime in Settings before the trial ends."*

### 3. Trial expiry notification
**New file:** `culla/Services/TrialReminderService.swift`

- `TrialReminderService.scheduleReminder(for:)` — requests notification permission and schedules a local `UNNotificationRequest` 24h before `expirationDate`.
- `SubscriptionManager.reconcileTrialReminder(info:)` — called on every `customerInfoStream` update; schedules when `periodType == .trial`, cancels when the entitlement leaves trial state. Guards against re-prompting with `scheduledReminderFor` check.
- Notification fires even when the app is closed (system-owned, not app-owned).
- Sandbox note: 7-day trial compresses to ~3 min; if already inside 24h window, fires in 5s instead for testability.

### 4. Paywall aesthetic redesign
**Commit:** pending push

Full visual overhaul of `PaywallSheet.swift` to match the app's design DNA. All changes are in-file (no new files, no new dependencies):

| Element | Before | After |
|---|---|---|
| Background | `Color(.systemBackground)` | Radial accent wash (`accent.opacity(0.18→0.06→.clear)`, blurred 40pt) |
| Hero icon | Plain `LaunchIcon` | Breathing accent glow behind icon (`easeInOut 2.4s repeatForever`) |
| Hero title tracking | 1.5 | 2 (matches splash exactly) |
| CullaEyes | Not present | Appears below hero icon when `showCullaEyes` setting is on |
| Feature icons | SF Symbol in accent | SF Symbol inside `accent.opacity(0.15)` rounded square chip |
| Package card (unselected) | `.ultraThinMaterial` + accent stroke | Unchanged |
| Package card (selected) | Accent stroke only | Full accent fill + white text + 1.02 scale + neon shadow glow (`radius 14, y 4`) |
| Package selection animation | `.easeInOut(0.15)` | `.spring(response: 0.32, dampingFraction: 0.82)` |
| Package selection haptic | None | `Haptics.swipeRight()` on change only |
| CTA button | Flat accent fill | Gradient fill + neon shadow + press-scale spring + `Haptics.startCullaing()` |
| CTA text color | Always white | Luminance-checked: flips to black on bright neons (`#FFE600`, `#CCFF00`, `#39FF14`) |
| Trial disclosure | Plain caption | Outlined pill (`RoundedRectangle(12)`) with `shield.lefthalf.filled` icon |
| Footer Restore | Secondary color | Accent-tinted |
| Entry animation | Instant | Staggered fade-up (5 sections × 0.06s delay, `spring(0.45, 0.85)`) |

Design references used from existing app code:
- `Color.adaptiveNeon` + `@Environment(\.appAccent)` — `GallerySidebarView.swift`
- `Haptics.swipeRight()` / `Haptics.startCullaing()` — `Haptics.swift`
- `CullaEyes()` with `.tint(accent)` — `CullaEyes.swift`
- Spring `(response: 0.32, dampingFraction: 0.82)` — canonical snap from `GallerySidebarView`

## Open / pending before App Store submission

- [ ] **ASC intro offer propagation** — monthly & yearly 7-day free trials are configured in App Store Connect ("Lista para enviar") but `StoreProduct.introductoryDiscount` is still returning `nil` in sandbox. Waiting on Apple's CDN. Once it propagates, trial text and the disclosure pill will appear automatically — no code change needed. See `Inbox/culla-trial-offer-not-propagating.md`.
- [ ] **Full sandbox end-to-end test** — complete a purchase with the fresh sandbox tester, verify entitlement activates, paywall dismisses, Settings shows "Manage subscription".
- [ ] **Trial expiry test** — let the ~3-min sandbox trial expire, verify `trialExpired → forced paywall` gate in `SplashGate` triggers correctly.
- [ ] **Bright accent visual check** — set `accentMode = "custom"`, pick `#FFE600` swatch, confirm CTA and selected card text flips to black.
- [ ] **App Store submission** — screenshots, metadata, review notes.

## Key decisions made this phase

- **No RevenueCatUI** — replaced to reduce binary size, eliminate the RC-managed paywall design, and keep full control over the subscription UX.
- **No push notifications** — trial reminders are local only; Apple already emails a receipt for every charge.
- **No "welcome to paid" notification** — duplicates Apple's receipt; in-app celebration (first-launch welcome) deferred to a future release. See `Ideas/paid-conversion-welcome.md`.
- **No PhotoCarouselBackground on paywall** — requires photo permission which may not be granted at first launch.
- **StoreKit config file skipped for now** — sandbox tester used instead; `.storekit` setup deferred. See `Resources/Swift/storekit-config-testing.md`.

## Related notes

- [[../Ideas/paid-conversion-welcome|Idea: In-app welcome after first paid conversion]]
- [[../../Inbox/culla-trial-offer-not-propagating|Open: Trial offer not propagating in sandbox]]
- [[../../../Resources/Swift/storekit-config-testing|Ref: StoreKit config file testing]]
