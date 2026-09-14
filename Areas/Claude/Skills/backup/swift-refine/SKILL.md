---
name: swift-refine
description: Tighten an existing Swift/SwiftUI file from the inside — performance, smoothness, refactoring, bug solving — without changing user-visible behavior. The internal counterpart to `/swiftui-redesign`. Explicit-invocation only — use when the user types `/swift-refine` or otherwise asks you to "tighten", "refactor", "optimize", "smooth out", or "audit" a specific Swift type or view. Enforces a strict plan-then-implement flow: read → critique → propose → wait for green light → implement → verify.
---

# Swift Refine

A repeatable playbook for refining a Swift/SwiftUI file from the inside: hot paths, allocations, redraws, gesture/animation smoothness, concurrency, state-machine clarity, lurking bugs. Output is a tighter, faster, less surprising implementation — with byte-identical user-visible behavior unless a bug fix demands a deliberate change (called out explicitly).

This is the internal counterpart to `/swiftui-redesign`. That skill goes *outward* (visuals, motion, expressive surfaces). This one goes *inward* (work-per-frame, lifetimes, races, dead branches).

## When this skill applies

The user typed `/swift-refine` (or named the skill explicitly). They want a specific Swift type / SwiftUI view audited and tightened.

The user almost certainly hasn't given you full requirements. They want you to be opinionated. Your job is to diagnose, propose, and execute — not to ask "what would you like changed?"

## Self-improving — read this first

This skill carries a sibling file: `LEARNINGS.md`, in the same directory as `SKILL.md` (`~/.claude/skills/swift-refine/LEARNINGS.md`). It's an append-only log of patterns, anti-patterns, and API quirks discovered across past runs.

**Every invocation must:**

