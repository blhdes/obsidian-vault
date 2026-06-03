---
title: Freemium Gates — Free Tier Limits
date: 2026-04-26
tags: [culla, freemium, monetisation, phase]
---

# Freemium Gates — Free Tier Limits

Commit: `d3fb7c7` — *feat: add freemium gates for free tier limits*

Related: [[phase-paywall-redesign]]

## What we built

The paywall is dismissible, so free users get a limited but usable app rather than a hard block on launch.

### Free tier limits

| Feature | Free | Pro |
|---|---|---|
| Swipe actions | 20 / day (dismiss + sort) | Unlimited |
| Active sidebar galleries | 3 max | 10 max |
| Duplicate sweep | ❌ locked | ✅ |
| Insights screen | ❌ locked | ✅ |
| Custom accent colours | ❌ locked | ✅ |
| Carousel / dynamic background | ❌ locked | ✅ |

Skip, favorite, and share swipes **do not** count toward the daily limit — only dismiss (left) and sort-to-gallery (right).

### Live counter

Free users see a `"X / 20 today"` pill in the swipe screen so they always know how many actions they have left.

---

## Key design decisions

**Grandfathering** — users who already had >3 galleries selected keep them; they just can't add more until upgrading. Retroactive enforcement would feel hostile.

**Daily swipe reset** — tracked in `UserDefaults` as a date string (`yyyy-MM-dd`) + count. Resets automatically when the calendar day rolls over. `SubscriptionManager` is the single source of truth.

**Consistent paywall surface** — every gate shows `PaywallSheet` (the same component). No custom "locked" screens — one paywall, one place to update copy.

**`effectiveMode` pattern** — `PhotoCarouselBackground` computes `effectiveMode = isPro ? backgroundMode : "off"` at render time. This means:
- Carousel dies the moment a trial expires (no need to reset `UserDefaults`)
- Saved Pro setting survives — it revives automatically on resubscribe

---

## Files changed

- `Services/SubscriptionManager.swift` — added `dailySwipeLimit = 20`, `freeGalleryLimit = 3`, `hasReachedDailyLimit`, `recordSwipe()`, `refreshDailyCount()`
- `Views/SwipeView.swift` — limit checks before dismiss/sort, live counter, dynamic gallery max
- `Views/ContentView.swift` — dynamic gallery max passed to GalleriesView
- `Views/GallerySelectionSheet.swift` — tapping a 4th gallery triggers paywall (not silent disable)
- `Views/DatePickerView.swift` — duplicate `+` button replaced with lock/Pro icon
- `Views/SettingsView.swift` — accent + background changes intercepted and reverted for free users
- `Views/PhotoCarouselBackground.swift` — `effectiveMode` enforcement
- `Views/GalleriesView.swift` — insights header shows lock icon, triggers paywall
