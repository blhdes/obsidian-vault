---
title: Calendar & Carousel performance journey
date: 2026-04-24
tags: [culla, performance, cache, swift, uikit, phimagemanager, async, ios]
---

# Calendar & Carousel performance journey

Long session optimising the calendar thumbnail pipeline and the dynamic carousel background. Ended up rewriting the cache story from the ground up — this note captures the **why** behind each decision so the next time you see a similar problem you know where to look.

Source files: `culla/Views/CalendarView.swift`, `culla/Views/PhotoCarouselBackground.swift`, `culla/Services/PhotoLibraryService.swift`.

---

## 1. The four-layer cache hierarchy (the headline lesson)

Thumbnails in this app live in **four places at once**, and the order you check them in matters a lot:

```
┌──────────────────────────────────┐  ← fastest, in-RAM UIImage
│ 1. NSCache<NSString, UIImage>    │     (countLimit 500, ~50 MB)
└──────────────────────────────────┘
             │ miss
             ▼
┌──────────────────────────────────┐  ← ~ms reads, survives app restarts
│ 2. Disk cache (JPEG, 0.85)       │     ~/Library/Caches/CalendarThumbnails/
└──────────────────────────────────┘
             │ miss
             ▼
┌──────────────────────────────────┐  ← Photos framework buffer
│ 3. PHCachingImageManager         │     (prefetch hints for incoming requests)
└──────────────────────────────────┘
             │ miss
             ▼
┌──────────────────────────────────┐  ← slowest — actual iCloud/device fetch
│ 4. PHImageManager.requestImage   │
└──────────────────────────────────┘
```

Each layer is roughly an **order of magnitude slower** than the one above. `loadThumbnail(for:)` walks them in order and **promotes on hit**: if we find the image on disk, we immediately put it in NSCache so the next read is instant.

Key takeaway: a good cache system isn't "one cache" — it's a ladder where you check the cheap thing first and only fall through on genuine misses.

---

## 2. Warm load at app launch (the magic trick)

This is the single biggest perceived-performance win.

When the user opens the app:
1. `DatePickerView.task` runs `requestAuthorization()`
2. Once permission resolves, we fire **`Task.detached(priority: .background)`** that calls `warmCalendarCache(from:to:)`
3. That task walks the whole date range, pulls every mosaic thumbnail ID, and loads each one into NSCache + disk — **before the user has even tapped the calendar button**

```swift
Task.detached(priority: .background) {
    await service.warmCalendarCache(from: warmEarliest, to: warmLatest)
}
```

The trick: it's **not awaited**. The detached task runs in the background while the user is still picking a date, scrolling, or looking at the splash. By the time they tap "Open calendar", the cache is hot, and the grid renders instantly.

Rules of thumb:
- **`.background` priority** — don't compete with UI work
- **Detached** — survives the originating view's lifecycle
- **Fire and forget** — if it never finishes, worst case the user waits the first time they open the feature

---

## 3. Capped concurrency sliding window (don't flood the pool)

When `warmCalendarCache` was first written, it spawned **one task per thumbnail**. On a 3-year library that's potentially 4000+ tasks in flight, all hitting the disk and Photos APIs simultaneously. The thread pool chokes, memory spikes, the UI stutters.

Fix: a **sliding window** with `withTaskGroup`. Keep at most 50 in flight at a time. When we hit the cap, `await group.next()` waits for one to finish, then we queue the next:

```swift
await withTaskGroup(of: Void.self) { group in
    var inFlight = 0
    for id in allIDs {
        if inFlight >= 50 {
            await group.next()
            inFlight -= 1
        }
        group.addTask(priority: .background) { [self] in
            _ = await self.loadThumbnail(for: id)
        }
        inFlight += 1
    }
}
```

50 is enough to saturate the disk/Photos pipeline. More doesn't go faster — it just wastes context switches. This pattern is reusable anywhere you need **bounded parallelism**.

---

## 4. JPEG disk cache (with alpha stripping)

First version wrote PNG to disk. Each thumbnail ~150 KB. On a large library that's hundreds of MB of disk churn for the warm cache alone.

JPEG at quality 0.85 is **10× smaller** (~15 KB) and ~10× faster to encode. But switching naively produced a flood of console errors:

```
⭕️ ERROR: 'culla' is trying to save an opaque image (56x120)
   with 'AlphaLast'. This would double memory when decoding.
```

