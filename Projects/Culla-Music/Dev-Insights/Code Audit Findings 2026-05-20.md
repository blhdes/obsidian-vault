---
title: Code Audit Findings — post-VM-extraction window
date: 2026-05-20
tags: [culla-music, audit, bugs, performance, refactor]
---

# Code Audit Findings — 2026-05-20

Findings from the audit window `c95c341..HEAD` (see [[Code Audit Tracker 2026-05-20]]). Each entry has a **severity**, **file:line**, **why it matters**, and a **fix** sketch.

## 🔴 Bugs (real broken behavior)

### B1. Artist-count cache refresh loops every picker open
**File:** `Views/SourceScopePickerSheet.swift:359-362`

```swift
let needsRefresh = artistTrackCounts.isEmpty
    || artistTrackCounts.count < libraryArtists.count
    || artistTrackCounts.values.contains(0)
```

`safeCountLibrarySongs` in `MusicLibraryService` deliberately returns `nil` for any artist whose `\.artists, contains:` filter comes back empty (uploaded tracks, fuzzy metadata, featured-only credits). So `artistTrackCounts.count` is *always* ≤ `libraryArtists.count`, and usually strictly less. The middle clause therefore fires **on every picker open**, undoing the disk-snapshot fast path the function was written to enable.

**Fix:** either (a) drop the count-mismatch clause and rely on the freshness check, or (b) write the *attempted* artist IDs to disk separately so the comparison is "we've tried all current artists" not "we have a count for all current artists."

---

### B2. Artist-source loader spins forever on error
**File:** `Views/HomeView.swift:423-433` (write) + `549-565` (read)

```swift
private func fetchArtistTrackCountIfNeeded(id: String) async {
    if artistTrackCounts[id] != nil { return }
    do {
        ...
        artistTrackCounts[id] = ids.count
    } catch {
        print("HomeView.fetchArtistTrackCount failed: \(error)")
    }
}
```

On error, `artistTrackCounts[id]` stays nil, and `isLoadingCount(for: .library)` returns `artistTrackCounts[id] == nil` → the `LinearLoader` on the Library mode card never stops. The user is told the count is still being computed even though we gave up.

**Fix:** distinguish loading-vs-failed. Either keep a `failedArtistCounts: Set<String>` sentinel and check both, or model `artistTrackCounts: [String: Result<Int, Error>]`. Simpler: write `artistTrackCounts[id] = 0` on failure and accept the misleading zero, but that contradicts the picker's "don't lie with 0" rule.

---

### B3. `RootView.activeConfig` is dead state with a misleading writer
**File:** `Views/RootView.swift:8` + `86-91`

```swift
@State private var activeConfig: SwipeConfig?     // declared
...
private func endSession() {
    withAnimation(.spring(...)) {
        activeViewModel = nil
        activeConfig = nil    // written here
    }
}
```

`activeConfig` is declared and nilled in `endSession`, but **never set** in `startSession` and never read anywhere. Either remove it, or set it in `startSession` and use it for things that currently dig into `vm.config` (e.g. `MusicSwipeView` could read its mode/source from `activeConfig`).

**Fix:** delete the property. Future-self will recreate it the day they need it.

---

### B4. `MembershipIndex.trackCount` returns `0` for unknown read-only playlists
**File:** `ViewModels/MembershipIndex.swift:105-117`

```swift
func trackCount(forPlaylistAMID amID: String?) -> Int? {
    guard let amID else { return nil }
    ...
    return countsCache?[amID] ?? 0
}
```

Comment says read-only playlists may be absent when the curated toggle is off — and the picker's `displayCount(for:)` explicitly handles this with `playlist.isEditable ? 0 : nil`. But `trackCount` here always returns 0. Today it's hidden by the fact that `ManagePlaylistsSheet` only iterates `editablePlaylists`, but anyone reusing `trackCount` for a read-only row will silently show "0". Easy footgun.

**Fix:** take editability into account at the call site, *or* return `nil` when `amID` isn't a key in `countsCache` and let callers default to 0 themselves.

---

## 🟡 Subtle bugs / edge cases

### M1. Duplicate full library walk on every picker open
**File:** `Services/MusicLibraryService.swift:307-336` + `Views/SourceScopePickerSheet.swift:314-318`

