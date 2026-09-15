---
title: Expo — Build & Run on iPhone Cheatsheet
date: 2026-09-15
tags: [expo, ios, iphone, build, dev-insight, cheatsheet]
---

# Expo — Build & Run on iPhone Cheatsheet

Quick reference for building and running **Ville Expo** on a physical iPhone with `npx expo`, plus how to nuke caches when things go weird. The project uses a **dev client** (not Expo Go) because `ios/` is checked in and `expo-dev-client` is a dependency.

> Run everything from the repo root: `cd /Users/agomezu/Claude/ville-du-cinema-mobile`

## TL;DR — daily workflow

```bash
# 1. iPhone reachable — either plugged in via USB (unlocked, "Trust this computer"
#    accepted) OR already paired for wireless debugging over the same Wi-Fi
#    (check with `xcrun devicectl list devices` — paired devices show as
#    `available (paired)` with no cable needed).
# 2. Build + install the dev client on the device (only needed when native code changed).
#    Name the device if more than one shows up in devicectl:
npx expo run:ios --device "Alejandro"

# 3. After that, just start Metro and open the app on the phone:
npx expo start --dev-client
```

Once the dev client is installed on the iPhone, you only need step 3 day-to-day. JS changes hot-reload — no rebuild needed.

## First-time setup on a new iPhone

1. Plug the iPhone into the Mac via USB.
2. On the iPhone: tap **Trust** when prompted.
3. Open Xcode once → **Settings → Accounts** → sign in with your Apple ID so signing works.
4. Open `ios/villeducinemamobile.xcworkspace` in Xcode once → select your dev team under **Signing & Capabilities** for the main target.
5. Run the build:
   ```bash
   npx expo run:ios --device
   ```
   First run takes 5–15 min (compiles all pods + native code).
6. On the iPhone: **Settings → General → VPN & Device Management → trust the developer certificate**.

## Common commands

| Command | What it does |
|---|---|
| `npx expo run:ios --device` | Build native app + install on connected iPhone. Use when native deps change or after `prebuild`. |
| `npx expo run:ios` | Same, but for the iOS Simulator. |
| `npx expo start --dev-client` | Start Metro bundler for the installed dev client. JS-only changes. |
| `npx expo start --dev-client -c` | Same, but clears Metro cache (`-c` = `--clear`). Try this when JS changes don't show up. |
| `npx expo start --dev-client --tunnel` | Use a tunnel if Mac & iPhone aren't on the same Wi-Fi. |
| `r` (in Metro terminal) | Reload the app. |
| `j` (in Metro terminal) | Open the JS debugger. |

## When to rebuild vs. just reload

- **Changed JS / TSX / styles** → just save the file. Fast Refresh handles it.
- **Changed `app.json`, added a native module, edited `ios/` or `android/`** → rerun `npx expo run:ios --device`.
- **Bumped Expo SDK or anything in `package.json` `dependencies` that's native** → clean rebuild (see below).

## Clean rebuild — from least to most nuclear

Go down the list only as far as you need to. Each step is more destructive than the previous.

### 1. Clear Metro / JS cache

Most "stale JS" or "weird import error" issues are fixed here.

```bash
npx expo start --dev-client -c
# also helpful:
watchman watch-del-all
rm -rf $TMPDIR/metro-*
```

### 2. Clean iOS native build

Use this when the bundle compiles but the iOS app crashes on launch or pods feel off.

```bash
rm -rf ios/build
rm -rf ~/Library/Developer/Xcode/DerivedData
cd ios && pod deintegrate && pod install && cd ..
npx expo run:ios --device
```

### 3. Reinstall node_modules

When `npm install` complains, lockfile drifted, or imports resolve weirdly.

```bash
rm -rf node_modules package-lock.json
npm install
cd ios && pod install && cd ..
npx expo run:ios --device
```

### 4. ☢️ Full nuke (regenerate native projects)

**Only when nothing else works.** `prebuild --clean` regenerates `ios/` and `android/` from `app.json` + config plugins. **This project has a committed `ios/` folder and `patches/` — running this will overwrite manual native tweaks.** Make sure git is clean first so you can diff.

```bash
git status                       # confirm clean working tree
rm -rf node_modules
npx expo prebuild --clean        # regenerates ios/ and android/
npm install
npx expo run:ios --device
```

After this, review `git diff ios/` carefully and restore anything intentional.

## Troubleshooting quick hits

| Symptom | Try |
|---|---|
| `iPhone is not connected` | Unlock the phone, replug USB cable, accept "Trust this computer". |
| `No development team selected` | Open `ios/*.xcworkspace` in Xcode → Signing & Capabilities → pick a team. |
| `Untrusted Developer` on iPhone | iPhone → Settings → General → VPN & Device Management → trust your cert. |
| App opens but shows red screen / module not found | `npx expo start --dev-client -c` (step 1 clean). |
| Pods error during build | Step 2 clean. |
| `Unable to resolve module` after dep change | Step 3 clean. |
| Native crash right after splash on a fresh SDK bump | Step 4 nuke. |

