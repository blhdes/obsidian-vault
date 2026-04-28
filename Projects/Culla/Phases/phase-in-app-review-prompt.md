---
title: In-App Review Prompt
date: 2026-04-28
tags: [culla, phase, review, app-store, ux]
---

## What was built

A two-phase in-app review prompt system using Apple's `SKStoreReviewController`. Prompts the user to rate the app on the App Store at two natural "success moments" during their first weeks of use.

---

## Trigger Conditions

| Phase | Condition |
|---|---|
| **First prompt** | ≥ 30 photos sorted AND ≥ 3 days since first launch |
| **Second prompt** | ≥ 10 days since first launch (start of second week) |

Each phase fires at most once, gated by a `UserDefaults` flag. Apple independently enforces a hard cap of 3 prompts per 365 days — there is no way to guarantee the dialog appears.

---

## Files Created / Changed

| File | Change |
|---|---|
| `Services/ReviewManager.swift` | New singleton service |
| `Views/DatePickerView.swift` | Added `.onAppear` trigger |

---

## How It Works

**`ReviewManager`** is a singleton initialized at app launch. It records `reviewFirstLaunchDate` in `UserDefaults` on first init. `checkAndRequestReview(sortedCount:)` evaluates both phases in sequence and calls `SKStoreReviewController.requestReview(in:)` when conditions are met.

```swift
// Trigger: DatePickerView re-appears every time user returns from SwipeView
.onAppear {
    ReviewManager.shared.checkAndRequestReview(sortedCount: sortedPhotos.count)
}
```

`sortedPhotos.count` comes from the existing `@Query(filter: #Predicate<SortedPhoto> { !$0.isImported })` in `DatePickerView` — counts only photos the user actually sorted (not imported ones).

---

## Key Decisions

- **`DatePickerView.onAppear` as the trigger point** — this view is conditionally shown/hidden relative to `SwipeView` in `ContentView`. It re-appears (and `.onAppear` re-fires) every time the user returns from a sorting session, which is the natural "success moment."
- **30 photos, not 100** — lower bar catches engaged early users who haven't built up a massive session history yet.
- **Second prompt at day 10, not day 14** — "second week" starts on day 8; day 10 gives a few days of buffer to actually be in-app rather than right at the week boundary.
- **No second-prompt photo threshold** — by day 10, any returning user is already satisfied enough; the time gate alone is sufficient.

Related: [[Projects/Culla/Culla]]
