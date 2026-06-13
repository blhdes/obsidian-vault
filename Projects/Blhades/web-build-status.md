---
title: BLH*DES — Web Build Status
date: 2026-06-09
tags: [blhades, web, dev, status]
---

# BLH*DES — Web Build Status

> Where the website stands (repo: `blhades-web-temp`). Brand index: [[Projects/Blhades/Blhades|BLH*DES]].

## Snapshot (2026-06-09)
- Storefront is being built **privately at `/preview/`**; the public `/` stays the **launch countdown** until **12 Aug 2026**.
- Home + product pages + waitlist all work locally. **Nothing is deployed yet** — the live site is untouched.

## What's built
- **Home storefront** (`/preview/`) — logo header, big hero artwork, the 9-piece *White Canvas* catalog in the "stagger" layout (hover reveals each piece's name + back/model shots), footer. Header has a light/dark toggle that's remembered.
- **Product page** (`/preview/piece/<slug>`) — big image + thin details column: numeral, name, **€60** (was €55 → €70 → €60 on 2026-06-13; see production-plan pricing revision), **Edition of 50**, sizes **XS–XL**, composition line. Every catalog tile links here.
- **Waitlist** — the drop isn't on sale yet, so **"Reserve" collects an email** instead of taking payment. Each signup is saved + tagged with which piece it came from, then a quiet "On the list" confirmation shows.

## Design locked
**White** surface · **Stagger** layout · **Inter** captions (the design tool's other options were dropped). Fabric line: *Organic combed cotton · 240 gsm · Cut in Portugal*.

## Architecture (plain words)
- One repo: **`frontend/`** (React + Vite) and **`backend/`** (a small Express server).
- **One app, two pages chosen by the URL**: anything under `/preview` shows the storefront, everything else shows the countdown. Each loads as its own separate bundle, so the countdown's black styling and the shop's white styling never bleed into each other.
- Storefront code lives in `frontend/src/preview/` — `data.js` (the 9 pieces + price/edition/fabric), `theme.js` (light/dark), `Storefront.jsx`, `ProductPage.jsx`, `Waitlist.jsx`, `PreviewApp.jsx` (routing).
- Product images were optimized **140 MB → ~2.9 MB** (WebP) and live in `frontend/public/preview/assets/`.
- Backend `POST /api/waitlist`: validates the email → appends it to `backend/waitlist.jsonl` (our own copy, gitignored) → forwards it to **Buttondown**. The forward is best-effort, so a signup is never lost if the service is down or the key isn't set yet.
- **Deploy model**: there's no build step on the server — you build locally and commit the result into `backend/dist`, which *is* the live site. The server only hands out files + runs the waitlist API.

## Open next steps
- [ ] **Get the Buttondown key** — make a free account at buttondown.email → Settings → Programming → API key → put it in `backend/.env` as `BUTTONDOWN_API_KEY=...`. **Until this is done, signups save locally only** (they don't reach the email tool).
- [ ] Decide: deploy `/preview` as an unlisted URL, or keep it local-only until launch.
- [ ] **Launch day (12 Aug 2026)**: point `/` at the storefront, and email the waitlist that it's live.
- [ ] Decide what data the per-piece **size availability** should reflect (right now all sizes show in stock for every piece).
- [ ] Optional polish: instant in-app navigation (no full page reload), a back/model image switch on the product page, JPEG fallback for very old browsers.

## Related
- [[Projects/Blhades/Blhades|BLH*DES index]]
- [[Projects/Blhades/couture-references|Couture & luxury-house references]]
