---
title: Culla — Trial not showing: root cause was Test Store API key
date: 2026-04-25
tags: [culla, paywall, revenuecat, sandbox, resolved]
---

# Culla — Trial not showing: root cause was Test Store API key

## What we found

After 10+ hours of waiting on ASC propagation and checking all the usual suspects (territories, eligibility group, offer type, subscription group), the actual cause was the RevenueCat API key in `SubscriptionManager.swift`.

**File:** `culla/Services/SubscriptionManager.swift:10`

```swift
private static let apiKey = "test_GjXIFqeHrLYHRHwcQHMhqeZgOPZ"
```

The `test_` prefix means it's a **Test Store key**, not a Sandbox/Production key. RevenueCat's Test Store completely bypasses StoreKit — purchases are simulated, intro offers never return `introductoryDiscount`, and ASC configuration is irrelevant while it's active.

## Why this matters

- All 10+ hours of ASC propagation waiting was moot — the app never contacted Apple.
- The "No packages could be found for offering 'default'" console warning was the same root cause.
- ASC fixes (territories = All, eligibility = New/All, offer type = Free) were correct — just aimed at the wrong problem.

## Fix

Swap in the **production API key** from RevenueCat dashboard:
> Project Settings → API Keys → Public App-Specific API keys (Apple)

It will start with `appl_` instead of `test_`. Once swapped, the trial shows up via StoreKit normally.

## Other console noise (not critical)

| Message | Verdict |
|---|---|
| `CoreData: error: Failed to stat .../default.store` (wall of text, ends with "Recovery attempt ... was successful!") | Harmless. First-launch CoreData directory walk on iOS 17+. |
| `Adding 'UIKitToolbar' as a subview of UIHostingController.view...` | Cosmetic SwiftUI/UIKit bridging warning. |
| `Error when syncing subscriber attributes` / `The subscriber was not found` | Consequence of Test Store confusion — disappears after key swap. |
| `com.apple.accounts Code=7` | Generic sandbox iCloud auth hiccup. Self-resolves. |

## Related

- [[culla-trial-offer-not-propagating]] — the original diagnostic note this resolved
- [[../Projects/Culla/Culla|Culla project]]
