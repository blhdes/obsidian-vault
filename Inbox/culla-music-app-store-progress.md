---
title: Culla Music — App Store submission progress
date: 2026-06-06
tags: [culla-music, app-store, shipping, progress]
---

# Culla Music — App Store submission progress

Where we are in getting **Culla Music** onto the App Store. Picking this up tomorrow.
(Filed in Inbox — move to `Projects/Culla-Music/Phases/` if you want it with the rest.)

## ✅ Done (code side is basically finished)

- **Privacy manifest** — added `CullaMusic/CullaMusic/PrivacyInfo.xcprivacy`. Declares: no tracking, no data collected, one required-reason API (`UserDefaults` via `@AppStorage`, reason `CA92.1`). Validated.
- **Privacy policy URL** — already live at `culla.app/music`. It matches the manifest (no data collected). *Tip: if the site has an anchor that jumps straight to the privacy section, paste that exact URL into App Store Connect.*
- **Bundle ID renamed** — `agu.CullaMusic2` → **`app.culla.music`** (both Debug + Release). No code referenced the old ID.
  - New App ID was **created manually** in the Developer portal with **MusicKit enabled** — catalog requests verified working on device. Description field = "Culla Music".
  - Distribution cert (team `56BK7T2JG7`) is present, so the submission signing path is fine.
- **iOS floor decided** — keeping **iOS 17**, NOT raising to 26. The pre-iOS-26 (non-glass) fallback was reviewed on-device and looks good.
  - Added a debug switch to preview it: `Helpers/DebugFlags.swift` → flip `previewLegacyUI` to `true`, build, look around, flip back. It's `#if DEBUG`-wrapped, so it can never ship enabled.
- **Launch screen** — already auto-generated (`UILaunchScreen_Generation = YES`). Nothing to do.

## ⏳ Left to do — all in App Store Connect (mostly web work)

1. **Create the app record** in App Store Connect on bundle ID `app.culla.music`.
2. **Screenshots** — 6.9" iPhone size is required (6.5" optional).
3. **Listing text** — name, subtitle, description, keywords. ← *Claude offered to draft this.*
4. **Privacy questionnaire** — answer **"Data Not Collected"** so it matches the manifest + policy.
5. **Age rating** + **category** (Music).
6. **Reviewer notes** — must flag: app needs Apple Music authorization, and it still works **without** an Apple Music subscription (30s previews). Prevents a Guideline 2.1 rejection if the reviewer tests on a non-subscriber account. ← *Claude offered to draft this.*
7. **Archive** (Release) in Xcode → upload → submit (TestFlight first is optional but recommended).

## ▶️ Next action for tomorrow

Have Claude **draft items #3 (listing text + keywords) and #6 (reviewer notes)** so they can be pasted straight in. Then move on to screenshots + the App Store Connect record.

## Notes / gotchas to remember
- MusicKit capability is **per-App-ID** — that's why the new bundle ID needed it re-enabled. Don't be surprised if anything else App-ID-scoped needs re-doing.
- Don't touch signing unless catalog requests actually 404 — it works as-is.
