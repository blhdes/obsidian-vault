---
title: Menu press chrome crops the SortChip's capsule glass
date: 2026-05-30
status: resolved
tags: [culla-music, ios-26, liquid-glass, swiftui, menu, ux-bug]
---

> [!success] Resolved 2026-05-30
> The `.buttonStyle(.plain)` fix below was **not enough** — the grey square was iOS's menu *lift platter*, which `.plain` can't suppress. See **Resolution** at the bottom for what actually worked.

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

With the system platter + shadow gone, the only background left is the flat capsule glass that was always there. The chevron is affordance enough; the trade-off is the chip no longer has a built-in press "bounce." Shared control, so it fixes every SortChip at once. ~~Build verified; awaiting on-device confirmation.~~ **On device, the grey square was still there — `.plain` does not suppress the lift platter. Superseded by the Resolution below.**

## Resolution (what actually worked)

`.buttonStyle(.plain)` only restyles the label's *button*; it never touches the menu's **lift platter** (the rounded-rect + shadow iOS morphs into the open menu). The clean fix is to stop bringing our own glass and let the system own it, so it morphs the *button's* shape instead of drawing a separate platter:

```swift
Menu { … } label: {
    Image(systemName: "arrow.up.arrow.down")   // icon only
}
.menuStyle(.button)
.buttonStyle(.glass)          // iOS 26 — the button *is* the glass
.buttonBorderShape(.circle)   // morph target is the circle, nothing to crop
.controlSize(.small)
.tint(.secondary)             // neutral press, no accent bloom
```

Two changes landed together:
1. **System-owned glass** (`.glass` + `.circle`) — the morph reshapes the circle the user is pressing, so there's no rectangular platter peeking out. No `.contentShape`, no shadow patching.
2. **Icon-only** — dropped the inline label + chevron. The labels are different lengths, so changing sort resized the capsule and that width change flickered. A fixed-size icon can't resize. Current selection survives via `accessibilityValue` + the menu's own checkmark.

Pre-iOS-26 falls back to a `.thinMaterial` circle with `.buttonStyle(.plain)` (those OSes don't draw the iOS 26 lift). **Confirmed good on device.**

## Takeaways

- A custom `Menu` label gets the system's rounded-rect highlight + shadowed lift **on top of** your styling. If your label is a non-rectangular shape (capsule, pill), that chrome will crop against it on touch.
- `.buttonStyle(.plain)` does **not** suppress the lift platter — it only restyles the label's button. Neither does `.contentShape(.contextMenuPreview, …)` (that reshapes the platter but leaves its shadow). Both fight the platter from outside and lose.
- What works: don't supply your own glass — give the button a **native** glass shape (`.buttonStyle(.glass)` + `.buttonBorderShape(.circle/.capsule)` on iOS 26). The menu then morphs *that* shape, so there's no separate platter to crop. Let the system own the surface instead of layering yours under its chrome.
- Orthogonal but worth pairing: an icon-only menu label has a fixed width, so changing the selection can't resize it — kills the resize flicker a variable-length label causes.

Related: [[culla-music]] · [[Liquid Glass Transparent Over Animated Mesh 2026-05-28]]
