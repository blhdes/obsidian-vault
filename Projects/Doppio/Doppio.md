---
title: Doppio (formerly beatmch / HalfTime)
date: 2026-06-01
updated: 2026-09-14
tags: [project, ios, swift, dj, doppio, halftime, beatmch]
---

# ⏱️ Doppio

> Renamed from **HalfTime** → **beatmch** → **Doppio** (decided 2026-06-10, see
> [[beatmch-app-naming|the naming note]] — *doppio movimento* = "twice as
> fast"). Everything was renamed on 2026-06-10 — codebase (folder `Doppio/`,
> `Doppio.xcodeproj`, bundle id `app.doppio`), the local repo folder
> (`Claude/doppio/`), and the GitHub repo (`blhdes/doppio`) — and the vault folder
> followed on 2026-06-11 (`Projects/HalfTime/` → `Projects/Doppio/`, links updated).
> (The bundle id landed as `app.doppio`, not `agu.doppio` as first noted here —
> corrected 2026-09-14 after checking `project.yml`.)

Index note for the **Doppio** iOS app — a minimalist BPM half-time / double-time
tool for DJs, built as a *living metronome*, not a calculator. Source code lives at
`/Users/agomezu/Claude/doppio/`.

## What it does

- **Swipe up/down** anywhere to set your track's BPM (fractional, 0.1 steps, 20–300).
  A faint scale on the right edge shows where you are — and you can grab that bar to
  jump to an absolute BPM.
- **Hold a second finger** for fine mode: the swipe slows ~10× so you nudge a decimal.
- Big number shows **half** of the source BPM; a **single tap** flips to **double**
  (for the drop). The motion shows both rhythms at once — result (bold) + source (faint).
- **Two-finger tap** cycles the beat style: Orbit · Ripple · Sweep · Pulse · Bare.
- **22 themes** (11 dark, 11 light), each a cross-hue mesh-gradient journey; **shake**
  the phone for a random one (grown from the original 12 on 2026-06-11 — corrected here
  2026-09-14).
- Haptic detent per whole BPM (per 0.1 in fine mode), firmer thud on the flip.
- Remembers last BPM, mode, beat style, and theme between launches.
- Respects **Reduce Motion** (backgrounds freeze, rings hold still, dots blink on the beat).

## Sections

- **[[Beat-Styles]]** — the five orb modes, what each draws, and their pace.
- **[[Ideas]]** — product ideas, feature sketches, UX experiments not yet decided.
- **[[Dev-Insights]]** — lessons learned while coding.
- **[[Projects/Doppio/Phases/phase-rename-theme-refresh-and-app-store-prep|Phases]]** —
  milestones / releases.

## Quick links

- Repo: `/Users/agomezu/Claude/doppio/` · GitHub: `blhdes/doppio`
- Open it: `cd doppio && xcodegen generate && open Doppio.xcodeproj`
- Xcode 26+ · iOS 18+ (Liquid Glass on iOS 26, frosted-material fallback below) · portrait-only

## Current state (2026-09-14)

- **Feature-complete, not yet on the App Store.** 5 beat styles, 22 cross-hue themes,
  mesh-gradient backgrounds, shake-to-theme, fine mode, an honest half/double
  twin-rhythm display, and a centred HALF/DOUBLE two-position switch. SwiftUI +
  `@Observable` view model, UserDefaults persistence, primed haptics.
- **App icon shipped** — a magenta "dd" doubled-letterform mark (light/dark/tinted
  variants), the winning concept from the logo-prompt idea note (now folded into
  the phase note below; the idea note itself was deleted since the decision shipped).
- **VoiceOver support** added for the tempo dial (adjustable orb, rotor actions for
  beat style/theme, mode-row button).
- **App Store submission prep done** — privacy manifest, export-compliance flag,
  bundle id finalized as `app.doppio`, marketing/privacy/support site in `docs/`,
  and full/short/Spanish listing copy in `store/`. The manual distribution steps
  (publish the site, capture screenshots, archive & upload, create the App Store
  Connect record) are still outstanding — see `store/CHECKLIST.md` in the repo.
- This cluster of work (2026-06-10 → 2026-06-22) wasn't captured anywhere in the
  vault until this audit — see the new
  [[Projects/Doppio/Phases/phase-rename-theme-refresh-and-app-store-prep|phase note]].
- See [[Dev-Insights]] for the earlier (2026-06-04) polish pass.

Related: [[Projects/Culla/Culla|Culla]] · DJ work in [[Areas/Mixing-DJing/]]
