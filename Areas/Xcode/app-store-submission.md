---
title: App Store submission — shipping a build for public release
date: 2026-05-30
tags: [xcode, app-store-connect, submission, review, distribution, asc]
---

# App Store submission

How we take an **already-uploaded build** and turn it into an app that's **live on the public App Store**. CullaMusic is the running example.

> **This note picks up where [[testflight-upload]] leaves off.** That note covers archiving the app, creating the app record, and uploading the build (Steps 1–3). Do those first. Once your build shows up in App Store Connect and finishes **Processing**, come back here.

## TestFlight vs the App Store — two different reviews

Easy to confuse, so get this straight first:

| | TestFlight (beta) | App Store (public) |
|---|---|---|
| Who installs it | Testers you invite | Anyone, worldwide |
| Apple's check | **Beta App Review** (lighter) | **Full App Review** (strict) |
| What Apple looks at | Roughly: does it launch, is it not malicious | **Everything**: metadata, screenshots, privacy, crashes, guideline compliance |
| Same build? | Yes — the *exact same uploaded build* can go through both |

You don't re-upload anything to go from TestFlight to the App Store. You attach the **same build** to an App Store version and fill in the store listing. Many people TestFlight first to shake out bugs, then submit that same build for public release.

## Our values (CullaMusic)

| Thing | Value |
|---|---|
| App / scheme | `CullaMusic` |
| Bundle ID | `agu.CullaMusic2` |
| Team ID | `56BK7T2JG7` (Alejandro Gómez Urrea) |
| Marketing version (users see) | `1.0` |
| Build number | `1` |
| Category | **Music** |
| Price | **Free** (v1) |
| Key permission | Apple Music library access (`NSAppleMusicUsageDescription`) |

---

## Step 0 — One-time account housekeeping

A build can be perfect and still be **un-submittable** because of paperwork. Check these once in [appstoreconnect.apple.com](https://appstoreconnect.apple.com):

- **Business → Agreements, Tax, and Banking.** The **Free Apps** agreement must show **Active**. If you ever charge money you also need the **Paid Apps** agreement (which needs tax + banking info). For a free v1, the Free agreement is all you need — but a *pending* agreement silently blocks submission.
- **Apple Developer Program membership** must be active (the $99/yr one).

---

## Step 1 — Fill in **App Information** (shared across all versions)

In ASC: **Apps → CullaMusic → App Information** (left sidebar, under "General").

- **Name** — up to 30 characters. This is the name on the store and home screen listing. (e.g. *Culla Music*)
- **Subtitle** — up to 30 characters, shown under the name. A short pitch, e.g. *"Swipe songs into playlists."*
- **Category** — **Primary: Music.** Secondary is optional.
- **Content Rights** — declare whether the app contains third-party content. CullaMusic shows *your own* Apple Music library via Apple's official MusicKit, so you don't ship third-party content yourself → the standard "does not contain, or has rights to" answer.
- **Age Rating** — answer the questionnaire (violence, mature themes, etc.). CullaMusic is a clean utility → expect a low rating (4+). Answer honestly; lying here is a fast rejection.

## Step 2 — **Pricing and Availability**

Left sidebar → **Pricing and Availability**.

- **Price** — choose **Free** (Price Tier 0) for v1.
- **Availability** — which countries. Default is all. Leave as-is unless you have a reason to limit.

## Step 3 — **App Privacy** (the "nutrition label")

Left sidebar → **App Privacy**. **This is required — you cannot submit without it.**

1. **Privacy Policy URL** — *mandatory*, even for a free app that collects nothing. It must be a real, reachable web page. (A simple GitHub Pages or Notion page stating "Culla Music does not collect or transmit personal data; library access stays on your device" is enough.)
2. **Data collection questionnaire** — Apple asks what data types you collect and why.
   - CullaMusic reads your Apple Music library **on-device** and stores playlist choices locally (SwiftData). If nothing is sent to a server, the honest answer is **"Data Not Collected."**
   - ⚠️ "Data Not Collected" means *nothing leaves the device*. If you later add analytics, crash reporting (e.g. a third-party SDK), or any network call that sends user data, you must update this.

---

## Step 4 — Create the version and fill **Prepare for Submission**

This is the per-release page. In ASC, the version (e.g. **1.0**) sits in the left sidebar under "iOS App." If it's the first release, ASC creates a `1.0` version automatically; otherwise click **+ Version** (top of sidebar) and type the marketing version.

Open it — the status banner reads **"Prepare for Submission."** Fill in:

### Screenshots (required)
- Apple now simplified this: you generally only need **one iPhone size** — the **6.9"** (or 6.7") set — and Apple scales it down for smaller iPhones. **ASC shows you exactly which sizes are required** — follow what it asks.
- If the app supports iPad, you also need **13" iPad** screenshots.
- Take them from the **iOS Simulator** of the right device (e.g. iPhone 16 Pro Max) with **⌘S**, or from a real device. They must show the *actual app*, not mockups with fake UI.
- 1–10 screenshots. The first 1–3 matter most (they show in search results).

### Text fields
- **Promotional text** — up to 170 chars. Shows above the description. **Editable any time without a new review** — handy for "what's new this week" blurbs.
- **Description** — up to 4000 chars. What the app does, in plain language.
- **Keywords** — up to 100 chars total, **comma-separated, no spaces** (`playlist,swipe,music,apple music,sort`). These feed search.
- **Support URL** — *required*. A page where users can get help (can be the same simple page as the privacy policy).
- **Marketing URL** — optional.
- **What's New** — only appears for **updates** (version > 1.0), describing changes since the last release.

