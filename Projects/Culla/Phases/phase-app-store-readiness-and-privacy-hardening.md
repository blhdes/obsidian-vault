---
title: App Store Readiness & Privacy Hardening
date: 2026-06-25
tags: [culla, phase, app-store, privacy, revenuecat, done]
status: shipped
---

# App Store Readiness & Privacy Hardening

Schematic record — reconstructed retroactively from git history (no phase note existed for this cluster). Commits `765e28f..d79dfee`, June 23–25, on top of the [[Projects/Culla/Phases/phase-settings-polish-insights-storage|Settings Polish & Insights]] phase. Culla was already live on the Store (builds 1–2, shipped as a paid app); this cluster prepared and shipped version 3.0.0 (build 4) as a free update with the paywall dormant.

## What shipped

- **Privacy manifest** (`765e28f`) — `culla/PrivacyInfo.xcprivacy` declares the `NSPrivacyAccessedAPICategoryUserDefaults` (`CA92.1`) required-reason and `NSPrivacyTracking = false`, clearing the App Store Connect `ITMS-91053` warning.
- **RevenueCat disabled** (`e4dc35f`) — `SubscriptionManager.shared.configure()` commented out in `CullaApp.swift`. Since `isPro` is hard-coded `true` and the paywall is unreachable, RevenueCat's result was never read anyway — but leaving it configured would still phone home and create an anonymous user ID, contradicting the "nothing leaves your device" privacy policy. Restores zero network calls at launch → App Privacy = *Data Not Collected*.
- **App Store submission assets** (`c30e73e`) — `store/CHECKLIST.md`, `store/METADATA.md` (+ `-es.md`), `store/SCREENSHOTS.md`, mirroring the doppio store-docs pattern. Written for a free app: paywall dormant, IAPs not submitted.
- **README brought current** (`31ca420`) — documented video sorting, the Stream/Mosaic background styles, the storage-reclaimed insight, and the privacy posture.
- **Incidental polish**: Settings identity header condensed into a one-line `SettingsAppFooter` (`c6c9e37`); stream-background perf fix resolving each photo once per frame instead of per cell (`a8c2078`); thumbnail-load retry so fast-scrolled gallery cells don't get stuck gray on a transient cache miss (`d79dfee`).

## Since this phase

Further incremental builds shipped without individual phase notes — currently at **version 3.5.0, build 7** (as of 2026-09-14). Worth a proper phase note if/when the paywall is re-enabled or another substantial milestone lands.

## Related

- [[Projects/Culla/Phases/phase-settings-polish-insights-storage|Settings Polish & Insights Reclaimed-Storage]] — the phase this builds on
- [[Projects/Culla/Culla|Culla]] — project index