**The gotcha**: PHImageManager delivers photos with `AlphaLast` pixel format (RGBA) even for fully opaque JPEGs. When you call `jpegData(compressionQuality:)` on an RGBA `UIImage`, the encoder complains and silently does extra work.

Fix: redraw into an **opaque** `UIGraphicsImageRenderer` context to strip the alpha before encoding:

```swift
let format = UIGraphicsImageRendererFormat()
format.opaque = true
format.scale = 1
let opaque = UIGraphicsImageRenderer(size: decoded.size, format: format)
    .image { _ in decoded.draw(at: .zero) }
guard let data = opaque.jpegData(compressionQuality: 0.85) else { return }
```

Lesson worth remembering: **"opaque-looking" isn't the same as "has no alpha channel."** The pixel format metadata matters for encoders.

---

## 5. Cache invalidation on library mutations

Any session-level cache has a consistency problem: what if the source data changes? In this app, the calendar's `_calendarDataCache` holds photo counts per day. If the user deletes a photo, the counts are now wrong.

Solution: **invalidate on every mutation**. Every method in `PhotoLibraryService` that changes the Photos library calls `invalidateCalendarDataCache()` after success:

| Method | Invalidates cache | Evicts thumbnails |
|---|---|---|
| `toggleFavorite` | ✅ (favourites count) | — |
| `addPhoto` | ✅ (album count) | — |
| `removePhoto` | ✅ (album count) | — |
| `deletePhotos` | ✅ (all counts) | ✅ (asset is gone) |

Only `deletePhotos` also evicts individual thumbnails from NSCache + disk, because that's the only one where the asset ID becomes permanently invalid.

---

## 6. Fresh coordinator on every sheet open (the SwiftUI-UIKit trap)

The calendar uses a `UICollectionView` wrapped in a `UIViewRepresentable`. SwiftUI sometimes **keeps the representable alive between sheet presentations** (during dismiss animation), which means the `Coordinator` persists too — including its `hasScrolledToInitial = true` flag. Result: scroll-to-date works the first time, never again.

Fix: force a tear-down by nil'ing out the data on disappear:

```swift
.onDisappear { viewData = nil }
```

When the sheet opens again, `viewData == nil` shows `ProgressView`, the task reloads, and when the real view reappears SwiftUI calls `makeCoordinator()` again — fresh state every time.

Lesson: **`.onDisappear` is your last chance to reset state that the view's identity might outlive.**

---

## 7. Timing-safe reveal (the initial scroll trick)

Calling `UICollectionView.reloadData()` resets `contentOffset` to `(0, 0)`. If you then call `setContentOffset` asynchronously, the user sees **one frame at the top**, then a jump. On fast devices (cache hit path) this was very visible.

Solution — hide the view, scroll when ready, reveal:

```swift
collectionView?.alpha = 0            // invisible before render
collectionView?.reloadData()
scrollWhenReady(for: selectedDate)   // retries until bounds.height > 0

// inside scrollWhenReady, once laid out:
scrollToMonth(for: date, animated: false)
UIView.animate(withDuration: 0.25, delay: 0, options: .curveEaseOut) {
    cv.alpha = 1
}
```

The view is composited at the correct offset from the very first visible frame. The 0.25s fade-in makes the reveal feel deliberate.

---

## 8. Monochrome at the image layer, not the view layer (scope discipline)

First attempt: `.saturation(monochrome ? 0 : 1)` on the whole calendar view. Worked — but desaturated **everything**, including the blue selection circle and today-ring tint colours. Not what we wanted.

Right approach: apply the filter **only to the pixels we want affected**. Pass `monochrome: Bool` down to `MosaicView`, and when a thumbnail loads, convert it through a grayscale `CGContext`:

```swift
private func toGrayscale(_ image: UIImage) -> UIImage {
    guard let cgImage = image.cgImage else { return image }
    guard let ctx = CGContext(
        data: nil, width: cgImage.width, height: cgImage.height,
        bitsPerComponent: 8, bytesPerRow: 0,
        space: CGColorSpaceCreateDeviceGray(),
        bitmapInfo: CGImageAlphaInfo.none.rawValue
    ) else { return image }
    ctx.draw(cgImage, in: CGRect(x: 0, y: 0, width: cgImage.width, height: cgImage.height))
    guard let result = ctx.makeImage() else { return image }
    return UIImage(cgImage: result, scale: image.scale, orientation: image.imageOrientation)
}
```

The `DeviceGray` colour space collapses RGB → luminance automatically. No CIFilter, no CIContext, no GPU round-trip. Just a cheap blit through a different colour space.

