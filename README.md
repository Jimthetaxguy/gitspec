# Build.MD

**Repo-native project management for multi-agent, multi-user codebases.**

Build.MD turns your Git repository into a complete project management system. Specs, stories, decisions, and progress tracking live next to your code — versioned, reviewable, and readable by every AI coding agent on your team.

No Jira. No ADO. No context switching.

## Quick Start

```bash
# Install into any project
curl -fsSL https://raw.githubusercontent.com/Jimthetaxguy/build-md/main/scripts/install.sh | bash

# Then tell your agent:
# "Run build-md init"
```

The init flow asks about your project, team, and workflow preferences, then generates everything: agent configs, documentation structure, enforcement hooks, and a local dashboard.

## What It Does

Build.MD is a **meta-skill** — it teaches AI coding agents and human contributors the same project management conventions through a shared contract.

- **AGENTS.md** as the canonical instruction file (Linux Foundation standard, native to Codex)
- **Platform adapters** for Claude Code, Cursor (.mdc), GitHub Copilot, and VS Code
- **Structured Markdown** with YAML frontmatter for specs, stories, notes, and decisions
- **Git hooks** that enforce commit conventions and trailer requirements
- **A change ledger** that auto-generates a traceable record of significant changes
- **Source code annotations** (`rnpm[impl SPEC-ID]`) for spec-to-code traceability
- **A local dashboard** that visualizes project state from repo data — no external database
- **24 curated principles** from Anthropic, OpenAI, Google, NVIDIA, Meta, Microsoft, xAI, SSI, and more

## Architecture

Build.MD uses a nine-layer architecture. See [SKILL.md](SKILL.md) for the full technical spec.

| Layer | What It Does |
|-------|-------------|
| 0 | Dual config targets (AGENTS.md + platform adapters) |
| 1 | Init skill (guided Q&A to bootstrap the repo contract) |
| 2 | Multi-agent contributor model (ownership namespacing, locking) |
| 3 | Appended rules pattern (append-only rule blocks, never edit existing) |
| 4 | Change ledger (two-phase IDs, signal filtering, append-only JSON) |
| 5 | Documentation + Git as visualization backend |
| 6 | Spec & code traceability (rnpm[...] annotations, graph.json) |
| 7 | HTML Kanban & sync (local dashboard over localhost) |
| 8 | Report generation (change reports, acknowledgment summaries) |

## Slash Commands

| Command | What It Does |
|---------|-------------|
| `/new-story "title"` | Scaffold a story with auto-incremented ID |
| `/new-spec "domain" "title"` | Scaffold a spec with domain-scoped ID |
| `/distill STORY-NNN` | Synthesize raw notes into an ADR |
| `/status-check` | Health check — orphaned TODOs, missing trailers, stale stories |
| `/pr-prep` | Distill notes + generate PR description + validate trailers |

## Agent Compatibility

| Agent | Config File | Status |
|-------|------------|--------|
| OpenAI Codex | `AGENTS.md` | Native (reads directly) |
| Claude Code | `CLAUDE.md` + `.claude/skills/` | Adapter |
| Cursor | `.cursor/rules/*.mdc` | Adapter |
| GitHub Copilot | `.github/copilot-instructions.md` | Adapter |
| VS Code | `.vscode/instructions.md` | Adapter |
| Gemini CLI | `AGENTS.md` | Native |

## Enforcement Levels

| Level | For | What It Enforces |
|-------|-----|-----------------|
| Gentle | Solo projects | Warnings only |
| Standard | Teams | feat/fix require Story:/Spec: trailers, daily notes required |
| Strict | Regulated domains | All of Standard + CI schema validation + distillation before merge |

## Principles

Build.MD ships with 24 curated principles from leading AI companies and researchers. They're embedded into agent configs during init and updated via `scripts/refresh-principles.py`.

Sources include: Anthropic (Dario Amodei), OpenAI (Sam Altman), NVIDIA (Jensen Huang), xAI (Elon Musk), Google DeepMind, Meta FAIR, Microsoft (Satya Nadella), SSI (Ilya Sutskever), Andrej Karpathy, LangChain, Ramp, Replit, Harvey AI, ToltIQ, Hebbia, and Sakana AI.

## Repository

**GitHub:** [github.com/Jimthetaxguy/build-md](https://github.com/Jimthetaxguy/build-md)

## License

[MIT](LICENSE)
