---
title: Culla
date: 2026-04-24
tags: [project, ios, swift, culla]
---

# 🎨 Culla

Index note for the **Culla** iOS app. Source code lives at `/Users/agomezu/Claude/culla-app/`.

## Current state (2026-06-03)

- **Living-Glass design system** shipped — reusable glass surfaces in `Helpers/` (iOS 26 Liquid Glass with an iOS 18 `.thinMaterial` fallback), two tiers: *calm* (`SettingsCard`) for utility, *loud* (`GlassPanel`) for destination sheets. See [[Projects/Culla/Phases/phase-living-glass-design-system|the phase note]].
- **Two-signal sidebar highlight** shipped; the **arc sidebar layout was abandoned and its code deleted** ([[c-arc-gallery-layout|postmortem]], now archived).
- **Freemium / paywall + the CullaEyes mascot are temporarily disabled** in the current build (`SubscriptionManager.isPro == true` for everyone; mascot call sites commented out). Code retained.
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
