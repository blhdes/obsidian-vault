---
title: Smart playlist suggestion chip
date: 2026-05-12
tags: [culla-music, idea, feature, suggestions, sidebar, ux]
---

# Smart playlist suggestion chip

We already build a per-song playlist membership index. We can use it (plus recent sort history) to suggest a likely target playlist for the current song — a faint *"Sort → X?"* hint above the sidebar.

## Why

- The membership index is essentially free — we built it in Phase 3 for the chips.
- Reduces decision friction when the user has many sidebar playlists and a song that fits multiple.

## Behavior

Suggestion fires when **both** conditions hold:

1. The current song shares ≥2 playlists with another song the user recently sorted into playlist X.
2. The user has not just dismissed a suggestion for the same song in this session.

The suggestion appears as a faint pill above the sidebar (or near the right-swipe area) that says **"Sort → X?"**. Tap → instantly fires the same right-swipe-onto-X action. The pill auto-fades after a few seconds.

## Heuristic

- Keep it simple: weight by Jaccard similarity between the current song's playlist set and the average playlist set for songs recently sorted into each candidate.
- Need a *minimum confidence threshold* — better to show nothing than a wrong suggestion. Tuning belongs in a small JSON-or-AppStorage block, not a Settings UI.

## Open questions

- **Where to render.** A pill above the sidebar competes with the drop-zone highlight. Maybe a small ghost-chip next to the membership chips instead, labeled "Suggested →" with the playlist name.
- **Cold start.** Needs ~10–20 prior sort actions before the heuristic stops being noise. Suppress until we have that history.
- **Dismiss behavior.** A swipe-to-dismiss on the suggestion that suppresses future suggestions for this song for the rest of the session.

## Size / risk

Medium. Risk: if the heuristic is wrong, it adds noise. Easy dismiss + a high-confidence threshold are the guardrails.
