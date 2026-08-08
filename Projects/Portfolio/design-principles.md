---
title: Design principles (anti AI-slop)
date: 2026-06-13
tags: [portfolio, design, website]
---

# Design principles — keep it human

Result of a full AI-slop audit (2026-06-13). These rules protect the site from drifting back into generated-template territory. Apply to every future change.

## What we keep (deliberate choices)

*Revised 2026-08-08 (editorial restyle): the palette went near-monochrome, the typeface went serif + grotesque, and thin section rules returned. Superseded choices struck through below.*

- **Pure white background (#FFFFFF), pure black ink (#000000), neutral greys** — no warm undertone anywhere, the photographs are the page's only color. ~~Warm paper (#F7F5F0) / ink (#1A1815)~~ tried first, **replaced 2026-08-08 same day**: "i don't like the off-white colour approach, can we make it just pure white and change the palette to something really minimalistic and basic." Dark version inverts (pure black #000000 bg / pure white #FFFFFF ink), no toggle. ~~One vermilion accent (#d9432b, the cinema red)~~ — retired 2026-08-08; the middot field (itself later deleted) had woken in ink
- **Inter, one typeface, site-wide** (decided 2026-08-08, replacing SF Mono; ~~Fraunces + Inter~~ tried the same day and reverted same day — user disliked the serif and the overall scale). Hierarchy comes from weight (400/500/600) and size only, no second display face. The nav masthead name is the one place given real weight/size presence (~2-3x the nav links beside it), matching the biancacensori.com reference; everything else stays restrained. Font sizes trend small throughout: body 16px, most headings 17-20px, eyebrow labels 12px
- Sections separated by **typographic scale + generous whitespace (~10vh per side)**. **No hairline/border dividers anywhere** — a standing rule, twice affirmed: 2026-06-13 ("they look very simple and HTML coded") and again 2026-08-08, when a redesign brief specified thin 1px rules, they were implemented, and the user firmly rejected them. The rule outranks contrary spec text; picture frames (like the app-screenshot border) and text underlines are exempt
- Tiny uppercase eyebrow labels: 12px, 0.2em letter-spacing (kickers, group titles, years)
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

## Effects: none (the middot field, 2026-07-11 &rarr; deleted 2026-08-08)

The site now has **zero effects** — the user deleted the middot field (the one sanctioned effect: a dot grid, invisible at rest, waking near the pointer) during the 2026-08-08 minimal multi-page pivot: "make it even more minimal, delete the hover creative code effect." Minimalism outranks even a well-behaved decoration.

For the record, the two tests the field passed — and that any future effect proposal must still pass before it's even worth suggesting: **at rest, the page is indistinguishable from having no effect at all** (motion only ever answers the visitor's own movement, never plays at them), and **the effect never competes with text** — it decorates around the content, dampened or excluded wherever type sits. Autonomous animation (load reveals, loops, parallax) stays banned. Given the deletion, the bar for proposing any effect at all is now very high.

## The principle behind all of it

Confidence is quiet. Every effect removed says "the work is enough." When in doubt, simplify; never decorate.

Related: [[Projects/Portfolio/site-structure|site-structure]], [[Projects/Portfolio/Portfolio|Portfolio]]