### Build
- Scroll to **Build** → click **+** (or "Add Build") → pick the processed build you uploaded (`1.0 (1)`).
- If no build appears, it's either still **Processing** or it failed export-compliance — go check the TestFlight tab.

### App Review Information
This is the box that decides whether a reviewer can actually *use* your app.

- **Sign-in required?** CullaMusic has no login of its own → leave the demo-account fields empty.
- **Contact info** — your name, phone, email (so Apple can reach you).
- **Notes** — free text for the reviewer. **This is critical for CullaMusic** (see next section).

### Version Release
Choose how it goes live *after* approval:
- **Manually release** — it sits as "Pending Developer Release"; you press the button. *Recommended for v1* so you control the exact moment.
- **Automatically release** — goes live the instant it's approved.
- **Phased release** — automatic rollout over 7 days (only for updates, not first release).

---

## Step 5 — The MusicKit gotcha (don't skip)

CullaMusic is **useless to a reviewer who can't log into Apple Music.** If the reviewer's test device has no Apple Music subscription, the app shows an empty/permission screen and gets **rejected as "broken"** — a classic, avoidable rejection.

**Paste a note like this into App Review Information → Notes:**

> Culla Music requires an **active Apple Music subscription** to function. Please sign the test device into an Apple ID that has Apple Music, and **grant the "Media & Apple Music" permission** when the app asks on first launch. The app reads your existing library, then lets you swipe songs left/right into playlists.

Also confirm the permission string is present (it is, in our project):

```
NSAppleMusicUsageDescription =
  "Culla Music needs access to your Apple Music library so you can swipe songs into playlists."
```

> Note: MusicKit access is granted by enabling the **MusicKit capability / App Service** for the App ID — **not** by adding a `com.apple.developer.musickit` entitlement by hand. (See the memory note on MusicKit entitlement gotchas.)

---

## Step 6 — Submit for review

Top-right of the version page: **Add for Review** → then **Submit for Review**. Apple asks a few yes/no questions:

- **Export Compliance** — uses only standard HTTPS encryption → usually **exempt** (same answer as the TestFlight export-compliance prompt). Answer honestly.
- **Content Rights** — confirms you have rights to everything shown.
- **Advertising Identifier (IDFA)** — does the app use ads / the ad identifier? CullaMusic has no ads → **No**.

Then confirm. Status flips to **Waiting for Review**.

## Step 7 — Watch the status

The version moves through these states:

| Status | Meaning |
|---|---|
| **Waiting for Review** | In Apple's queue |
| **In Review** | A reviewer is actively testing it |
| **Pending Developer Release** | ✅ Approved — waiting for *you* to press release (if you chose Manual) |
| **Ready for Sale** | 🎉 Live on the App Store |
| **Rejected** | Needs fixes — Apple writes why in **Resolution Center** |

**Timeline:** App Review is usually **24–48 hours**, often faster (sometimes under a day). You'll get email at each step.

---

## Common first-submission rejections (and how we avoid them)

| Reason | Avoid it by |
|---|---|
| Reviewer "couldn't test" the app | The **Apple Music subscription note** in Step 5 |
| Privacy policy URL missing / broken | A real, reachable page (Step 3) |
| App Privacy questionnaire incomplete | Fill it fully before submitting (Step 3) |
| Crash or obvious bug on launch | TestFlight it first; test a clean install |
| Screenshots don't match the app | Use real Simulator/device captures, not mockups |
| Incomplete metadata | Don't leave required fields blank |
| Placeholder / demo content visible | Ship real, finished UI |

If rejected, read the **Resolution Center** message, fix it, and **resubmit** — you usually don't need a new build unless the bug is in the code.

## After approval — going live

- If you chose **Manual release**: open the version → **Release This Version**. It appears on the store within a few hours (search indexing can lag a bit).
- If **Automatic**: it's already live.

## Shipping updates later

For version `1.1`, `1.2`, …:

1. Bump the build: increment **`CURRENT_PROJECT_VERSION`** every upload; bump **`MARKETING_VERSION`** when the user-facing version changes. (See [[testflight-upload]] → "Bumping the build.")
2. Re-archive + upload (Steps 1–3 of the TestFlight note).
3. In ASC, **+ Version**, fill in **What's New**, attach the new build, **Submit for Review**.

---

## Pre-submission checklist (copy this)

```
[ ] Free Apps agreement = Active (Business tab)
[ ] App Information: name, subtitle, category (Music), age rating done
[ ] Pricing: Free, availability set
[ ] App Privacy: policy URL live + data questionnaire complete
[ ] Screenshots uploaded for the size(s) ASC requires
[ ] Description + keywords + support URL filled
[ ] Build 1.0 (1) attached (finished Processing)
[ ] App Review Notes: Apple Music subscription instructions pasted
[ ] Release option chosen (Manual recommended for v1)
[ ] Export compliance / IDFA questions answered
[ ] Submitted → status "Waiting for Review"
```

## Related

- [[testflight-upload]] — archive + upload the build (the steps before this note)
- [[instruments-profiler]] — profiling before you ship
- [[Projects/Culla-Music/culla-music|Culla Music]] — the app we're shipping
- [[Xcode]] — index
