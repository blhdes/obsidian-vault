---
title: Colourway Selector — Research & Decision
date: 2026-06-12
tags: [blhades, web, design, ux, research, ecommerce]
---

# Colourway Selector — Research & Decision

How premium e-commerce sites let you pick a colour variant on the product page, researched 2026-06-12 after three unconvincing dot-component iterations on the BLH*DES storefront. **Decision at the bottom: written names, no swatch hardware.**

## What the reference sites actually do

Verified by inspecting live product pages (headless screenshots), not from memory:

### Balenciaga — garment thumbnails
- The selector is a row of **tiny photos of the actual garment** in each colourway, next to the product title; the colour name lives in the title itself ("…oversize **negro**").
- Most informative pattern: you click the real shirt, not an abstraction.
- Same school: Jacquemus, Prada, Miu Miu.

### Our Legacy — chips + the written colourway name
- Small swatch dots under the title, but the heavy lifting is done by the **colourway name written out** beneath the product name ("Black Clean Jersey").
- Even at peak Swedish minimalism the selected chip still needs a ring — evidence that a naked dot can't carry the selected state alone.
- Same school: Acne (colour as text in the title, variants as related products), COS/Arket (dot + name label).

### The Row / Lemaire / Auralee — colour as typography
- Almost no graphical swatch hardware at all: the colourways are **words**. Selected = full ink, others muted.
- The most minimal pattern in the field, used precisely by the most luxury-coded houses.

## What the UX research says

- **NN/g** ([Design Guidelines for Selling Products with Multiple Variants](https://www.nngroup.com/articles/products-with-multiple-variants/)): the recurring *luxury-specific* failure is variant selection that's **too subtle to notice** during normal scanning (their Coclico/Arhaus examples). Minimal restraint must not cost discoverability.
- **Baymard** ([swatch research](https://baymard.com/blog/mobile-interactive-color-swatches)): never communicate colour by swatch alone — **pair it with the name**; swatches should be ≥32px on desktop, ~40px touch targets; confusing option selection drives ~17% of cart abandonments.

## The convergent insight

What makes these selectors feel premium isn't a better dot — **it's that the colour is named, in type.** "Black" written in the site's caption voice is simultaneously more luxurious and more usable than any 9–14px circle. Dots are UI hardware; for a monochrome, type-driven brand (REPENT, NO RULES — the designs *are* words), language is the native selector.

## The three candidates proposed

1. **Written names only** (The Row school) — `BLACK  WHITE` in the caption style; selected = full ink, unselected = muted, ink on hover. Zero new shapes. ⭐ **Chosen.**
2. **Chip + written name** (Our Legacy school) — soft chips, selected colour's name printed beside the row; the word is the selected state.
3. **Garment thumbnails** (Balenciaga school) — ~40×50 px flat-shot miniatures, selected full opacity. Most informative, heaviest visually.

## Decision (2026-06-12)

**Option 1 — written names.** Implemented as the shared `Colourways` component in `frontend/src/preview/Storefront.jsx`, used by the home tiles, mobile tiles, and the product page (`ProductPage.jsx`). Details:

- Caption typography (Inter Tight, 10px, tracked, uppercase) — same voice as numeral/sizes/composition.
- Selected: `palette.fg`. Unselected: `palette.muted`, transitions to ink on hover (the affordance).
- Hit areas padded ~10px beyond the word (Baymard's touch floor) + `aria-pressed` on real buttons.
- Bonus: when Reserve becomes a real order, the colourway is already a named value ("Black"), not a dot index.

Failed iterations, for the record: bordered dots with double-ring (stock-component feel) → chips with underline mark (read as *more* components) → size-as-state chips (still abstraction hardware). The lesson: stop refining the dot, remove it.

Related: [[Projects/Blhades/web-build-status|Web Build Status]] · [[Projects/Blhades/Blhades|BLH*DES index]] · [[Projects/Blhades/production-plan|Production Plan]]
