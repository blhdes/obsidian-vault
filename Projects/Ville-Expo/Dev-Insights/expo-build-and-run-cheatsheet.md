---
title: Expo — Build & Run on iPhone Cheatsheet
date: 2026-05-19
tags: [expo, ios, iphone, build, dev-insight, cheatsheet]
---

# Expo — Build & Run on iPhone Cheatsheet

Quick reference for building and running **Ville Expo** on a physical iPhone with `npx expo`, plus how to nuke caches when things go weird. The project uses a **dev client** (not Expo Go) because `ios/` is checked in and `expo-dev-client` is a dependency.

> Run everything from the repo root: `cd /Users/agomezu/Claude/ville-du-cinema-mobile`

## TL;DR — daily workflow

```bash
# 1. iPhone plugged in via USB, unlocked, "Trust this computer" accepted.
# 2. Build + install the dev client on the device (only needed when native code changed):
npx expo run:ios --device

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
xcrun simctl list devices    # list available iOS simulators
xcrun xctrace list devices   # list connected physical devices
```

## Related

- [[Ville-Expo]] — project index.
