---
title: Mosaic Background, Video Sorting & Gallery Polish
date: 2026-06-14
tags: [culla, phase, background, video, sorting, localization, sidebar, done]
status: shipped
---

# Mosaic Background, Video Sorting & Gallery Polish

Schematic record — reconstructed retroactively from git history during a vault audit (no phase note existed for this cluster). Commits `2d386ca..1041c6d`, 2026-06-11 → 2026-06-14, immediately before the [[Projects/Culla/Phases/phase-settings-polish-insights-storage|Settings Polish & Insights]] phase.

## What shipped

- **Video sorting** (`2d386ca`, `d059347`, `547d6ea`) — videos ride the same swipe stack as photos: single-flight prepare, reversible audio session, muted auto-play with a duration badge. Toggle via "Include videos" in Settings.
- **Mosaic background** (`ceb5547`, `f20cdec`, `2dcfb97`) — a second dynamic-background style (Album Artwork-style flip-tile grid) alongside the existing Stream wall; flips walk the whole selected gallery instead of a fixed 36-photo pool.
- **App-wide localization into 8 languages** (`0960c89`) via String Catalogs, plus an in-app language shortcut in Settings (`9fca1af`).
- **Sortable gallery pills** (`87ba9db`) — Custom / Name / Photo Count / Date Created / Recently Updated sort on both gallery sheets (`GallerySelectionSheet`, `GalleriesView`); the choice is shared, persisted, and flips direction on re-tap.
- **Accent-tinted sidebar mode** (`a507f73`) — new "Sidebar colour" setting (Per gallery / Accent) in Settings. Accent mode walks a single accent hue light→dark across the selected galleries (`accentSpectrum(...)` in `GallerySidebarView.swift`) and disables per-gallery colour customization everywhere it surfaced; Per-gallery mode is unchanged and stored `colorHex` is preserved either way. **Partially realizes** [[Projects/Culla/Ideas/gallery-color-themes|the gallery-color-themes idea]] — one alternative mode shipped, not the full multi-theme picker system the idea sketches.
- **Adjustable background blur** (`456e983`) — user-tunable carousel blur in Settings; duplicate-pair comparisons sharpen relative to it.
- `GalleryDetailView` header extracted into named subviews (`b5a5ec7`); README caught up to document sort pills + recent settings (`1041c6d`).

## Related

- [[Projects/Culla/Phases/phase-settings-polish-insights-storage|Settings Polish & Insights Reclaimed-Storage]] — the phase immediately after this one
- [[Projects/Culla/Phases/phase-app-store-readiness-and-privacy-hardening|App Store Readiness & Privacy Hardening]] — later phase; its README update documents this cluster's features
- [[Projects/Culla/Ideas/gallery-color-themes|gallery-color-themes]] — the idea partially realized by the accent-tinted sidebar mode
- [[Projects/Culla/Culla|Culla]] — project index
