---
title: Living-Glass Design System & v-next-chores
date: 2026-06-03
tags: [culla, phase, design-system, liquid-glass, swiftui, sidebar, done]
status: shipped
---

# Living-Glass Design System & v-next-chores

The current design foundation for Culla, merged to `main` from the `v-next-chores` branch (range `52758b9..aba8ba8`). Unlike the other (one-off) phase notes, this one documents a **living system** the app is now built on — kept in `Phases/` as the current design record rather than archived.

## 1. Living-Glass design system

A reusable set of glass surfaces in `culla/Helpers/`, ported and adapted from the sibling app **Culla-Music**. Target floor is **iOS 18.0**, so everything has an iOS-18 `.thinMaterial` fallback under the iOS-26 Liquid Glass.

| File | What it is |
|---|---|
| `GlassSurface.swift` | `.glassSurface(in:tint:interactive:)` modifier + `GlassStack` — the core primitive (iOS 26 glass, iOS 18 `.thinMaterial` fallback) |
| `GlassPanel.swift` | "Loud" destination panel + `SettingsToggleRow` + `GlassChipPicker` |
| `SettingsCard.swift` | "Calm" card surface for Settings / utility screens |
| `GradientCapsuleButton.swift` | Gradient capsule CTA (has a `tint`/`role` param for red destructive actions) |
| `HeroIconTile.swift` | Glass hero icon tile |
| `AccentEnvironment.swift` | gained `Color.foregroundOnTintedGlass(in:)` — flips label text to white when a tinted-glass surface uses a dark light-mode neon |

**Two-tier convention:** *calm* (`SettingsCard` on flat `systemBackground`) for utility/Settings; *loud* (`GlassPanel` on flat `systemBackground`) for destination sheets (Galleries, Insights, Select Galleries, Duplicate Sweep states). Per-gallery `gallery.color` carries the "selected" state (tinted glass + colored halo) — Culla's own identity signal, used instead of a generic accent.

**Deliberately NOT redesigned** (don't "fix" these): the HomeScreen (`DatePickerView` + its Culla methods), `CalendarView`, the swipe **card** mechanics/gestures (`SwipeView`, `PhotoCardView` — only chrome was re-skinned), photo-dense grids (`AlbumImport`, `PhotoGridPicker` — photos read best on neutral backgrounds), and **Duplicate Sweep** (a prior redesign broke it and was reverted).

**No animated mesh background.** `LivingMeshBackground` was removed (2026-05-28) — it kept cropping under nav/safe-area inserts. All "loud" screens sit on flat `Color(.systemBackground)`. Don't reintroduce a mesh without an explicit ask.

## 2. Two-signal sidebar highlight (+ arc layout deleted)

Ported from culla-music's `PlaylistSidebarView`. Replaced the single weak highlight (`neonColor.opacity(0.85)`, which fails for pale neons) with a **two-signal** pattern: gradient fill **+** a 3pt solid leading bar (luminance-independent, works for any color). Plus a continuous `textOpacity` ramp tied to `dragProgress` (no snap at the drag boundary) and a material cap so a sliver of the photo always bleeds through.

The dead **arc layout** (`GalleryArcView`, `FanArcShape`, `SidebarLayout`) was **deleted** in the same effort — see [[c-arc-gallery-layout|the arc postmortem]] and [[phase-sidebar-v2-port]] (both archived).

## 3. Carousel refine (`/swift-refine`)

`PhotoCarouselBackground.swift` tightened (commit `aba8ba8`): cancel-aware load (fixes a wrong-album race on fast switching), caching released per batch, noise grain computed once, and `manager.images` hoisted in the `Canvas` draw closure. Details in [[calendar-and-carousel-performance-journey|the carousel performance journey (§11)]].

## 4. Features turned off (code retained)

- **Freemium model + paywall** — `SubscriptionManager.isPro` is hard-coded to `true`; everyone is treated as Pro, every gate is dormant. See [[phase-paywall-redesign]] and [[phase-freemium-gates]] (both archived).
- **CullaEyes mascot** — every call site is commented out; the Settings toggle is removed. `CullaEyes.swift` retained.

## Related

- [[Projects/Culla/Culla|Culla]] — project index
- Reference implementation: culla-music repo at `/Users/agomezu/Claude/culla-music-app`
