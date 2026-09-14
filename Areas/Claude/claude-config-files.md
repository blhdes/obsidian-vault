---
title: Claude config files — cheat sheet
date: 2026-04-24
tags: [claude, config, meta, reference]
---

# 🗂️ Claude config files on this Mac

Quick map of every file that shapes Claude's behavior — where it lives, what it does, and the scope it applies to.

## TL;DR — the scope ladder

Later layers override earlier ones.

1. **User-global** (every project) → `~/.claude/`
2. **Project-shared** (checked into git) → `<project>/CLAUDE.md`
3. **Project-local** (private, gitignored) → `<project>/CLAUDE.local.md` or `<project>/.claude/`

---

## Claude Code (CLI)

| File | Path on this Mac | What it does |
|---|---|---|
| **Global instructions** | `~/.claude/CLAUDE.md` | Your personal "manifesto" — tone, code standards, workflow. Auto-loaded in **every** Claude Code session. |
| **Global settings** | `~/.claude/settings.json` | CLI config: model, plugins, effort level, notifications, remote control. Currently: `model=opus`, `effortLevel=xhigh`, plugin `swift-lsp` enabled. |
| **Session state** | `~/.claude.json` | Claude Code's internal state — recent projects, auth cache, onboarding flags. Managed by the CLI; don't hand-edit. |
| **Skills** | `~/.claude/skills/<name>/SKILL.md` | Custom reusable skills, auto-discovered in every chat. You have: `obsidian-vault`. |
| **Plans** | `~/.claude/plans/*.md` | Plan files written during `/plan` mode. |
| **Plugins** | `~/.claude/plugins/` | Installed plugins + marketplace cache. |
| **Per-project memory** | `~/.claude/projects/<encoded-path>/` | Auto-memory + sessions for a specific project directory. Your Claude folder's memory lives at `~/.claude/projects/-Users-agomezu-Claude/memory/`. |

## Claude Desktop (app)

| File | Path on this Mac | What it does |
|---|---|---|
| **MCP servers** | `~/Library/Application Support/Claude/claude_desktop_config.json` | Declares MCP (Model Context Protocol) servers the **desktop app** can connect to — e.g. filesystem, Gmail, Drive. Restart the app after editing. |
| **App config** | `~/Library/Application Support/Claude/config.json` | Desktop app preferences (managed by the app UI). |

> ⚠️ `claude_desktop_config.json` only affects the **desktop app**, not the CLI. The CLI configures MCP servers via its own `settings.json` or `/mcp` command.

## Per-project files

Drop these inside any project folder (e.g. `~/Claude/culla-app/`):

| File | What it does | Commit to git? |
|---|---|---|
| `CLAUDE.md` | Project-specific instructions: architecture, build commands, conventions. Auto-loaded when Claude runs in this project. | ✅ yes — shared with the team |
| `CLAUDE.local.md` | Personal overrides (experimental rules, WIP notes, secrets guidance). | ❌ no — gitignore it |
| `.claude/settings.json` | Project-scoped CLI settings (permissions, hooks, env vars). | Usually yes |
| `.claude/settings.local.json` | Your personal per-project settings. | ❌ no |

### Real examples in `~/Claude/`

- `~/Claude/Obsidian/CLAUDE.md` — vault write-conventions for Claude
- `~/Claude/asset.cafe/CLAUDE.md` + `~/Claude/asset.cafe/.claude/CLAUDE.local.md`
- `~/Claude/village/CLAUDE.md`

---

## How they load (mental model)

When you run Claude Code in a project, it stacks configs like this:

```
~/.claude/CLAUDE.md              ← you (global)
        ↓
~/.claude/settings.json          ← your CLI defaults
        ↓
<project>/CLAUDE.md              ← project (team)
        ↓
<project>/CLAUDE.local.md        ← project (you only)
        ↓
<project>/.claude/settings.*     ← project settings
```

The deeper file **wins** when rules conflict.

## Quick edit shortcuts

- **Change tone / coding style everywhere** → edit `~/.claude/CLAUDE.md`
- **Switch model / effort level** → edit `~/.claude/settings.json` or run `/config` / `/model`
- **Add a new skill** → `mkdir ~/.claude/skills/<name>/` + write `SKILL.md`
- **Add project instructions** → create `CLAUDE.md` at the project root
- **Add MCP servers to the desktop app** → edit `~/Library/Application Support/Claude/claude_desktop_config.json`, then restart Claude Desktop

## Related notes

- [[Areas/Claude/Skills/Docs/obsidian-vault]]
- [[Home]]