1. **Load `LEARNINGS.md` at the start of Phase 0** and treat its contents as additional rules layered on top of SKILL.md. If a learning conflicts with this file, the learning wins (it's newer evidence).
2. **At the end of Phase 7**, distill 0–3 *non-obvious* new entries and append them. Trivial restatements of SKILL.md content do not earn an entry. The bar is: "future-me would be smarter for having this."

The skill should get sharper with each use. If you find yourself re-discovering the same lesson twice, that's a signal the first lesson wasn't written clearly enough — rewrite it instead of duplicating.

## The phases

You **must** complete phases 0–3 and wait for the user's confirmation before writing any code. Skipping ahead produces churn.

### Phase 0 — Load prior learnings

Before reading the target, read `~/.claude/skills/swift-refine/LEARNINGS.md` if it exists. Scan for entries tagged with:

- `[perf]` — measurable optimizations, hot-path traps
- `[concurrency]` — Task/MainActor/cancellation gotchas
- `[gesture]` — drag/long-press recognizers and their interactions
- `[state]` — state-machine clarity, observable scope
- `[memory]` — captures, cycles, leak shapes
- `[api]` — Swift/SwiftUI API quirks
- `[anti-pattern]` — refactors that *looked* right but regressed something
- `[convention]` — opinionated defaults proven by prior runs

Hold them in working memory for the rest of the run. If a learning is directly relevant to a phase below, surface it in chat ("Per prior learning: X — applying that here").

### Phase 1 — Read the target and its context

Don't refine in the dark. Before forming any opinion:

1. **Read the target file in full** (every line). Don't skim — bugs hide in the lines you skipped.
2. **Read the surrounding code it actually touches**:
   - The consumer(s) — who instantiates this, who passes inputs, what callbacks they expect
   - Services / models it depends on, especially anything async
   - Helpers it calls into (extensions, modifiers, shared types)
   - Anything sharing state with it (`@AppStorage` keys, environment values, notifications)
3. **Skim recent commits** that touched the file: `git log --oneline -20 -- <path>`. The commit history tells you what's been tried and what bugs have already been fixed — don't reintroduce them.
4. **Check auto-memory** for feedback notes or constraints tied to this code.
5. **Verify the deployment target** by reading the `.pbxproj` at the **target level** (project-level is overridden). Relevant whenever you'd reach for `@Observable`, `withAnimation(completion:)`, `onGeometryChange`, or other modern APIs.

Read in parallel — fire multiple `Read` / `Bash(grep)` calls in one message.

### Phase 2 — Honest critique

Write a short diagnosis in chat. Be direct, no preamble. Cover the dimensions that *actually apply* to the file in front of you — don't run through them for completeness:

- **Hot paths.** What runs per gesture tick, per animation frame, per body re-evaluation? Is anything O(n) where O(1) is possible? Is anything done eagerly that could be lazy?
- **Allocations and redraws.** Are arrays/dictionaries rebuilt every body call when they don't change? Are computed properties expensive but un-memoized? Does an observable touch ripple wider than it needs to?
- **Concurrency.** Are Tasks cancelled when superseded? Is `Task.isCancelled` checked after every `await`? Is `@MainActor` correctly placed (or correctly absent)? Are there races between "user did X" and "in-flight Y just returned"?
- **State machine.** Can the view/type be in inconsistent states? Are there pairs/triples of booleans that should be an enum? Are there transitions the code allows but never intends?
- **Gestures and animations.** Is direction lock correct? Is `predictedEndTranslation` used where it should be? Are simultaneous gestures resolved deterministically? Are animation curves consistent with the rest of the project?
- **Memory.** Closures capturing self strongly when they shouldn't. Long-lived Tasks holding their owner. Observers never removed.
- **Bugs in waiting.** Off-by-one. Division by zero in the empty-list case. Force-unwraps with no invariant guarding them. `try?` that hides a real error. `guard else { return }` that silently does nothing when something *did* go wrong.
- **API misuse.** Wrong overload, deprecated form, expensive system call where a cheap one exists.
- **Naming and shape.** Does the code read as it acts? Are mutable variables disguising state machines? Are 6-deep `if/else` chains hiding what's really one switch?

Then end with a one-line summary of the dominant theme. ("This file is fine structurally — the issue is purely per-frame allocations in `cardLayout`." or "Three separate bugs are reachable from rapid gestures; the rest is fine.")

### Phase 3 — Propose a direction

Name the direction concretely. Examples:

- "Cancel-and-reuse" — single in-flight Task, cancel-on-supersede
- "Precompute the layout table" — turn per-frame O(n) work into one cached `[Slot]`
- "Lift the state machine" — collapse `isDragging` / `isHolding` / `hasFlung` into one enum
- "Tighten the cancellation guards" — every `await` site now has an `if Task.isCancelled { return }` immediately after
- "Drop the GeometryReader" — replace with `containerRelativeFrame` / `ScaledMetric`

For each change in the direction:

- **What changes** (one sentence)
- **Why it earns its place** (the bug it kills or the work it saves — not "looks cleaner")
- **Risk** if any (what user-visible behavior could regress; how you'll verify it didn't)

Add a **file checklist** in `| File | Action |` table form. Identify which files are new vs modified.

Close with **open questions** the user must answer before code is written. Always include:

- **Behavior preservation contract** — confirm with the user which behaviors are sacrosanct (e.g., gesture feel, exact animation timing) so you can verify against them.
- **Bug-fix vs no-change calls** — if the audit found bugs, list them and ask which the user wants fixed in this pass vs deferred (a bug fix *will* change user-visible behavior; flag it explicitly).
- **Scope** — confirm the refine is limited to the file(s) you propose, not a cascade.

**Stop here.** Do not write a single line of code until the user confirms.

### Phase 4 — Wait for green light

If the user redirects ("don't bother with X, but tighten Y") — go back to Phase 3 with the new direction. Don't merge directions and don't quietly do both.

If the user says "go", proceed to Phase 5.

### Phase 5 — Implement

Order of operations:

1. **Make one change at a time.** Refactors that touch many places at once should be split into per-concept commits. If you're tempted to "while I'm in here…" — stop. That's the impulse that hides regressions.
2. **Preserve user-visible behavior byte-identical.** Same gesture → same outcome. Same animation timing. Same callback firing order. If a *bug fix* requires changing visible behavior, that change must be the one already-agreed-upon item from Phase 3 — not a quiet rider.
3. **Preserve public API of the type** unless the contract is broken. Call sites shouldn't have to change for a refactor.
4. **Run the build after each meaningful change**, not just at the end. Catching a typo right after typing it is 10× cheaper than catching it after five more edits.
5. **Track work with `TaskCreate`** when you're touching 4+ files OR making 3+ conceptually distinct changes. Mark each one completed as you go.
6. **Don't introduce abstractions for hypothetical reuse.** Three similar lines beat a premature helper. Refactor the third occurrence — not the first.
7. **Comment policy follows the global manifesto.** Only when *why* is non-obvious: an invariant, a workaround, a deliberate ordering. Don't explain *what* — the names should do that.

### Phase 6 — Verify

1. Run `xcodebuild -project <path>.xcodeproj -scheme <scheme> -configuration Debug -destination 'generic/platform=iOS' build` — pipe to `tail` to keep tool output small.
2. Check for **both** errors AND warnings. Re-run with `grep -E "warning:|error:"` if needed.
3. Output a **change-set table** with `| File | Action |` rows.
4. Output a short **what to verify on device** section: any behavior that depends on real input (gesture feel, animation smoothness, race against real network latency, real-data sizes). Type-checking does not prove these.
5. Output a **what didn't change** line — explicit confirmation that the user-visible behavior contract from Phase 3 still holds, with the one called-out exception if a bug fix changed it.
6. Suggest `/run` or `/verify` if there's any doubt.

### Phase 7 — Capture new learnings

Before the run ends, take 60 seconds to reflect. Ask:

1. **Did I trip over anything?** A misleading API surface, a sneaky invalidation rule, a Task lifecycle that surprised me.
2. **Did I make a non-obvious choice that worked?** A pattern worth repeating — e.g., "moving the layout table to a `static let` killed per-card allocations without changing the type's API."
3. **Did a prior `LEARNINGS.md` entry contradict reality?** Update it instead of appending — stale learnings are worse than missing ones.
4. **Did the user redirect me?** A correction is a strong signal. Capture *why* they redirected, not just what they wanted.

Append entries using this format:

```markdown
## YYYY-MM-DD — Short title

**Tags:** [perf] [concurrency] [gesture] [state] [memory] [api] [anti-pattern] [convention]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action.
```

Cap at 3 entries per run. Quality over completeness — a noisy LEARNINGS.md is a learnings file nobody reads.

**Do not append if:**

- The lesson restates something already in SKILL.md.
- The lesson is project-specific (Culla, that one weird playlist API) — those belong in the project's auto-memory, not the global skill.
- The lesson is "I should be more careful" without a concrete rule.

When you're done, tell the user what you captured (one line each) so they can challenge or refine.

## Critique heuristics

Patterns to look for when reading any Swift/SwiftUI file. Not a checklist to run through — a vocabulary for naming what you see.

### Performance / hot paths

- **Per-frame allocation.** `let frames = [Frame(...), Frame(...), ...]` inside a body call. Hoist to `static let` or a `@State` cache keyed on inputs.
- **Quadratic gesture handlers.** Recomputing the full layout for every `.onChanged` tick when only one parameter moved. Cache the static bits; only the changing parameter should drive recompute.
- **GeometryReader cascade.** A `GeometryReader` invalidates anything reading its proxy on every layout pass. Prefer `containerRelativeFrame`, `ScaledMetric`, alignment guides, or `onGeometryChange(for:of:action:)` (iOS 17+) for surgical reads.
- **Hidden O(library) calls.** Anything that walks a full collection inside a per-event handler. Look for `.first(where:)` over `[Song]` or `[Playlist]` of unknown size — fine for tens, suspect for thousands.
- **`Image(uiImage:)` from a synchronous decode inside `body`.** Decode off-main, cache, then render.

### Concurrency

- **Task that should be `Task<Void, Never>?` and cancelled.** Long-running per-event work (typing debounces, search, accent extraction) that doesn't cancel its predecessor will pile up. Pattern: store a handle, `?.cancel()` on entry, assign the new one.
- **`await` without `Task.isCancelled` after.** When the awaited value comes back, the world may have moved on. Check cancellation *and* check that the input the work was for still matches the current input.
- **`@MainActor` mismatch.** A non-isolated method poking `@Published` / `@State` / view properties needs a hop. The compiler now usually catches this in Swift 6 mode, but Swift 5 mode is silent.
- **`Task.detached` "to escape the actor."** Almost always wrong. You're either fighting actor isolation that exists for a reason, or papering over a thread-safety bug.
- **Structured cancellation broken by `Task { }`.** Spawning an unstructured Task from inside another loses parent cancellation. Use `async let` or `withTaskGroup` for child work.

### State machine clarity

- **Boolean pair masquerading as state.** `isDragging` + `isHolding` + `isFlying`. Ask: which combinations are *valid*? If <4 of 8 (or 16) are, it's an enum.
- **Optional-as-flag.** `var highlightedID: UUID?` is fine. `var error: Error?` *and* `var isShowingError: Bool` is a bug factory — pick one.
- **State that's also a computed thing.** If `isEmpty` is stored and updated by hand, it'll get out of sync. Make it a computed property of the source-of-truth.

### Gestures

- **No direction lock.** A drag that means "horizontal pan" and a drag that means "vertical reveal" should commit to an axis early (compare dominant magnitude of `translation` *and* `predictedEndTranslation`) and stay locked for the rest of the gesture.
- **Missing `predictedEndTranslation`.** Flick recognition without it leaves quick-flick gestures registering as below-threshold. The predicted value matters.
- **Deadzone forgotten.** Tiny drags that should be no-ops still triggering "highlight" feedback because the threshold is 0.
- **Highlight that never clears.** State set in `.onChanged` that isn't cleared on `.onEnded` will linger.
- **Simultaneous gesture collision.** `.highPriorityGesture` next to `.gesture` next to `.contextMenu` — order and modifier choice matter and the rules are subtle. If two recognizers compete, document which wins and why.

### Memory

- **`Task { [weak self] in … }` not used in cases where `self` is long-lived (services, view models).** A captured strong `self` in a Task held by a stored property is a cycle.
- **`NotificationCenter` observers without removal.** Especially in `final class` services. Use `withObservationTracking` or async streams when you can.
- **`Combine` cancellables stored as `var cancellables: Set<AnyCancellable> = []` — fine, but only if the owner outlives the publisher.**

### Bugs in waiting

- **Division by zero / NaN.** `position / duration` when `duration == 0` and `duration` is `TimeInterval` (Double) silently produces `inf` or `NaN` and propagates.
- **Force unwraps.** Every `!` is an invariant assertion. If the invariant isn't documented in a comment *and* enforced upstream, it's a crash waiting on rare inputs.
- **`try?` that hides errors.** Especially around async work. Replace with `do/catch` and log, or thread the error to the caller. Silent failures are the worst kind.
- **`guard else { return }` doing nothing when something failed.** A return on the failure path is fine — but the failure deserves at least a log if it's not actively expected.
- **Animation transactions captured wrong.** State changes inside `withAnimation` that the change happens *outside* (via a Task callback) won't animate. Animation context is captured by *invocation site*, not by *state mutation site*.

## Modern Swift / SwiftUI APIs worth knowing

### Observation (iOS 17+)

- `@Observable` macro replaces `ObservableObject` + `@Published`. Tracking is per-property, not per-object — so views only re-render when the *specific* property they read changes.
- Inject with `@Bindable` for two-way bindings on properties.
- Migration value: a screen reading 1 property from a 20-property model used to re-render on every property change; now it only re-renders when its 1 property changes.

### Structured concurrency

- `Task.isCancelled` — cheap, check after every `await`.
- `try Task.checkCancellation()` — throw on cancel; use when the function returns `throws`.
- `withTaskCancellationHandler` — cleanup on cancel without polling.
- `async let` — concurrent child tasks with structured cancellation propagation.

### SwiftUI body invalidation

- A view's `body` re-evaluates when *any* of its `@State`, `@Observable` property reads, environment reads, or parent-passed properties change.
- `EquatableView` (or applying `.equatable()` to a view that conforms to `Equatable`) lets SwiftUI short-circuit identical re-renders. Use sparingly — equality must be cheap.
- `.id(value)` forces identity changes, which forces full re-creation. Useful for "reset everything" but expensive.

### Animation completion

- `withAnimation(_:completion:)` (iOS 17+) — fires when the animation logically completes. Drives "do X after the morph lands" without a fixed timer.
- `.transaction { $0.animation = … }` — set animation context for a specific state change inside an environment.

### Geometry reads

- `onGeometryChange(for:of:action:)` (iOS 18+) — fires only when the *derived value* changes, not every layout pass. Vastly cheaper than `GeometryReader { ... }` for "tell me when my width crosses X."
- `.background { GeometryReader { … } }` — measure without disrupting layout. The classic before iOS 18.

### Drawing / rasterization

- `.drawingGroup()` — composites the subtree into a single Metal-backed layer. Faster for many small overlapping views; slower for views that change often (defeats SwiftUI's diffing).
- `Canvas { context, size in … }` — imperative draw API. Cheaper than ZStack of many shapes when you have >50ish primitives. Loses `.foregroundStyle` propagation — pass color explicitly.
- `.compositingGroup()` — fuses a subtree's effects before applying parent modifiers. Affects blend modes and opacities.

### Task lifecycle pattern (canonical)

```swift
@State private var inflight: Task<Void, Never>?

func startSearch(_ query: String) {
    inflight?.cancel()
    inflight = Task { @MainActor in
        let results = try? await service.search(query)
        if Task.isCancelled { return }
        guard query == currentQuery else { return } // input no longer current
        self.results = results ?? []
    }
}
```

Two guards: cancellation (the Task was superseded) *and* input identity (a faster Task may have already finished with a newer input). The second is what kills "stale results flash in".

## Conventions (opinionated)

These are defaults; project-specific guidelines override if they conflict.

- **Measure before optimizing.** Don't refactor "for performance" without naming what slowed down and how you'll see the win. If you can't articulate the regression you're fixing, don't refactor it.
- **Make impossible states unrepresentable.** Enums beat boolean pairs. Sum types beat product types when only some combinations are valid.
- **Cancel before start.** Any per-event Task (search, accent extraction, image decode) should cancel its predecessor. Store a handle.
- **Guard cancellation *and* identity.** After every `await`, check `Task.isCancelled` *and* check the input is still current.
- **Refactor the third occurrence, not the first.** Premature abstractions cost more than duplicated lines.
- **Comment policy.** Only when *why* is non-obvious. Never restate what.
- **Don't introduce async where sync is fine.** Wrapping a synchronous computation in `Task { … }` adds a hop and a cancellation surface without any benefit.
- **Don't break user-visible behavior in the name of refactoring.** If you can't show the change is behavior-identical, it's a feature change — flag it as one.

## Anti-patterns to refuse

- **Don't optimize without a named regression.** "This looks slow" is not a reason.
- **Don't refactor for hypothetical reuse.** YAGNI applies harder to abstractions than to code.
- **Don't quietly fix bugs found mid-refactor.** Surface them in Phase 3; let the user decide. A "while I was in there I also fixed…" commit is exactly how subtle behavior changes ship.
- **Don't use `Task.detached` to escape isolation.** The isolation is usually correct; you're hiding a real problem.
- **Don't use `try?` to silence an error you should handle.** Either handle it or thread it out.
- **Don't add `try/catch` blocks that swallow errors silently.** At minimum log with context; at best, surface to caller.
- **Don't reach for `GeometryReader` when a simpler API suffices.** It's a hammer that turns every read into an invalidation source.
- **Don't replace a Rectangle/.fill(material).opacity(binding)` pattern with a helper modifier** if the opacity is bound to a gesture or animation value. Per `swiftui-redesign` learnings, the helper drops continuous control. (Apply on this side too — refactors must preserve gesture feel.)

## What the deliverable looks like

A typical run leaves the user with:

1. **A modified target file** with the named change applied, identical user-visible behavior, and dead code removed.
2. **Possibly one new helper file** if a pure-logic extraction made the target genuinely simpler. New helpers live next to their consumer.
3. **A green `xcodebuild`.**
4. **A short report** with the change set, what to verify on device, and the behavior-preservation confirmation.
5. **0–3 new LEARNINGS entries** if the run surfaced something non-obvious.
