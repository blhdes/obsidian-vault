---
title: career-launch skill
date: 2026-09-14
tags: [claude, skill, career, portfolio, meta]
---

# 🚀 `career-launch` skill

Drives the multi-month push to land a creative job abroad (~Dec 2026–Feb 2027): the portfolio website, new work to show, and the job-search/relocation plan — plus a separate, parallel local-stability track (Spanish oposiciones). Stateful: the Obsidian vault is the source of truth, not the skill file.

## Where it lives

```
~/.claude/skills/career-launch/SKILL.md
```

## How to invoke

**Auto-fires** on trigger phrases — no need to type the command name every time. Triggers include: `/career-launch`, `/career`, `/portfolio`, "work on the portfolio", "next chapter", "job search", "apply abroad", "moving to Paris/Amsterdam", "what's next for the portfolio", "oposiciones", "temario", "función pública", or any reference to `Projects/Portfolio/` or `Areas/Oposiciones/`.

## What it does

1. **Always reads state first** — `Projects/Portfolio/Portfolio.md` (and `Areas/Oposiciones/Oposiciones.md` when that track is active) before saying anything, then gives a 1–2 line recap and waits for a go-ahead.
2. **Coordinates three connected workstreams** toward the abroad goal:
   - **A. Portfolio website** — `~/Claude/portfolio/`, live at alegomez.studio.
   - **B. New work to show** — apps (Culla, CullaMusic live; Doppio/Warket/Village in the pipeline) + the fashion brand (~Aug–Sep 2026) + curated photography/cinema.
   - **C. Job search & relocation** — a 5-phase pipeline in `Job-Search/`, worked one city/industry per session, never all at once.
3. **Plus a fourth, separate track: oposiciones** — a Spanish civil-service exam pursued as a local safety net, explicitly *not* blended into the abroad pitch.
4. **Holds tone constraints** — this work has scared the user before, so every step stays small, concrete, and confidence-building; no overselling his level.

## When NOT to use it

- Generic Swift/app coding on Culla/CullaMusic/Doppio/etc. that isn't about *positioning* them for the portfolio → just work on the app directly.
- One-off oposiciones study questions unrelated to tracking progress → answer directly; the skill's job is state-tracking and pacing, not being the only way to discuss the exam.

## Backup

`SKILL.md` is mirrored at [[../backup/README|Areas/Claude/Skills/backup/career-launch/]], last synced **2026-09-14**. Re-copy it there after any real change to this skill.

## Related notes

- [[../_index|_index]] — Claude skills index
- [[../../../../Projects/Portfolio/Portfolio|Portfolio project hub]]
- [[../../../../Areas/Oposiciones/Oposiciones|Oposiciones hub]]
