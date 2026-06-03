---
title: Calendar View → Gallery Mode for Sorting
date: 2026-04-26
tags: [culla, idea, feature, calendar, sorting, gallery]
---

> [!success] Shipped 2026-06-03 — as `PhotoGridPickerView`
> The core of this idea was built: the calendar sheet has a photo-icon button that opens a
> scrollable photo grid (`culla/Views/PhotoGridPickerView.swift`, wired from
> `DatePickerView`). **Variation from the original sketch:** tapping a photo jumps the
> date wheel to that photo's date (rather than starting a sorting session from that exact
> photo). Close enough to call this done; the "start session from the tapped photo"
> nuance is the only unbuilt part, left as a possible refinement.

## Idea

In the calendar view, add the ability to switch into a full gallery view — similar to the picture-selection UI in the duplicate sweep feature.

**Flow:**
1. User opens the calendar view.
2. Taps a "gallery mode" toggle (or button).
3. The date-picker wheel disappears, replaced by a full gallery grid of photos.
4. User taps a photo — it becomes the **starting image** for a sorting session.
5. Sorting begins from that selected photo.

**Why it's interesting:**
- Gives users a visual, photo-first way to kick off sorting (vs. navigating by date).
- Reuses the familiar duplicate-sweep gallery pattern — less new UI to learn.
- The date-picker hiding keeps the screen clean and focused during sorting.

Related: [[Projects/Culla/Culla]]
