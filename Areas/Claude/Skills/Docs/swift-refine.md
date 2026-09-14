---
title: swift-refine skill
date: 2026-05-22
tags: [claude, skill, swift, swiftui, refactor, performance]
---

# 🔧 `swift-refine` skill

A repeatable playbook for tightening a Swift/SwiftUI file from the **inside** — hot paths, allocations, redraws, gesture/animation smoothness, concurrency, state-machine clarity, lurking bugs. Output is a faster, less surprising implementation with byte-identical user-visible behavior (unless a bug fix demands a deliberate change, which gets called out).

The internal counterpart to [[swiftui-redesign]] — which goes *outward* (visuals, motion, expressive surfaces). This one goes *inward*.

## Where it lives

```
~/.claude/skills/swift-refine/SKILL.md
```

## How to invoke

**Explicit invocation only** — Claude won't fire this automatically. Use one of:

- Type the command: `/swift-refine`
- Name it: *"use the swift-refine skill on `LibraryView.swift`"*
- Use trigger verbs that match the description: *"tighten this view"*, *"optimize this"*, *"smooth out the scroll"*, *"refactor this"*, *"audit this for performance"*

## The enforced flow

The skill is strict about plan-then-implement. Five phases:

1. **Read** — pulls the target file (and a few callers/siblings if needed) into context.
2. **Critique** — lists what's wrong: redundant work-per-frame, allocations in body, missing `@Observable` boundaries, race conditions, dead branches.
3. **Propose** — concrete changes with trade-offs. Doesn't touch the file yet.
4. **Wait for green light** — user approves, redirects, or rejects each item.
5. **Implement + verify** — applies the approved changes, runs the build, reports results.

This is deliberate: catches misalignment before code changes, so you don't end up reverting half a diff.

## What it audits

- **Work per frame** — anything heavy inside `body`, computed properties hit on every layout
- **Allocations** — closure captures, value-type churn, string formatting in hot paths
- **Redraws** — missing `@Observable`, over-broad bindings, `id(_:)` misuse
- **Gestures & animations** — `withAnimation` boundaries, transaction propagation, gesture predicates
- **Concurrency** — actor hops, `MainActor` correctness, `Task` lifetime, `AsyncSequence` consumption
- **State machines** — implicit states, untested branches, race-prone enum cases
- **Lurking bugs** — dead code, `// TODO:` rot, force-unwraps, `[weak self]` correctness

## When NOT to use it

- You want **visual** changes → use [[swiftui-redesign]] instead.
- You want a quick edit, not an audit → just ask Claude directly without invoking the skill.
- You haven't written the code yet — this skill refines, it doesn't draft.

## Backup

`SKILL.md` + `LEARNINGS.md` are mirrored at [[../backup/README|Areas/Claude/Skills/backup/swift-refine/]], last synced **2026-09-14**. Re-copy them there after any real change to this skill.

## Related notes

- [[swiftui-redesign]] — the outward counterpart
- [[../_index|_index]] — Claude skills index
- [[Resources/Swift/Swift]]
