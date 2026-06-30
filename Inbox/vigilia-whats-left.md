---
title: Vigilia — what's left (pick up next session)
date: 2026-06-26
tags: [vigilia, inbox, status, todo]
---

# Vigilia — what's left

Quick capture to pick up next session. **The app is feature-complete**: the full ritual runs end to end on device (name → seal → wish → ascend → void). Code at `/Users/agomezu/Claude/vigilia/`, pushed to **github.com/blhdes/vigilia** (last commit `84e2cdc`). Full design record in [[Projects/Vigilia/Vigilia|Projects/Vigilia/]].

## Next step (do this first)

A **feel pass on device**: run the current build and judge how the **per-glyph ascension** and the **fixed bottom handle + dimming glass** actually land. Report back "slower / higher / more scattered / handle too cramped / glass too bright" and we tune. Nothing else is judged well until this is felt.

## What's left, in four buckets

1. **Feel (on device, by eye):**
   - Curate the **seed wording** (drafted across the four registers, not final).
   - The **colour & light values** (warm black; text glow in its two states).
   - The **ascension + handle feel** (duration, rise, stagger, glass prominence).

2. **Two engineering gaps (buildable without watching):**
   - **Long entries:** scroll-to-caret so the bottom fade never hides the line being typed.
   - **Accessibility:** VoiceOver can't seal (handle gesture is the only path); text doesn't scale with Dynamic Type. (Reduce Motion is done.)

3. **One decision:** keep the name **Vigilia**, or not.

4. **Release prep (when shipping):** **app icon** (source the real asset, do not freehand a logo), App Store listing + screenshots, TestFlight pass. Voice notes stay deferred to v2.