## Useful sanity-check commands

```bash
npx expo-doctor          # checks SDK / package versions for known issues
npx expo install --check # flags packages that don't match the installed Expo SDK
npx tsc --noEmit          # typecheck before rebuilding — catches errors in seconds instead of after a 10+ min native build
npx jest                  # run the test suite
xcrun simctl list devices    # list available iOS simulators
xcrun xctrace list devices   # list connected physical devices (USB)
xcrun devicectl list devices # list connected/paired physical devices, USB or same-Wi-Fi wireless debugging — shows name, hostname, pairing state. Preferred over xctrace: this is how "Alejandro" (wireless, no cable) showed up as `available (paired)` on 2026-09-15.
```

## Dependency health check (do this before a rebuild after time away)

After ~2 months dormant, `expo-doctor` found 17 packages behind their SDK 55 patch version **and** a missing `react-native-worklets` peer dependency that `react-native-reanimated` 4 needs outside Expo Go — expo-doctor called out that the dev-client build could crash without it. That's a different class of finding than a version mismatch, so don't skip past it.

```bash
npx expo install --check   # lists packages behind the installed SDK version (does not change anything)
npx expo-doctor             # broader health check — also catches missing peer deps expo install --check won't show
npx expo install <package>  # installs one missing SDK-compatible peer dep (e.g. react-native-worklets)
npx expo install --fix      # aligns every listed package to its SDK-expected version in one shot
npx expo-doctor             # re-run to confirm 20/20 (or however many) checks pass
```

**Gotcha:** `expo install --fix` can also move `jest`/`@types/jest` to the version the SDK template expects (in our case *down* from 30.x to 29.7 — the fix goes both directions, not just upward). If tests then fail with `'ts-node' is required for the TypeScript configuration files`, that's because jest 29 needs `ts-node` to parse `jest.config.ts` and jest 30 didn't — `npm install --save-dev ts-node` fixes it. Confirm afterward with `npx jest`.

If `npm install`/`expo install --fix` renames a patched package's version (e.g. `react-native` 0.83.2 → 0.83.10), `patch-package` will warn about a filename mismatch on the next install even though the patch still applies — rename the file under `patches/` to match (`mv patches/react-native+0.83.2.patch patches/react-native+0.83.10.patch`) so the warning stops recurring.

After any dependency change that touches native modules, do a clean prebuild before running on device (see "☢️ Full nuke" below) rather than trusting the existing `ios/` folder — a new native module (like `react-native-worklets`) needs to be linked into the Xcode project, which only `prebuild` does.

## Agentic / scripted builds — backgrounding gotchas

Lessons from running this whole loop unattended via Claude Code in one session (2026-09-15). A clean `expo run:ios --device` after `prebuild --clean` took ~15–20 min (compiling every native pod from scratch); an incremental rebuild after a JS/TSX-only change took under 2 min. Plan polling intervals accordingly.

- **Never background a long build with a manual trailing `&` inside the command string, even under a tool that also has its own "run in background" option.** Doing both at once means the tool's own process tracker sees the *wrapper* (which returns instantly after backgrounding) exit immediately and reports "completed" — while the real `xcodebuild`/`expo run:ios` process is still running, detached, for real, for another 15 minutes. Confirmed the process was still alive with `ps aux | grep xcodebuild` after a premature "completed" notification. **Fix:** pass the plain command (redirecting to a log file if you want, e.g. `npx expo run:ios --device "Alejandro" > build.log 2>&1`) and let the tool's own backgrounding flag manage the process — don't add `&`/`disown` yourself.
- **Poll with `ps aux | grep xcodebuild` + `tail -N build.log`** rather than blocking on the whole thing. `xcodebuild`'s own stdout is line-buffered per compiled file, so `tail` gives real incremental progress, not just a final dump.
- **`expo run:ios` reuses an already-running Metro bundler on port 8081 instead of starting its own** (logs `› Skipping dev server` when it finds one). This means a second `expo run:ios --device` invocation, run while an earlier one's Metro is still up, will NOT spin up an independent instance — there's only one Metro serving the device. **Don't kill "leftover" `node .../expo` processes without first checking `lsof -i :8081`** — one of them is very likely the live JS server the already-installed dev-client app needs to load anything at all. Killing it doesn't crash the app immediately, but it can't fetch a bundle until Metro is back — confirmed this by accidentally killing it mid-session and having to restart with `npx expo start --dev-client` (properly backgrounded this time) before the app could do anything.
- **Typecheck before every rebuild**: `npx tsc --noEmit` takes seconds and catches most mistakes that would otherwise only surface after the full native build finishes. Diff its output against a baseline run (e.g. `git stash` + rerun) to separate pre-existing errors from ones you just introduced, rather than assuming every reported error is new.

## Related

- [[Ville-Expo]] — project index.
- [[Projects/Ville-Expo/Phases/phase-07-social-polish-reposts-and-reliability]] — the session that produced the lessons above.
