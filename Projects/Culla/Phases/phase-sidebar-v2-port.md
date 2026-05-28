---
title: Sidebar v2 — port two-signal highlight from culla-music
date: 2026-05-28
tags: [culla, phase, sidebar, swiftui, deferred]
---

# Sidebar v2 — port two-signal highlight from culla-music

**Status:** Deferred. Audited 2026-05-28, ready to pick up later.
**Why deferred:** Other v-next chores in flight; user wants to revisit after current branch ships.

Origin: asked Claude to compare Culla's `GallerySidebarView` to culla-music's `PlaylistSidebarView` and propose what to port.

## TL;DR

Culla's sidebar already does **one thing better** than music's — it has `isLongPress` mode that runs a lighter veil so the photo stays readable. Keep that.

Culla is behind music in **three places**: weak highlight signal (fails for pale gallery colors), snapping text opacity ramp at the drag boundary, and no per-row visual identity beyond the color.

Plus there's dead `SidebarLayout` enum + `GalleryArcView` code carrying a "restore in vNext" TODO that bloats `SwipeView` + `SettingsView` with dead branches.

## What was audited

**Culla source files**
- `culla/Views/GallerySidebarView.swift` — current sidebar (panel layout)
- `culla/Views/SwipeView.swift` — host (lines 76–83, 213–230, 572 for sidebar wiring)
- `culla/Views/GalleryArcView.swift` — dead arc layout
- `culla/Models/SidebarLayout.swift` — enum gating the two layouts (only `.panels` is live)
- `culla/Views/SettingsView.swift` lines 14–15, 165–170 — commented-out arc picker

**culla-music reference**
- `CullaMusic/Views/PlaylistSidebarView.swift` — what we're porting from
- `CullaMusic/Views/MusicSwipeView.swift` — host call site
- `CullaMusic/Helpers/AccentEnvironment.swift` — has `appAccentSecondary` env value (Culla does not)

**Deployment floor:** iOS 18.0 (target-level in `culla.xcodeproj/project.pbxproj`, NOT the 26.2 project-level value — recurring footgun). No `#available` gating needed for anything in the plan.

## Critique — where Culla is behind

1. **Highlight is a single signal — fails for pale colors.** Culla floods the highlighted row with `neonColor.opacity(0.85)`. For yellow `#FFE600` or cyan `#00FFEE`, this barely reads against `.ultraThinMaterial`. Music solves it with a **two-signal pattern**: gradient fill + a 3pt solid leading bar. The leading bar is luminance-independent — works for any color.

2. **`textOpacity` snaps at the drag boundary.** Culla's text goes from `0.5 → 0.65` the millisecond `isDragging` flips true (small pop). Music interpolates with `dragProgress` for a continuous ramp:
   ```swift
   let p = Double(max(0, min(1, dragProgress)))
   let target: Double = isHighlighted ? 1.0 : 0.7
   return 0.5 + (target - 0.5) * p
   ```

3. **No per-row visual identity beyond the color.** Music carries `PlaylistCoverView` (44pt thumb). Culla rows are text-only. Galleries don't intrinsically have artwork — could use a count badge, latest-photo thumb, or stay text-only.

## Where Culla is ahead (don't regress)

- **`isLongPress` parameter** — modulates `materialOpacity` (lighter veil 0.35 during long-press so the photo stays visible) and `backgroundOpacity` (non-highlighted rows get 0.6 fill instead of fading away). Music has nothing like this. **Keep.**

## What's NOT worth porting

- **Music's `panelTint`** (faint accent-secondary wash across the whole panel) — works for music because there's *one* session-wide accent. Culla's panels are each their own color; an over-panel wash would have to pick one to win.
- **`appAccentSecondary` env value** — same reason. Galleries don't have a secondary color in the SwiftData model; adding one is a data-migration lift not worth this scope.

## Proposed direction — "Two-signal highlight + smoother ramps"