Lesson: **match the scope of a filter to the scope of the pixels you actually want changed.**

---

## 9. Carousel-specific: screen-scale-aware thumbnail size

The `PhotoCarouselBackground` was requesting 150×150 thumbnails for 110pt slots. On a @3x screen, 110pt = 330px display — so the 150px image was being upscaled 2.2×. Fine at blur radius 7 (you can't see it), awful at blur radius 1 (duplicates mode).

Fix:

```swift
private static let thumbSize: CGSize = {
    let side = ceil(110 * UIScreen.main.scale)
    return CGSize(width: side, height: side)
}()
```

Now the requested size matches the actual pixel footprint. Photos delivers at native resolution, no upscaling. ~16 MB for 36 images vs ~3 MB before — a trivial price for sharp output.

Rule of thumb: **`thumbSize` should equal `displayPoints × screen scale`.** Anything less is visible blur; anything more is wasted memory.

---

## 10. Carousel-specific: `.task(id:)` as a reload trigger

The carousel needs to reload its pool when the user changes album or mode. SwiftUI's `.task(id:)` modifier does this for free:

```swift
.task(id: "\(backgroundMode)-\(albumIdentifier ?? "")") {
    await manager.load(...)
}
```

Whenever the composite id string changes, SwiftUI **cancels the old task and fires a new one**. No manual observer plumbing, no Combine subjects, no `onChange` dance.

One gotcha discovered later: if the id doesn't encode everything the task depends on, the task never re-runs. The "carousel not loading on fresh install" bug came from this — permission state wasn't in the id, so even after auth was granted the task never re-fired. Fix there was to default `backgroundMode` to `"off"` so new users don't hit the race at all.

---

## 11. Carousel: `.task(id:)` cancellation doesn't reach a continuation-based load (2026-06-03)

Section #10 says `.task(id:)` "cancels the old task and fires a new one." True — but that's only half the story, and the other half was a real bug.

`PhotoBackgroundManager.load()` fetches up to 36 thumbnails in a loop: `for asset { await fetch(asset) }`, where `fetch` wraps Photos' callback `requestImage` in `withCheckedContinuation`. **A bare continuation does not honor cancellation** — it keeps awaiting until its callback fires. So on a fast album switch:

- The superseded load kept fetching all remaining images for an album the user had already left (pure waste).
- Worse, the old and new `load()` interleave on the same `@MainActor` object, and **both assign `self.images` at the end**. Last writer wins — which could be the *old* album. Fast switching could leave the wrong album's photos on screen.

The fix (`/swift-refine`, commit `aba8ba8`): opt into cancellation explicitly.

```swift
for asset in assets {
    if Task.isCancelled { return }        // stop fetching for the stale album
    if let img = await fetch(asset) { loaded.append(img) }
}
guard !Task.isCancelled else { return }   // don't let a superseded load clobber the current album
images = loaded
```

**Lesson:** cancellation only reaches an `await` site that opts in. Any callback bridge (`withCheckedContinuation`, delegate, completion handler) won't return on cancel by itself — put `if Task.isCancelled { return }` at the top of the awaiting loop *and* a `guard` right before the final state write. A "sometimes shows the previous album after a fast switch" symptom that tracks *switch speed* is this race, not a fetch bug.

Same pass also: released the previous batch's `stopCachingImagesForAllAssets()` before priming a new one (caching used to accumulate across switches), computed the noise grain once instead of per switch, and hoisted `manager.images` to a local inside the `Canvas` draw closure (was an observation-tracked read per cell per frame).

---

## The before/after, roughly

| | Before | After |
|---|---|---|
| Disk cache format | PNG, ~150 KB/file | JPEG 0.85 opaque, ~15 KB/file |
| Warm cache concurrency | Unbounded (thousands of tasks) | 50-task sliding window |
| Calendar open (2nd time) | Top flash + jump to date | Instant fade-in at date |
| Monochrome coverage | Everything inc. tint | Only thumbnail pixels |
| Carousel thumb size | 150px (2.2× upscale) | Screen-scale exact |
| Cache consistency after deletes | Stale counts | Invalidated on every mutation |

---

## Related

- [[Culla]] — project index
- Commits: `c9dfdc7` (JPEG + concurrency cap), `34ce331` (cache key + lifecycle), `f1677b5` (invalidation + heart), `58f58f7` + `08c7092` + `3a5e7ab` (calendar scroll & reveal), `25be6d6` (monochrome scope), `d357714` (carousel resolution), `45f8d2a` (default off)
