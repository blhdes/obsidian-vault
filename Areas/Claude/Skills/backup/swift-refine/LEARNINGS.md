# Swift Refine — Learnings

Append-only log of patterns, anti-patterns, and API quirks discovered while running `/swift-refine`. Read at the start of each invocation as additional rules; append 0–3 new entries at the end. Be concrete or stay quiet — vague entries pollute the file.

Format:

```markdown
## YYYY-MM-DD — Short title

**Tags:** [perf] [concurrency] [gesture] [state] [memory] [api] [anti-pattern] [convention]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action.
```

---

<!-- entries appended below -->

## 2026-05-22 — Per-tick dominant-axis gate freezes gestures mid-drag

**Tags:** [gesture] [anti-pattern]
**Context:** A scrub gesture filtered each `.onChanged` tick with `guard abs(translation.width) >= abs(translation.height) else { return }`. Real-world finger drags wobble — the moment vertical briefly outpaces horizontal, the per-tick guard early-returns and `dragX` stops updating, but the gesture is still active so the deck *freezes* until horizontal catches back up. Reads to users as "the gesture randomly cut out."
**Lesson:** Direction locks need to be decisions, not filters. Pick the axis on the first tick past `minimumDistance` (via a `@State enum DragAxis { undecided, horizontal, ignored }`), then honor that lock for the rest of the gesture. `.onEnded` resets to `.undecided`. The per-tick guard is wrong even when individual ticks would pass it.

## 2026-05-22 — `Task.isCancelled` is the only race guard that works for value-type Views

**Tags:** [concurrency] [api]
**Context:** Initially planned a "snapshot fetchKey, re-read after await, bail if changed" identity guard alongside `Task.isCancelled` in a SwiftUI view's `.task(id:)` body. Realized the captured `self` in a value-type View closure is a *copy* — `self.fetchKey` after `await` returns the same value as before, because the struct's stored properties don't mutate, the new instance is a different struct entirely. The identity check can never fire.
**Lesson:** For value-type SwiftUI views, the only race guard between `await` and `@State` mutation is `Task.isCancelled` (combined with `.task(id:)` for the cancel trigger). Don't write input-identity guards by re-reading View properties post-await — they will silently always pass. If you need true input identity, pass the value into the async function explicitly and compare to a captured snapshot of *that* — but in `.task(id:)` setups, the framework already does this for you.

## 2026-05-22 — Stacked `.shadow` modifiers double per-tick render cost; collapse on the focus axis

**Tags:** [perf]
**Context:** Five overlapping cards each had two `.shadow()` modifiers cross-fading via a continuous `centreness` value tied to drag position. Body re-evaluated per gesture tick, so 10 offscreen shadow rasterizations were happening 60× per second during a scrub.
**Lesson:** When two shadows cross-fade based on the same continuous parameter, prefer dropping the secondary entirely if the primary's curve already covers the visual range — `appAccent.opacity(0.35 * centreness)` already fades to invisible at off-centre, so no second shadow is needed to fill the gap. Save the cross-fade pattern for cases where the two shadows are genuinely different geometry (e.g., directional light + glow).

## 2026-05-22 — A "rest" opacity branch inside a container with outer `.opacity(progress)` is always dead code

**Tags:** [anti-pattern] [api]
**Context:** A sidebar empty-state used `.opacity(isDragging ? 0.85 + 0.15*progress : 0.6)` inside a panel whose parent applied `.opacity(Double(dragProgress))`. The `: 0.6` "rest" floor multiplied by an outer opacity of 0 always paints zero pixels, so the branch is never visible — but it reads like real intent and confuses the next reader.
**Lesson:** When stacking opacities across container levels, audit the inner conditional against the outer's domain. If the outer is `.opacity(progress)` and the inner has a "rest" branch for `progress == 0`, the rest branch is dead. Collapse to a single expression of progress (`0.85 + 0.15 * progress`) or move the floor outward where it can actually paint.

## 2026-05-22 — Name shared haptic helpers by signal, not by input gesture

**Tags:** [convention] [anti-pattern]
**Context:** `Haptics.swipeRight()` was used both for the right-swipe playlist-assign and for the up-swipe Loved action because both wanted a `.medium` impact. A later refactor split the assign haptic out (`sidebarDrop`) but left `swipeRight` firing on the *vertical* Loved gesture, with a band-aid comment "(no target)". A function named for the input gesture quietly outlives its accuracy.
**Lesson:** Name haptic helpers by the *signal* they convey (`loved`, `dismiss`, `sidebarDrop`, `confirm`), never by the input gesture (`swipeRight`, `swipeLeft`, `longPress`). Gestures get reassigned to different actions over time; the haptic vocabulary should describe what the user is *being told*, not what their finger did.

## 2026-05-23 — Two surfaces, same "next item" question → one helper or they drift

**Tags:** [state] [convention] [anti-pattern]
**Context:** A hero preview and a carousel both answered "what's the next song in this mode?" with their own copy of the filter logic. The carousel correctly excluded sorted+dismissed (and playlists in unsorted mode); the hero ran an unfiltered library request. Users saw the hero surface a song the carousel had already skipped — visible only when you compared the two surfaces side-by-side, which is exactly the case (tap hero → carousel).
**Lesson:** Whenever two surfaces share an upstream question — what to exclude, how to sort, what counts as "in scope" — extract one helper that both call, even if the bodies look only ~10 lines each. Diverging copies that *happen to agree today* will silently disagree the first time one is changed and the other isn't. Bonus: split `.task(id:)` keys when only part of the input changes (e.g. `deckKey` vs `leadKey`) — SwiftUI runs them concurrently for free, and you avoid re-walking the library every time only the lead song changes.

## 2026-05-23 — Splitting one `@State` array into `lead + deck` keeps the scrub deck cheap

**Tags:** [perf] [state]
**Context:** Hero scrub deck originally held one `artworks: [Artwork]` that loadArtworks() rebuilt on every refetch — including when only the carousel-handoff "lead" song changed. Refactored into two `@State`s (`deckArtworks`, `leadArtwork`) with a computed `combinedArtworks` derived once per body call via a local `let cards = combinedArtworks` at the top of the rendering ViewBuilder.
**Lesson:** When part of a collection updates on a hot path (carousel close → new lead) and the rest is stable (the deck), splitting into two `@State`s + a computed combiner is cheaper than one mutable array AND eliminates a class of races (the deck task can't clobber the lead task's write and vice versa). Read the computed property once per body via a `let` so per-iteration ForEach access doesn't re-allocate the combined array.

