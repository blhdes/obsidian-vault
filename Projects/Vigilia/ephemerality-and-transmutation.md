---
title: Ephemerality & transmutation
date: 2026-06-25
tags: [vigilia, design, concept, ephemerality]
---

# Ephemerality & transmutation

This is the defining feature of [[Vigilia|Vigilia]] and the one most likely to be misread as something missing. It is worth stating its reasoning carefully, because nearly everything else in the app exists to support it.

## The behaviour

When you finish, you "send" the note and it **disappears from the device forever**. The app is **local-only and ephemeral**: no persistence, no backend, no accounts, no sync. Nothing you write is ever stored, transmitted, or recoverable. There is no history to return to, because there is no history.

## Not saving is the feature, not a limitation

The instinct, when an app keeps nothing, is to read it as a technical shortcoming that is being politely hidden. Here it is the opposite. **Not saving is the entire point.**

- A thing you can re-read is a thing you **accumulate**. Accumulation invites you back to the grievance, to re-read it, to keep the wound warm. That is the **habit of a diary**.
- A thing that vanishes the moment you finish is a thing you **let go of**. The act is complete when it disappears. That is a **release**, not a record.

So the absence of storage is what separates this app from journaling. It makes the app an act of letting go rather than a place to keep score. A pleasant side effect: it also keeps the whole thing **radically simple to build** — no database, no server, no auth, no sync conflicts. But the simplicity is the bonus, not the reason. The reason is what ephemerality does to the user, not to the codebase.

## The metaphor: transmutation / ascension, never deletion

How the disappearance is *experienced* matters as much as that it happens. The committed metaphor is **transmutation / ascension**, and it is deliberately **not deletion or erasure**.

- **Erasing reads as repression.** Something is wiped, struck out, made to never have happened. That is the gesture of pushing a feeling down and pretending it is gone.
- **Ascending reads as offering.** What you wrote, charged with feeling, **turns to light and rises**. It is not destroyed; it is given up and away.

These produce opposite emotional aftertastes from the same underlying "the note is gone." One leaves you having suppressed something; the other leaves you having released it. Vigilia is built entirely on the second.

> **Design law:** this distinction must survive into every later choice. Anything that reads as deleting, wiping, crossing-out, shredding, or trashing is wrong, no matter how technically convenient. The note must always *rise and dissolve*, never *get erased*.

## Where this shows up downstream

This is not an isolated feature; it is the principle two other decisions are built on:

- The closing animation is an **ascension**, words coming apart into light and rising, explicitly not a wipe — see [[interaction-flow|the interaction flow]] (the release / ascension beat).
- The whole visual language, **light that emerges from the text**, is what makes "turning to light and rising" legible at all — see [[aesthetic-direction|the aesthetic direction]].

Related: [[Vigilia|Vigilia]] · [[interaction-flow|The interaction flow]] · [[aesthetic-direction|The aesthetic direction]]
