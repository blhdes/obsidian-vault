---
title: The aesthetic direction
date: 2026-06-25
tags: [vigilia, design, aesthetic, typography, motion]
---

# The aesthetic direction — "Vigilia"

The look and feel of [[Vigilia|the app]] has its own name, **Vigilia**, and its own governing image: **a darkened chapel where the only thing present is a single candle — and that candle is the user, writing.** Everything below is downstream of that one picture. When a future visual decision is unclear, return to the image and ask which choice serves it.

## The three foundational choices

The whole direction rests on three choices that were made first. Everything else is a consequence of these, so they should be touched last and most carefully:

1. **Near-total darkness, with light that emerges** (rather than light that is simply switched on).
2. **Apple's system typography** (rather than a custom or licensed face).
3. **The sacred felt as *suggested, never named*** (rather than depicted, or absent).

## Light and colour

The black is **deep but not flat**. It carries a **minimal warmth**: an almost imperceptible **blue-violet underneath**, rather than a cold neutral gray. It should feel like the inside of a dark room at night, not like a switched-off screen.

The text is **not pure white**. It is a **faint, warm-bone light, like luminous ink** — as if the letters themselves were glowing rather than being printed in white.

The governing principle of the entire app:

> **The light emerges from the text, not from an illuminated background.** The user's words are the only thing glowing in the dark.

This single principle pays for a lot. It is *why* the dimming of the locked wound works dramatically **for free** (see [[interaction-flow|the interaction flow]]): when the wound is locked, it literally **lowers its own light and recedes** into the dark, while the well-wishing written below it **burns at full glow.** No special effect is needed for the contrast — **the darkness does the dramatic work** on its own. Light-as-text is also what makes the ascension legible: text made of light can *become* light and rise (see [[ephemerality-and-transmutation|Ephemerality & transmutation]]).

The precise warm hue of the black, and the exact luminosity values of the text in its two states (active vs. dimmed), are still to be set — see [[open-questions|open questions]].

## Typography — New York

The typeface is **New York, Apple's system serif.** It was chosen for a specific reason: it is described as a face that works as a **traditional reading face at small sizes** *and* as a **graphic display face at large sizes**. That dual role is exactly what this app needs from a single family.

Being a system font, it is also practically clean: **no embedding, no external licensing**, and it is available in SwiftUI through the **`.serif` font design**.

It is used in **two registers**, and the relationship between them carries meaning:

- **New York display, light weight, generous size, wide leading** — for the **seed phrases**, so they **breathe like verses**.
- **New York regular, at reading size** — for the **user's own text**.

The seeds are kept **thinner or fainter than the user's text**. The rule behind this:

> **The app whispers; the user speaks.** The user's voice must carry more weight than the invitation.

The interface is the quieter presence in every pairing. The person is always the louder one on the page.

## The sacred, suggested not named

This is the **subtle, load-bearing choice**, and the easiest to violate by accident. There is **no religious iconography anywhere** — no crosses, no incense, no symbols of any tradition.

Instead the ritual is allowed to filter through only **three invisible channels**:

1. **Rhythm** — the pauses, the breaths, the deliberate slowness of every transition.
2. **The quasi-liturgical cadence of the seed-phrase language** — prayer-shaped sentences that **never cite a tradition**. (Writing these banks is an [[open-questions|open task]].)
3. **The quality of the light** — the candle penumbra described above.

The test of whether this is working:

> **A believer feels the echo of prayer; a secular user feels only a deep calm. Neither one ever sees a symbol that expels them.**

That is the entire meaning of *"it's intuited, not named."* The sacredness is in the rhythm, the cadence, and the light — never in a depicted thing. The moment a recognizable symbol appears, half the audience is shut out and the spell breaks.

## Motion

Everything moves **slowly, at the tempo of a breath, not of a UI animation.** Nothing bounces. Nothing is "snappy." This is **not an app that responds fast; it is an app that holds a space.**

> Test every future animation or transition against that sentence: *does it hold the space, or does it react quickly?* If it feels responsive, it is wrong here.

Related: [[Vigilia|Vigilia]] · [[interaction-flow|The interaction flow]] · [[ephemerality-and-transmutation|Ephemerality & transmutation]] · [[open-questions|Scope & open questions]]
