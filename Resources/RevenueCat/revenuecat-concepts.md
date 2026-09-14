---
title: RevenueCat — Core Concepts & App Setup
date: 2026-04-26
tags: [revenuecat, ios, subscriptions, iap]
---

# RevenueCat — Core Concepts & App Setup

## The Three Core Labels

Understanding these three things is the foundation of RevenueCat. They are separate but connected.

### Products
A **Product** is a direct mirror of what you created in App Store Connect. It's just a product ID (e.g. `agu.culla.lifetime`) registered inside RevenueCat so RC knows it exists.

> Think of it as: "this is a thing Apple sells for me."

### Offerings
An **Offering** is a *collection of packages* you present to the user — essentially, what your paywall shows. Each package inside an offering wraps one product.

You can have multiple offerings (e.g. an A/B test variant), but one must be marked as **Current** — that's the one your app loads by default.

> Think of it as: "this is the menu I show on my paywall."

### Entitlements
An **Entitlement** is an *access level* you grant when a purchase is made. It's the bridge between "user bought something" and "user has pro features unlocked."

In code, you check the entitlement by name (e.g. `"Culla Pro"`) — not the product ID. This means you can add new products later without changing your app code.

> Think of it as: "this is what the user is allowed to do after buying."

---

### How they connect

```
Product (agu.culla.lifetime)
    └── attached to → Entitlement ("Culla Pro")
    └── wrapped in  → Package (Lifetime) inside Offering (default)
```

When a user buys a package → RevenueCat activates the entitlement → your app checks `isPro`.

---

## Setting Up a New App in RevenueCat (Full Checklist)

These are the exact steps to configure a new iOS app from scratch, learned while fixing Culla Pro's test API key issue.

### 1. Create the App in RevenueCat
- In your RC project, go to **Apps → + New App → App Store**
- Set the **App name** and **Bundle ID** (must match Xcode exactly)

### 2. Upload the In-App Purchase Key (StoreKit 2)
- In App Store Connect → **Users and Access → Integrations → In-App Purchase**
- Generate a new key, download the `.p8` file (`SubscriptionKey_XXXX.p8`)
- Upload it to RevenueCat, fill in **Key ID** and **Issuer ID** from the same page
- This key has **no role selection** — it's a single-type key

### 3. Upload the App Store Connect API Key
- In App Store Connect → **Users and Access → Integrations → App Store Connect API**
- Generate a new key with role: **App Manager** (Finance alone is not enough)
- Download the `.p8` file (`AuthKey_XXXX.p8`)
- In RevenueCat → **Project Settings → App Store Connect API** → upload with Key ID + Issuer ID
- This is what lets RC validate that products exist in App Store Connect

### 4. Add Products
- In RC → **Products → + New**
- Add each product ID exactly as it appears in App Store Connect
- After adding the API key (Step 3), Store Status should turn green. "Could not check" means Step 3 is missing or wrong.

### 5. Create Entitlements
- In RC → **Entitlements → + New**
- Name must match the string in your app code exactly (e.g. `Culla Pro`)
- Attach all relevant products to this entitlement

### 6. Create an Offering
- In RC → **Offerings → + New Offering**, identifier: `default`, mark as **Current**
- Inside it, create one **Package** per product (Lifetime, Annual, Monthly, etc.)
- Attach each package to its corresponding product

### 7. Update the API Key in Code
- Replace the `test_XXXX` key in your app with the live `appl_XXXX` key
- The live key is found in RC → **Project Settings → API Keys**
- The `test_` prefix causes StoreKit 2 transactions to fail in production

---

## Notes
- The `appl_` (public) API key is safe to commit to source code — it's embedded in the app binary and can't grant dashboard access.
- Always use a real device to test purchases — the simulator doesn't support StoreKit properly.

Related: [[Projects/Culla/Culla]]