```swift
// SourceScopePickerSheet.artistsList:
.task {
    await loadArtistsIfNeeded()         // walk #1 — refreshLibraryArtists()
    await loadArtistCountsIfNeeded()    // walk #2 — fetchAllArtistTrackCounts() calls
}                                       //          refreshLibraryArtists() AGAIN
```

`fetchAllArtistTrackCounts()` starts with `let artists = try await refreshLibraryArtists()` which clears `artistCache` and re-pages the entire library a second time. For a power user with 500+ artists that's an extra ~5 round-trips plus a full cache wipe (which briefly nulls out `artwork(forArtistID:)` for any concurrent reader).

**Fix:** have `fetchAllArtistTrackCounts(using:)` accept the already-fetched array, or short-circuit `refreshLibraryArtists` when called within the same render pass.

---

### M2. `loadCounts` and `triggerRecompute` can race
**File:** `Views/HomeView.swift:144-149`

```swift
func triggerRecompute() {
    pendingRecompute?.cancel()
    pendingRecompute = Task { @MainActor [weak self] in
        await self?.recomputeCounts()
    }
}
```

`triggerRecompute` only cancels prior triggered tasks, not the initial `recomputeCounts()` kicked off inside `loadCounts()`. Flipping the curated toggle while cold-start is still walking the library means two concurrent walks race to write the cache. Both writes hit the same `UserDefaults` keys with the same `today` value but potentially different `unsortedFingerprint` → the loser's stale-fingerprint write wins.

**Fix:** make the initial walk cancellable too. Store the initial-load task in the same `pendingRecompute` slot.

---

### M3. `MusicSwipeView.flyOff` uses non-cancellable `DispatchQueue.asyncAfter`
**File:** `Views/MusicSwipeView.swift:558-565`

```swift
DispatchQueue.main.asyncAfter(deadline: .now() + flyDuration) {
    highlightedID = nil
    withAnimation(.easeOut(duration: slideInDuration)) {
        cardOffset = .zero
        action()
    }
}
```

If the user double-taps to skip mid-fly-off, the second flyOff's scheduled block can run *after* the new card has already animated in, snapping `cardOffset` back to zero a beat too late. A cancellable `Task.sleep` would let the second invocation pre-empt.

**Fix:** swap to `Task { try await Task.sleep(...) }` and store the handle in a `@State` cancellation token.

---

### M4. `MembershipIndex.schedulePersist` snapshots on every mutation
**File:** `ViewModels/MembershipIndex.swift:311-325`

```swift
private func schedulePersist() {
    persistTask?.cancel()
    let snapshot: [String: [String]] = index.mapValues { $0.map(\.rawValue) }
    persistTask = Task.detached(priority: .utility) {
        try? await Task.sleep(for: .milliseconds(250))
        ...
    }
}
```

For a burst of swipes the snapshot allocation runs N times (each O(n) in song count) but only the last task actually persists. Moving `index.mapValues` *inside* the detached task — guarded by `Task.isCancelled` after the sleep — collapses the work to a single allocation per burst.

**Fix:** defer the snapshot to inside the task, after the sleep clears.

---

### M5. `MusicLibraryService.refreshLibraryArtists()` clears the artwork cache mid-fetch
**File:** `Services/MusicLibraryService.swift:201-219`

```swift
artistCache.removeAll(keepingCapacity: true)
while true { ... }
```

`HomeView` shows an `ArtistThumbnail` whose artwork comes from `MusicLibraryService.shared.artwork(forArtistID:)`. If the user has an artist source picked and the picker is opened (triggering `refreshLibraryArtists`), the cache is briefly empty until the first page lands → the thumbnail on Home momentarily falls back to the initials placeholder.

**Fix:** build the new cache in a temp dictionary and atomically replace at the end of pagination.

---

### M6. `ArtistDetailSheet.resolve` may surface the wrong artist on name collision
**File:** `Services/MusicLibraryService.swift:633-652`

```swift
return response.artists.first(where: { $0.name.lowercased() == lower })
    ?? response.artists.first
```

For an unmatched-library track by "Tyler", the catalog search returns multiple Tylers and the fallback picks whichever Apple sorted first. The user sees a wrong-artist hub with no indication of the mismatch.

**Fix:** only return the exact-match candidate. If none matches, return nil → the `FallbackArtistView` already exists for this case and handles it cleanly with a Google search.

---

