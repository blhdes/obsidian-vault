---
title: "Phase 1 — Liquid Glass Redesign"
date: 2026-06-18
tags: [warket, swiftui, ios, design, phase]
---

# Phase 1 — Liquid Glass Redesign

First post-MVP **design phase**. The MVP build (milestones M0–M5, see [[Projects/warket-native/mvp-implementation-plan|MVP plan]]) got the app *working*; this phase made it *feel native and modern* — without touching any data/state logic.

> Status: **shipped & merged to `main`** (PR #11). Builds clean.

## What shipped

- **Living vault door (Unlock)** — centered Instrument Serif hero with a fade-in entrance, a frosted-glass phrase field, a glass "Generate" chip (sparkle bounce on tap), and a bold accent-gradient CTA. Replaced the old top-packed form on a flat black fill.
- **Animated "market pulse" background** — a calm teal `MeshGradient` that slowly drifts, the native echo of the web landing's `MarketPulse.tsx` canvas. (This **retires** the "Landing MarketPulse animation" item from the [[Projects/warket-native/deferred-backlog|deferred backlog]].)
- **Glass Lists & Assets** — rows float as inset glass cards over the mesh; glass grid card; shared glass tag pills. Native `List` behaviors (swipe, drag-reorder, EditButton) all preserved.

## Key decisions

- **Two new helpers** in `Theme/`: `GlassSurface` (centralizes iOS 26 Liquid Glass gating) and `MarketPulseBackground` (the mesh).
- **Deployment floor stays iOS 17.** iOS 18 (`MeshGradient`) and iOS 26 (Liquid Glass) features are gated behind `#available`, with material / static-gradient fallbacks. So older devices get a graceful, still-polished version.
- **Reduce Motion** freezes the mesh on a static frame.
- **Float glass via `.listRowBackground`, not row content** — keeps the system navigation chevron + swipe + reorder fully native.

## Open follow-ups

- On-device pass to fine-tune row inset / chevron alignment (couldn't verify pixels in `xcodebuild`).
- A light theme would need glass tints + mesh colors re-tuned for a bright background (still deferred — see backlog).

---
Project index: [[Projects/warket-native/warket-native|warket — Native Port]]
