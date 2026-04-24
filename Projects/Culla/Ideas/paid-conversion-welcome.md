---
title: In-app welcome after first paid conversion
date: 2026-04-24
tags: [culla, paywall, retention, idea, revenuecat]
---

# In-app welcome after first paid conversion

## The idea

When a user transitions from free (or trial) to an active Culla Pro entitlement for the first time, show a **one-time in-app celebration** the next time they open the app — not a push/local notification.

Examples: subtle confetti, a toast, or a small welcome sheet like *"🎉 Welcome to Culla Pro — try the duplicate sweep →"* with a deep link to the feature.

## Why not a notification?

- Apple already sends an email receipt and a system notification ~24h before *every* charge (trial conversion + every renewal). A local notification from us would be pure duplication.
- Unlike the trial-ending reminder (which lets users cancel before the charge — actionable), a "you've been charged" alert has no action the user can take in-app.
- Notifications are best for things users need to know *outside* the app. Welcome moments are emotional, not informational — they belong where the user is already engaged.
- Recurring renewal alerts feel like spam and can trigger buyer's remorse.

## Why once-only, not every renewal?

A monthly or yearly "you're still subscribed!" reminder would be intrusive and redundant with Apple's receipt. The celebration only has emotional payoff the *first* time someone becomes Pro.

## Sketch implementation

```swift
@AppStorage("hasShownPaidWelcome") private var hasShownPaidWelcome = false

// In the root view, observe SubscriptionManager:
.onChange(of: subscriptions.isPro) { _, isPro in
    if isPro && !hasShownPaidWelcome {
        showWelcome = true
        hasShownPaidWelcome = true
    }
}
```

Works for trial-converted, direct subscription, and lifetime buyers — all three get the same one-shot welcome.

## When to revisit

Ship the trial-ending reminder first (already built). Only revisit this idea if analytics show **high churn in the first month post-conversion** — solve a measured problem, not a hypothetical one.

## Related

- [[Culla]] — project index
- [[../../../Resources/Swift/storekit-config-testing]] — useful for sandbox-testing the trial-to-paid transition when this eventually ships