### M7. `MusicLibraryService.fetchAllArtistTrackCounts` partial failure invalidates the whole snapshot
Combined with **B1**, a single artist's network failure means the persisted snapshot is missing one key → next picker open re-fetches *all* artists. One flaky artist = whole-batch refetch forever.

**Fix:** persist the *attempted* artist ID list alongside the counts, and only refetch artists not in that list (plus any new ones).

---

## ⚡ Performance / smoothness

### P1. `SourceScopePickerSheet.filteredSortedPlaylists` / `filteredSortedArtists` recompute on every render
**File:** `Views/SourceScopePickerSheet.swift:182-236`

Both are computed vars that filter + sort on each body evaluation. Typing in the search field triggers per-keystroke re-renders. For libraries with ~500 artists each keystroke runs a `localizedStandardContains` pass over the full set followed by a sort.

**Fix:** memoize with `@State` updated via `.onChange(of: searchQuery)` and `.onChange(of: sort field)`. Or wrap in a small `@Observable` filter model.

---

### P2. `MembershipIndex` rebuilt eagerly on cold launch even when not needed yet
**File:** `Views/HomeView.swift:389-393`

```swift
if initialSnapshot.isEmpty, !vm.playlists.isEmpty {
    let index = MembershipIndex(service: MusicLibraryService.shared)
    await index.rebuild()
    sourceTrackCounts = index.countsSnapshot()
}
```

`MembershipIndex.rebuild` fetches every playlist's tracks. On first launch this blocks the Home count flow before the user has indicated any intent to sort. Acceptable price for accurate counts, but consider: only do it once the user opens the picker, OR opportunistically and *don't* await it on Home's task.

**Fix:** kick it off non-blocking — `Task { ... }` instead of `await`. The picker's `.task` already re-uses the on-disk snapshot, so it'll pick up the result whenever it lands.

---

### P3. Per-frame allocations in `cardStack`
**File:** `Views/MusicSwipeView.swift:374-422`

`viewModel.playlistMemberships(for: next)` and `viewModel.dismissedDate(for: next)` are called every body evaluation — i.e., every drag tick. `MembershipIndex.memberships(for:)` does cache, so that's cheap after the first hit. `dismissedDate(for:)` may not — verify it's not hitting SwiftData each call.

**Fix:** if `dismissedDate` isn't cached, pre-compute it once per song change with `.task(id: current?.id)` and store in `@State`.

---

### P4. `MusicLibraryService.artistLibrarySongIDs` returns a fresh array every call
**File:** `Services/MusicLibraryService.swift:255-257`

Wrapping `artistLibrarySongs(...).map { $0.id.rawValue }` allocates a new `[String]` each call. Used by `HomeView.fetchArtistTrackCountIfNeeded` and unsorted/dismissed exclusion paths. Caching the ID array alongside `artistSongCache` is cheap and avoids repeated mapping.

**Fix:** add `private var artistSongIDsCache: [MusicItemID: [String]]` and populate alongside `artistSongCache`.

---

## 🧹 Refactoring / code quality

### R1. `SourceScopePickerSheet` is doing too much (655 lines, one file)
**File:** `Views/SourceScopePickerSheet.swift` (whole file)

State: 10 `@State` + 4 `@AppStorage`. Concerns: segmented mode switching, search, two sort fields × two directions, list rendering for two distinct row types, async loading for two count surfaces, persisted-snapshot warming. Even unmodified, this file is hard to read end-to-end.

**Suggested split:**
- `PickerSortStore` (the @AppStorage + the choice enums + their bindings)
- `ArtistRowsLoader` (the loadArtists + loadArtistCounts + needsRefresh logic)
- `ArtistPlaceholder` is fine on its own — already extractable

The two sort-choice enums (`PlaylistSortChoice`, `ArtistSortChoice`) are nearly identical and could share a generic implementation parameterized by `Field: SortField`.

---

### R2. `HomeView.body` mixes layout, state coordination, and gear-icon overlay
**File:** `Views/HomeView.swift:253-421`

170-line body. The settings gear in the top-trailing overlay, the start button at the bottom, three ModeCards in the middle, and the sourceFilterButton + sourceTransferPicker layer between them. Easier to navigate if the body were just `VStack { topBar; modesSection; sourceSection; orderSection; startButton }` with each as a private helper.

---

### R3. Dead-state and unused declarations
- `Views/RootView.swift:8` — `activeConfig` (see **B3**)
- `ViewModels/MembershipIndex.swift:302` — `cache.removeAll(keepingCapacity: true)` inside `loadPersisted` runs against an already-empty dictionary on init. Cosmetic but misleading.

