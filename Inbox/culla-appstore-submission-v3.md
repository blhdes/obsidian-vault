---
title: Culla App Store submission — next steps (v3.0.0 build 4)
date: 2026-06-24
tags: [culla, appstore, release, checklist]
---

Submission runbook for shipping the next Culla update to App Store Connect. This is an
**update** to the existing app record (bundle `agu.culla`, App Store ID `6761316914`) —
version **3.0.0**, build **4**. Source docs live in `culla-app/store/`.

> Paywall is **dormant** this release — everyone is unlocked, listing is written as a free
> app. RevenueCat `configure()` is disabled → no network calls → **Data Not Collected**.

## Next steps (all on my side)

1. **Confirm the website loads** — `culla.app` and `culla.app/#privacy` (privacy policy).
   Must stay accurate: nothing leaves the device, RevenueCat off.

2. **Screenshots** — need **two sets**: iPhone **6.9"** and iPad **13"** (Culla is universal,
   both required). Stage colorful galleries first, 5–6 shots each per `store/SCREENSHOTS.md`.
   Claude can resize raw shots to exact pixels.

3. **Archive & upload** (Xcode on Mac):
   - Confirm version `3.0.0`, build `4` (bump build if `4` was already uploaded — every
     upload needs a higher number).
   - Destination: **Any iOS Device (arm64)** → **Product → Archive** →
     **Organizer → Distribute App → App Store Connect → Upload**.

4. **Refresh the listing** (appstoreconnect.apple.com → existing Culla app):
   - New version **3.0.0**, paste English from `store/METADATA.md`, add **Spanish** from
     `store/METADATA-es.md`.
   - **App Privacy → No data collected** (label = "Data Not Collected", tracking = No).
   - Upload both screenshot sets, pick build `4` once processed (~15 min).
   - Category **Photo & Video**, age **4+**, price **Free**.

5. **Submit** — ⚠️ **do NOT attach the subscription/IAP products** — paywall is dormant so a
   reviewer can't trigger a purchase; attaching IAPs gets them rejected. Ship binary as Free,
   then **Add for Review → Submit**.

## Flags to handle before archiving

- Uncommitted changes to `project.pbxproj` and `Localizable.xcstrings` — verify version/build
  still `3.0.0 (4)`.
- **What's New** text in `METADATA.md` is written for the full 3.0 jump — trim lines that
  already shipped in the last public build before pasting.

## Quick reference

- Bundle ID `agu.culla` · Team `56BK7T2JG7` · Version/build `3.0.0 (4)`
- iPhone + iPad · Portrait · Min iOS 18.0
- Photo & Video · 4+ · Free (paywall dormant)
- Privacy: Data Not Collected · Tracking No · RevenueCat disabled
- Listing languages: English (U.S.) + Spanish
- App Store ID `6761316914`

## After approval

When monetizing again (later version): restore real `isPro` / `hasReachedDailyLimit` /
`subscriptionExpired` logic in `SubscriptionManager.swift` (bodies preserved in comments),
un-hide the Settings subscription card, point the paywall's "Privacy" link at the own policy,
re-enable RevenueCat, and only then submit the IAPs for review.

Related: [[Projects/Culla/Culla|Culla]]
