---
title: Gym Rest Timer App — Hands-Free iOS Idea
date: 2026-04-27
tags: [idea, ios, swift, app]
---

# Gym Rest Timer App

## The Problem
Built-in gym timers are too manual and keep the screen on, draining battery. No good app currently combines hands-free control + battery efficiency.

## Core Idea
A rest timer app you control without touching your phone — via voice or headphone gestures — while the countdown shows on the Dynamic Island or Lock Screen so the screen stays off.

## Key Features
- **Live Activities (ActivityKit):** Timer displayed in Dynamic Island (iPhone 14 Pro+) or Lock Screen banner (older devices, iOS 16.1+) — no screen needed
- **Voice commands:** `SFSpeechRecognizer` for on-device "go" / "stop" keywords, or `App Intents` for "Hey Siri, start rest timer"
- **Headphone gesture detection:** Intercept play/pause events via `AVAudioSession` as a trigger
- **Music-safe audio beeps:** `AVAudioSession` with `.mixWithOthers` so the end-of-rest beep doesn't stop the music

## Tech Stack
| Need | API |
|---|---|
| Glanceable timer (no screen) | ActivityKit / Dynamic Island |
| Voice trigger | SFSpeechRecognizer or App Intents |
| Headphone button detection | AVAudioSession |
| Beep without stopping music | AVAudioSession `.mixWithOthers` |
| UI | SwiftUI |

## Market Gap
Apps like *Seconds Pro* and *Rest Timer* exist but none combine:
- Dynamic Island countdown
- Voice trigger
- Music-safe audio

## Requirements
- iOS 16.1+ minimum (Live Activities)
- Dynamic Island on iPhone 14 Pro+ / iPhone 16 Pro+
- Lock Screen banner fallback for all other supported devices