## 2026-05-26 — Capture the real platform error before "fixing" a failing write — it may be a hard API limit, not a bug

**Tags:** [api] [anti-pattern]
**Context:** A "Move out" sort added the song to the destination but left it in the source, with a misleading toast. It was tempting to treat the removal as a fixable bug (pagination? ID mismatch? retry?). Instrumenting the actual throw revealed `ICPlaylistUpdateErrorDomain` "Updating playlists are only allowed when updating a playlist that your app has created" — `MusicLibrary.shared.edit` (the only remove API) works ONLY on app-created playlists. No code fix could ever make it work for a user's Music-app playlist.
**Lesson:** When a write/edit/delete throws and the cause isn't obvious, add a one-shot `print(error)`, reproduce once, and read the real domain/code BEFORE designing a fix. An opaque failure is often a hard platform restriction, in which case the correct move is to *gate the feature where it can't work* (and report honestly), not to keep "fixing" a call the OS will always reject. Also: one capability flag (here `isEditable`) can silently conflate two independently-permissioned operations (add vs. remove) — when behavior diverges, split the flag.

## 2026-05-26 — A sticky flag set by a fallible heuristic needs a *reachable* reset, or delete it

**Tags:** [state] [anti-pattern]
**Context:** A "read-only" brand was stored as a persistent `Bool` set on any write failure, intended to clear on the next successful write. But a branded playlist was hidden from every surface that could issue a write, so the only reset path was unreachable — the flag was a one-way trapdoor. A prior fix had "fixed" the same bug by *relocating* the latch (from `isEditable` to a new flag) instead of removing it.
**Lesson:** When a boolean is set by a heuristic that can be wrong (a single network failure ≠ proof of a permanent condition), trace the reset path concretely and confirm a user can actually reach it. If the state is re-derivable from an authoritative source each sync (here, Apple's `kind`/name), prefer deleting the stored flag entirely and recomputing — a value that's always re-derived can never get stuck. Relocating a latch is not fixing it. (SwiftData: dropping a `@Model` attribute is a safe lightweight migration.)

## 2026-05-30 — `@Observable` view models that touch a `@Environment` ModelContext must be `@MainActor`

**Tags:** [concurrency] [state] [memory]
**Context:** A cold-launch freeze traced to an `@Observable final class` (no `@MainActor`) whose `async` methods touched the main-actor-bound SwiftData `ModelContext` (from `@Environment`) and mutated `@Observable` state. A nonisolated `async` method called from a `@MainActor .task` runs on the *background* pool (SE-0338), so the heavy first-run path (insert every row + `save()`) wrote to the main context off-actor and hung. Bonus trap: `Task { @MainActor in await self?.method() }` does NOT pin a *nonisolated* async method to main — the call hops straight back off; the wrapper is a false comfort.
**Lesson:** Any view model that reads/writes a `@Environment(\.modelContext)` context or mutates `@Observable` state the view renders should be `@MainActor` on the *type*, not patched with per-`Task` `@MainActor` closures. Library walks inside stay responsive because they're `await`/IO-bound and yield. If you genuinely need background DB work, make a *separate* `ModelContext` from the container — never hand the main context across an actor boundary.

## 2026-05-30 — Cold-vs-warm launch asymmetry fingerprints an actor-boundary write, not "slow"

**Tags:** [concurrency] [convention]
**Context:** "First launch after install freezes; second launch is fine" was the decisive clue. Caches (UserDefaults counts, on-disk snapshot, existing SwiftData rows) are all cold on run #1, so the heavy *writes* (mass insert + save) only happen once; run #2 does light updates and early-returns. A pure perf problem would jank every launch; a deterministic first-only hang points at a heavy operation crossing an actor/thread boundary exactly when the cache is empty.
**Lesson:** When a hang reproduces only on the first cold launch, don't reach for "optimize the walk." Find what's *heavy only when caches are empty* (first-run inserts, first-run index build) and check which actor/thread it runs on. The fix is usually correct isolation, not less work.

## 2026-05-31 — An undo path must re-check the inverse op's permission, not inherit the forward op's optimism

**Tags:** [state] [api] [anti-pattern]
**Context:** Undoing a "sort song into playlist" sometimes flashed a "Couldn't remove" error. The forward action (add) is permitted on many playlists; its inverse (remove) was permitted on far fewer (here: only app-created playlists). The undo handler blindly issued the remove with no gate, so it threw on every playlist the add had happily accepted. The "sometimes" was the tell — a timing-independent error that correlates with a *property of the target*, not with speed, points at a capability mismatch, not a race.
**Lesson:** When auditing undo/reverse logic, never assume "we were allowed to do X, so we're allowed to un-do X." The inverse operation often has its own, narrower permission (delete vs. insert, remove vs. add, revoke vs. grant). Apply the *same gate the forward feature already uses* (here `createdByApp`, mirroring the "Move out" gate) at the undo site, and when the inverse genuinely can't run, tell the user honestly rather than attempting a doomed call and catching the error as if it were a transient fault. A "sometimes" failure that tracks a data attribute (not load/latency) is a permission/state bug, not a race.

## 2026-06-01 — A second pager that bypasses the single-flight task handle reopens double-paging

**Tags:** [concurrency] [anti-pattern]
**Context:** A lazy feed coalesced scroll-prefetch through `pagingTask == nil`. A later "jump to date" feature added a *second* paging path (`loadUntil`) that called the page function directly in a loop without ever setting `pagingTask`. So during a jump's `await`, a scroll-triggered prefetch saw `pagingTask == nil`, started concurrently, and both loops read the same offset cursor → duplicate ids in the ForEach + a skipped page. The existing guard was real but only protected one of the two entrances.
**Lesson:** A single-flight guard keyed on a *task handle* only protects the path that sets the handle. When a new code path pages the same cursor, it won't see that handle. Put the reentrancy guard on the *shared mutation function itself* (a `guard !isPaging` flag set at entry, reset on exit) so every caller — task-coalesced or direct-loop — is mutually excluded, regardless of which one set the handle.

## 2026-06-01 — To reuse a fetch for a safety-gated follow-up, return its result; don't re-fetch

**Tags:** [api] [convention]
**Context:** Wanted to stop a session-start path from walking all playlists twice: `membershipIndex.rebuild()` fetched + toggled an `isRebuilding` view flag (drives a cold-launch skeleton), then a separate `reconcile` re-fetched the same data, deliberately using `try?` so a failed fetch reconciles nothing (its safety rule). Fetching once strictly inside the call site forced a choice between losing the skeleton (bypass `rebuild`) or weakening the safety (reconcile against a possibly-stale index after a silent `rebuild` failure).
**Lesson:** When two operations need the same fetch AND the second has a *success dependency* on the first (only run if the fetch succeeded), the owning method must surface its result — make it `@discardableResult func … -> Data?` returning the value on success / `nil` on failure. The caller does `if let data = await fetch() { dependent(data) }`: one walk, the `if let` IS the safety gate, and `@discardableResult` keeps every existing fire-and-forget caller compiling untouched. A method that fetches, mutates view state, and swallows its error can't be safely composed until it returns that error signal.

## 2026-06-02 — `.contentTransition(.symbolEffect(.replace))` is inert across an if/else that swaps view *types*

**Tags:** [api] [anti-pattern]
**Context:** A pill swapped a calendar `Image` for a `ProgressView` via `if isJumping { ProgressView() } else { Image(...).contentTransition(.symbolEffect(.replace)) }`. The symbol-replace content transition reads like it animates the glyph→spinner change, but `.contentTransition` only fires when a view keeps its identity and its *content* changes (e.g. the same `Image` swaps `systemName`). An if/else produces two different view identities, so insertion/removal is governed by `.transition`, and the symbol effect never runs — the actual cross-fade came from a sibling `.animation(_:value:)`.
**Lesson:** `.contentTransition(...)` only applies to content changes *within stable identity*. If a state flip swaps between two different view types (Image↔ProgressView, Text↔Image), the modifier is dead — the visible animation is whatever `.transition`/`.animation(value:)` provides. To actually get a symbol-replace effect, keep one `Image` and change its `systemName`; otherwise delete the modifier as the honest no-op it is.

## 2026-06-02 — A `ClosedRange` literal built from caller-supplied bounds is a latent crash; normalise inside the component

**Tags:** [api] [anti-pattern]
**Context:** `DateJumpSheet` fed `DatePicker(in: lowerBound...upperBound)` straight from caller bounds. Both current callers pass `(oldest, newest)` so lower ≤ upper holds today — but `lowerBound...upperBound` traps (not clamps) the instant a future caller inverts them, and the component had no defence. The clamp-into-span line right above it *looked* like the guard but only protected the initial `selection`, not the range literal.
**Lesson:** Any `a...b` `ClosedRange` literal whose bounds come from outside the type is a hard-crash waiting on the inverted case — `Range`/`ClosedRange` require lower ≤ upper. A presentational component that takes `lowerBound`/`upperBound` should normalise once in `init` (`min(a,b)...max(a,b)`) and use that everywhere, so correctness doesn't depend on every caller's ordering discipline. Don't mistake an adjacent `min(max(x, lo), hi)` clamp for protection of the range literal — they're separate sites.

## 2026-06-02 — A computed array read in a parent modifier arg allocates per body pass, even if the child hoisted it

**Tags:** [perf] [api]
**Context:** A scrub deck already did `let cards = combinedArtworks` once inside its rendering subview (honoring a prior "read once per body" learning), but `body` *also* read `!combinedArtworks.isEmpty` in the `.gesture(including:)` mask — rebuilding the 5-element `[lead] + deck` array a second time on every gesture tick, since `body` re-evaluates per drag tick.
**Lesson:** Hoisting a computed collection inside the child view does NOT cover reads in the *parent's* modifier arguments — `.gesture(including:)`, `.disabled(...)`, `.opacity(...)`, etc. evaluate during the parent's own body pass and re-run the computed property. When such a site needs only a scalar fact (`.isEmpty`, `.count > 0`), give it a dedicated non-allocating computed (`leadArtwork != nil || !deckArtworks.isEmpty`) rather than `someArray.isEmpty`; reserve the array build for the one place that actually needs the elements. Grep every read of a hot computed property, not just the render path.

## 2026-06-02 — Neither `@Observable` nor `@State` dedupes an equal write — gate the setter on a gesture hot path

**Tags:** [perf] [state] [api]
**Context:** A BPM dial called `vm.setBPM(...)` on every `SpatialEventGesture` tick. The `@Observable` model assigned `bpm` unconditionally; within one BPM step the rounded value is identical, but `@Observable`'s generated setter notifies observers *regardless of equality* (it never compares old/new), and the `didSet` re-ran UserDefaults persistence — so the view re-evaluated and the app wrote to disk on every touch event, not on every actual change. The view's `@State` landing-point dictionary had the same shape: reassigned every tick via `.filter` even when no finger lifted.
**Lesson:** On a continuous-gesture write path, gate the mutation yourself — both `@Observable` setters and SwiftUI `@State` invalidate on every assignment, equal-valued or not. Compute the new value, `guard new != current else { return }`, then assign. For a `@State` collection rebuilt each tick, check `contains(where:)` before reassigning so a steady drag does zero writes. This converts "re-render + persist per tick" into "per actual change" with byte-identical behavior, and is invisible to any correctness check — only a per-frame/IO profile (or reasoning) reveals it.

## 2026-06-03 — `withCheckedContinuation` doesn't propagate `.task(id:)` cancellation — the loop must check `Task.isCancelled`

**Tags:** [concurrency] [api] [anti-pattern]
**Context:** A `@MainActor` `@Observable` loader fetched up to 36 thumbnails via `for asset { await fetch(asset) }`, where `fetch` wrapped Photos' callback `requestImage` in `withCheckedContinuation`. Driven from `.task(id: album)`. On a fast album switch SwiftUI cancelled the old task, but a bare continuation keeps awaiting until its callback fires — so the superseded loop ran to completion AND its trailing `self.images = loaded` raced the new loop's write (two loads interleaving on the same actor), occasionally leaving the *wrong* album on screen.
**Lesson:** Cancellation only reaches an `await` site that opts in. A `withCheckedContinuation` (or any callback bridge) won't throw/return on cancel by itself — put `if Task.isCancelled { return }` at the top of the awaiting loop AND a `guard !Task.isCancelled` immediately before the final state write. The loop guard stops wasted work; the pre-write guard kills the stale-clobber race. A "sometimes shows the previous item after a fast switch" symptom that tracks *switch speed* is this race, not a fetch bug.

## 2026-06-03 — Reading an `@Observable` array inside a `Canvas`/`TimelineView` draw closure tracks per access — hoist it once per frame

**Tags:** [perf] [api]
**Context:** A `Canvas` inside `TimelineView(.animation)` indexed `manager.images[idx]` and read `manager.images.count` for every visible cell (~36) at 30fps. Each touch of the `@Observable` property goes through the generated getter + array retain/release, ~2000×/sec, and every read also registers the closure as an observer of that property.
**Lesson:** The "read the computed/observable once per body" rule extends into `Canvas`/`TimelineView` draw closures — they re-run on every timeline tick, so a property read in the inner draw loop is a per-cell-per-frame cost. Bind `let images = manager.images` at the top of the closure and index the local. Bonus: the local also lets you `guard !images.isEmpty` once, making a downstream `% count` provably crash-safe instead of relying on a parent `if !isEmpty` that's evaluated in a separate pass.

## 2026-06-03 — A "selected first" grouping toggle should regroup on demand, not live per tap

**Tags:** [perf] [state] [convention]
**Context:** A filter list got a "Selected first" sort toggle that floated chosen rows to the top. Wiring it to reorder live on each selection tap (`onChange(of: selectionStore)`) re-ran a full locale-sensitive sort over the entire list per tap — ~20–60ms at a few thousand rows — purely to redo a partition the sort order doesn't depend on, and it yanked the tapped row out of view (teleport-to-top).
**Lesson:** For a selection-grouped list at scale, regroup only when the grouping inputs change (toggle the option, change sort field/direction, change search) — NOT on each individual selection tap. Tapping should just flip the row's checkmark in place (the row reads the selection set, so body invalidation updates it for free). This is cheaper (zero per-tap sort) AND better UX (no row-jump). Only consider live-reorder for short lists where re-sort is trivial and the row-jump is invisible; even then it's a deliberate product choice, not a default.

## 2026-06-03 — Hoisting a hot computed read out of a `rowBuilder(for:)` ForEach function means adding a parameter

**Tags:** [perf] [api]
**Context:** Rows were built by `private func filterRow(for: Playlist) -> some View` called inside `ForEach`. The function read `excludedSet` — an `@AppStorage`-backed computed property that decodes a comma-joined string into a fresh `Set` on every access — so every visible row, every body pass, re-decoded the whole string (a Set allocation per scroll frame). The section above it *already* decoded the same set once for a count.
**Lesson:** The "read the hot computed once per body" rule, when the per-row work lives in a `rowBuilder(for:) -> some View` helper, can't be satisfied by a local inside the helper (the helper re-runs per row). Decode/compute once at the section level and thread the value in as a row-builder *parameter* (`filterRow(for: x, excluded: set)`). Reuse the decode the section already did for its count instead of adding a second. Grep every call site of a decode/computed property, including the ones hidden inside per-row builder functions — they don't look like a body read but they are one.

## 2026-06-05 — `try?` guards a throw, not a successful-but-empty fetch; on a cold open the two diverge

**Tags:** [concurrency] [api] [anti-pattern]
**Context:** A History reconcile diffed saved sort records against a live Apple-Music membership fetch behind `guard let data = try? await fetch() else { return }`. On a cold first open `refreshUserPlaylists` returns `[]` *without throwing* (the library mirror hasn't synced yet), so the `try?` passed, the diff saw "this song is in no playlist," and it voided + persisted `voidedAt` on every live sort — corrupting both the History UI and the swipe deck. The reconciler's own doc-comment said "pass only a successfully-fetched, non-empty map," but neither caller enforced it.
**Lesson:** An eventually-consistent resource (a freshly-synced library, a just-created remote object) commonly returns **empty-but-successful** before it's ready — distinct from both "threw" and "genuinely empty." `try?`/`guard let` only filters the throw. Any reconcile/diff that treats *absent* as *removed* must additionally gate on a positive readiness signal (`!data.songIDs.isEmpty`, a non-zero count, a `hasSynced` flag) before it's allowed to write deletions/voids. And when you must tell "not ready yet" from "the item is genuinely gone," **catch the throw explicitly instead of `try? ... ?? []`** — `try?` collapses the throw into the same empty the "gone" case produces, so a one-shot unsynced read flashes every row as "unavailable." Branch: bounded-retry on throw (cap it — an unbounded retry is the infinite-skeleton trap), accept-empty only on a successful walk.

## 2026-06-05 — A doc-comment that says "callers must gate on X" is a wish until the gate lives in the callee

**Tags:** [convention] [anti-pattern]
**Context:** A shared `SortedSongReconciler.reconcile(membership:)` carried the warning "Pass only a successfully fetched [non-empty] map — reconciling against a stale/empty map would falsely void live sorts." Two call sites existed; both gated only on `try?` (throws), neither on emptiness — so the documented precondition was violated by 100% of callers, and the helper happily corrupted data when handed the empty map its own comment warned about.
**Lesson:** When a shared, side-effecting helper has a precondition the caller "must" satisfy, assume a caller will eventually skip it — because the comment isn't on the call site where the mistake is made. Push the guard *into the callee* where it's unbypassable (here: have `reconcile` no-op on an empty membership, or take a `readiness` arg it checks), or at minimum grep every call site when you touch the helper and verify each one actually enforces the stated contract. A precondition documented but not enforced is just a latent bug with good intentions.

## 2026-06-08 — Offset-cursor paging that breaks early must advance by items *consumed*, not page size

**Tags:** [api] [anti-pattern]
**Context:** A library walk fetched 100-item pages but stopped collecting at `desired` (50), then did `pageOffset += page.count`. Breaking mid-page and advancing by the full page silently skipped items 50–99 every call — on a low-exclusion library it dropped ~half the collection from a swipe deck. Tell: a sibling method walking an *in-memory* array did `offset += 1` per item (correct), so only the method paging the external API by offset had the bug.
**Lesson:** Any loop that re-requests an external resource by integer offset and can `break` before exhausting a page must advance the cursor by the number of items it actually examined (`consumed`), never by `page.count`. Same trap hides in the exhaustion check: `if page.count < pageSize { exhausted = true }` wrongly fires when you broke early on a short final page — gate it on `consumed == page.count`. When two sibling methods answer the same "next N" question — one over an in-memory array, one over a paged API — diff their cursor-advance lines; the array one is usually right and the paged one is where the off-by-page lives.

## 2026-06-08 — A threshold-triggered refill is multi-flight by construction; @MainActor doesn't serialize it

**Tags:** [concurrency] [anti-pattern]
**Context:** `advance()` spawned an unguarded `Task` to page more songs whenever `queue.count < refillThreshold`. Because the threshold fires once per *consumed* item, a fast swipe run past it spawned a fresh refill on every swipe while the first fetch was still awaiting — several concurrent pagers all read the same service cursor `offset` before any wrote it back, returning overlapping batches → duplicate cards. The whole VM was main-actor isolated (`SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor`), which lulls you into thinking the cursor reads can't race.
**Lesson:** Any refill gated on `count < threshold` is inherently multi-flight — the threshold *guarantees* repeated spawns across the fetch window, so it MUST be single-flighted with a stored task handle (`guard task == nil`, clear in `defer`), not just "it's on the main actor so it's fine." `@MainActor` serializes synchronous regions only; every `await` is a suspension point where another main-actor task runs, so a `read offset → await → write offset` cursor sequence still interleaves and double-reads. Cancel the handle on any path that resets the cursor (reload/jump) and re-check `Task.isCancelled` after the await before appending, or the stale fetch clobbers the freshly-reset deck.

## 2026-06-08 — A timer-ticked `@Observable` read at a view's root re-renders the whole screen during steady playback

**Tags:** [perf] [api]
**Context:** A swipe screen fed its progress bar by reading `MusicLibraryService.shared.playbackPosition` (an `@Observable` singleton whose timer updates it every 0.1–0.2s during preview) inside the top view's `body` — via a `cardStack` computed property, so the read was attributed to the root view. Result: the *entire* screen (sidebar filter+double-sort, every overlay, the gesture set) re-evaluated 5–10×/sec for the whole duration a song played — the steady state, not an edge case. Invisible to gesture/draw-loop reasoning because the driver is *background playback*, not a finger or a `TimelineView`.
**Lesson:** When a body reads an `@Observable` property that a timer/observer ticks at high frequency (playback position, elapsed time, download progress), that read anchors the *whole* enclosing View's body to the tick — and a computed-property ViewBuilder (`var cardStack: some View`) does NOT create a new attribution boundary, so the read still belongs to the root. The fix is a *leaf View*, not a `let` hoist (a `let` can't decouple body passes when the read itself is the dependency): push the ticking read into a small child View that takes the stable inputs as params and reads the service internally. Only that leaf re-renders per tick. To find these, grep `body`/computed-ViewBuilders for reads of any `@Observable` updated off a `Timer`/`addPeriodicTimeObserver`/`CADisplayLink` — the cost hides in normal use, not in a profile of a gesture.

## 2026-06-08 — A ticking read inside a `LazyHStack`/`ForEach` row is NOT reliably scoped, and extracting it can kill an unrelated per-tick scan for free

**Tags:** [perf] [api]
**Context:** Same `playbackPosition`-driven progress chrome as the entry above, but in a carousel where the read sat inside a `LazyHStack` `ForEach` row built by a `coverCard(song:) -> some View` *method* (not a `View` struct). Tempting to assume "it's in a lazy row, so it's already isolated." It isn't: a method returning `some View` adds no attribution boundary, and lazy containers defer *realization*, not observation scope — so the read can still re-render the parent body. The parent's `body` also opened with `let centered = feed.songs.first(where:)` — an O(n) scan over a list that pages into the hundreds — which therefore re-ran on every tick too.
**Lesson:** Don't assume a `ForEach`/`LazyHStack`/`List` row already scopes a high-frequency `@Observable` read — only a real row *`View` struct* does; a `rowBuilder(for:) -> some View` method does not. Extract the row into a leaf `View` and put the ticking read inside its `body`, gated by the condition that needs it (e.g. read `playbackPosition` only inside `if isCentered && isPlaying`) so non-active rows never subscribe. Bonus payoff: once the ticking property leaves the parent's dependency set, any *other* expensive work at the top of the parent `body` (a `first(where:)` scan, a sort) stops running per tick as a side-effect — verify by checking what the parent body no longer re-evaluates, not just the row.

## 2026-06-08 — Two derived cache keys built from identical inputs = a removed dimension left behind

**Tags:** [anti-pattern] [convention]
**Context:** A count cache built `libraryFingerprint` and `unsortedFingerprint` as two separate `let`s that were byte-identical strings (`"\(sorted):\(dismissed)"`), and the method's doc-comment claimed "unsorted adds the chip toggle to its fingerprint." A prior commit had deleted that toggle — so the dimension the second fingerprint existed to capture was gone, leaving two identical-but-separate bindings that still *read* as intentional ("these must differ for a reason").
**Lesson:** When two derived keys / fingerprints / hashes are computed from the same inputs, don't assume the duplication is defensive — suspect a removed input dimension and check git log for a dropped toggle/option/param. The doc-comment will often still describe the removed dimension, which is the tell. Collapse to one binding and rewrite the comment to match reality; keeping two "for future extensibility" just preserves a lie. (Separate *cache slots* keyed by the same fingerprint can still be legitimate when the stored *values* differ — library count vs unsorted count — so collapse the fingerprint, not necessarily the slots.)

## 2026-06-09 — Share two near-twin chrome views by the pixels, keep the affordance + deliberate animation at the call site

**Tags:** [convention] [api]
**Context:** A play/pause disc + progress ring were duplicated across a carousel cover and a swipe card — intentional "family," but they'd drifted once and cost a multi-iteration bug. The two genuinely diverge in three ways: who owns the tap (carousel = passive `.allowsHitTesting(false)` overlay routed through the cover's `Button`; swipe = the disc *is* a `Button`), disc/ring sizes, and the ring's smoothing (carousel eases the trim with `.linear(0.2)`; the swipe hot-clip ring deliberately steps un-animated to avoid a competing transaction next to the disc).
**Lesson:** Extract the *visual* of near-twin chrome (the glyph + glass + scrim, the trimmed ring) into one size-parameterized `View`, but do NOT try to fold gesture-ownership into it — leave the `Button`/`allowsHitTesting` wrapper at each call site (this also keeps the "disc must be a ZStack sibling, not an overlay" rule intact per-site). For a deliberate animation difference, pass a per-site toggle (here `smoothingValue: Double?` — non-nil animates the trim, nil steps it) rather than forking the component. Two occurrences normally don't earn an abstraction, but a documented drift-bug history flips that: the shared component is what kills the "diff the twins by hand" tax.

