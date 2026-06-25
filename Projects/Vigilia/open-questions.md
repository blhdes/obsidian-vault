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
- **The two seed-phrase banks.** Write the actual bank of **welcome seeds** (the changing opening line) and the bank of **second / loving-kindness seeds** (the "now wish them something good" beat). Both must be in that **quasi-liturgical cadence that never names a tradition** — see the sacred-suggested-not-named section of [[aesthetic-direction|the aesthetic direction]]. This is content writing, and it is as load-bearing as any code.
- **The minimum iOS version.** Not yet chosen.
- **The ascension animation technique.** Two candidate approaches for the closing transmutation (see [[interaction-flow|the interaction flow]], the release beat): a **particle system**, or **dissolving the actual glyphs** of the text. To be decided — likely a build-time experiment, judged against whether it reads as *rising and offering* rather than *dispersing decoratively*.
- **The exact colour and luminosity values.** The precise **warm hue of the black**, plus the **text luminosity values in its two states** (active / full glow vs. dimmed / receded). See the light-and-colour section of [[aesthetic-direction|the aesthetic direction]].

## Status

**Concept locked.** Next step: SwiftUI scaffolding. The open questions above do not block starting the scaffold; most of them (colour values, animation technique, seed copy) are best resolved *against a running build* rather than on paper.

Related: [[Vigilia|Vigilia]] · [[interaction-flow|The interaction flow]] · [[aesthetic-direction|The aesthetic direction]] · [[ephemerality-and-transmutation|Ephemerality & transmutation]]
