# GitSpec

**Repo-native project management for multi-agent, multi-user codebases.**

GitSpec turns your Git repository into a complete project management system. Specs, stories, decisions, and progress tracking live next to your code — versioned, reviewable, and readable by every AI coding agent on your team.

No Jira. No ADO. No context switching.

---

## Requirements

- Git 2.9+ (for `core.hooksPath` support)
- Bash 4+
- Python 3.9+ (standard library only — no `pip install`)
- A modern browser (for the local dashboard)

GitSpec has **no runtime dependencies** beyond the above. No Node, no Docker, no package manager. Every file it installs is plain text or a standard-library Python script.

## Install

GitSpec installs from a local clone — it does not support `curl | bash` by design (the installer needs the templates, schemas, and scripts as siblings on disk to copy from). **Read the script before running it.**

```bash
git clone https://github.com/Jimthetaxguy/gitspec.git
cd gitspec

# Audit the installer (takes 5 minutes to read end-to-end):
less scripts/install.sh

# Preview every action without modifying anything:
./scripts/install.sh /path/to/your/project --dry-run

# Install:
./scripts/install.sh /path/to/your/project
```

Every install writes a timestamped receipt to `<target>/.gitspec-install-receipt.txt` listing every action taken. See [`SECURITY.md`](SECURITY.md) for the full safety model.

### Installer flags

| Flag | Purpose |
|---|---|
| `--dry-run` | Print the plan and exit without writing anything. |
| `--yes` / `-y` | Non-interactive. Required when stdin is not a TTY (e.g., CI). |
| `--no-hooks` | Skip Git hook installation. |
| `-h` / `--help` | Show help. |

## What It Does

GitSpec is a **meta-skill** — it teaches AI coding agents and human contributors the same project management conventions through a shared contract.

- **AGENTS.md** as the canonical instruction file (Linux Foundation standard, native to Codex)
- **Platform adapters** for Claude Code, Cursor (`.mdc`), GitHub Copilot, and VS Code
- **Structured Markdown** with YAML frontmatter for specs, stories, notes, and decisions
- **Git hooks** that enforce commit conventions and trailer requirements
- **A change ledger** that auto-generates a traceable record of significant changes
- **Source code annotations** (`rnpm[impl SPEC-ID]`) for spec-to-code traceability
- **A local dashboard** that visualizes project state from repo data — no external database
- **24 curated principles** from Anthropic, OpenAI, Google, NVIDIA, Meta, Microsoft, xAI, SSI, and more

## What It Does Not Do

Explicit non-goals. If a future version breaks any of these, that's a regression.

- **No network calls during install.** Installer reads/writes only in the local clone and target directory.
- **No telemetry.** GitSpec does not phone home. Ever.
- **No global configuration changes.** `git config` writes are repo-local. Shell configs (`.bashrc`, `.zshrc`) are not modified.
- **No external services.** No Jira, Linear, Slack, or webhook integrations. The repo is the only backend.
- **No binary artifacts.** Every tracked file is plain text.
- **No runtime dependencies beyond the requirements above.** No `pip install`, no `npm install`.

## Architecture

GitSpec uses a nine-layer architecture. See [SKILL.md](SKILL.md) for the full technical spec.

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
| `/onboard-agent` | Brief a fresh agent on the repo's conventions and current backlog |
| `/rebuild-ledger` | Re-derive `.ledger/changes.json` from git log when it has drifted |

Plus the global `/gitspec` skill — invoke from any Claude Code session to learn what GitSpec is, get install instructions, or see the architecture.

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

GitSpec ships with 24 curated principles from leading AI companies and researchers. They're embedded into agent configs during init and updated via `scripts/refresh-principles.py`.

Sources include: Anthropic, OpenAI, NVIDIA, xAI, Google DeepMind, Meta FAIR, Microsoft, SSI, Andrej Karpathy, LangChain, Ramp, Replit, Harvey AI, ToltIQ, Hebbia, and Sakana AI.

## Troubleshooting

**`ERROR: This installer cannot be run via 'curl | bash'`**
By design. Clone the repo first, then run `./scripts/install.sh`. See the [Install](#install) section.

**`ERROR: stdin is not a TTY`**
You're running in CI or piping input. Pass `--yes` for non-interactive mode, or `--dry-run` to preview.

**`ERROR: source tree incomplete — missing ...`**
The `gitspec` clone is missing files. Re-clone with `git clone https://github.com/Jimthetaxguy/gitspec.git`.

**`ERROR: target directory does not exist`**
Create the target directory first: `mkdir -p /path/to/project && ./scripts/install.sh /path/to/project`.

**Git hooks not running after install**
Run `git config --get core.hooksPath` inside the target repo. It should print `.hooks`. If not, re-run the installer without `--no-hooks`.

**Dashboard shows empty state**
The dashboard reads from `.ledger/changes.json` and `docs/`. Create at least one story (`/new-story "first"`) or commit at least one change matching the trailer convention, then refresh.

## Project Status

GitSpec is a released **skills pack**, not an actively-maintained service. The author is not committing to ongoing maintenance, issue response, or PR review. Use it, fork it, adapt it — that's what the MIT license is for. See [CHANGELOG.md](CHANGELOG.md) for what shipped and [CONTRIBUTING.md](CONTRIBUTING.md) if you'd still like to send a PR upstream.

## Security and Warranty

The software is provided **"AS IS"** under the MIT License, without warranty of any kind. See [LICENSE](LICENSE) for the full disclaimer.

If you find a security issue, you may open a private GitHub Security Advisory (**Security → Advisories → New draft**). No response is guaranteed. See [SECURITY.md](SECURITY.md) for the audit checklist and the intentional-behavior statements that describe what the software does and does not do.

## Repository

**GitHub:** [github.com/Jimthetaxguy/gitspec](https://github.com/Jimthetaxguy/gitspec)

## License

[MIT](LICENSE)
