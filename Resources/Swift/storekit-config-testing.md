---
title: StoreKit Configuration File — local purchase testing
date: 2026-04-24
tags: [swift, ios, storekit, testing, xcode, revenuecat]
---

# StoreKit Configuration File — local purchase testing

Mocks the App Store inside Xcode so you can test buy / restore / trial flows **without any Apple ID or real money**. Much faster than cycling sandbox testers.

Works standalone or in front of RevenueCat — RC's SDK will pick up local StoreKit products as if they came from App Store Connect, as long as the **Product IDs match** what's configured in the RC dashboard.

## Setup

1. In Xcode: **File → New → File → iOS → StoreKit Configuration File** → name it e.g. `Culla.storekit`.
2. Open the file, click **+** → **Add Auto-Renewable Subscription** (or consumable / non-consumable as needed).
3. Set the **Product ID** to exactly match what's configured in your RC dashboard / ASC (e.g. `culla_pro_monthly`, `culla_pro_yearly`, `culla_pro_lifetime`).
4. Configure price, duration, intro offers, free trials — all editable in the GUI.
5. Edit scheme: **Product → Scheme → Edit Scheme → Run → Options → StoreKit Configuration** → pick your `.storekit` file.
6. Run the app. Purchases now go through the local sandbox — instant and free.

## Managing transactions

Xcode → **Debug → StoreKit → Manage Transactions…** lets you:

- **Delete** individual transactions (instantly "unbuys" a non-consumable — the fix for a stuck lifetime purchase)
- **Refund** a transaction (tests `.revoke` flow)
- **Approve / decline** ask-to-buy prompts
- **Expire** subscriptions on demand (tests post-expiry UI, e.g. forced paywalls)
- **Fail** a renewal (tests billing-retry state)

Or right-click the `.storekit` file → **Delete All Transactions** for a full reset.

## Why this beats sandbox for UI iteration

| | StoreKit config | Sandbox Apple ID |
|---|---|---|
| Reset non-consumable | 1 click | Must create a new tester (non-consumables persist forever per tester) |
| Trial expiry | On-demand via "Expire" | Wait ~3 min (accelerated but real-time) |
| Needs internet | No | Yes |
| Needs Apple ID | No | Yes |
| Tests StoreKit → RC pipeline | No ⚠️ | Yes |

**Use sandbox** when you need to verify the real StoreKit → RC → app chain before shipping. **Use `.storekit`** for everything else.

## RevenueCat + `.storekit` gotcha

RC caches `CustomerInfo` locally under an anonymous app user ID. If you reset transactions in Xcode but RC still thinks the user is Pro:

- **Delete the app** from the simulator to wipe the cached RC user ID, OR
- In the RC dashboard, find the customer (app user ID is printed on launch when `Purchases.logLevel = .info`) and delete them.

## Related

- [[Swift]] — vault index
