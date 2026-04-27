---
title: Wraparound C-Arc Gallery Layout for SwipeView
date: 2026-04-26
tags: [culla, idea, swipeview, gesture, ui-pattern]
---

# Wraparound C-Arc Gallery Layout for SwipeView

## The Idea

Instead of vertical panels on the right half of the screen, galleries wrap around the right edge in an inverted-C (almost semicircle) arc. The arc auto-adjusts its segment sizes based on how many galleries are selected.

**Left side stays reserved for dismiss** — same as today. Everything else is fair game.

This frees up the current up/down swipe directions (favourite ↑ / share ↓) and makes sorting feel more organic — more like throwing a card in a direction than sliding it into a slot.

## Key Design Goals

- Arc spans ~210° (top-right-bottom), leaving ~150° on the left for dismiss
- Segments are equally spaced across the arc — responsive to N galleries
- Larger "content zone" than dead space (vs. the current 50/50 split)
- Nearest arc segment highlights as the finger drags toward it
- Hit-testing via **drag angle**, not CGRect frame lookup

## How It Differs from Today

| | Current | Arc Layout |
|---|---|---|
| Gallery display | VStack of equal rectangles, right half | Curved arc, wraps top/right/bottom |
| Hit testing | `GalleryFramePreferenceKey` (CGRect) | Angle from drag vector |
| Swipe directions | Right → gallery, Up → fav, Down → share | All non-left directions → galleries |
| Feel | Structured, column-like | Radial, expressive |

## Code Sketches

### 1. Arc segment angle math

```swift
// 210° arc, open on the left (dismiss zone)
let arcStart: Angle = .degrees(105)   // top-left quadrant
let arcSpan = 210.0
let segmentAngle = arcSpan / Double(galleries.count)

func arcMidAngle(for index: Int) -> Angle {
    .degrees(arcStart.degrees + segmentAngle * (Double(index) + 0.5))
}
```

### 2. Hit-testing via drag angle (replaces `GalleryFramePreferenceKey`)

```swift
// Drop into updateHighlight() in SwipeView
func galleryIndex(for translation: CGSize) -> Int? {
    guard translation.width > 0 || abs(translation.height) > 30 else { return nil }
    // atan2 in standard math coords (right = 0°, CCW positive)
    let angle = atan2(-translation.height, translation.width) * 180 / .pi
    let normalized = ((angle - arcStart.degrees)
        .truncatingRemainder(dividingBy: 360) + 360)
        .truncatingRemainder(dividingBy: 360)
    guard normalized <= arcSpan else { return nil }
    return min(Int(normalized / segmentAngle), galleries.count - 1)
}
```

### 3. Arc label positioning (overlay on the card)

```swift
// Inside a GeometryReader wrapping the card
ForEach(Array(galleries.enumerated()), id: \.element.id) { i, gallery in
    let angle = arcMidAngle(for: i)
    let radius: CGFloat = geo.size.width * 0.44
    let x = cos(angle.radians) * radius
    let y = -sin(angle.radians) * radius
    GalleryArcLabel(gallery: gallery, isHighlighted: highlightedIndex == i)
        .offset(x: x, y: y)
        .opacity(dragProgress > 0 ? 1 : 0)
}
.frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .trailing)
```

## Files to Touch

- `culla/Views/GallerySidebarView.swift` — replace `GallerySidebarItem` VStack with arc overlay
- `culla/Views/SwipeView.swift` — replace CGRect hit-test (`galleryFrames`) with angle-based lookup; update `updateHighlight()` and `handleSwipeEnd()`

## Open Questions

- Do favourite/share gestures move somewhere else, or get reassigned to arc slots?
- Arc radius: fixed or proportional to screen width?
- Animate arc in on first drag, or always visible at low opacity?

Related: [[Projects/Culla/Culla]]
