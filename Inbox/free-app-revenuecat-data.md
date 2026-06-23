---
title: Going free — do we lose RevenueCat usage data?
date: 2026-06-22
tags: [culla, revenuecat, analytics, inbox]
---

# Going free — do we lose RevenueCat data?

**Context:** Made Culla totally free (removed paywalls / RevenueCat link) to reduce
download friction and get more real usage. Plan to maybe return to freemium later.
Worry: do we lose the RevenueCat data (active users/day) we like for tracking real usage?

## Short answer: No, you're not losing anything.

We only **hid the freemium logic** — the RevenueCat SDK is still fully alive.

In `culla/Services/SubscriptionManager.swift`:

```swift
var isPro: Bool { true }   // everyone treated as Pro now
```

The paywall gates are stubbed to the "unlocked" path, but the SDK still runs:

- `CullaApp.swift:26` still calls `configure()` on every launch
- `SubscriptionManager.swift:66` still runs `Purchases.configure(...)`
- `SubscriptionManager.swift:70` still listens to `customerInfoStream`

That last bit is the key: every app open pings RevenueCat's servers, and that ping is
exactly what RevenueCat counts as an **Active User**. So the "active users/day" chart
keeps filling in — paywall or not.

## The two worries, answered

- **Past data** — never at risk. RevenueCat doesn't delete history when the app changes.
  Even if we *had* ripped out the SDK, old dashboard numbers would still be there.
- **Future data** — still flowing, because the SDK still phones home on launch. New free
  users show up as new customers. Revenue charts flatten to $0 (no purchases), but the
  **usage** charts (Active Users, New Customers) keep working.
- **Cost** — not a concern. RevenueCat free tier covers up to ~$2.5k/month tracked
  revenue; we're now at $0.

## Honest caveat

RevenueCat tells you *how many* people opened the app, not *what they did* (screens,
photos sorted, retention). It was built to track money, not behavior. For a real usage
picture later, two easy options:

- **App Store Connect → Analytics** — free, already collecting (active devices, sessions,
  retention), zero code.
- **TelemetryDeck** or **Aptabase** — privacy-first, indie-friendly, a few lines to add
  when we want deeper engagement data.

## Recommendation

Do nothing right now. Keeping the SDK configured means usage data stays continuous **and**
re-enabling freemium later is trivial (old logic is sitting in the commented-out lines,
ready to swap back). **Don't delete `Purchases.configure()`** thinking it's dead weight —
that single line is what keeps active-user tracking alive.