---

### R4. `MusicLibraryService` is 935 lines covering 6 distinct domains
**File:** `Services/MusicLibraryService.swift` (whole file)

Sections: authorization, library paging, library artists (NEW), playlists, unsorted, dismissed, playback (full-song + hot clip), and audio session. The artist additions pushed this past a reasonable single-actor boundary. Worth extracting:

- `ArtistLibraryService` (artist caches, fetches, counts) — clean home for the things in **B1, M1, M5, M7, P4**
- `MusicPreviewPlayer` (full-song + clip + fade envelope + audio session)

The main service shrinks to library + playlists + auth.

---

### R5. `HomeViewModel.recomputeCounts` has two parallel cache lanes hand-rolled in one function
**File:** `Views/HomeView.swift:41-138`

Library cache and unsorted cache share structure (date + fingerprint + value keys, freshness check, write-back on miss) but are interleaved. A `CountCache` struct with `read()` / `write(date:fingerprint:value:)` would dedupe the UserDefaults plumbing and keep the actual recompute loop focused on the iteration.

---

### R6. `MusicSwipeView` has 11 `@State` properties + 3 toast/undo Tasks
**File:** `Views/MusicSwipeView.swift:25-53`

`toastTimer`, `undoHideTask`, `showUndo`, `showRemovalSheet`, `artistSheetSong`, `isLongPressing`, `cardOffset`, `highlightedID`, `playlistFrames`, `dynamicAccent`, plus 3 `@AppStorage`. The toast/undo coordination (timer task + auto-hide) is a coherent unit that could live in a `ToastCoordinator` similar to the existing extracted `UndoCoordinator`.

---

## 📊 Status

- [x] Audit pass complete
- [x] Findings written to vault
- [x] **Batch 1 (2026-05-20):** B1+M7 (`560ea63`), B2 (`6e356e7`), M1 (`2805334`), M5 (`fb40c86`)
- [x] **Batch 2 (2026-05-20):** M4 (`7d30e73`), P1 (`f37a140`), P3 verified — already O(1) via `DismissedDateStore.dates`
- [x] **Batch 3 (2026-05-20):** B3 (`301cf86`), B4 (`27b8224`), M6 (`f2b1732`)
- [x] **Batch 4 (2026-05-20):** M2 (`02deea5`), M3 (`a216824`), P2 (`0cf73b1`)
- [x] **P4 audited, skipped:** the audit overstated call frequency. Only call site is `HomeView.fetchArtistTrackCountIfNeeded`, which fires once per source pick (result cached in HomeView state). Map allocation is not a hot path; ship cost > value.
- [ ] **Refactors R1–R6** — outstanding, not blocking

## Outcome

All four severity-tagged bug findings (B1–B4), all seven medium findings (M1–M7), and three of four perf findings (P1, P2, P3) are resolved across 11 commits with no regressions. Build passed after each commit.

**Net effect:**
- Source picker: snapshot cache works as designed, no more thrashing on artists with no library matches, search/sort scales to 500+ artists.
- Artist hub: no more wrong-artist on name collisions; loader stops spinning on errors.
- Home: cold-launch doesn't block on a full playlist walk; toggle-flips during cold-start cancel cleanly instead of racing the cache.
- Swipe deck: rapid re-swipes no longer leave a phantom slide-back firing after the new card; artist thumbnails don't flicker during library refresh.
- Persistence: burst-swipe disk writes do one snapshot per 250 ms instead of N.

## Refactor backlog (not started)

| Tag | Surface | Effort |
| --- | --- | --- |
| R1 | Split `SourceScopePickerSheet` (655 lines) | medium |
| R2 | Decompose `HomeView.body` (170-line body) | small |
| R4 | Extract `ArtistLibraryService` + `MusicPreviewPlayer` from `MusicLibraryService` (935 lines) | medium |
| R5 | Extract `CountCache` from `HomeViewModel.recomputeCounts` | small |
| R6 | Extract `ToastCoordinator` from `MusicSwipeView` | small |

R3 (dead-state cleanup) was absorbed into B3.

## Related

- [[Code Audit Tracker 2026-05-20]] — the window and themes this audit covered
- [[Projects/Culla-Music/culla-music|Culla Music project index]]
