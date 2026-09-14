---
name: glassify
description: Sweep a SwiftUI app for Liquid Glass opportunities and apply them — make the UI more elegant, modern, and Apple-current using iOS 26 glass APIs (glassEffect, GlassEffectContainer, glassEffectID/glassEffectTransition, scrollEdgeEffectStyle, ToolbarSpacer, backgroundExtensionEffect, buttonStyle(.glass)) WITHOUT loudening the design or breaking data/state logic. Explicit-invocation only — use when the user types `/glassify`, or asks to "find liquid glass opportunities", "make it more glassy / more Apple", "modernize the glass", or "audit for Liquid Glass". Whole-app sweep by default; pass a file to focus one screen. Strict flow: map → find → propose → wait for green light → implement → verify.
---

# Glassify

A focused counterpart to `/swiftui-redesign`. Where that skill rethinks one screen's whole design, **`/glassify` does one thing: find every place the app could adopt or upgrade to Liquid Glass, rank them, and (after approval) apply them** — so the app feels more elegant, modern, and Apple-current without a visual rewrite.

The bar is **taste, not coverage.** A great glassify run adds 4 surgical glass moves the user didn't know were possible; a bad one paints glass on everything and loses the brand. More glass is not the goal — *more-correct* glass is.

## When this skill applies

The user typed `/glassify` (or asked to hunt for Liquid Glass opportunities / make the app "more Apple"). They want glass-specific upgrades, not a redesign of layout, copy, or data flow.

- **Default:** whole-app sweep — scan every SwiftUI view.
- **Focus mode:** if the user names a file ("`/glassify HomeView.swift`"), scan only that screen plus the helpers it touches.

You are expected to be opinionated and to **respect restraint** — see the guardrails. Finding 30 places to add glass is easy and wrong; finding the 5 that elevate the app is the job.

## Self-improving — read this first

This skill carries a sibling `LEARNINGS.md` in the same directory. It's an append-only log of glass-specific patterns and traps.

**Every invocation must:**

1. **At the start of Phase 0, load `~/.claude/skills/glassify/LEARNINGS.md`** AND scan `~/.claude/skills/swiftui-redesign/LEARNINGS.md` for `[api]` / `[gating]` / `[convention]` entries — the redesign skill has a deep glass corpus this skill inherits. Treat both as rules layered on top of this file; if a learning conflicts with SKILL.md, the learning wins.
2. **At the end of Phase 7**, append 0–3 *non-obvious* new glass learnings to **glassify's own** `LEARNINGS.md`. Trivial restatements don't earn an entry.

## The phases

Complete phases 0–3 and **wait for the user's confirmation before writing any code.**

### Phase 0 — Load prior learnings

Read both learnings files (above). Hold `[api]`, `[gating]`, `[anti-pattern]`, `[convention]` glass entries in working memory. Surface any directly-relevant one in chat ("Per prior learning: X").

### Phase 1 — Map the surface

Don't propose glass blind. Establish three things, firing parallel reads/greps:

1. **Compile floor + SDK.** Read the **target-level** `IPHONEOS_DEPLOYMENT_TARGET` in the `.pbxproj` (project-level is overridden — look for the value surrounded by `INFOPLIST_KEY_*` lines). Then `xcrun --sdk iphonesimulator --show-sdk-version`: **the gated iOS 26 glass branch only compiles if the SDK is ≥ 26**, regardless of `#available`. If SDK < 26, the entire skill degrades to `.ultraThinMaterial`/`.regularMaterial` suggestions — say so and stop proposing `glassEffect`.
2. **Existing glass vocabulary.** `grep` for `glassEffect|glassSurface|GlassEffectContainer|GlassStack|buttonStyle(.glass)`. Find the project's centralized helper (it usually has one — e.g. `glassSurface(in:tint:interactive:)` + `GlassStack`). **You extend that helper; you never reinvent gating inline.** Note any morph helpers already present (`glassEffectID` wrappers).
3. **Restraint guidelines.** `git log --oneline -20` for lines like "scope accent to critical surfaces", "quiet the settings tier", "redesign: slim …". Check auto-memory for UI-convention notes. These tell you what NOT to glassify.

Then **inventory candidate surfaces**: walk the view files (or the focus file) and list every floating control, chrome button, pill/badge, card, sheet, toolbar, ScrollView/List, and selection state. This inventory is the raw material for Phase 2.

### Phase 2 — Find the opportunities

Walk the **Opportunity Catalog** (below) against each inventoried surface. For every real hit, record:

