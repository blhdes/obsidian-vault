---
title: Vigilia
date: 2026-06-25
tags: [project, ios, swift, swiftui, vigilia, design]
status: concept locked
---

# 🕯️ Vigilia

The founding record of a new iOS app, working title **Vigilia**. These notes were migrated from the original design conversation, which no longer exists. They are the only memory of it. For that reason they are written to preserve **reasoning, not just conclusions** — when I come back weeks from now, the *why* under each decision is what will stop me from quietly undoing a good choice by accident.

If a later idea contradicts something here, that is allowed, but it should be a decision made on purpose, against the reasoning, not a drift.

## What it is

An iOS app, Swift / SwiftUI, that turns a loving-kindness meditation (**Metta Bhavana**) into a single digital ritual. The guiding premise is *"love your enemy as you love yourself."*

You open the app and bring to mind someone who has recently hurt you: a betrayal, an insult, a disrespect. The entire purpose is then to **turn toward wishing that person well** — praying for them, picturing them bathed in light, bringing positive energy to that person and that situation. The app does not help you vent, analyze, or record the grievance. It helps you make the turn from the wound to the well-wishing, once, and then let it go.

## The spirit: a frame, not a journal

Vigilia is a **frame, not a journal**. It is minimalist on purpose. It holds no content of yours over time and gives you nothing to scroll back through. Its only job is to **hold a space well enough that you want to return to it**. Every design decision in these notes is ultimately in service of that one sentence: does this make the space more worth returning to, or less.

## The one feature that everything else protects

When you finish, you "send" the note and it **disappears from the device forever**. Local-only, ephemeral, no persistence, no backend, no accounts, no sync.

This is the crux of the whole app, and it is easy to mistake for a missing feature, so it has its own note. Not saving is **the feature**, not a limitation being hidden. And the disappearance is framed as **transmutation / ascension**, deliberately not as deletion. Full reasoning in [[ephemerality-and-transmutation|Ephemerality & transmutation]]. That distinction is load-bearing and is meant to survive into every later design choice.

## The map

The substance lives in four notes. Read them in this order:

1. **[[ephemerality-and-transmutation|Ephemerality & transmutation]]** — the defining feature, and why disappearance is an offering rather than an erasure.
2. **[[interaction-flow|The interaction flow]]** — the single session, beat by beat, with the reasoning under each beat: welcome seed → naming the wound → the swipe that locks it → the loving-kindness seed → the well-wishing → the ascension → the void.
3. **[[aesthetic-direction|The aesthetic direction]]** — "Vigilia" the look and feel: a darkened chapel lit by one candle. Light, colour, typography, the sacred suggested-not-named, and motion.
4. **[[open-questions|Scope & open questions]]** — what is in v1, what was deferred, and the decisions still to settle before or during the build.

## On the name

**Vigilia** is doing double duty right now: it is both the working product name *and* the name of the aesthetic direction (the chapel-and-candle feeling, see [[aesthetic-direction|the aesthetic note]]). It is undecided whether the shipped product keeps this name. The aesthetic direction keeps the name regardless; the product name is an [[open-questions|open question]].

## Status

**Concept locked.** Next step is the SwiftUI scaffolding. Technically the app is small by design: local-only, no backend, a single writing surface and a handful of animated states. The hard part was never the engineering; it is protecting the atmosphere, which is what these notes exist to do.
