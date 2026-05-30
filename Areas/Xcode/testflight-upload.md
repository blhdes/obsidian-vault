---
title: TestFlight & App Store Connect — uploading a build
date: 2026-05-27
tags: [xcode, testflight, app-store-connect, distribution, asc]
---

# TestFlight & App Store Connect

How we get a build of Culla onto **TestFlight** so people can install it before it's on the App Store. Written for our actual setup — copy the commands as-is.

## Our values (fill-in-the-blanks for next time)

| Thing | Value |
|---|---|
| App / scheme | `CullaMusic` |
| Project file | `CullaMusic/CullaMusic.xcodeproj` |
| Bundle ID | `agu.CullaMusic2` |
| Team ID | `56BK7T2JG7` (Alejandro Gómez Urrea) |
| Distribution cert | `Apple Distribution: Alejandro Gómez Urrea` ✓ already installed |
| Signing | Automatic |

## The one thing to understand first: internal vs external

This is the whole ballgame for *how fast* a build is shareable.

- **Internal testers** — people you add to **your own team** in App Store Connect (up to 100). They can install **minutes after Apple finishes processing** the build. **No review.** Fast.
- **External testers** — a shareable public link, or anyone outside your team. Requires **Beta App Review** by Apple. The **first build** typically takes **hours to a day**. Later builds are usually faster but still not instant. This wait is Apple's queue — *nothing we do locally speeds it up.*

> ⚠️ **Reality check:** "Send a TestFlight link to outside people in 20 minutes" is **not possible** on a first-ever build. Plan for external sharing to land later that day or the next.

## Timeline at a glance

| Step | Who controls it | Rough time |
|---|---|---|
| Archive the app | Us | 2–5 min |
| Create app record in ASC | Us (browser) | ~2 min |
| Upload build | Us (Xcode) | 3–5 min |
| Apple **processing** | Apple | 5–15 min (sometimes more) |
| Export compliance answer | Us | 1 min |
| Share with **internal** team | — | immediate after processing |
| **Beta App Review** (external) | Apple | **hours → a day** (first build) |

---

## Step 1 — Archive the app

The archive is the signed, store-ready bundle. This is also the step that flushes out any signing problems, so always do it first.

From the repo root:

```bash
cd CullaMusic
rm -rf /tmp/CullaMusic.xcarchive
xcodebuild \
  -project CullaMusic.xcodeproj \
  -scheme CullaMusic \
  -configuration Release \
  -destination 'generic/platform=iOS' \
  -archivePath /tmp/CullaMusic.xcarchive \
  archive \
  -allowProvisioningUpdates
```

Look for **`** ARCHIVE SUCCEEDED **`** at the end. It also runs Apple's `-validate-for-store` check during the build, so a success here means the bundle is genuinely upload-ready.

> The archive may be signed with the *Apple Development* identity — that's fine. The **upload** step re-signs it for the store automatically.

## Step 2 — Create the app record (browser, first time only)

You only do this once per app. Builds can't be used until this record exists.

1. [appstoreconnect.apple.com](https://appstoreconnect.apple.com) → **Apps** → blue **+** → **New App**
2. Fill in:
   - Platform: **iOS**
   - Name: e.g. *Culla*
   - Primary language: pick one
   - **Bundle ID: `agu.CullaMusic2`** (should already be in the dropdown — automatic signing registered it)
   - SKU: any unique string, e.g. `cullamusic2`
   - Access: Full
3. **Create.**

## Step 3 — Upload the build (Xcode)

Open the archive in Xcode's Organizer:

```bash
open /tmp/CullaMusic.xcarchive
```

Then in the Organizer window:

1. Select the **CullaMusic** archive at the top.
2. **Distribute App** → **App Store Connect** → **Upload**.
3. Accept the defaults (**automatically manage signing**) → **Upload**.

> This needs an Apple ID for team `56BK7T2JG7` signed into Xcode (Settings → Accounts). If automatic signing worked in Step 1, you're already signed in.

## Step 4 — After upload (App Store Connect → app → TestFlight tab)

1. The build shows **"Processing"** (5–15 min usually). Wait it out — refresh the TestFlight tab.
2. Answer the **export compliance** question. For a normal app using only standard HTTPS, the answer is usually *exempt / no* — but answer honestly for what the app actually does.
3. To share:
   - **Internal:** add testers under **Internal Testing**, attach the build → they can install right away.
   - **External:** create an **External group**, add the build, fill in **"What to test"** + test info, then **Submit for Beta App Review**. Wait for Apple (hours → a day on a first build).

---

## Bumping the build for the next upload

App Store Connect rejects a build number it has already seen. Before re-archiving, bump it:

- `MARKETING_VERSION` (e.g. `1.0`) = the version users see.
- `CURRENT_PROJECT_VERSION` (e.g. `1`) = the build number — **increment this every upload** (`1` → `2` → `3`…), even if the marketing version doesn't change.

Set both in Xcode target → **General** tab, or in the build settings.

## Fast alternative — ad-hoc IPA (no review)

When you need a build in front of a **few specific people right now** and can't wait for Beta App Review:

1. Collect each person's **device UDID** (Settings → General → About on their iPhone, or via Xcode when plugged in).
2. Register those UDIDs in the Apple Developer portal → Devices.
3. Re-archive, then **Distribute App → Release Testing (Ad Hoc)** → export the `.ipa`.
4. Send them the `.ipa` (AirDrop / Apple Configurator / a tool like Diawi). They install and trust the profile.

Trade-off: no Apple review (instant), but capped to the devices you registered and clunkier to install than a TestFlight link.

## Quick reference

| Symptom / goal | Do this |
|---|---|
| "Is it even uploadable?" | Run the archive command (Step 1) — `ARCHIVE SUCCEEDED` = yes |
| Share with my own devices/team fast | Internal testers — no review |
| Share a public link with outsiders | External group → Beta App Review (slow first time) |
| Need it in front of 2–3 people *now* | Ad-hoc IPA |
| "Build number already used" error | Bump `CURRENT_PROJECT_VERSION`, re-archive |
| Build stuck "Processing" forever | Usually resolves in <30 min; if truly stuck, re-upload with a bumped build number |

## Related

- [[app-store-submission]] — the next step: take this uploaded build to a **public** App Store release
- [[Projects/Culla/Culla|Culla]] — the app we ship through this pipeline
- [[instruments-profiler]] — profiling before you ship
- [[Xcode]] — index
