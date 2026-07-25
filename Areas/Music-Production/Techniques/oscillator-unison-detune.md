---
title: Oscillator Unison Detune
date: 2026-07-24
tags: [ableton, drift, sound-design, raw, detune, lead]
---

# Oscillator Unison Detune

Two oscillators playing the **same waveform, slightly out of tune with each other** (a few cents apart) beat against one another — the tiny, constantly-shifting phase difference between two near-identical waves is what reads as "raw," "analog," or "alive," as opposed to a single, mathematically pure oscillator which reads as clean/digital.

## Why this beats a post-effect for rawness

[[chorus-ensemble-width|Chorus-Ensemble]] fakes a similar effect by mixing the dry signal with a delayed, modulated copy — useful for width, but it's still fundamentally *one* waveform plus a processed echo of itself. True unison detune uses **two real oscillators actually generating sound simultaneously** inside the synth — the beating is native to the waveform itself, not a delay-line artifact. It tends to sound grittier and more physical, closer to real analog oscillator drift, than any effect placed after the fact.

## Applied — LEAD ([[../Track-Sketches/hardgroove-134|Hardgroove 134]])

The LEAD patch still sounded "too clean" after Saturator + Resonance + Phaser-Flanger were all already in the chain. The fix: **Osc 2 turned back on**, same waveform as Osc 1 (Sawtooth), **Detune ~5-15 cents**. This was the single change that actually delivered the raw/gritty character the previous effects-based attempts only partially achieved — confirming the "clean" quality was coming from the oscillator stage itself, not something fixable downstream.

## When to reach for this vs. other "grit" tools

- **Too clean/thin at the source** (a single oscillator sounds too pure) → Osc unison detune, at the instrument level.
- **Needs harmonic distortion/dirt** → Saturator, after the filter.
- **Needs width/thickness without changing pitch character** → Chorus-Ensemble, as an effect.

These stack, but if a patch still sounds too polished after Saturator/resonance, check the oscillator stage before adding more effects.
