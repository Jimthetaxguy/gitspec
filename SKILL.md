---
name: build-md
description: >
  Repo-native project management meta-skill for multi-agent, multi-user codebases. 
  Works across Claude Code, Cursor, Codex, GitHub Copilot, and VS Code agents. 
  Use when setting up a new project, initializing documentation infrastructure, 
  onboarding a contributor (human or agent), or when anyone asks about project planning, 
  specs, stories, change tracking, documentation-driven development, or work visualization. 
  Triggers on "init", "build.md", "scaffold", "set up my repo", "project management", 
  "track work", "documentation structure", "how should we organize this project", 
  "add a story", "new spec", or any mention of repo-native PM. This is the first skill 
  to reach for when starting any new project or onboarding into an existing one.
---

# Build.MD — Repo-Native Project Intelligence

Build.MD turns your Git repository into a complete project management system that every 
AI coding agent and every human contributor understands natively. No Jira. No ADO. No 
context switching. Your specs, stories, decisions, and progress live next to your code — 
versioned, reviewable, and machine-readable.

## The Core Idea

The repo is the single source of truth. Specs, stories, and notes are structured Markdown 
with YAML frontmatter. Git history is the changelog. Commit trailers link every change to 
the work it implements. Agent config files teach every AI tool on your team the same 
conventions. A lightweight local applet renders all of this visually — but the applet has 
no data of its own. If it dies, nothing is lost.

## Architecture: Nine Layers

### Layer 0 — Dual Config Targets

AGENTS.md is now an official standard under the Linux Foundation's Agentic AI Foundation 
(donated Dec 2025, alongside Anthropic's MCP and Block's Goose). It's the universal 
instruction file format — Codex reads it natively, and it's converging as the cross-tool 
standard. Build.MD uses AGENTS.md as the canonical source and generates platform-specific 
adapters where needed.

| Agent / Tool | Config File | How It Works |
|---|---|---|
| OpenAI Codex | `AGENTS.md` at root | **Native** — reads AGENTS.md directly with hierarchical discovery |
| Claude Code | `CLAUDE.md` + `.claude/skills/` | Adapter — references AGENTS.md |
| Cursor | `.cursor/rules/*.mdc` | Adapter — modern .mdc files with YAML frontmatter (`description`, `alwaysApply`, `globs`) |
| GitHub Copilot | `.github/copilot-instructions.md` | Adapter — references AGENTS.md |
| VS Code Agent | `.vscode/instructions.md` | Adapter — references AGENTS.md |
| Gemini CLI / Others | `AGENTS.md` at root | Native — reads AGENTS.md directly |

**Important design principle:** Research shows that LLM-auto-generated AGENTS.md files 
actually *reduce* task success vs developer-written ones (by 2-4 extra steps per task, 
20-23% higher inference cost with no quality benefit). Build.MD's init flow generates a 
*structured template* with the right sections and vocabulary, but leaves content decisions 
to the human. The agent fills in the scaffolding; the developer fills in the substance.

One source of truth, many projections. Never duplicate maintenance.

### Layer 1 — The Init Skill

On first run, the init skill bootstraps the contributor into the repo's contract through 
a guided conversation. It covers:

- Directory schema (where specs, stories, notes live)
- Status vocabulary (the only valid values for `status:` frontmatter)
- Commit trailer convention (`Story:`, `Spec:`, `Closes:`)
- Note-taking contract (raw daily notes → distilled ADR before PR)
- How to invoke the local applet

The init skill is intentionally generic — it describes the *pattern*, not any specific 
project's content. Project-specific context lives in a separate layer.

To run init, read `skills/init-interview.md` and follow its interview flow.

### Layer 2 — Multi-Agent / Multi-User Contributor Model

Multiple humans and multiple agents work in parallel without stomping each other.

**Ownership namespacing:**
```
docs/notes/{contributor}/          ← human contributors
docs/notes/agents/{agent-id}/      ← agent sessions
docs/stories/                      ← shared, owned by PR author
docs/specs/                        ← shared, gated by review
```

**Conflict resolution** uses frontmatter locking:
```yaml
locked_by: "agent:claude-session-abc123"
locked_at: "2026-04-22T23:00:00Z"
```

Lock TTL is configurable (default 30 minutes). Force-unlock via commit trailer.

### Layer 3 — Appended Rules Pattern

Instead of one monolithic instruction file, Build.MD uses append-only rule blocks:

```
AGENTS.md                         ← root invariants (never modified after init)
.agents/rules/01-stories.md       ← story authoring rules
.agents/rules/02-commits.md       ← commit convention rules
.agents/rules/03-notes.md         ← note-taking rules
.agents/rules/04-distillation.md  ← ADR synthesis rules
.agents/rules/05-visualization.md ← applet interaction rules
.agents/rules/06-principles.md    ← co-build principles (auto-updated)
```

Each platform adapter assembles these blocks in its own format. Adding a new rule never 
touches existing files — clean, reviewable Git history.

### Layer 4 — Change Ledger (Two-Phase IDs, Signal Filtering)

The ledger at `.ledger/changes.json` is a machine-readable record of significant changes:

