---
title: TestFlight Feedback — Empty Gallery & Limited Photo Access
date: 2026-04-29
tags: [culla, phase, testflight, onboarding, permissions, bug-fix]
---

## Context

First real TestFlight user feedback. User had granted **limited photo access** on iOS, skipped the tour, and started a session with no galleries created or selected.

## Issues addressed

### 1. Bug — sidebar auto-repopulation after explicit deselect-all
**Root cause:** `hasInitializedSidebar` was `@State` in `SwipeView`, which resets every time `SwipeView` is recreated (i.e. every time the user goes back to DatePickerView and starts a new session). So deselecting all galleries in Manage → back → start session → `@State` resets to `false` → `onAppear` sees empty IDs + non-empty galleries → silently re-populates.

**Fix:** Promoted to `@AppStorage("hasInitializedSidebar")`. One-time auto-fill, persists forever. Explicit user deselect-all is now respected.

### 2. UX — right-swipe into empty sidebar felt dead
**Fix:** Added early branch in `handleSwipeEnd` — if the user crosses the right swipe threshold with no galleries set up, snap back + toast *"Add a gallery first"* + auto-open the Manage sheet.

Also improved the sidebar empty-state: added icon, bolder text, and a *"Tap Manage ↘"* sub-hint. Higher opacity so it's actually readable during a drag.

### 3. GallerySelectionSheet appearing as a black void
**Root cause:** When `galleries` is empty the old `List` had no sections to render; combined with the dark background, it looked broken.

**Fix:** Branched the sheet body — when `galleries.isEmpty`, shows a proper `ContentUnavailableView` with prominent **Create New Gallery** and **Import from Phone** CTAs. The old list view is preserved for the non-empty case, extracted into its own `galleryList` computed view.

### 4. Limited photo access — no feedback, no recovery path
**Fix:** Added a soft banner to `DatePickerView` (via `.safeAreaInset(edge: .top)`) that appears whenever `photoService.authorizationStatus == .limited`. Two CTAs:
- **Select More** → presents `PHPhotoLibrary.shared().presentLimitedLibraryPicker(from:completionHandler:)`
- **Settings** → deep-links to app settings

Dismissible per session (`@State var limitedBannerDismissed`).

**Follow-up bug during testing:** After deselecting all in the picker, then re-selecting photos, `DatePickerView` was stuck on the "No Photos selected" empty state.

**Fix:** Extracted library-loading logic from `.task` into a reusable `loadLibrary()` function. The picker's completion handler now calls `loadLibrary()` on dismiss, so `noPhotosAvailable`, `earliestDate`, and `latestDate` are always in sync with the current selection.

> Gap remaining: if user changes selection via **Settings.app** instead of the in-app picker, the reload doesn't fire. Would need a `PHPhotoLibraryChangeObserver`. Low priority for now.

## Files changed

- `SwipeView.swift` — `@AppStorage` for `hasInitializedSidebar`, auto-open Manage on empty right-swipe
- `GallerySidebarView.swift` — richer empty-state UI
- `GallerySelectionSheet.swift` — `ContentUnavailableView` branch for no-galleries state
- `DatePickerView.swift` — limited access banner, `loadLibrary()` extraction, picker completion handler

## Commit

`1c1c3cf` — fix: address TestFlight feedback on empty gallery state and limited photo access

## Related

- [[Projects/Culla/Phases/phase-onboarding-gallery-selection|Phase: Onboarding Gallery Selection]]
- [[Projects/Culla/Culla|Culla]]