## 2026-06-09 — A reusable scroll-on-overflow (marquee) text view needs an idle-alignment param, but the scrolling copy stays leading-anchored

**Tags:** [api] [convention]
**Context:** A `MarqueeText` built for a left-aligned album track row was reused for a *centre-aligned* carousel title. Dropping it in as-is would have left short (non-overflowing) titles jammed to the leading edge instead of centred under the cover. The fix was a single `alignment: Alignment = .leading` param applied only to the truncating base copy's `.frame(maxWidth:.infinity, alignment:)`; the absolutely-positioned scrolling overlay kept its hardcoded `.leading`.
**Lesson:** When generalizing a scroll-when-it-overflows text view to a new alignment, the alignment governs ONLY the fit/idle state (truncated or shrink-to-fit) — the moving overlay must always start at the leading edge, because once the text overflows the slot "centred" is meaningless and a centre-anchored slide reads wrong. Add the alignment as a defaulted param so existing call sites are untouched. Bonus bridge: to feed such a UIFont-measuring marquee from a SwiftUI `.system(.title3, design: .rounded).weight(.semibold)`, build the UIFont via `UIFont.systemFont(ofSize:weight:.semibold).fontDescriptor.withDesign(.rounded)` — `withDesign` preserves the weight trait.

## 2026-06-09 — A body-root `.animation(_:value:)` added to gate an overlay couples its fade to first-render

