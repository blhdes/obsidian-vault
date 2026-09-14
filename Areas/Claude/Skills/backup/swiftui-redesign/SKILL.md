---
name: swiftui-redesign
description: Rethink an existing SwiftUI screen using modern iOS APIs (Liquid Glass, MeshGradient, symbolEffect, contentTransition) to make it bolder and more expressive while preserving its data/state logic byte-identical. Explicit-invocation only — use when the user types `/swiftui-redesign` or otherwise asks you to "rethink", "redesign", or "modernize" a specific SwiftUI view. The skill enforces a strict plan-then-implement flow: read → critique → propose → wait for green light → implement → verify.
---

# SwiftUI Redesign

A repeatable playbook for redesigning a SwiftUI screen using current Apple APIs (iOS 18 / 26 era). The end product is a bolder, more cohesive view — Liquid Glass surfaces, ambient motion, expressive transitions — without breaking any data flow, sheets, or hero animations the existing screen depends on.

## When this skill applies

The user typed `/swiftui-redesign` (or named the skill explicitly). They want a specific SwiftUI view rethought visually.

The user almost certainly hasn't given you full requirements. They want you to be opinionated. Your job is to diagnose, propose, and execute — not to ask "what would you like changed?"

## Self-improving — read this first

This skill carries a sibling file: `LEARNINGS.md`, in the same directory as `SKILL.md` (`~/.claude/skills/swiftui-redesign/LEARNINGS.md`). It's an append-only log of patterns, anti-patterns, and API quirks discovered across past runs.

**Every invocation must:**

