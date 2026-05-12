---
title: Dynamic accent color from song artwork
date: 2026-05-12
tags: [culla-music, idea, feature, theming, ux]
---

# Dynamic accent color from song artwork

Right now the sidebar accent and the drop-target highlight come from a fixed `AccentPalette` swatch picked in Settings. Photo Culla pulls colors from images — Culla Music could do the same, extracting the dominant color from the current song's artwork and using it as the live accent.

## Why

- Each song would get a tiny visual signature without adding UI chrome.
- Makes the swipe view feel alive between cards — the world shifts subtly with each track.
- More "Culla" — the photo app's entire identity is artwork-driven theming.

## Behavior

- On track change, sample 1–2 dominant colors from the current artwork.
- Cross-fade the sidebar accent + drop-target glow to the new color over the same duration as the artwork cross-fade.
- Settings retains the static palette as a **manual override** for users who don't want the dynamism (or who hit ugly colors on busy artwork).

## Open questions

- **Extraction.** Use a simple bucketed-histogram pass on a downscaled `UIImage`, or hand it off to a small Core Image kernel. Don't pull in a heavy palette library.
- **Saturation / luminance clamp.** Raw dominant colors are often too dark or too washed out for an accent. Clamp into a comfortable HSL range (something like S ≥ 0.4, L between 0.45 and 0.7) before applying.
- **Album-art availability.** Cache the extracted color alongside the song's local row so we don't re-sample on every refill. Key: `songID`.
- **`ArtworkImage` source.** We render artwork via MusicKit's `ArtworkImage` — pulling pixels back out for sampling may not be straightforward. May need to fetch via `Artwork.url(width:height:)` separately and sample from a `URLSession` download.

## Size / risk

Small to medium. Highest visual payoff per line of code in the candidate list. Main risk: the saturation/luminance clamp needs care, otherwise muddy artwork produces muddy UI.