**Tags:** [perf] [api] [anti-pattern]
**Context:** A first-run guide overlay was gated with `if show { … }` and animated by adding `.animation(.easeOut, value: show)` at the *root* of the host view's body. `show` flips true exactly as the screen settles on cold entry (morph completes, accent extracts, autoplay starts), so the body-wide modifier swept all those coincident diffs into one transaction — reading as cold-launch jank.
**Lesson:** Never animate a conditional overlay by dropping `.animation(_:value:)` at the body root — it animates every coincident change in the whole subtree at the instant the gate flips. Wrap the conditional in its own `ZStack` and put the `.animation(value:)` on *that*, so only the overlay's insert/remove is in the transaction. Asymmetric per-side `.transition(.opacity.animation(…delay))` then buys a delayed fade-in without a second `@State`.

## 2026-06-10 — Inferring "first run" from data shape re-fires when the user empties the thing

**Tags:** [state] [anti-pattern]
**Context:** A one-time sidebar auto-fill was gated on `allSatisfy { !$0.isInSidebar }` ("nothing is in the sidebar yet"). That condition is also true after the user deliberately removes every entry — so the next sync silently repopulated a sidebar the user had just emptied, overriding their choice.
**Lesson:** A "seed once" behavior must be gated on a persisted has-run flag (UserDefaults bool), never on the data looking empty — empty-by-default and emptied-by-the-user are indistinguishable from the data alone. When adding the flag to a shipped app, set it (without seeding) whenever the data shows the seed already happened, so existing installs can't get a surprise re-seed later; and don't burn the flag while the source list is still empty (a cold pre-sync launch isn't a completed first run).

## 2026-06-10 — A static sibling inside a `TimelineView` closure is re-diffed every tick; scope the timeline to the moving subtree

**Tags:** [perf] [api] [anti-pattern]
**Context:** A BPM orb wrapped its whole ZStack — animated Canvas *and* a big static `Text` with `contentTransition`/`minimumScaleFactor` — in `TimelineView(.animation(minimumInterval: 1/30))`. The number depends only on the BPM, yet was re-evaluated and re-diffed 30×/s. The file even carried a `minimumInterval: .infinity` "freeze" hack for its no-motion style, which existed *only because* the static Text was trapped inside the timeline and the timeline therefore had to exist.
**Lesson:** `TimelineView` should wrap exactly the subtree that reads `timeline.date` — extract it (e.g. a `motionLayer` computed property) and keep static siblings as plain ZStack peers outside. A `schedule`-freezing hack (`minimumInterval: .infinity`, `paused:`) is the tell: if you're freezing a timeline so a non-animated child stops costing, the child shouldn't be inside the timeline at all — restructure so the idle state simply doesn't mount one.

## 2026-06-10 — An opacity ramp along an arc is one conic-gradient stroke, not N capped segments

**Tags:** [perf] [api]
**Context:** A radar-sweep comet faked its fading tail with 36 short chord `Path`s per ring per frame (72 paths + strokes per frame at 30fps), each stroked at increasing opacity. `GraphicsContext.Shading.conicGradient` with `Gradient(stops:)` draws the same ramp in a single stroke of one arc path.
**Lesson:** To fade a stroke *along* an arc in Canvas, stroke one `addArc` path with `.conicGradient(Gradient(stops:), center:, angle: tailAngle)` — stops: clear at 0, full at `span/(2π)`, clear again just after so nothing paints past the head. Coordinate quirks that make it work: in SwiftUI's y-down space `addArc(..., clockwise: false)` sweeps visually clockwise (matching increasing-angle motion), the conic fraction also grows clockwise from `angle`, and the "clear" stop must be `color.opacity(0)` (not `Color.clear`, which is transparent black and can tint the ramp). Anchor the gradient at the tail angle so the path and shading share a reference; a small filled head dot hides the cut-off head cap.

## 2026-06-10 — Memoizing a derived ordering of SwiftData models can't live in the view; onChange won't see in-place mutations

**Tags:** [perf] [state] [api]
**Context:** Wanted to stop a body that re-runs per drag tick from re-filtering + re-sorting a playlist list each frame. The obvious view-side fix — `@State` memo + `.onChange(of: viewModel.playlists)` — silently never invalidates: mutating a property *inside* a `@Model` (e.g. `isInSidebar`) and reassigning the array keeps the same instances, which compare equal, so `onChange` doesn't fire.
**Lesson:** Put the memo on the (reference-type) view model, where every mutation path already funnels through one refresh method that can nil the memo key. Fold collaborator-owned inputs (e.g. a counts cache on another `@Observable`) into the key via an explicit `private(set) var generation: Int` bumped wherever that collaborator invalidates — exact invalidation, one cheap string compare per body pass. Mark the memo storage `@ObservationIgnored` so the lazy fill during a body read isn't a tracked write back into the observation system.

## 2026-06-11 — An explicit .task kick plus onChange(of: vm?.property) is a guaranteed double trigger

**Tags:** [concurrency] [anti-pattern]
**Context:** A view kicked off video playback from its `.task` ("onChange misses the initial value") AND from `.onChange(of: viewModel?.currentIdentifier)`. But the view model starts nil and is loaded inside that same `.task`, so the observed value demonstrably changes nil → first-identifier after load — onChange DOES fire, and both paths ran the same prepare concurrently (double network fetch, transient second AVPlayer).
**Lesson:** "onChange doesn't fire for the initial value" is only true when the value is already settled at first body; if the initial value is produced asynchronously after appear, the nil→loaded transition IS a change and onChange fires. When you keep both triggers for safety, dedupe in the callee (early-return when the requested input is already active) rather than reasoning about which trigger wins — the dedup also covers future callers.

## 2026-06-11 — Same-input duplicate loads slip past an identifier-equality guard; use a generation token

**Tags:** [concurrency] [state]
**Context:** A player's post-await race guard was `guard activeIdentifier == identifier`. Two loads for the *same* identifier can be in flight at once (double trigger; undo back to a card within its load window) — both pass the equality check, both build players, one leaks a moment of playback.
**Lesson:** Input-identity guards only discriminate *different* inputs. When the same input can legitimately be requested twice concurrently, guard with a monotonic `generation` counter: bump on every prepare/teardown, capture locally, compare after the await. Equality on the input then becomes the *dedup* (early-return before starting), and the generation is the *staleness* check after.

## 2026-06-11 — AVAudioSession .playback escalation is one-way unless teardown deactivates with notifyOthersOnDeactivation

**Tags:** [api] [state]
**Context:** Unmuting a video set `.playback` + `setActive(true)` (pausing the user's Music — intended). Moving to the next card reset the *category* to `.ambient` but never deactivated, so Music stayed paused for the rest of the app session — a sticky escalation with no reachable reset.
**Lesson:** Pair every `.playback`+`setActive(true)` escalation with a de-escalation site: `setActive(false, options: [.notifyOthersOnDeactivation])` then back to `.ambient/.mixWithOthers`, gated on an `isEscalated` flag. Put it in the player teardown path (after `pause()` — deactivating a busy session throws), not in the mute toggle, so re-muting mid-video doesn't thrash the session but the next card reliably hands audio back.

## 2026-06-11 — A `while !Task.isCancelled` loop in a struct View's `.task` never sees updated view inputs

**Tags:** [concurrency] [state] [api]
**Context:** A mosaic background ran an indefinite flip loop inside `.task(id:)`, reading `self.images.count` each iteration to pick random photos. The View is a struct, so the loop's `self` is a frozen copy from task start — after the parent swapped in a new (smaller/larger) photo pool, the tiles *rendered* the new pool but the loop kept picking indices from the old pool's count, skewing distribution or never showing some photos. No crash (a `% count` masked it), so it read as "works."
**Lesson:** The 2026-05-22 "captured self is a copy" rule applies even harder to *long-lived loops*: a post-await identity guard silently always passes, and a loop silently uses stale inputs forever. Every view input a `.task` loop reads must be folded into the task id (restart-to-recapture) — or the mutable state must live in `@State`/a reference type, which the boxed storage keeps current across struct copies. Audit a `.task(id:)` by listing the inputs its closure touches and diffing that list against the id string; any input missing from the id is frozen at task start.

## 2026-06-14 — A per-drag-tick rebuild is only a "regression" when N is large OR the path is steady-state

**Tags:** [perf] [convention] [anti-pattern]
**Context:** A sidebar built an accent-colour `spectrum` array inside `body`, which re-runs every drag tick (`dragProgress` churns). The file's own learnings are full of "fix the per-tick recompute," which pulled hard toward caching it in `@State`. But the honest magnitude: accent-mode-only (off by default), N capped at 10, and only during an *active drag* — a transient gesture, not steady-state. The `@State` cache also risked a first-frame colour flash. The correct call was to leave it.
**Lesson:** Don't reflexively fix a per-tick recompute just because it's per-tick — weigh N and duration first. The prior per-tick wins in this codebase all had large N (36 cells, hundreds of rows) or *steady-state* drivers (background playback ticking for the whole song). A small-N (≤~10) rebuild bounded to a transient gesture is not a named regression worth a caching mechanism + its first-frame/flash risk. "Measure before optimizing" cuts both ways: it also licenses *declining* an optimization out loud, with the magnitude as the reason.

## 2026-06-14 — Extracting `body` siblings into a `@ViewBuilder` property preserves VStack spacing identically

**Tags:** [api] [convention]
**Context:** Collapsed a deeply-nested header (`Button` + an `if showColorPicker { … }` disclosure, two siblings inside a `VStack(spacing: 8)`) into a single `@ViewBuilder private var colorPickerSection`. The worry: would moving two stack children behind one property name change how `VStack(spacing:)` distributes spacing between them?
**Lesson:** It doesn't. A `@ViewBuilder` property returning `(A; if cond { B })` produces a `TupleView<(A, Optional<B>)>`, and a `VStack(spacing: n) { theProperty }` flattens that TupleView into the *same* per-child layout as `VStack(spacing: n) { A; if cond { B } }` inline — spacing applies between A and B either way. So extracting body siblings into a `@ViewBuilder` var to tame nesting is layout-safe by construction (no wrapper view, no spacing change); reserve the byte-identical worry for cases where you accidentally add a real container (an extra `VStack`/`Group` with its own spacing) around the extracted pieces.

## 2026-06-18 — A partial-update DTO of optionals omits nil — "pass nil to clear" silently no-ops the column

**Tags:** [api] [anti-pattern]
**Context:** A REST PATCH used an `AssetUpdate` struct of all-optional fields (`var image_url: String?`, etc.) whose whole point was "only non-nil fields are sent." Saw an inconsistency — `insert` mapped empty→`nil` (stored NULL) while `update` sent `""` — and "fixed" update to also map empty→`nil` for parity. That's a regression: Swift's synthesized `Encodable` encodes optionals with `encodeIfPresent`, so a `nil` field is **omitted** from the JSON, and a PATCH that omits a column leaves it **unchanged** — so clearing the image would silently fail (old value persists, reappears on reload). The empty string was the *only* way to clear the column with that encoder.
**Lesson:** For a partial-update DTO built from optionals (the omit-nil-to-leave-unchanged pattern), `nil` means "don't touch," NOT "set to NULL" — so you cannot clear a column by passing `nil`; you need an explicit JSON null (a double-optional / custom `encode` that distinguishes omit from null) or a sentinel like `""`. INSERT and UPDATE legitimately differ here: on insert an omitted column takes its DEFAULT (often NULL), on update it's left as-is, so a `NULL`-vs-`""` asymmetry between the two paths is frequently *correct*, not a bug. Before "fixing" such an inconsistency, confirm how the encoder treats nil and what the DB does with an omitted vs explicitly-null column.

## 2026-06-18 — A sheet whose error-swallowing parent returns Void always dismisses, even on failure

**Tags:** [state] [convention] [anti-pattern]
**Context:** An editor sheet's `save()` did `await onSave(draft); dismiss()`. The parent's `onSave` wrapped the network write in `do/catch`, showed an error toast in `catch`, and returned normally (Void) — so `dismiss()` ran unconditionally and a failed save closed the sheet, discarding everything the user had typed (the toast even flashed behind the dismissing sheet). `isSaving` was set true and never reset, masked only because the sheet always closed.
**Lesson:** When a child commits via an `async` callback owned by a parent that catches-and-swallows its own errors, the callback MUST surface a success signal (`async -> Bool`, or `throws` rethrown) — a Void callback gives the child no way to tell success from failure, so any "dismiss after await" fires on both. Gate the dismiss on the signal (`if await onSave() { dismiss() } else { isSaving = false }`); the parent returns `true` at the end of its `do` and `false` in `catch`, keeping toast/haptic/reload exactly where they were. Audit any `await callback(); dismiss()`/`pop()`/`reset()` sequence where the callback can fail without throwing.

## 2026-06-19 — A gitignored .xcodeproj means the generator manifest is source-of-truth; pbxproj edits are throwaway

**Tags:** [convention] [api]
**Context:** Added 3 new Swift files to a SwiftUI app and hand-edited `project.pbxproj` (PBXBuildFile + PBXFileReference + group child + Sources-phase entry, ×3 files) to make local `xcodebuild` pass. Later found `warket.xcodeproj` is gitignored and generated by XcodeGen from `project.yml`, whose target globs the whole source folder (`sources: - path: warket`).
**Lesson:** Before hand-editing `project.pbxproj` to register new files, run `git check-ignore` on it and look for a generator manifest (`project.yml` = XcodeGen, `Project.swift` = Tuist). If the `.xcodeproj` is generated + gitignored and the source dir is globbed, new files are picked up automatically by `xcodegen generate` — the pbxproj edits only make the *current local* project compile and must NOT be committed (they're regenerated). Don't keep burning effort maintaining pbxproj as if it were source.

## 2026-06-19 — A single-row insert helper that RETURNINGs the row is the wrong tool inside a bulk import loop

**Tags:** [perf] [api]
**Context:** An import loop reused `addAsset(...)` (one `.insert(...).select().single()`) once per asset, and computed the next position via `fetchAssets(select "*").map(\.position).max()`. So importing N assets = N insert round-trips each returning a discarded full row, plus a full-rows read per list just to find one max.
**Lesson:** Bulk paths want bulk primitives: a single `.insert([rows])` with no `.select()` (no per-row round-trip, no discarded RETURNING), and a `select("col").order(desc).limit(1)` one-row read for a max/extreme instead of pulling every row to reduce client-side. A per-item helper that returns the created object is built for interactive single-add UX; reusing it in a loop silently multiplies round-trips and payload. When mirroring a web/JS data path, copy its query *shape* (the web here already did batch-insert + limit-1), not just its result.

## 2026-06-22 — The Reduce-Motion branch of a TimelineView closure is where static views hide

**Tags:** [perf] [api] [anti-pattern]
**Context:** A BPM orb's `motionLayer` had already (per the 2026-06-10 lesson) pulled the static number *out* of its 30fps timeline. But the `if reduceMotion { … } else { Canvas }` branch *inside* the timeline closure still put two static guide `Circle`s alongside the two blinking dots — so under Reduce Motion those two real SwiftUI circles were rebuilt+diffed 30×/s for the whole session, while the normal path correctly used a cheap `Canvas`. Easy to miss precisely because the headline timeline-scoping was already done and the accessibility branch reads as "the simple fallback."
**Lesson:** When auditing a `TimelineView` you think is already scoped, check its *conditional branches* too — the Reduce-Motion / fallback path is a classic place static views get trapped in the per-tick closure, because attention goes to the animated path. Split `motionLayer` into `@ViewBuilder` per-mode, hoist the static rings to siblings *outside* an inner timeline that wraps only the moving dots. Note the magnitude honestly (2 circles) but it's steady-state under Reduce Motion (runs forever, not a transient gesture), which is the category that earns the fix per the 2026-06-14 rule.

## 2026-07-14 — A lossy-shortened category label used as a chart domain needs a uniqueness check

**Tags:** [api] [anti-pattern]
**Context:** An era histogram labeled decade bins with `'%02ds` (1990 → "'90s") and pinned ordering via `.chartXScale(domain: labels)`. The shortening is lossy: 1920 and 2020 both produce "'20s", so a sample spanning a century puts a duplicate string in the categorical domain — Swift Charts merges/misplaces those bars. Invisible in every "normal" test because most libraries span < 100 years.
**Lesson:** Whenever a categorical axis label is derived by a lossy transform (`% 100`, prefix-truncation, initials), check `Set(labels).count == labels.count` before using them as plot categories or a pinned domain, and fall back to the lossless form on collision. A pinned `chartXScale(domain:)` makes the bug worse, not better — the domain itself carries the duplicate. Same trap for any keyed ForEach keyed on the shortened label.

## 2026-07-14 — Converting `try?` to logged `do/catch` inside a post-await loop needs a cancellation gate first

**Tags:** [concurrency] [convention]
**Context:** Upgraded a portrait-fetch loop from `(try? await resolve())` to `do/catch` + `print` so real network failures stop masquerading as "no result." But the loop runs after earlier awaits; if the owning `.task` is cancelled mid-loop, every remaining iteration's await throws `CancellationError` — which the new catch would log as N phantom "lookup failed" lines.
**Lesson:** When adding error logging to awaits that previously hid under `try?`, add `if Task.isCancelled { return }` at the loop head (or catch `is CancellationError` separately) in the same change. The silent-`try?` version accidentally tolerated cancellation noise; the logging version turns that same noise into misleading diagnostics unless cancellation is filtered explicitly.
