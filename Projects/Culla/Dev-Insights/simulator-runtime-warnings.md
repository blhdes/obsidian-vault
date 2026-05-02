---
title: Harmless Xcode Simulator Runtime Warnings
date: 2026-05-02
tags: [culla, xcode, simulator, debugging]
---

A common set of warnings in the Xcode console during simulator runs — all harmless. Safe to ignore unless they appear on a real device.

## Simulator-only noise

These come from system services the simulator doesn't fully support:

- `com.apple.accounts Code=7` — simulator can't access real account services
- `RBSServiceErrorDomain "Client not entitled"` / `elapsedCPUTimeForFrontBoard` — RunningBoard process monitoring doesn't work in the simulator
- `usermanagerd.xpc was invalidated` — user management service not available in sim
- `LaunchServices: process may not map database` — sandbox restriction, doesn't happen on real devices

## RevenueCat "No packages found" warning

```
WARN: No packages could be found for offering with identifier Culla Pro
```

Expected in development. StoreKit products aren't configured for the sandbox/simulator. Works fine in TestFlight and production once live.

## UIHostingController subview warnings

```
Adding 'UIKitToolbar' / '_UIReparentingView' as a subview of UIHostingController.view is not supported
```

Triggered by Apple's own system UI (share sheet, context menus). Not caused by our code, can't be fixed from our side. Common in any SwiftUI app that uses `.sheet` with UIKit-backed content.

## Image decompression errors

```
Error -17102 decompressing image -- possibly corrupt
```

Some test photos in the simulator library have unsupported or corrupt data. ImageIO logs this but falls back gracefully. Doesn't appear with real photos on a real device.

## Context menu warning

```
Called -[UIContextMenuInteraction updateVisibleMenuWithBlock:] while no context menu is visible
```

Spurious UIKit log, likely from the share sheet or a system context menu interaction. Harmless.

## Rule of thumb

If any of these appear on a **real device** during TestFlight, investigate. In the simulator, ignore them.
