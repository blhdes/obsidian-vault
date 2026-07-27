---
title: Portfolio
date: 2026-06-12
tags: [project, portfolio, career, website]
---

# 🌍 Portfolio

Index note for the **portfolio website** project — the bridge to the next chapter.

## The goal

**Updated 2026-07-11 — two stages.** Stage 1 (now): land a better-paying **local creative job** (Barcelona area / Sant Cugat, or Madrid) — creative agencies, production houses, marketing — to earn and save. Stage 2 (mid-/long-term): the original dream, a **creative job abroad** (Paris, Amsterdam, or anywhere with better professional outcomes than Spain), funded by Stage 1. The original Dec 2026 – Feb 2027 window now applies to landing the *local* job.

The blocker isn't experience — it's **visibility**. The work exists (shipped apps, cinema background, photography, soon a fashion brand) but lives nowhere anyone can see it. The portfolio fixes that.

## What it is

A **personal website in English** that shows work, not credentials. Four sections:

1. **Apps** — the 2 apps live on the App Store are the strongest proof: *"I shipped real products."* Doppio, Warket and Village join as they're finished.
2. **Photography** — a curated selection (10–20 best shots, not everything).
3. **Projects** — cinema background work + the fashion brand once it launches (~Aug–Sep 2026, a centerpiece: brand identity, product, photos).
4. **Bio / About** — short, in English, telling the story *cinema → apps → brand*. The unusual mix is the angle, not a weakness.

## Principles

- **Free hosting** (GitHub Pages or similar) — no monthly cost.
- **English first** — written for the cities we're aiming at.
- **Show, don't list** — every section is work you can look at, not bullet points.
- It should feel *designed* — the site itself is a portfolio piece.

## Timeline

| When | Milestone |
|---|---|
| Month 1 (~July 2026) | Site live with apps + photography + bio |
| Month 3 (~Sep 2026) | Fashion brand section added at launch |
| Months 4–8 | Apply with a real portfolio, well before the deadline |

## Roadmap

- [x] **Site structure** — one-page scroll, see [[Projects/Portfolio/site-structure|site-structure]]
- [x] **Bio / About** — draft v2 approved 2026-06-13, see [[Projects/Portfolio/bio|bio]]
- [x] **Hero repositioned** 2026-07-11 — from personal intro to professional candidacy (Product design · UX · Photography, "story and image" line, AI as headline skill, fashion brand removed). Final copy + decisions in [[Projects/Portfolio/bio|bio]]
- [x] **Hero precision pass** 2026-07-11 — name scales to 8.5rem desktop, vermilion middots in the kicker (the hero's one accent, echoing nav Contact), tightened spacing rhythm, slightly shallower top padding so the work stays near the fold. Composition unchanged (kept quiet per [[Projects/Portfolio/design-principles|design-principles]]; "film credits" hero idea considered and declined)
- [x] **Hero middot field** 2026-07-11, v2 2026-07-12, v3 2026-07-13 — the site's one interactive effect: a dot grid, invisible at rest; dots near the pointer wake in vermilion and settle back when it leaves. v1 was rejected as too subtle and column-bound; v2 is full-bleed (edge to edge), brighter, with a longer settle, and adds a **legibility mask**: dots under the hero text barely wake, so the effect decorates around the content (user rule: effects never compete with text). Chosen over "darkroom develop" and "viewfinder" concepts for exactly that reason. **v3: the field no longer stops at the hero** — it dissolves into the Apps section (dots get scarcer and softer row by row, a halftone-style grain fade, gone partway into the app grid), so the effect introduces the work instead of ending at a rigid edge. The wake also follows the pointer while scrolling, awake dots lean ~2px toward the cursor, and the apps' section head / screenshots / metadata joined the legibility mask. Passes [[Projects/Portfolio/design-principles|design-principles]] because nothing moves until the visitor does (the "still at rest" test recorded there). Pointer-only: touch screens and reduced-motion visitors get the plain hero.
- [ ] **Gather raw material** ← current step (user's task)
	- [x] App info: **Culla** (live: https://apps.apple.com/us/app/culla/id6761316914) and **CullaMusic** (pending Apple review). Both live at **culla.app**. Screenshots gathered and wired in for Culla, CullaMusic and Doppio (verified 2026-07-27).
	- [ ] Photography: 10–20 best shots, user gathering them, ETA ~**2026-06-19**
	- [ ] Projects (pending): short film as **DOP**, distributed on **MUBI**: https://mubi.com/es/es/films/mia-marc, plus 2 more pieces to gather
- [x] **CV section zoned** 2026-07-11 — #cv is sent directly to recruiters, so it now reads as a distinct document: full-bleed band one paper-tone deeper (new `--paper-2` token, both themes, no divider lines) + two-column desktop layout (Experience left, Education/Skills/Languages/Interests right) so the whole CV reads at a glance. **About integrated into the band** (opens the document: portrait + story, then the structured CV below); the separate About nav link removed, `#about` anchor kept working for old links
- [x] **Copy audit: self-evident text removed** 2026-07-11 — cut all "site explaining itself" copy: under-construction promises ("more on the way" ×2), the fashion-brand tease in the Projects note, "Live on the App Store" ×3 (badge already says it), the CV section note, the Leica title decoration, plus em-dash and "coded" violations. App descriptions now say what each app does (Culla: photo clean-up by swipe; CullaMusic: Apple Music sorting by swipe; Doppio: living metronome)
- [x] **Site typeface decided** 2026-07-11 — **SF Mono** (JetBrains Mono fallback for non-Apple), chosen via a 21-font cycle test on the live hero; test apparatus removed after the decision. Details in [[Projects/Portfolio/design-principles|design-principles]]
- [ ] **Build the site** — skeleton built 2026-06-13 at `/Users/agomezu/Claude/portfolio/` (plain HTML/CSS/JS). Design: minimal editorial, warm paper + ink + vermilion accent, SF Mono typeface (since 2026-07-11), name **Ale Gómez**. Pending: real screenshots, photos, portrait.
- [x] **Publish** — live at **https://alegomez.studio** since 2026-06-13 (GitHub Pages, repo: https://github.com/blhdes/portfolio, domain via Porkbun). Details in [[Projects/Portfolio/domain|domain]].
- [ ] Add fashion brand section at launch
- [ ] **Job search & relocation** — workstream started 2026-06-14, see [[Projects/Portfolio/Job-Search/Job-Search|Job-Search]]. **Pivot 2026-07-11: local-first** (Barcelona/Sant Cugat + Madrid) to earn & save; abroad stays the mid-term goal. **2026-07-11: 202 companies with direct-contact emails** collected in [[Projects/Portfolio/Job-Search/outreach-directory|Outreach Directory]] — next: user skims and shortlists. **2026-07-27: first outreach drafted** (Division Global, Paris — internship address) ahead of the local-first sequencing, user's call; portfolio confirmed shareable v1 so the send gate holds.

## Related

- Job search: [[Projects/Portfolio/Job-Search/Job-Search|Job-Search & Relocation]]
- App projects: [[Projects/Culla/Culla|Culla]], [[Projects/Doppio/Doppio|Doppio]], Warket, Village
