---
title: Scope & open questions
date: 2026-06-25
tags: [vigilia, scope, open-questions]
---

# Scope & open questions

What is settled about scope for [[Vigilia|Vigilia]], and what is deliberately left open to decide before or during the build. Update this note as things get resolved (and record *why*, the same way the rest of these notes do).

## Scope: v1 is text only

**v1 is text only.** Voice notes were considered and **explicitly deferred to a second iteration.** The reasoning: voice adds **real complexity** (microphone permissions, recording, handling audio) for **dubious benefit in a first build.** It can come later **if the app catches on**. This is a deferral with a rationale, not a rejection — revisit it once v1 exists and is worth extending, not before.

## Open questions to settle

These are unresolved on purpose. None of them should be answered by default or by accident; each deserves a real decision.

- **The final product name.** Keep **"Vigilia"** for the shipped product, or not? Note that "Vigilia" stays as the name of the [[aesthetic-direction|aesthetic direction]] regardless; this question is only about the product.
- **The seed-phrase wording (finalize).** The banks now exist, restructured into [[four-registers|four registers]] and **drafted** in `Seeds.swift`, but the wording is not final — it still needs curating. Both the welcome lines and the loving-kindness turns must stay in that **quasi-liturgical cadence that never names a tradition** — see the sacred-suggested-not-named section of [[aesthetic-direction|the aesthetic direction]]. This is content writing, and it is as load-bearing as any code.
- **The exact colour and luminosity values.** The precise **warm hue of the black**, plus the **text luminosity values in its two states** (active / full glow vs. dimmed / receded). See the light-and-colour section of [[aesthetic-direction|the aesthetic direction]].

## Resolved (2026-06-26)

Settled on contact with a running build:

- **Minimum iOS version → iOS 18.0.** Needed for the ascension's `TextRenderer` (per-glyph text effects, iOS 18+) and the modern SwiftUI niceties, and it matches the floor of the user's other apps.
- **Ascension technique → a per-glyph dissolve** (not a particle system). Each letter lifts, drifts, blurs, and fades on a staggered schedule, via `TextRenderer`. Chosen because it is the literal realization of *"the words themselves come apart into light"*; a particle system risked the confetti failure mode the design forbids. Reduce Motion turns it into a quiet fade. See [[interaction-flow|the build revisions]].
- **The prompts → [[four-registers|four matched registers]]**, drawn coherently. The seed *structure* is settled; the *wording* is drafted but not final (above).

## Status

**Built and iterating on device.** The scaffold is well past done and the full flow runs. What is left is tuning against the phone — the colour and luminosity values and the final seed wording — plus the product-name decision. Nothing structural is blocking.

Related: [[Vigilia|Vigilia]] · [[interaction-flow|The interaction flow]] · [[aesthetic-direction|The aesthetic direction]] · [[ephemerality-and-transmutation|Ephemerality & transmutation]]