Targeted port. NOT a rewrite. The architecture (per-gallery `colorHex`, `isLongPress` mode, frame preference key, gesture wiring) stays exactly as-is.

### Layers

| Change | What it does | API |
|---|---|---|
| **Leading accent bar** | 3pt full-height `Rectangle().fill(gallery.color)` on the highlighted row, **in addition** to the existing full-row tint. Unambiguous edge cue even for pale neons. | Plain SwiftUI |
| **Continuous `textOpacity` ramp** | Replace step function with `0.5 + (target - 0.5) * dragProgress` — text fades in *with* the drag. | Plain math |
| **Highlight gradient** | Tighten the highlighted fill by stacking `gallery.color` over a 0.6-opacity `.leading→.trailing` gradient of `[gallery.color, gallery.color.opacity(0.7)]`. Subtle direction without needing a secondary palette field. | `LinearGradient` |
| **Drop dead arc code** | Delete `SidebarLayout.swift` + `GalleryArcView.swift`; inline `GallerySidebarView` in `SwipeView`; drop the `@AppStorage("gallerySidebarLayout")`, `sidebarLayout` computed prop, and the `switch` in the overlay. Removes ~6 dead branches across 3 files. | — |
| **Re-tune `materialOpacity`** | Currently `Double(dragProgress)` for swipe — at 100% pull the photo is fully obscured. Cap at `0.85 * dragProgress` so a sliver always bleeds through. | Tweak constant |

### File checklist

| File | Action |
|---|---|
| `culla/Views/GallerySidebarView.swift` | Modify — add leading bar, gradient fill, smooth `textOpacity` ramp, tuned material cap. ~30 lines changed in `GallerySidebarItem`. |
| `culla/Views/SwipeView.swift` | Modify — remove `@AppStorage("gallerySidebarLayout")`, `sidebarLayout` computed prop, `switch` in overlay. Direct `GallerySidebarView(...)` call. |
| `culla/Views/SettingsView.swift` | Modify — delete commented-out arc picker block (lines 14, 15, 165–170 at time of audit). |
| `culla/Models/SidebarLayout.swift` | **Delete.** |
| `culla/Views/GalleryArcView.swift` | **Delete.** |

No new files. No data-model changes. No new helpers. `isLongPress` parameter and behaviors stay intact.

## Open questions (decide before implementing)

1. **Delete the arc enum + `GalleryArcView`, or keep them dormant?** They carry a "restore in vNext" TODO, but if the arc shape has known SwiftUI clip-shape problems, it's speculative storage. Lean **delete** — easier to resurrect from git history than to debug stale dead branches. Related: see [[Projects/Culla/Ideas/c-arc-gallery-layout|c-arc-gallery-layout]] in Ideas.
2. **Per-row identity element** — count badge (cheap: `gallery.sortedPhotos.count`), latest-photo thumb (expensive: async Photos fetch), or skip both? Current proposal skips both.
3. **Reduce-motion** — the existing `.spring(response: 0.32...)` on `isHighlighted` is focal (responding to user input), not ambient → leave on per SKILL.md convention.

## Acceptance criteria

- Highlighted row reads as "you're here" for *every* neon in the palette, including `#FFE600`, `#00FFEE`, `#39FF14`.
- Text on rows fades in continuously with the drag — no snap at the threshold.
- `SidebarLayout`, `GalleryArcView`, and the `@AppStorage("gallerySidebarLayout")` are all gone (or, if kept, the picker in Settings is restored and the arc actually renders).
- `isLongPress` mode still keeps the photo readable behind a lighter veil.
- A sliver of the photo bleeds through even at 100% drag (no full blackout).
- `xcodebuild` green; no new warnings.

## Related

- [[Projects/Culla/Ideas/c-arc-gallery-layout|c-arc-gallery-layout]] — original arc idea
- culla-music repo at `/Users/agomezu/Claude/culla-music-app` — reference implementation
- `LEARNINGS.md` entries (2026-05-20) on Liquid Glass gating + (2026-05-27) on List re-skinning — relevant background
