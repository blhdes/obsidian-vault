---
title: Domain decision
date: 2026-06-13
tags: [portfolio, domain, website]
---

# Custom domain — DECIDED: alegomez.studio ✓

**Bought 2026-06-13 on Porkbun** (renewal ~$25/yr, next: June 2027, auto-renew ON). DNS pointed at GitHub Pages same day: 4 A records (185.199.108–111.153) + `www` CNAME → `blhdes.github.io`. Site answers at http://alegomez.studio; HTTPS cert auto-issued by GitHub/Let's Encrypt, then `https_enforced` switched on. Porkbun settings verified: domain lock ON, contact privacy ON, Porkbun SSL not needed (GitHub provides the cert).

Research below kept for reference (decision was option 1 of the shortlist).

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
