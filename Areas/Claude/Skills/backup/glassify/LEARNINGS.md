# Glassify — Learnings

Append-only log of Liquid Glass patterns, traps, and API quirks discovered while running `/glassify`. Read at the start of each invocation as additional rules. **Also scan `../swiftui-redesign/LEARNINGS.md` for `[api]`/`[gating]`/`[convention]` glass entries** — this skill inherits that corpus. Append 0–3 new entries here at the end of a run. Be concrete or stay quiet.

Format:

```markdown
## YYYY-MM-DD — Short title

**Tags:** [api] [gating] [convention] [anti-pattern] [layout] [motion]
**Context:** What the situation was (1-2 sentences).
**Lesson:** The rule going forward (1-3 sentences). Lead with the action.
```

---

## 2026-06-01 — `#available` is runtime-only; verify the installed SDK compiles iOS 26 glass first

**Tags:** [gating] [api] [anti-pattern]
**Context:** Before writing a `glassSurface` helper on an iOS 18 floor, checked `xcrun --sdk iphonesimulator --show-sdk-version`. SDK 26.2, so the gated `glassEffect`/`Glass` code compiles. Had the SDK been < 26, that branch would have failed to compile *even behind* `if #available(iOS 26.0, *)`.
**Lesson:** `if #available` is a runtime guard — it does NOT exempt code from compiling against the active SDK. Before committing to any iOS 26 glass branch, run `xcrun --sdk iphonesimulator --show-sdk-version`. If ≥ 26, write the gated helper; if < 26, skip the glass branch entirely and propose `.ultraThinMaterial`/`.regularMaterial` instead.

## 2026-05-20 — Centralize Liquid Glass gating in one helper, never inline

**Tags:** [convention] [gating]
**Context:** A redesign needed glass at ~8 sites and would have scattered `if #available(iOS 26, *)` blocks if applied inline.
**Lesson:** Add (or reuse) a single `glassSurface(in:tint:interactive:)` + `GlassStack` helper before glassifying. Every call site becomes a one-liner and OS gating lives in one file. Delete any narrower predecessor the same pass — leaving both creates "which do I use here" decisions.

## 2026-06-02 — A glassEffectID shape-morph needs two MUTUALLY-EXCLUSIVE states; coexisting elements get materialize instead

**Tags:** [api] [anti-pattern]
**Context:** Wanted to morph a mode-tile cluster *into* a source pill, but the tiles show when `source == nil` and the pill shows whenever `mode == .library` — so when no source is picked, **both are on screen at once**. A shared `glassEffectID` shape-morph between them is semantically wrong: there's no single glass shape traveling from A to B.
**Lesson:** Before wiring a `glassEffectID` shape-morph between elements A and B, confirm they're genuinely mutually-exclusive render states (one replaces the other). If they coexist before the transition, deliver the *coordinated* version instead: each gets its own id in a shared `GlassEffectContainer`, the leaving cluster `.materialize`s out while the arriving chips `.materialize` in. Same liquid read, correct semantics.

## 2026-06-02 — For `.materialize`, the GlassEffectContainer must live OUTSIDE the `if`, not inside it

**Tags:** [api] [gating] [layout]
**Context:** Making a chip crystallize in/out via `.glassEffectTransition(.materialize)`. First instinct was to wrap the glass in its container at the same place it's conditionally created.
**Lesson:** A glass child only *materializes* if its `GlassEffectContainer` is a **stable parent** that outlives the child's appear/disappear. Put the container OUTSIDE the `if` (e.g. `.overlay { GlassStack { conditionalChip } }`). Container inside the `if` = container and child appear together = no materialize, just a plain insert. Corollary: a VStack-based `GlassStack { singleChild }` (even wrapping one `ZStack`) is a zero-layout-cost way to give an ad-hoc glass element the container `.materialize` requires.

## 2026-06-03 — In a mature glass app, glassify's job shifts from ADD to PROPAGATE; the best find is often a discontinuity fix

**Tags:** [convention] [anti-pattern]
**Context:** Swept a glass-mature app (nearly every surface already glassed; 3 main screens already fluid). The temptation was to manufacture net-new glass on the carousel and sheets. But the carousel's backdrop is deliberately flat (glass would be wasted), the busiest sheet deliberately avoids surfaces, and auth/empty/new-playlist were already mature. The single highest-value finding was that a *prior* commit gave the Settings screen `softScrollEdge()` but its presented sheets didn't get it — a visual discontinuity at the present boundary.
**Lesson:** When glassify runs on a mature app, expect to REFUSE most of the catalog and surface only a few hits — and weight them toward *propagation/consistency fixes* (a sheet that doesn't match the scroll-edge/glass treatment its parent recently gained) over net-new glass. After any prior glass change to a screen, grep its `.sheet`/`.fullScreenCover` destinations and check they carry the same edge-effect/vocabulary; a lone soft scroll edge on the parent is an unfinished change, not a finished one. "Few findings, mostly fixes" is the correct shape of a mature-app sweep, not a failed one.

## 2026-05-29 — Gesture-ramped material opacity is NOT replaceable with a glass helper

**Tags:** [api] [anti-pattern] [motion]
**Context:** Nearly swapped a `Rectangle().fill(.ultraThinMaterial).opacity(dragProgress)` for `glassSurface(in:)` during a glass pass. The explicit Rectangle exists so its opacity binds to the drag value — that's what fades the surface *with* the gesture.
**Lesson:** When a material/glass surface needs to ramp with a gesture or any continuous binding, keep the explicit `Rectangle().fill(.material).opacity(binding)` pattern. `glassSurface()` applies the material to the view but you lose independent opacity control — replacing it silently regresses the drag feel (no compile error, just worse).
