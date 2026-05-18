---
title: App Icon Design — Recraft Prompts
date: 2026-05-18
tags: [culla, phase, design, icon, branding]
---

## Goal

Generate Culla's app icon/logo using Recraft. Target aesthetic: **iOS ecosystem feel + minimalism with a punch** — think Apple Music / Podcasts / Voice Memos / Notes energy.

What "iOS ecosystem" means in practice:
- Squircle (rounded square) canvas
- Single centered glyph
- Subtle gradient or flat pastel background
- No text (unless it's a single letter mark)
- No glossy bevels, no fake shadows
- Flat vector, premium feel
- 1024×1024 source size (Apple's requirement)

---

## Prompt directions to try

### 1. Gradient + abstract waveform (Apple Music-adjacent)

> iOS app icon, squircle rounded square canvas, smooth vertical gradient from warm coral to deep magenta, single centered minimalist sound wave glyph in pure white, slight inner glow, flat vector, no text, no shadow, ultra-clean, Apple Human Interface Guidelines style, 1024x1024

### 2. Monochrome glyph on soft pastel (Notes / Reminders feel)

> iOS app icon, rounded square with soft cream background, single centered geometric music note symbol in matte black, generous negative space, flat vector illustration, minimalist, no gradient, no text, Apple system app aesthetic, 1024x1024

### 3. Vinyl / disc abstraction (Podcasts-adjacent)

> iOS app icon, squircle canvas, radial gradient from deep indigo center to soft lavender edge, single centered concentric-circle vinyl record motif in white with a small dot offset, flat vector, minimalist, no text, no realistic textures, premium Apple ecosystem style, 1024x1024

### 4. Letter-mark "C" for Culla (Calendar / Mail-style)

> iOS app icon, rounded square canvas, smooth gradient background from soft peach to dusty rose, single centered letter C in custom rounded sans-serif, white, perfectly geometric, flat vector, minimalist, no text other than the C, Apple-style system app, 1024x1024

---

## Recraft tweaks that usually help

- Add **"flat vector, no photorealism, no 3D"** → stops it from adding glossy bevels.
- Add **"no text, no letters"** unless you actually want the C → Recraft loves sneaking in fake words.
- Specify **"1024x1024"** → Apple's required source size.
- Closer phrase: **"in the style of iOS system apps"** if results drift too generic.

---

## Next steps

- [ ] Pick a direction (gradient/mono/vinyl/letter-mark)
- [ ] Generate 3–5 variants in Recraft
- [ ] Decide on final palette (tie into Culla's existing color system?)
- [ ] Export at 1024×1024 + run through an iOS icon resizer for all required sizes
- [ ] Drop into `Assets.xcassets/AppIcon.appiconset/`

Related: [[Projects/Culla/Culla]]