- **Location** (`File:line` — clickable)
- **Current state** (what it is now: bare button, `.ultraThinMaterial`, isolated glass, segmented control…)
- **Proposed glass move** (one sentence)
- **API** (the exact iOS 26 modifier)
- **Why it earns its place** (elegance/cohesion/Apple-correctness — not "looks cool")
- **Restraint check** (does this stay calm? does it have a backdrop to refract over? does it touch a deliberately-quiet tier?)
- **Tier**: 🟢 safe/calm · 🟡 bold (more motion or a tier shift)

Discard anything that fails the restraint check. A hit you can't justify on elegance is noise.

### Phase 3 — Propose, ranked

Open with a one-paragraph read of the app's *current* glass maturity (none / partial / mature). This sets expectations — a mature app gets fluid-glass upgrades, a bare app gets first-glass adoption.

Then a **ranked findings table**:

| # | Surface | Current → Glass move | API | Tier |
|---|---------|----------------------|-----|------|

Rank by elegance-per-risk: calm high-impact first. Then a **file checklist** (`| File | Action |`). Then **open questions** — always include:

- **Compile floor** — restate the target/SDK from 1.1 and the gating consequence.
- **Reduce-motion** — should glass morphs degrade to `.identity` cut? (Recommend yes.)
- **Tier conflicts** — name any finding that touches a deliberately-quiet screen and ask before loudening it.
- **Which findings to apply** — let the user check off the subset. Default to the 🟢 set.

**Stop. Do not write code until the user confirms.**

### Phase 4 — Wait for green light

If the user trims the set, take exactly that subset. If they redirect ("not the tiles, do the toolbar"), re-rank — don't merge.

### Phase 5 — Implement

1. **Extend the central glass helper first** (add gated `glassMorphID` / `glassMorphTransition` / `softScrollEdge` / etc. as needed — no-ops below iOS 26). All new gating lives in that one file.
2. **Targeted `Edit`s**, never full rewrites. Touch only the surfaces in the approved set.
3. **Preserve data/state/layout byte-identical.** ViewModels, `@State`, `.task`, `.onChange`, computed helpers, paddings, and spacing stay put. Glass is a surface change, not a refactor. When you must wrap something in a container, prefer a layout-neutral wrapper (`GlassStack(spacing: 0) { existingChild }`) so nothing reflows.
4. **Preserve `matchedGeometryEffect` / `matchedHero` tags** — they're contracts with parent screens.
5. **For `.materialize`, put the `GlassEffectContainer` OUTSIDE the `if`** that creates the element, so the container is a stable parent and the child crystallizes inside it.
6. Track with `TaskCreate` when touching 4+ files.

### Phase 6 — Verify

1. `xcodebuild -project <…>.xcodeproj -scheme <scheme> -configuration Debug -destination 'generic/platform=iOS Simulator' build` piped to `grep -E "error:|warning:|BUILD (SUCCEEDED|FAILED)"`.
2. Fix any error/warning you introduced.
3. Output a **change-set table** + a **caveats** section (motion you couldn't eyeball, deployment-target mismatch, surfaces left alone and why).
4. Note that glass motion must be checked on-device; offer `/run` or `/verify`. (Never boot the simulator yourself if the project forbids it — many do.)

### Phase 7 — Capture learnings

Append 0–3 non-obvious glass learnings to **glassify's** `LEARNINGS.md` (format below). Skip anything that restates SKILL.md or is purely project-specific (those go to the project's auto-memory). Tell the user what you captured, one line each.

```markdown
## YYYY-MM-DD — Short title

**Tags:** [api] [gating] [convention] [anti-pattern] [layout] [motion]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action.
```

## The Opportunity Catalog

The hunting checklist. Each item is a *pattern to find*, the *glass move*, and the *guardrail*.

