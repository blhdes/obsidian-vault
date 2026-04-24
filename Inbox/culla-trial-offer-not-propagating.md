---
title: Culla — 7-day trial offer not showing after 30+ min wait
date: 2026-04-24
tags: [culla, paywall, revenuecat, sandbox, debugging, open]
---

# Culla — 7-day trial offer not showing after 30+ min wait

## Current state

- Custom paywall is shipped (`b190515`), renders packages correctly: Monthly 1,99 US$ / Yearly 9,99 US$ / Lifetime 14,99 US$.
- CTA reads **"Continue"** for all three. Trial disclosure never appears.
- Fresh sandbox Apple ID created after wiping old lifetime purchase. Clean reinstall performed.
- ASC intro offers: both Monthly and Yearly were stuck on **"Missing Metadata"**, fixed to **"Lista para enviar"** (Ready to Submit).
- Waited 30+ minutes post-fix — still nothing.

## Next diagnostic step (resume here)

Add to `PaywallSheet.loadOfferings()` right after fetching offerings:

```swift
for package in offerings.current?.availablePackages ?? [] {
    let p = package.storeProduct
    print("— \(package.identifier) [\(p.productIdentifier)]")
    print("  intro:", p.introductoryDiscount as Any)
}
print("— eligibility:", eligibility)
```

**Branch on output:**
- `intro: nil` everywhere → Apple's sandbox hasn't pushed the offer yet. Keep waiting (can take hours) or try Step 3 below.
- `intro: Optional(...)` with data → app-side bug; inspect why `introductoryTrialDays(_:)` returns nil despite populated discount.

## Most likely ASC pitfalls to double-check

1. **Territories** — default is *US only*. Must be **All** (or include sandbox tester's country).
2. **Eligibility group** — *"For which customers"* must be **New Subscribers** or **All Customers**, not *Existing Subscribers*.
3. **Offer type** — must be **Free** (not "Pay as you go" with $0).
4. **Subscription group** — Monthly + Yearly should share the same subscription group.

## Simulator reset if still stuck

- Fully quit Simulator (Cmd+Q on the Simulator app).
- **Device → Erase All Content and Settings** or switch devices.
- Re-sign sandbox, reinstall, retry.

## Related

- [[../Projects/Culla/Culla|Culla project]]
- [[../Resources/Swift/storekit-config-testing]] — the `.storekit` config file would sidestep all of this propagation pain when we have time to set it up
