---
title: Soulseek port stays CLOSED — CGNAT audit + fixes
date: 2026-06-04
tags: [networking, soulseek, cgnat, router, inbox]
---

# Soulseek port stays CLOSED — CGNAT audit + fixes

**Status: confirmed CGNAT. Router port forwarding can't help. Current fix = leave it closed.**

## The problem

Running Soulseek on listening port **56968**. The port checker
(`http://tools.slsknet.org/porttest.php?port=...`) reports the port **CLOSED**,
meaning other peers can't open incoming connections to my machine.

## What we checked (the audit)

1. **Wrong port in the checker URL.** First test used `?port=56969` while the
   client actually listens on `56968` — a one-digit typo. Always test the *real*
   port: `http://tools.slsknet.org/porttest.php?port=56968`.

2. **Router admin panel** (Comtrend **GRG-4280us**, fiber/PON, at `192.168.1.1`).
   - ARP table showed a gateway `100.76.0.1` with MAC `00-00-5e-00-01-ff`
     (a VRRP / ISP-gateway signature) — first hint of CGNAT.
   - `WAN` tab only had **Bridge Mode** — ⚠️ do **not** enable it (turns the
     router into a dumb pass-through, needs a factory reset to undo).
   - `Status → Device` → **WAN Configuration** gave the proof:

     | Field | Value |
     |---|---|
     | WAN IP Address | `100.76.156.85` |
     | Gateway | `100.76.0.1` |
     | IPv4 Default Gateway | `100.76.0.1` |
     | Name Servers | `212.230.135.2`, `212.230.135.1` (Spanish fiber ISP) |

## The finding: CGNAT

The WAN IP `100.76.156.85` sits in the **carrier-shared range** `100.64.0.0` –
`100.127.255.255` (the reserved CGNAT block). So:

- The router never gets a real public IP — it gets a shared internal carrier one.
- The public IP a website sees (`93.176.132.98`) is the ISP's **shared exit door**,
  used by many customers at once. I don't control it.
- The gatekeeping happens on the ISP's equipment, one level above the house.

**Therefore port forwarding on this router does nothing.** The closed port is by
design on the ISP side, not a misconfiguration.

> Soulseek still works behind CGNAT: I can download from anyone who *has* an open
> port (most well-seeded material). I just can't connect to the minority of users
> who are *also* behind a closed port.

## Three ways forward

### 1. Call the ISP (cleanest)
Ask them to take me off CGNAT or assign a **public IPv4** address. Often free or a
few €/month. Then normal router port forwarding would work. Downside: depends on
the ISP agreeing.

### 2. VPN with port forwarding
Route Soulseek through a VPN that offers port forwarding (e.g. **AirVPN**, or
**ProtonVPN** paid plans). Gives an openable port regardless of what the ISP does.
Downside: small monthly cost + a bit of setup + slight speed hit.

### 3. Leave it closed ✅ (current choice)
Do nothing. Soulseek keeps downloading from the many open-port users. Zero cost,
zero setup; only lose access to the minority of closed-port peers.

## If I ever go the port-forwarding route (after escaping CGNAT)
1. Find this computer's local IP (`System Settings → Wi-Fi → Details`, e.g. `192.168.1.x`).
2. Router → **Port Forwarding / NAT / Virtual Server** → rule: external `56968` →
   internal `56968` → this computer's local IP → protocol **TCP**.
3. Allow the Soulseek app through the macOS firewall (`System Settings → Network → Firewall`).
4. Re-test `http://tools.slsknet.org/porttest.php?port=56968`.
