---
title: MusicKit Catalog API — Why "Client not found" persisted after enabling MusicKit
date: 2026-05-11
tags: [culla, dev-insight, musickit, codesigning, apple-developer, post-mortem]
---

## Symptom

Building the hot-clip preview feature, every `MusicCatalogSearchRequest` / `MusicCatalogResourceRequest` failed with:

```
Failed retrieving MusicKit tokens: Error Domain=ICError Code=-8200
"Media API Token Service responded with status code: Not Found (404).
 This suggests that "agu.CullaMusic2" was likely not registered as a
 valid client identifier."
... AMSStatusCode=404, message=Client not found
```

`MusicLibraryRequest` (library access via the user's Apple Music account) worked fine. Only the **catalog API** failed. MusicKit had already been enabled as an App Service on the `agu.CullaMusic2` identifier in the developer portal **2-3 days earlier**, so propagation was not the issue.

## Root cause (the non-obvious bit)

A Development certificate for the App ID's team **did not exist on this Mac**. The team owning `agu.CullaMusic2` (and the MusicKit checkbox) is the **Developer Program team** `56BK7T2JG7`. But `security find-identity -v -p codesigning` showed:

```
1) "Apple Development: agomezurrea@gmail.com (T8Y59Q7DTM)"   ← Personal Team
2) "Apple Distribution: Alejandro Gómez Urrea (56BK7T2JG7)"  ← Dev Program, but Distribution-only
```

There was **no Apple *Development* cert for team `56BK7T2JG7`**. Debug builds need a Development cert (Distribution certs only sign Release / TestFlight / App Store builds). With nothing else available, Xcode automatic signing was using the Personal Team's Development cert to sign the binary while still stamping `TeamIdentifier=56BK7T2JG7` (because the project's `DEVELOPMENT_TEAM` setting says so).

Apple's MusicKit token service then saw: *"request signed by a cert from team T8Y59Q7DTM, but claiming to be on team 56BK7T2JG7 for bundle agu.CullaMusic2"* → can't reconcile → **404 / Client not found**, regardless of the portal checkbox being on.

## How to confirm this is the bug

Two commands:

```bash
# 1. Show signing identities — look for an "Apple Development" cert for the
#    team that owns the App ID with MusicKit enabled.
security find-identity -v -p codesigning

# 2. Inspect the built device app's cert authority and team identifier — they
#    must come from the same team.
codesign -dvvv ~/Library/Developer/Xcode/DerivedData/<App>-*/Build/Products/Debug-iphoneos/<App>.app
```

If `Authority` (cert team) and `TeamIdentifier` (app's team) disagree, that's the smoking gun.

## The fix

In Xcode → **Settings → Accounts** → select the Apple ID → select the Developer Program team → **Manage Certificates…** → `+` → **Apple Development**.

Then clean build folder (⇧⌘K), reinstall on device. After that, `security find-identity` shows a third entry — `Apple Development: ... (56BK7T2JG7)` — automatic signing picks it up, codesign authority and team identifier line up, and the token service returns a valid MusicKit dev token. Catalog API requests succeed.

## How this overlaps (and updates) the prior MusicKit memory note

The prior note in `feedback_musickit_capability.md` is still correct in saying:

- **Don't** add `com.apple.developer.musickit` to an iOS `.entitlements` file (it's macOS-only and breaks the build).
- **Don't** rely on Xcode's "+ Capability" picker — MusicKit isn't listed there for this account.

But its claim that *"native iOS apps don't actually consume an entitlement from that flag — the framework is gated by the App ID's metadata at Apple's backend"* is **incomplete**. The App ID metadata gates it, **and** the request must be signed with a cert from the same team that owns the registered App ID. Wildcard profiles signed by a different team will fail with the same 404 even when everything in the portal looks correct.

## Diagnostic anti-pattern this round taught me

The error message — *"agu.CullaMusic2 was likely not registered as a valid client identifier"* — strongly implied the portal was the problem. It nudged me to verify the portal config (which was correct) instead of inspecting the **actual signing identity on disk** first. The portal page and the built binary are two halves of the same lock — checking only the half the error message names is a recipe for chasing your tail.

**How to apply next time:** when an Apple service returns "client not found" / "not registered" for a bundle ID that *is* registered, run `security find-identity` + `codesign -dvvv` on the built app **before** re-checking the portal. The 30-second cert audit either confirms or rules out the most-common cause that the error string buries.

## Related

- Commits enabling the feature: `5fba887` (toggle + AVPlayer path), `ad92b0f` (catalog search bridge that exposed the cert issue).
- Prior MusicKit gotcha note: [[Projects/Culla-Music/Dev-Insights/CullaMusic MusicKit Playback Regression 2026-05-07]].
- Memory file to update with this cert-team learning: `feedback_musickit_capability.md`.
