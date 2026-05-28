---
title: iOS 26 Liquid Glass fails to composite over animated MeshGradient
date: 2026-05-28
tags: [culla-music, ios-26, liquid-glass, swiftui, rendering-bug]
---

## Context

`ManagePlaylistsSheet.swift` — the Playlists sheet has two segments (Sidebar / Filter). Each segment shows its rows inside a glass slab that sits on top of `LivingMeshBackground` (a `TimelineView`-driven `MeshGradient` updating at 30 fps). On iOS 26 only.

## Symptoms

- The Filter slab rendered **transparent at rest** — you could see straight through to the mesh.
- Brief flashes of the row UI appeared only **while scrolling**, then snapped back to transparent.
- Sidebar was much less affected (taller slabs hit it harder, and Filter has more rows).
- **Invisible to screenshots and ReplayKit** — every capture showed the bug fixed, which made it impossible to share evidence and sent debugging in the wrong direction for an hour.

## Root cause

iOS 26 Liquid Glass (`.glassEffect` / `.glassSurface`) is rendered by the **present-time compositor**. When the layer underneath is animating at 30 fps (the mesh) and the glass area is large, the compositor can fail to produce a glass sample for a frame and just draws the layer below straight through. The bigger the glass surface, the more area there is to fail on per frame — which is why Filter (more rows = taller slab) was hit worse than Sidebar.

Screenshots and ReplayKit capture from an **earlier render pass**, before the compositor stage that does Liquid Glass. In that pass the glass is drawn correctly via the standard SwiftUI material path, so the bug never appears in any recording.

## Fix

1. Replaced `.glassSurface(in: RoundedRectangle(...))` with `.background(.thinMaterial, in: RoundedRectangle(...))` on both slabs and the empty state — same material `glassSurface` falls back to on iOS < 26. Reliable, no compositor dependency.
2. Removed `.transition(.opacity)` from the segment swap. When the glass failure compounded with an opacity transition starting from 0, the Filter subtree could land stranded at the faded-out end and never recover.

## Takeaways

- If a SwiftUI bug **vanishes** in screenshots and screen recordings, suspect the iOS 26 compositor layer (Liquid Glass, hover/press highlights, focus rings). Don't waste time asking for a screenshot — you won't get one.
- Liquid Glass over an animating background is a known-fragile combination. Use `.thinMaterial` (or another standard SwiftUI material) when the surface is large or sits over a high-frequency `TimelineView`.
- The same principle would apply to other places in the app that layer `.glassSurface` over `LivingMeshBackground` — worth checking if more screens show the same symptom later.

Related: [[Projects/Culla-Music/Culla-Music|Culla-Music]]
