---
title: Culla
date: 2026-04-24
tags: [project, ios, swift, culla]
---

# 🎨 Culla

Index note for the **Culla** iOS app. Source code lives at `/Users/agomezu/Claude/culla-app/`.

## Current state (2026-09-14)

- **Live on the App Store** (as a paid app initially, builds 1–2; now shipping free with the paywall dormant). Currently at **version 3.5.0, build 7**.
- **App Store readiness & privacy hardening** shipped since June — privacy manifest declaring the `UserDefaults` required-reason API, RevenueCat's `configure()` disabled so the app makes zero network calls while freemium is dormant (keeps App Privacy at *Data Not Collected*, matching the published policy), submission runbook + listing copy in `store/`, a thumbnail-load retry fix for fast-scrolled cells, and a stream-background perf pass (resolve each photo once per frame instead of per cell). No phase note existed for this cluster — see the new [[Projects/Culla/Phases/phase-app-store-readiness-and-privacy-hardening|phase note]].
- **Mosaic background, video sorting & gallery polish** shipped (2026-06-11 → 06-14, just before the Settings Polish phase) — a second dynamic-background style, video sorting in the swipe stack, sortable gallery pills, an accent-tinted sidebar mode, adjustable background blur, and app-wide localization into 8 languages. No phase note existed for this cluster either — see the new [[Projects/Culla/Phases/phase-mosaic-video-gallery-polish|phase note]].
- **Living-Glass design system** shipped — reusable glass surfaces in `Helpers/` (iOS 26 Liquid Glass with an iOS 18 `.thinMaterial` fallback), two tiers: *calm* (`SettingsCard`) for utility, *loud* (`GlassPanel`) for destination sheets. See [[Projects/Culla/Phases/phase-living-glass-design-system|the phase note]].
- **Settings polish + Insights reclaimed-storage** shipped — Settings identity header (since condensed into a one-line `SettingsAppFooter`), blur numeric readout, and an extracted `AccentPalettePicker`; Insights is a full-screen destination with a real "storage reclaimed" stat (its photo count mirrors the Deleted row by construction), localized into all 8 languages. See [[Projects/Culla/Phases/phase-settings-polish-insights-storage|the phase note]].
- **Two-signal sidebar highlight** shipped; the **arc sidebar layout was abandoned and its code deleted** ([[c-arc-gallery-layout|postmortem]], now archived).
- **Freemium / paywall + the CullaEyes mascot are still temporarily disabled** in the current build (`SubscriptionManager.isPro == true` for everyone; mascot call sites commented out; RevenueCat left unconfigured — see privacy hardening above). Code retained.
- **Accessibility and the paid-conversion welcome moment remain fully open ideas** (untouched in code); **gallery color themes is partially realized** by the accent-tinted sidebar mode above — the full multi-theme picker is still unbuilt. See [[Ideas]].
- Deployment floor: **iOS 18.0** (target-level — *not* the 26.2 project-level value, a recurring footgun).

## Sections

- **[[Ideas]]** — product ideas, feature sketches, UX experiments that haven't been decided on yet.
- **[[Dev-Insights]]** — lessons learned while coding: bugs fixed, patterns discovered, decisions and their reasoning.
- **[[Phases]]** — milestones, releases, roadmap notes. One note per phase/sprint.

## Quick links

- Repo: `/Users/agomezu/Claude/culla-app/`
- Docs: `/Users/agomezu/Claude/culla-app/docs/`

## How to use this space

When working on Culla, ask Claude things like:
- _"Save this as a dev-insight in Projects/Culla/Dev-Insights/ — [what I learned]"_
- _"New idea note in Projects/Culla/Ideas/ — [the idea]"_
- _"Start a Phase note for the App Store submission"_
