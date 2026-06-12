---
title: Domain decision
date: 2026-06-13
tags: [portfolio, domain, website]
---

# Custom domain — research (pending decision)

Site is live at https://blhdes.github.io/portfolio/ — a custom domain is optional polish. `alegomez.com` is **taken**. Availability below checked against the real registries (RDAP) on 2026-06-13; can change any day, so don't sit on a favorite for weeks.

## Availability check (2026-06-13)

| Domain | Status | Rough price/year |
|---|---|---|
| **alegomez.studio** | ✅ Available | ~20–25€ |
| **alegomezurrea.com** | ✅ Available | ~10–12€ |
| alegomez.design | ✅ Available | ~35–50€ |
| alegomez.me | ✅ Available | ~15–20€ |
| alegomez.dev | ✅ Available | ~12–15€ |
| alegomez.photography | ✅ Available | ~20€ |
| alegomez.es | ✅ Available | ~8€ |
| alegomez.com | ❌ Taken | |
| gomezurrea.com | ❌ Taken | |
| alegomez.site | ? (registry blocked the query) | |

## Claude's shortlist

1. **alegomez.studio** — top pick. "Studio" covers the whole practice at once (apps, photography, film, fashion brand), reads as a creative practice rather than a CV site, short and easy to say in an interview.
2. **alegomezurrea.com** — timeless full-name .com, cheapest, never feels trendy. Trade-off: long, and "Urrea" gets mangled abroad.

**Skip:** `.dev` (says "only a programmer"), `.photography` (boxes into one discipline), `.es` (ties to Spain when the goal is moving abroad).

## Where to buy

**Porkbun** or **Cloudflare Registrar** — near-cost pricing, no sneaky renewal markups (avoid GoDaddy-style registrars).

## After buying

Tell Claude which one → connecting it to GitHub Pages takes ~10 min:
1. DNS records at the registrar (A/AAAA or CNAME to `blhdes.github.io`)
2. Custom domain setting in the repo (https://github.com/blhdes/portfolio → Settings → Pages)
3. Wait for HTTPS certificate, then enforce HTTPS

Related: [[Projects/Portfolio/Portfolio|Portfolio]] (roadmap), [[Projects/Portfolio/site-structure|site-structure]]