1. **Static glass → fluid glass.** Isolated glass surfaces that appear/disappear or visually cluster but aren't inside a `GlassEffectContainer` and carry no `glassEffectID`. → Group them in one container with a shared `@Namespace`; tag each with `glassEffectID`; inserts get `.glassEffectTransition(.materialize)`, continuous surfaces get `.matchedGeometry`. *Guardrail: only cluster glass that's actually related; don't span a `Spacer` to merge unrelated controls.*
2. **Bare floating chrome.** Buttons/pills/badges floating over content on a solid fill, `Color.opacity`, or no background. → `glassSurface(in:)` (a `Circle` for icon buttons, `Capsule` for labeled). *Guardrail: needs content behind it to refract.*
3. **Pre-glass material veils.** `.ultraThinMaterial` / `.regularMaterial` backgrounds that predate Liquid Glass. → Upgrade to `glassEffect` where the surface floats over dynamic content. *Guardrail: keep material for full-bleed scrims and gesture-ramped opacity (glass can't be opacity-driven per-frame).*
4. **ScrollViews / Lists without an edge effect.** → `.scrollEdgeEffectStyle(.soft, for: .all)` so content diffuses under bars. *Guardrail: `.soft` for calm screens, `.hard` only when a crisp divider is wanted.*
5. **Toolbars with ungrouped items.** → `ToolbarSpacer` to split items into their own floating glass capsules (iOS 26 auto-glasses toolbar items). *Guardrail: group by meaning, not to decorate.*
6. **Glass elements inserted with `.move`/`.opacity`/`.scale`.** → Swap the appear animation for `.glassEffectTransition(.materialize)` inside a stable container — fewer competing transforms, the Apple-correct insert.
7. **Heavy selection fills where glass reads cleaner.** A selected row painted with a big solid block. → glass tint + a 1pt accent border + chevron. *Guardrail: if the project deliberately uses a bold solid-accent fill for THE primary selector, leave it — that's an intentional choice, not a miss.*
8. **NavigationSplitView / detail backgrounds.** → `.backgroundExtensionEffect()` so the detail's content reaches under the sidebar/inspector for the seamless iOS 26 look.
9. **Secondary `.borderedProminent` / hand-rolled capsules.** → `buttonStyle(.glass)` / `.glassProminent` for *secondary* actions. *Guardrail: the ONE hero CTA per screen stays opaque/gradient — glass would make it lose the hierarchy fight (see anti-patterns).*

## Modern API reference (iOS 26)

```swift
content.glassEffect(.regular.tint(accent).interactive(), in: shape)   // single surface

GlassEffectContainer(spacing: 10) { /* glass children */ }            // shared refraction + morph host

child.glassEffectID(id, in: namespace)                                // morph identity within a container
child.glassEffectTransition(.materialize)                             // .materialize | .matchedGeometry | .identity

scrollView.scrollEdgeEffectStyle(.soft, for: .all)                    // .automatic | .soft | .hard
detail.backgroundExtensionEffect()                                    // extend under sidebar/inspector
ToolbarSpacer(.fixed, placement: .topBarTrailing)                     // split toolbar items into glass groups
Button(…) .buttonStyle(.glass)                                        // or .glassProminent
```

All iOS 26+. Centralize the `#available` gating in the project's glass helper file — never sprinkle `if #available` at call sites. Canonical helper shape:

```swift
extension View {
    @ViewBuilder func glassSurface<S: Shape>(in shape: S, tint: Color? = nil, interactive: Bool = false) -> some View { /* glassEffect on 26, .thinMaterial fallback */ }
    @ViewBuilder func glassMorphID<ID: Hashable>(_ id: ID, in ns: Namespace.ID) -> some View { /* glassEffectID on 26, self otherwise */ }
    @ViewBuilder func glassMorphTransition(_ style: GlassMorphStyle, reduceMotion: Bool = false) -> some View { /* .identity when reduceMotion */ }
    @ViewBuilder func softScrollEdge() -> some View { /* scrollEdgeEffectStyle(.soft, .all) on 26 */ }
}
struct GlassStack<Content: View>: View { /* GlassEffectContainer on 26, VStack otherwise */ }
```

## Anti-patterns to refuse

- **The hero CTA is not glass.** On a glassy screen the primary action must be a bold, opaque accent/gradient capsule so it wins the hierarchy. Glass frames the *path* to the CTA, not the CTA.
- **Glass over a flat `systemBackground` is wasted.** With nothing behind it to refract, glass reads as plain material. *Flag* it, but don't force glass there — either give it a backdrop (only if the screen wants one) or leave plain material. Never re-introduce an ambient/mesh background to a screen that was deliberately quieted.
- **Don't loudens a deliberately-quiet tier without asking.** A retiered/calm Settings (or similar) is a hard constraint — confirm before adding glass there, and keep it whisper-quiet (a soft scroll edge, not glass chips with halos).
- **Don't paint glass with the accent everywhere.** Accent tint on glass marks the one selected state, not every surface.
- **Don't break `matchedGeometry` / `matchedHero` tags** when wrapping a view in a container.
- **Don't trust the user-stated deployment target** — read the target-level pbxproj value, and confirm the SDK compiles glass at all.
- **Don't reduce-motion the morphs away silently.** Gate them to `.identity`; symbol pulses on focal elements can stay.

## What the deliverable looks like

1. A short read of the app's current glass maturity.
2. A ranked findings table the user trims.
3. Helper-file additions (gated), then targeted edits to the approved surfaces — data/state/layout intact, hero tags intact.
4. A green `xcodebuild`.
5. A change-set table + caveats + on-device check suggestion.
