---
title: glassify skill
date: 2026-09-14
tags: [claude, skill, swift, swiftui, liquid-glass, ui]
---

# 🪟 `glassify` skill

A focused counterpart to [[swiftui-redesign]]. Where that skill rethinks a whole screen, `/glassify` does one thing: find every place a SwiftUI app could adopt or upgrade to iOS 26 Liquid Glass, rank them, and (after approval) apply them — without loudening the design or touching data/state logic.

The bar is **taste, not coverage** — a good run adds 4 surgical glass moves the user didn't know were possible; a bad one paints glass on everything and loses the brand.

## Where it lives

```
~/.claude/skills/glassify/SKILL.md
~/.claude/skills/glassify/LEARNINGS.md   ← append-only log of glass-specific patterns/traps
```

## How to invoke

**Explicit invocation only** — Claude won't fire this automatically. Use one of:

- Type the command: `/glassify` (whole-app sweep) or `/glassify HomeView.swift` (focus one screen)
- Ask to "find liquid glass opportunities", "make it more glassy / more Apple", "modernize the glass", "audit for Liquid Glass"

## The enforced flow

1. **Load prior learnings** — this skill's own `LEARNINGS.md` plus `[api]`/`[gating]`/`[convention]` entries from [[swift-refine]]'s and [[swiftui-redesign]]'s sibling files; a learning wins over the skill file if they conflict.
2. **Map the surface** — checks the actual compile floor (`IPHONEOS_DEPLOYMENT_TARGET` + installed SDK version) since the iOS 26 glass branch only compiles on SDK ≥ 26; finds the project's existing glass helper (extend it, never reinvent gating inline); checks recent git log / memory for restraint conventions.
3. **Find the opportunities** — walks an "Opportunity Catalog" against every floating control, chrome button, card, sheet, toolbar, and selection state; records location, current state, proposed move, exact API, why it earns its place, and a restraint check. Discards anything that fails the restraint check.
4. **Propose → wait for green light → implement → verify** — same discipline as [[swift-refine]]/[[swiftui-redesign]]: no code until the user approves the list.
5. **Append 0–3 non-obvious learnings** to its own `LEARNINGS.md` at the end — trivial restatements don't earn an entry.

## When NOT to use it

- A full visual rethink of a screen (layout, copy, data flow) → use [[swiftui-redesign]] instead.
- Performance/correctness work → use [[swift-refine]] instead.
- The project's SDK is below iOS 26 → the skill self-degrades to `.ultraThinMaterial`/`.regularMaterial` suggestions and says so; don't force `glassEffect` calls that won't compile.

## Backup

`SKILL.md` + `LEARNINGS.md` are mirrored at [[../backup/README|Areas/Claude/Skills/backup/glassify/]], last synced **2026-09-14**. Re-copy them there after any real change to this skill.

## Related notes

- [[swiftui-redesign]] — the whole-screen redesign counterpart
- [[swift-refine]] — the inward (performance/correctness) counterpart
- [[../_index|_index]] — Claude skills index
- [[Resources/Swift/Swift]]