1. **Load `LEARNINGS.md` at the start of Phase 0** and treat its contents as additional rules layered on top of SKILL.md. If a learning conflicts with this file, the learning wins (it's newer evidence).
2. **At the end of Phase 7**, distill 0–3 *non-obvious* new entries and append them. Trivial restatements of SKILL.md content do not earn an entry. The bar is: "future-me would be smarter for having this."

The skill should get sharper with each use. If you find yourself re-discovering the same lesson twice, that's a signal the first lesson wasn't written clearly enough — rewrite it instead of duplicating.

## The phases

You **must** complete phases 0–3 and wait for the user's confirmation before writing any code. Skipping ahead produces churn.

### Phase 0 — Load prior learnings

Before reading the target view, read `~/.claude/skills/swiftui-redesign/LEARNINGS.md` if it exists. Scan for entries tagged with:

- `[gating]` — deployment-target / `#available` patterns
- `[api]` — API quirks, gotchas, performance traps
- `[convention]` — opinionated defaults proven by prior runs
- `[anti-pattern]` — things that looked right but produced churn

Hold them in working memory for the rest of the run. If a learning is directly relevant to a phase below, surface it in the chat ("Per prior learning: X — applying that here").

### Phase 1 — Read the screen and its context

Don't redesign in the dark. Before forming any opinion:

1. **Read the target view file in full** (every line, not just the body).
2. **Read the surrounding helpers it actually uses**:
   - Accent environment / palette helpers
   - Model types it consumes (the enum / struct definitions, not just the names)
   - Sheets and child views it presents
   - Any custom transitions / hero namespaces it participates in
3. **Verify the actual deployment target by reading the `.pbxproj`** — never trust user-stated values. Look for the `IPHONEOS_DEPLOYMENT_TARGET` at the **target level** (project-level is overridden). This determines which APIs need `#available` gating.
4. **Skim recent commits** with `git log --oneline -20` to surface opinionated guidelines that aren't in CLAUDE.md. Lines like "refactor: scope accent colouring to critical surfaces only" tell you what *not* to do.
5. **Check auto-memory** for feedback notes about UI conventions in this project.

Read in parallel — fire multiple `Read` / `Bash(grep)` calls in one message.

### Phase 2 — Honest critique

Write a short diagnosis in chat. Be direct, no preamble. Cover at least:

- **Entry/identity** — does the screen have personality at the top, or does it open feeling like a settings dialog?
- **Hierarchy** — are equal-weight controls competing? Is the primary action visually the primary action?
- **Dead space** — are `Spacer()`s sandwiching nothing? Is the screen using its vertical budget?
- **Accent usage** — is the brand color carrying meaning or sprinkled decoratively?
- **CTA character** — utilitarian `.borderedProminent`, or does it invite?
- **Motion** — does anything breathe? Music/photo/social apps especially deserve ambient life.
- **Modern API gaps** — is Liquid Glass / MeshGradient / symbolEffect / contentTransition used, or is the screen visually frozen in iOS 15?

Then list what's missing in one tight paragraph.

### Phase 3 — Propose a bold direction

Name the direction (e.g., "Living Glass", "Hero card", "Layered dashboard"). For each layer of the new design:

- What changes
- Which iOS API drives it
- Why it earns its place (not just "looks cool")

Add a **file checklist** in `| File | Action |` table form. Identify which files are new vs. modified.

Close with **open questions** the user must answer before you write code. Always include:

- **Deployment target floor** — confirm what you read in step 1.4, and flag any gating needs.
- **Animation budget / reduce-motion** — should ambient backgrounds gate on `accessibilityReduceMotion`?
- **Dynamic vs static behaviors** — for any preview/hero element you're proposing, does it refresh on selection changes, or stay fixed?

**Stop here.** Do not write a single line of code until the user confirms.

### Phase 4 — Wait for green light

If the user redirects ("not that direction, do X instead") — go back to Phase 3 with the new direction. Don't try to merge directions.

If the user says "go", proceed to Phase 5.

### Phase 5 — Implement

Order of operations:

1. **Create new helper files first** (subviews, modifiers, backgrounds). The main view file should be the last thing you touch — by then all the symbols it references already exist.
2. **Touch the main view via targeted `Edit` calls**, not a full rewrite. Replace `body`, replace specific subviews, replace the small private struct components. Preserve everything else verbatim.
3. **Preserve the data/state logic byte-identical.** ViewModels, `@State`/`@AppStorage` properties, `.task` setup, `.onChange` handlers, computed helpers like `count(for:)` — do not touch unless the redesign genuinely requires it. The redesign should be a layout change, not a refactor.
4. **Preserve hero/matched-geometry tags.** `matchedGeometryEffect` / `matchedHero` ids are contracts with parent screens — losing one breaks a navigation animation.
5. **Extract subviews when the main file would exceed ~250 lines after the edit.** Per the global manifesto: files over 200 lines need extraction. New components live next to the consumer (`HomeHeroArtStack.swift` next to `HomeView.swift`).
6. **Gate iOS 26 APIs** consistently. Use the helper modifier pattern (see "Conventions" below) instead of sprinkling `if #available` inline at every call site.
7. **Track work with `TaskCreate`** when you're touching 4+ files. Mark each one completed as you go.

### Phase 6 — Verify

1. Run `xcodebuild -project <path>.xcodeproj -scheme <scheme> -configuration Debug -destination 'generic/platform=iOS Simulator' build` — pipe to `tail` to keep tool output small.
2. Check for **both** errors AND warnings. Re-run with `grep -E "warning:|error:"` if needed.
3. Output a **change-set table** with `| File | Action |` rows.
4. Output a short **caveats** section: deployment-target mismatches, layout risks on smaller phones, anything you couldn't visually verify.
5. Suggest `/run` or `/verify` if the user wants to see it on simulator before merging.

### Phase 7 — Capture new learnings

Before the run ends, take 60 seconds to reflect. Ask:

1. **Did I trip over anything?** A surprising API, a misleading project setting, a layout that broke on a phone size, a fallback that misbehaved.
2. **Did I make a non-obvious choice that worked?** A trick worth repeating — e.g., "filtering by `\.id, equalTo:` beats walking the library for single-ID lookups."
3. **Did a prior `LEARNINGS.md` entry contradict reality?** Update it instead of appending — stale learnings are worse than missing ones.
4. **Did the user redirect me?** A correction is a strong signal. Capture *why* they redirected, not just what they wanted.

Append entries to `~/.claude/skills/swiftui-redesign/LEARNINGS.md` using this format:

```markdown
## YYYY-MM-DD — Short title

**Tags:** [api] [gating] [convention] [anti-pattern] [layout] [motion]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action, not the story.
```

Cap at 3 entries per run. If you have more candidates, pick the three most likely to bite on a future run. Quality over completeness — a noisy LEARNINGS.md is a learnings file nobody reads.

**Do not append if:**

- The lesson restates something already in SKILL.md.
- The lesson is project-specific (Culla, that one weird playlist API) — those belong in the project's auto-memory, not the global skill.
- The lesson is "I should be more careful" without a concrete rule.

When you're done, briefly tell the user what you captured (one line each), so they can challenge or refine.

## Modern API reference (iOS 18 / 26)

### Liquid Glass (iOS 26+ — needs fallback)

```swift
// Single surface
content.glassEffect(.regular.tint(accent).interactive(), in: shape)

// Container — adjacent glass shapes refract into each other
GlassEffectContainer(spacing: 10) {
    VStack(spacing: 10) { children }
}

// Union — morph two glass shapes together (hero handoffs)
.glassEffectUnion(id: "key", namespace: ns)
```

Fallback for iOS 18-25: `.background(shape.fill(.thinMaterial))` + optional tint overlay.

### MeshGradient (iOS 18+)

Animated ambient backgrounds. Use 9 control points on a 3×3 grid; wander the 4 interior points on a slow Lissajous curve (~5-7% amplitude, ~15-second period).

```swift
TimelineView(.animation(minimumInterval: reduceMotion ? .infinity : 1.0/30.0)) { timeline in
    let t = reduceMotion ? 0 : timeline.date.timeIntervalSinceReferenceDate
    MeshGradient(width: 3, height: 3, points: meshPoints(at: t), colors: colors)
}
```

Always cap with a `.ultraThinMaterial` veil (~0.4 opacity dark / ~0.55 light) for text contrast.

### Symbol effects (iOS 17+, some 18+)

- `.symbolEffect(.bounce, value: trigger)` — discrete reaction to state changes
- `.symbolEffect(.pulse, options: .repeating)` — slow heartbeat
- `.symbolEffect(.pulse.byLayer)` — multi-layer pulse (good for dots, badges)
- `.symbolEffect(.breathe)` — iOS 18.0+, ambient
- `.symbolEffect(.wiggle, value:)` — discrete attention pull
- `.contentTransition(.symbolEffect(.replace))` — for toggle icons that swap

### Content transitions (iOS 17+)

- `.contentTransition(.numericText(countsDown: true))` — animated digit ticks for counters
- `.contentTransition(.opacity)` — cross-fade for text/label swaps
- `.contentTransition(.identity)` — opt out

### Animations

- `.snappy(duration:)` — tight, no overshoot
- `.smooth(duration:)` — eased, soft
- `.bouncy(duration:)` — playful overshoot
- `.spring(response: 0.4, dampingFraction: 0.78)` — predictable physical

Choose explicitly. Defaulting everything to `.easeInOut` is the iOS-15 look.

### Layout

- `Spacer(minLength:)` — adapts to smaller screens without crushing
- `containerRelativeFrame(.horizontal)` — frame as fraction of container
- `phaseAnimator([phases]) { content, phase in }` — choreograph multi-step sequences
- `scrollTransition` — visual effects tied to scroll position

## Conventions (opinionated)

These are defaults; let the project's existing guidelines override if they conflict.

- **Accent on critical surfaces only.** The brand color marks the CTA and the *one* primary selection state. It does not paint every checkmark, every chevron, every icon. If the repo's `RootView` deliberately avoids global `.tint`, respect that.
- **CTAs are usually NOT glass.** A Liquid Glass screen needs a bold, opaque CTA to win against the surroundings. Use a gradient capsule with an accent shadow instead.
- **Selected state = accent halo + chevron, not full accent fill.** A tinted glass with `shadow(color: accent.opacity(0.28), radius: 16, y: 8)` + a trailing `chevron.right` reads as "selected" without dominating.
- **Background animation must be gentle.** ~5-7% control-point wander, ~15-second cycle. If it draws the eye, it's too much.
- **Numeric counters get `numericText(countsDown:)`.** Direction matches semantics — counting *down* to zero (unsorted dwindling) vs *up* (collection growing).
- **Toggle icons get `.symbolEffect(.replace)` via contentTransition.** Avoid hard cuts on state changes.
- **Honor `accessibilityReduceMotion`** on anything ambient. Symbol pulses can stay (they're focal); background gradients should freeze; spring transitions should shorten.
- **One-off helpers are fine.** Don't invent a "reusable" abstraction for a component used in exactly one place. `HomeHeroArtStack` is local to Home; that's correct.

## Anti-patterns to refuse

- **Don't trust user-stated deployment target.** Always verify the `.pbxproj`.
- **Don't rewrite the whole file** when 3-4 targeted `Edit` calls cover the change.
- **Don't paint everything with the accent.** It loses meaning.
- **Don't skip the reduce-motion gate** for ambient animations.
- **Don't add abstractions for hypothetical reuse.** Three similar lines beats a premature helper.
- **Don't break `matchedGeometryEffect` / `matchedHero` tags.** They're contracts with parent screens.
- **Don't add `try/catch` blocks that swallow errors silently.** If a preview-artwork fetch fails, return `nil` and let a placeholder render — but log the error if it's actionable.

## A helper modifier pattern for Liquid Glass

When the project doesn't already have one, drop in a small helper to centralize the iOS 26 gating instead of sprinkling `if #available` at every call site:

```swift
extension View {
    @ViewBuilder
    func glassSurface<S: Shape>(
        in shape: S,
        tint: Color? = nil,
        interactive: Bool = false
    ) -> some View {
        if #available(iOS 26.0, *) {
            self.modifier(GlassSurfaceModifier(shape: shape, tint: tint, interactive: interactive))
        } else {
            self.background {
                shape.fill(.thinMaterial)
                    .overlay(shape.fill(tint?.opacity(0.18) ?? .clear))
            }
        }
    }
}

@available(iOS 26.0, *)
private struct GlassSurfaceModifier<S: Shape>: ViewModifier {
    let shape: S
    let tint: Color?
    let interactive: Bool
    func body(content: Content) -> some View {
        var effect: Glass = .regular
        if let tint { effect = effect.tint(tint) }
        if interactive { effect = effect.interactive() }
        return content.glassEffect(effect, in: shape)
    }
}

struct GlassStack<Content: View>: View {
    let spacing: CGFloat
    @ViewBuilder var content: () -> Content
    init(spacing: CGFloat = 10, @ViewBuilder content: @escaping () -> Content) {
        self.spacing = spacing
        self.content = content
    }
    var body: some View {
        if #available(iOS 26.0, *) {
            GlassEffectContainer(spacing: spacing) { VStack(spacing: spacing) { content() } }
        } else {
            VStack(spacing: spacing) { content() }
        }
    }
}
```

Once this lives in `Helpers/`, every glass surface in the redesign becomes a single-line call.

## What the deliverable looks like

A typical run leaves the user with:

1. **New helper file(s)** — animated background, glass modifier, hero subview — in `Helpers/` or alongside their consumer in `Views/`.
2. **A modified main view file** with the body replaced and one small private subview (the row/tile component) redesigned.
3. **All existing data/state logic intact** — no ViewModel changes, no `.task` rewrites, no signature changes on the screen's `onStart` / callback inputs.
4. **A green `xcodebuild`.**
5. **A short report** with the change set, caveats, and a suggestion to run the app on simulator.
