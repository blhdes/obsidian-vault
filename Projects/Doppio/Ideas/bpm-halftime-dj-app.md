---
title: BPM Half/Double DJ App
date: 2026-06-01
tags: [halftime, idea, dj, swift, swiftui, ios]
---

# BPM Half/Double DJ App

The founding idea for [[Projects/Doppio/Doppio|HalfTime]]. A minimalist iOS app
(Swift/SwiftUI) for DJs that does quick BPM math live.

## Core idea
- You enter an **original BPM** on screen.
- The app automatically calculates and displays **half** of it.
- **Swipe up/down** to change the original BPM — the half-time output updates instantly.

## The toggle
- A **single quick tap** flips the mode: the origin BPM becomes the **1/2 value**, so
  the app now calculates and displays the **double** instead.
- Intended for "drop touch" — switching between half-time and double-time on the fly.

## Why it's useful
Fast halftime/double-time reference without doing the math in your head mid-set.

## Decisions (2026-06-01)
- ✅ **Fractional BPM** — stored as `Double`, snapped to 0.1 steps for a clean display.
- ✅ **Persist last BPM + mode** between launches (UserDefaults).
- ✅ **Haptics on** — detent tick per whole BPM while swiping, firmer thud on the flip.
- Kept the **tap = toggle** model (not showing both numbers at once).

## Still open
- Show **half *and* double at the same time** instead of toggling? Less tapping in a
  dark booth — candidate for a future layout. (The motion itself already shows both
  rhythms at once — bold result + faint source — but the *number* still only shows one
  at a time via tap-to-flip. Genuinely undecided as of 2026-09-14.)

## Done since (checked 2026-09-14)
- ✅ Custom app icon — shipped 2026-06-21, a magenta "dd" doubled-letterform mark. See
  [[Projects/Doppio/Phases/phase-rename-theme-refresh-and-app-store-prep|the phase note]].
- ✅ Persist between launches, haptics, fractional BPM — all done (see Decisions above).

---
Built: scaffold at `/Users/agomezu/Claude/halftime-app/` — see [[Projects/Doppio/Doppio|Doppio]] index (renamed from HalfTime 2026-06-10).
