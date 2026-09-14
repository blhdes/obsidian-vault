---
title: Vigilia
date: 2026-06-25
tags: [project, ios, swift, swiftui, vigilia, design]
status: building
---

# 🕯️ Vigilia

The founding record of a new iOS app, working title **Vigilia**. These notes were migrated from the original design conversation, which no longer exists. They are the only memory of it. For that reason they are written to preserve **reasoning, not just conclusions** — when I come back weeks from now, the *why* under each decision is what will stop me from quietly undoing a good choice by accident.

If a later idea contradicts something here, that is allowed, but it should be a decision made on purpose, against the reasoning, not a drift.

## What it is

An iOS app, Swift / SwiftUI, that turns a loving-kindness meditation (**Metta Bhavana**) into a single digital ritual. You bring to mind something that weighs on you, name it, and then **turn toward wishing it well** — and then let it go. The app does not help you vent, analyze, or record the grievance; it helps you make the turn from the wound to the well-wishing, once.

The original premise was the hardest case, *"love your enemy as you love yourself"*: bring to mind someone who has recently hurt you, and turn toward wishing *them* well. That case is still the sharpest one the app offers, but it is no longer the only one. The app now holds space for **four registers** of grief — a person who hurt you, a way you have hurt yourself, a shared situation, or a loss with no one to blame. Full reasoning in [[four-registers|The four registers of grief]]; the short version is that grief is not only caused by others, and an enemy-only app would sit unused on the many nights you are simply grieving.

## The spirit: a frame, not a journal

Vigilia is a **frame, not a journal**. It is minimalist on purpose. It holds no content of yours over time and gives you nothing to scroll back through. Its only job is to **hold a space well enough that you want to return to it**. Every design decision in these notes is ultimately in service of that one sentence: does this make the space more worth returning to, or less.

## The one feature that everything else protects

When you finish, you "send" the note and it **disappears from the device forever**. Local-only, ephemeral, no persistence, no backend, no accounts, no sync.

This is the crux of the whole app, and it is easy to mistake for a missing feature, so it has its own note. Not saving is **the feature**, not a limitation being hidden. And the disappearance is framed as **transmutation / ascension**, deliberately not as deletion. Full reasoning in [[ephemerality-and-transmutation|Ephemerality & transmutation]]. That distinction is load-bearing and is meant to survive into every later design choice.

## The map

The substance lives in five notes. Read them in this order:

1. **[[ephemerality-and-transmutation|Ephemerality & transmutation]]** — the defining feature, and why disappearance is an offering rather than an erasure.
2. **[[four-registers|The four registers of grief]]** — how the app widened from enemy-only to four kinds of grief (a person, yourself, a situation, a formless loss), and why.
3. **[[interaction-flow|The interaction flow]]** — the single session, beat by beat, with the reasoning under each beat: welcome seed → naming the wound → the gesture that locks it → the loving-kindness seed → the well-wishing → the ascension → the void. (Includes the build revisions, where several mechanisms changed on contact with a real device.)
4. **[[aesthetic-direction|The aesthetic direction]]** — "Vigilia" the look and feel: a darkened chapel lit by one candle. Light, colour, typography, the sacred suggested-not-named, and motion.
5. **[[open-questions|Scope & open questions]]** — what is in v1, what was deferred, and the decisions still to settle (and the ones now resolved).

## On the name

**Vigilia** is doing double duty right now: it is both the working product name *and* the name of the aesthetic direction (the chapel-and-candle feeling, see [[aesthetic-direction|the aesthetic note]]). It is undecided whether the shipped product keeps this name. The aesthetic direction keeps the name regardless; the product name is an [[open-questions|open question]].

## Status

**Built and working on device, dormant since 2026-06-26.** The full flow runs end to end — name, seal, wish, ascend, void — and that hasn't changed: `git log` shows no commits past 2026-06-26 (`84e2cdc`, the per-glyph ascension animation), and the working tree is clean, so nothing has drifted from what's described here — the project has simply sat untouched for about 2.5 months (checked 2026-09-14), not actively iterating despite the framing below. The code lives at `/Users/agomezu/Claude/vigilia/` and is pushed public to **github.com/blhdes/vigilia**. Several decisions evolved once it was running on a real phone (the seal gesture, how the welcome line leaves, the ascension technique); those revisions and their reasoning are recorded at the foot of [[interaction-flow|the interaction flow]], and the open items — still open, none resolved since — are in [[open-questions|scope & open questions]].

Technically the app is small by design: local-only, no backend, a single writing surface and a handful of animated states. The hard part was never the engineering; it is protecting the atmosphere, which is what these notes exist to do.
