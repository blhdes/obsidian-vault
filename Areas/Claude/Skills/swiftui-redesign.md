---
title: swiftui-redesign skill
date: 2026-05-22
tags: [claude, skill, swift, swiftui, design, ui]
---

# ✨ `swiftui-redesign` skill

A repeatable playbook for redesigning a SwiftUI screen using current Apple APIs (iOS 18 / 26 era) — Liquid Glass surfaces, MeshGradients, `symbolEffect`, `contentTransition`, ambient motion. The end product is a bolder, more cohesive view without breaking any data flow, sheets, or hero animations the existing screen depends on.

The outward counterpart to [[swift-refine]] — which goes *inward* (work-per-frame, races, dead branches). This one goes *outward* (visuals, motion, expressive surfaces).

## Where it lives

```
~/.claude/skills/swiftui-redesign/SKILL.md
```

## How to invoke

**Explicit invocation only** — Claude won't fire this automatically. Use one of:

- Type the command: `/swiftui-redesign`
- Name it: *"use the swiftui-redesign skill on `OnboardingView`"*
- Use trigger verbs that match the description: *"rethink this view"*, *"redesign this screen"*, *"modernize this"*

## The enforced flow

Same plan-then-implement discipline as [[swift-refine]]:

1. **Read** — target view + supporting types
2. **Critique** — what's visually flat, dated, or under-using modern APIs
3. **Propose** — concrete design moves with trade-offs (no code yet)
4. **Wait for green light** — user approves or redirects each item
5. **Implement + verify** — applies approved changes, builds, reports

## Hard guarantee: data/state logic is byte-identical

The skill only touches **how things look**, not how state flows. Sheets, `@Observable` chains, `Binding`s, hero animations, navigation paths — all preserved exactly. The risk of breaking app logic during a redesign is zero by design.

## What it pulls from

- **Liquid Glass** — `.glassEffect()`, layered translucency, ambient depth
- **MeshGradient** — non-flat backgrounds, color-of-the-week-style palettes
- **`symbolEffect`** — animated SF Symbols (bounce, pulse, variableColor)
- **`contentTransition`** — number flips, identity transitions
- **`scrollTransition`** — content-aware scroll effects
- **Custom shapes & materials** — replacing flat `Color()` fills with depth

## When NOT to use it

- You want **performance/correctness** changes → use [[swift-refine]] instead.
- You want a *new* view from scratch → just ask Claude directly; this skill rethinks existing screens.
- You want a marketing/landing page → use the `frontend-design` plugin skill instead (it's web-focused).

## Working with it

The user "almost certainly hasn't given full requirements" — the skill expects you to be opinionated. Claude's job is to **diagnose, propose, and execute**, not to ask "what would you like changed?" in phase 2. So phrase your invocation as a target, not as a question:

- ✅ *"redesign LibraryView"*
- ✅ *"modernize the onboarding flow"*
- ❌ *"what could we do to improve LibraryView?"* (this gets a generic answer, not the skill's full critique)

## Backup

`SKILL.md` + `LEARNINGS.md` are mirrored at [[backup/README|Areas/Claude/Skills/backup/swiftui-redesign/]], last synced **2026-09-14**. Re-copy them there after any real change to this skill.

## Related notes

- [[swift-refine]] — the inward counterpart
- [[_index]] — Claude skills index
- [[Resources/Swift/Swift]]
- [[Projects/Culla/Culla]]
