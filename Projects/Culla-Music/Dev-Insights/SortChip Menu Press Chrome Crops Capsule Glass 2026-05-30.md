---
title: Menu press chrome crops the SortChip's capsule glass
date: 2026-05-30
tags: [culla-music, ios-26, liquid-glass, swiftui, menu, ux-bug]
---

## Context

`SortChip.swift` — the shared sort control (a glass capsule that opens a flat sort menu). Used by the Playlists sheet (Sidebar + Filter tabs) and Home's "Sort From" picker. The capsule background is `.glassSurface(in: Capsule())`.

## Symptoms

- On **touch**, a background appeared *behind* the capsule that looked "cropped" / half-cut and badly integrated — its corners stuck out past the rounded capsule ends.
- At rest the chip looked fine; the problem only showed during the press.

## Root cause

A plain `Menu` draws its **own** press chrome on top of whatever label you give it:
- a rounded-**rectangle** gray highlight, and
- a lifted "preview" platter with a **drop shadow**.

Both have square-ish corners. Layered under a `Capsule()` glass, they peek out at the rounded ends → the cropped, mismatched look. The old code tried to patch this with `interactive: true` glass + `.contentShape(.contextMenuPreview, Capsule())` to reshape the lift silhouette, but that only reshaped the platter — it didn't remove the shadow, and the two chrome layers still fought the capsule.

## Fix

Route the menu through a plain button style so iOS skips its press chrome entirely:

```swift
Menu { … } label: {
    label.glassSurface(in: Capsule())   // flat, no interactive:, no contentShape
}
.menuStyle(.button)
.buttonStyle(.plain)
```

With the system platter + shadow gone, the only background left is the flat capsule glass that was always there. The chevron is affordance enough; the trade-off is the chip no longer has a built-in press "bounce." Shared control, so it fixes every SortChip at once. **Build verified; awaiting on-device confirmation.**

## Takeaways

- A custom `Menu` label gets the system's rounded-rect highlight + shadowed lift **on top of** your styling. If your label is a non-rectangular shape (capsule, pill), that chrome will crop against it on touch.
- `.menuStyle(.button)` + `.buttonStyle(.plain)` is the clean way to suppress that chrome — prefer it over reshaping the lift with `.contentShape(.contextMenuPreview, …)`, which leaves the shadow behind.
- General pattern: when custom chrome and system chrome both draw, removing the system layer beats trying to make it match. Simpler and no shadow.

Related: [[culla-music]] · [[Liquid Glass Transparent Over Animated Mesh 2026-05-28]]
