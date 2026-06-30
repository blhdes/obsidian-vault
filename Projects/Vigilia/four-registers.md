---
title: The four registers of grief
date: 2026-06-26
tags: [vigilia, design, concept, registers]
---

# The four registers of grief

A foundational widening of the concept, decided 2026-06-26. The app was born enemy-only: *"love your enemy as you love yourself,"* bring to mind the person who hurt you, wish *them* well. It now holds space for **four registers** of grief, not one:

1. **A person** — another who wronged you. (The original "enemy" case.) The "who" is *them*.
2. **Yourself** — regret, shame, the harm you caused. The "who" is *yourself*.
3. **A shared situation** — a rift, a conflict, more than one caught in it. The "who" is *all of you*.
4. **A formless loss** — grief with no one to blame: illness, circumstance, a death no one chose. The "who" is *it, and you in it*.

## Why widen it

This is not scope creep; it is the app becoming more itself. Three reasons, in order of weight:

- **It serves the one locked goal.** The whole app exists to [[Vigilia|hold a space you want to return to]]. An app that only works when you are angry at a specific person sits unused on the *many* nights you are not angry at anyone, only grieving. Breadth is what makes it worth returning to.
- **It is the truer shape of the practice.** Metta Bhavana traditionally moves through stages — kindness for yourself, for a loved one, for a neutral person, for a difficult person, for everyone. The enemy is the *apex*, the hardest stage, but it is one stage. The original app captured only the apex; the registers restore the rest.
- **The hardest case is not lost.** Blessing the one who hurt you is still the sharpest door the app offers. It is now one door among several, not the only one.

The cost we accepted, and the guard against it: breadth can blur a sharp, distinctive app ("the one for blessing your enemy") into a vague "process any feeling" app. The guard is to keep **each register sharp** rather than flattening everything into one set of open, generic lines. A self-directed prompt should sound nothing like a formless-loss prompt.

## How a session lands in the right register, without a selector

The obvious way to support four kinds of grief is to ask the user to pick one at the start. That was **rejected**: a "choose a category" step is exactly the visible machinery the app refuses (see [[interaction-flow|why it isn't a wizard]]). The structure must stay in the language, not in screens.

The resolution: **matched register pairs, drawn at random.** Each time the app opens, it draws *one* register, then shows a welcome line **and** its loving-kindness turn from **that same register**. The two always cohere — you are never asked to "wish *them* well" about a grief that has no "them." The user simply meets a different doorway each time and brings their night to it. Within a register, any welcome pairs with any turn, so each register keeps a single consistent "who."

## Status

Implemented in `Seeds.swift` as register-grouped banks (`Seeds.draw()` returns a coherent welcome+turn pair); `RitualModel` draws a fresh pair each launch and each new vigil. The **wording is drafted, not final** — curating it is still on [[open-questions|the open list]]. The README reflects the widened concept.

Related: [[Vigilia|Vigilia]] · [[interaction-flow|The interaction flow]] · [[open-questions|Scope & open questions]] · [[aesthetic-direction|The aesthetic direction]]
