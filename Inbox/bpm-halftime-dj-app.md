---
title: BPM Half/Double DJ App
date: 2026-06-01
tags: [idea, dj, swift, swiftui, ios, app]
---

# BPM Half/Double DJ App

A minimalist iOS app (Swift/SwiftUI) for DJs that does quick BPM math live.

## Core idea
- You enter an **original BPM** on screen.
- The app automatically calculates and displays **half** of it.
- **Swipe up/down** to change the original BPM — the half-time output updates instantly.

## The toggle
- A **single quick tap** flips the mode: the origin BPM becomes the **1/2 value**, so the app now calculates and displays the **double** instead.
- Intended for "drop touch" — switching between half-time and double-time on the fly during a mix.

## Why it's useful
Fast halftime/double-time reference without doing the math in your head mid-set.

## Open questions (decide later)
- Should it accept fractional BPMs, or round to whole numbers?
- Persist last BPM between launches?
- Haptic feedback on the tap-toggle?
- Show both half *and* double at once instead of toggling?

---
Related: DJ work in [[Areas/Mixing-DJing/]] · existing iOS project [[Projects/Culla/Culla|Culla]]
