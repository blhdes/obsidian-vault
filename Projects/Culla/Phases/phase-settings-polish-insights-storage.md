---
title: Settings Polish & Insights Reclaimed-Storage
date: 2026-06-14
tags: [culla, phase, design-system, settings, insights, storage, localization, swiftui, done]
status: shipped
---

# Settings Polish & Insights Reclaimed-Storage

A polish-and-feature sprint on top of the [[phase-living-glass-design-system|Living-Glass design system]]. Merged to `main`, commits `93d021d..56d8db3` (over base `1041c6d`). Two threads: refining the Settings screen, and turning Insights into a focused full-screen destination with a real "storage reclaimed" stat.

## 1. Settings polish (`93d021d`)

Refinement *within* the calm tier — no new loudness, no mesh.

- **Identity header at the top** (`SettingsAppHeader.swift`, new). App icon + "Culla" wordmark + version line. Replaces the old `versionFooter` that was stranded alone at the bottom, so the screen opens with a face (iOS per-app-settings convention). App icon is read at runtime: try `CFBundleIcons → CFBundlePrimaryIcon → CFBundleIconFiles.last`, then fall back to `UIImage(named: "AppIcon")` (asset-catalog icons aren't always in `CFBundleIconFiles`), then degrade to wordmark-only.
  > **Superseded 2026-06-24** (`c6c9e37`): the header ate too much space at the top of the sheet, so it was moved back to the bottom and condensed into a one-line footer — `SettingsAppHeader` renamed to `SettingsAppFooter`, the 3-line stack collapsed to "Culla · Version x (n) · © year" beside a small icon. See [[Projects/Culla/Phases/phase-app-store-readiness-and-privacy-hardening|App Store Readiness & Privacy Hardening]].
- **Blur slider got a numeric readout.** It gave zero feedback before — now shows the value (0–20) beside the label with `.contentTransition(.numericText())`.
- **Extracted `AccentPalettePicker.swift`** (new). The 12-swatch custom-accent grid + `ColorPicker` moved out of `SettingsView`. It's self-contained — owns its `customAccentHex`/`customPaletteHexes` `@AppStorage` and its own selected index, initialising in `onAppear`. Because it only renders while in "Custom" mode, its `onAppear` *is* the "entered custom mode" initialiser, so `SettingsView`'s `onChange(of: accentMode)` shrank to just the Pro-paywall guard. Net: `SettingsView` dropped from 358 → 287 lines.

## 2. Insights: reclaimed-storage feature (`26873bf`)

A real "Storage" card showing how much space photo deletions have freed.

- **Single measurement chokepoint.** All five delete paths (swipe, gallery-delete, duplicate sweep, dismissed-photos select/all) funnel through `PhotoLibraryService.deletePhotos(identifiers:)`. So bytes are measured *there*, once, before deletion (the assets are gone afterwards), and accumulated into a `totalReclaimedBytes` (Double) UserDefaults key. Every screen's delete is covered for free — no plumbing through call sites.
- **No public PHAsset file-size API.** Size is summed across `PHAssetResource.assetResources(for:)` reading the `fileSize` resource value via KVC; falls back to 0 when unavailable so the total degrades gracefully.
- **Photo count mirrors the Deleted row, by construction.** The card's "Freed by deleting N photos" reads `totalDeletedPhotos` *directly* (the same value as the Details "Deleted" row) rather than a parallel counter — so the two can never desync. The byte total is tracked independently and can lag (e.g. 0 for photos deleted before this feature shipped) while the count stays correct. Card shows when `totalDeletedPhotos > 0`; bytes formatted with `ByteCountFormatter`.

## 3. Insights goes full-screen (`26873bf`)

- Presentation changed from `.sheet` → `.fullScreenCover` (in `GalleriesView`). A large sheet recedes its parent into a card that peeks behind the top edge; full-screen reads as a focused destination with nothing behind it. User-preferred from a UX standpoint.
- **Gotcha:** a `fullScreenCover` presents in its *own* presentation context, so the root view's `.statusBarHidden(!statusBarVisible)` (set in `CullaApp`) doesn't reach it. Fix: re-apply `.statusBarHidden(!statusBarVisible)` *inside* `InsightsView` (reading the same `@AppStorage` key) so it honours the "Show status bar" toggle. Same caveat would apply to any other root-level modifier you expect a cover/sheet to inherit.

## 4. Localization (`56d8db3`)

- Three new strings — `Storage`, `reclaimed`, `Freed by deleting %lld photos` — translated into all 7 non-English languages (es, de, fr, it, ja, pt-BR, zh-Hans).
- **Merged via a python script that preserves the catalog's compact `json.dump` format** instead of running `xcodebuild -exportLocalizations`. An Xcode catalog sync rewrites the whole `.xcstrings` with spaced-colon formatting (`"key" :`), producing a ~12,000-line all-noise diff. The script appends only the new keys → a clean 138-line, zero-deletion diff. (A plain `xcodebuild build` can *also* trigger this reformat — watch for it.)

## Reusable takeaways

- Full-screen covers / sheets are separate presentation contexts — re-apply root modifiers (status bar, etc.) inside them.
- For a metric that must equal another displayed value, read that value directly; don't maintain a parallel counter that can drift.
- Incremental `.xcstrings` edits: merge with a script in the existing format, never let an Xcode sync reformat the whole catalog.

## Related

- [[Projects/Culla/Phases/phase-living-glass-design-system|Living-Glass design system]] — the foundation this builds on
- [[Projects/Culla/Culla|Culla]] — project index