- **Pending phase** (branches): IDs are `CHG-PENDING-{shortHash}` — allows parallel agents to write without collision
- **Finalized phase** (main): IDs are reassigned to sequential `CHG-0001`, `CHG-0002`, etc.
- **Signal filtering**: Commit type → signal mapping (feat/fix → critical, perf/refactor → notable, test → conditional)
- **Exclusions**: chore, style, ci, build commits are not recorded

Run `scripts/ledger-update.py --finalize` on main branch after merging to convert all pending IDs.

Read `scripts/ledger-update.py` for implementation and usage.

### Layer 5 — Documentation + Git as the Visualization Backend

The local applet reads directly from:

1. **Git history** — `git log` with structured output
2. **Frontmatter YAML** — story status, priority, assignments
3. **Commit trailers** — `Story:` and `Spec:` trailers
4. **ADR files** — decision history

No separate database. The applet is a thin rendering layer over repo data.

**Local applet components:**

| Component | Purpose |
|---|---|
| HTTP file server | Serves board over localhost to bypass CORS |
| Manifest builder | Walks docs/, parses frontmatter, writes manifest JSON |
| WebSocket bridge | Watches filesystem, pushes diffs to board |

### Layer 6 — Spec & Code Traceability (rnpm[...] Annotations, graph.json)

Annotations in source code link implementation back to specs:

```python
# rnpm[impl SPEC-AUTH-003]     — implements the spec
# rnpm[verify SPEC-AUTH-003]   — test verifies the spec
# rnpm[risk SPEC-AUTH-003]     — known risk related to spec
# rnpm[depends SPEC-AUTH-003]  — code depends on spec
```

The `scripts/build-graph.py` script scans source files, stories, specs, and the ledger
to generate `.ledger/graph.json` — a complete traceability graph with nodes and edges.

Read `templates/rules/07-annotations.md` for annotation rules and `scripts/build-graph.py`
for graph generation.

### Layer 7 — HTML Kanban & Sync

The local applet renders the board over localhost:

```bash
python scripts/serve.py
# Opens http://localhost:3000 with live dashboard
```

Reads directly from .ledger/, docs/, and git history. No separate state.

### Layer 8 — Report Generation (Change Reports, Acknowledgment Summaries)

Generate reports spanning commits, specs, and stories:

```bash
python scripts/generate-report.py --from v1.0 --to HEAD
```

Output includes change summaries, acceptance criteria, and acknowledgment templates
for changelog/marketing.

Read `scripts/generate-report.py` for implementation.

### Layer 9 — The Principles Engine

Build.MD ships with curated best practices from leading AI companies and researchers, 
organized by domain. A refresh script pulls updates on a schedule.

Read `principles/PRINCIPLES.md` for the full catalog. Read `scripts/refresh-principles.py` 
for the update mechanism.

## Getting Started

### Install

```bash
# Option 1: One-line install
curl -fsSL https://raw.githubusercontent.com/org/build-md/main/scripts/install.sh | bash

# Option 2: Clone as template
degit org/build-md .build-md && .build-md/scripts/install.sh

# Option 3: Claude Code skill
claude install-skill https://github.com/org/build-md
```

The installer:
1. Detects which agent tools are present
2. Writes only the adapters for installed tools
3. Symlinks hooks into `.git/hooks/`
4. Creates the canonical `AGENTS.md`
5. Builds the initial manifest so the applet works immediately

### Initialize

Tell your agent: **"Run build-md init"**

This triggers the interview flow in `skills/init-interview.md`. The agent asks about your 
project, team, workflow preferences, and enforcement level. Based on answers, it generates 
everything.

### Day-to-Day Usage

Once initialized, the system is mostly invisible. You write code, commit with trailers, 
and the hooks + ledger script handle the rest. When you want to see progress:

```bash
# Open the dashboard
python scripts/serve.py
# or
open applets/dashboard.html  # (limited without server)

# Generate a change report
python scripts/generate-report.py --from v1.0 --to HEAD

# Refresh best practices
python scripts/refresh-principles.py
```

## Enforcement Levels

| Level | Who It's For | What It Enforces |
|---|---|---|
| **Gentle** | Solo projects, prototypes | Warnings only, trailers suggested |
| **Standard** | Teams (default) | feat/fix require Story:/Spec: trailer, daily notes required |
| **Strict** | Regulated, high-traceability | All of Standard + CI schema validation + distillation required before merge |

## Reference Files

Read these as needed — they contain the detailed implementation for each component:

| File | What It Contains |
|---|---|
| `skills/init-interview.md` | The full Q&A flow for project initialization |
| `templates/AGENTS.md.template` | The canonical agent instruction template |
| `templates/adapters/` | Platform-specific adapter templates |
| `templates/schemas/` | JSON Schemas for story, spec, ADR frontmatter |
| `templates/hooks/` | Git hook scripts |
| `templates/rules/` | The append-only rule block templates |
| `principles/PRINCIPLES.md` | Curated best practices catalog |
| `scripts/` | All automation (install, serve, ledger, refresh, report) |
| `applets/dashboard.html` | The self-contained progress dashboard |
