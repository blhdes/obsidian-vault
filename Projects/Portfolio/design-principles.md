---
title: Design principles (anti AI-slop)
date: 2026-06-13
tags: [portfolio, design, website]
---

# Design principles — keep it human

Result of a full AI-slop audit (2026-06-13). These rules protect the site from drifting back into generated-template territory. Apply to every future change.

## What we keep (deliberate choices)

- Warm paper background (#faf8f3), ink text, **one vermilion accent** (#d9432b, the cinema red); dark version follows the system scheme (#181613 / #ece9e2 / #e8553d), no toggle
- SF Mono typeface (decided 2026-07-11 after cycling ~20 Apple built-ins; replaced Switzer). Apple devices get the real SF Mono via `ui-monospace`; everyone else gets **JetBrains Mono** from Google Fonts, the closest free equivalent. The mono voice reads technical and systematic, matching the "ships products with AI" story
- Sections separated by **typographic scale + whitespace**: oversized section titles as landmarks, note on the same baseline. **No hairline/border dividers anywhere** (user: "they look very simple and HTML coded") — added 2026-06-13, replaced the original hairline approach
- Plain underlined links, like print

## Banned patterns (found and removed in the audit)

**Copy**
- Em dashes (standing rule)
- Rhetorical-question headers ("Looking for someone like me?")
- Craft-signaling ("Built by hand…")
- "Where X and Y meet" slogan constructions as headlines; concrete statements of what Ale makes instead
- Filler CTAs ("See the work ↓")

**Design**
- Scroll-reveal / fade-up animations — content is simply there
- Numbered sections (01, 02, 03…)
- Pill-shaped badges
- Animated link underlines, hover slide/bounce gimmicks
- Arrow glyphs (↗ ↓) sprinkled on links
- Full-viewport hero that hides the work below the fold
- Dramatic inverted (black) footer; the footer is quiet, same paper

## The one sanctioned effect (2026-07-11)

The **middot field**: a grid of dots behind the hero, invisible at rest, that wake in vermilion near the pointer and settle back when it leaves. It extends the site's existing middot accent rather than importing a new motif. Since 2026-07-13 the field has no bottom edge: it dissolves gradually into the Apps section (dots get scarcer and softer until they're gone partway into the app grid), so the one effect introduces the work rather than living in a fixed box.

Why it doesn't break the rules — and the two tests any future effect must pass: **at rest, the page is indistinguishable from having no effect at all** (motion only ever answers the visitor's own movement, never plays at them), and **the effect never competes with text** — it decorates around the content, dampened or excluded wherever type sits (rule added 2026-07-12; the field uses a legibility mask over the hero text). Autonomous animation (load reveals, loops, parallax) stays banned. Touch screens and reduced-motion visitors get the plain hero.

## The principle behind all of it

Confidence is quiet. Every effect removed says "the work is enough." When in doubt, simplify; never decorate.

Related: [[Projects/Portfolio/site-structure|site-structure]], [[Projects/Portfolio/Portfolio|Portfolio]]
