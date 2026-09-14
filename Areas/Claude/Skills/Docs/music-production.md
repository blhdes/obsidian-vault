---
title: music-production skill
date: 2026-09-14
tags: [claude, skill, music, ableton, meta]
---

# 🎹 `music-production` skill

Resumes the beginner-to-mid electronic-music-production learning journey in Ableton Live. Stateful: the vault at `Areas/Music-Production/` is the source of truth, not the skill file — it reads progress first, teaches next, and saves the lesson before delivering it in chat.

## Where it lives

```
~/.claude/skills/music-production/SKILL.md
```

## How to invoke

**Auto-fires** on trigger phrases: `/music-production`, `/produce`, "next session", "session N", "continue the music journey", "back to the track", "let's keep working on the track", or any reference to producing in Ableton tied to `Areas/Music-Production/`.

## What it does

1. **Reads state first** — `Progress.md` (what's covered, where we left off, what's queued) and `Roadmap.md` (the 6 paths and their progress %) — then gives a tight 1–2 line recap and waits for a go-ahead before a full lesson.
2. **Calibrates teaching level to Progress.md** — anything already logged there is treated as known and used without re-explaining; only genuinely new concepts get a first-mention explanation. Mechanical step-by-steps are skipped for workflows the user has already done.
3. **Session structure**: one-line lead-in → the lesson (sectioned, diagrams/tables where useful) → 🎹 homework (5–15 min, concrete Ableton actions) → one-line tease for next time.
4. **Saves before teaching** — writes a content note into the right subfolder (`Ableton/`, `Theory-Basics/`, `Techniques/`, or `Track-Sketches/`) *before* delivering the chat lesson, so the work survives an interruption.
5. **Stays genre-neutral and technical** — no "YouTuber" framing, no railroading into one style; flags when a technique is style-specific.

## When NOT to use it

- The user explicitly wants **self-directed experimentation** instead of a guided lesson — periodically drop the tutorial structure and just log a Track-Sketch instead of teaching.
- A DJing/library question (Engine DJ, Mixxx, Soulseek imports) → that's [[download-music]] / [[tunebat]] territory, not production.

## Backup

`SKILL.md` is mirrored at [[../backup/README|Areas/Claude/Skills/backup/music-production/]], last synced **2026-09-14**. Re-copy it there after any real change to this skill.

## Related notes

- [[../_index|_index]] — Claude skills index
- [[../../../Music-Production/Progress|Music-Production Progress]]
- [[../../../Music-Production/Roadmap|Music-Production Roadmap]]
