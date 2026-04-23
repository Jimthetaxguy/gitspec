# Init Interview Flow

When a contributor runs `gitspec init`, guide them through this conversation. Ask one 
question at a time. Adapt based on answers. Explain why each question matters.

## Detection Phase (Automatic — No Questions)

Before asking anything, silently detect:

1. **Which agent configs exist** — check for `.cursorrules`, `.cursor/rules/`, 
   `.github/copilot-instructions.md`, `.codex/`, `.vscode/instructions.md`, `CLAUDE.md`
2. **Whether Git is initialized** — if not, offer to `git init`
3. **Whether there's an existing AGENTS.md** — if so, this is a re-init or onboarding
4. **Language/framework** — scan for `package.json`, `Cargo.toml`, `pyproject.toml`, 
   `go.mod`, etc.
5. **Existing docs structure** — check for `docs/`, `README.md`, `.github/`

Report what you found: "I can see this is a [language] project using [tools]. Let me 
ask a few questions to set up your project management layer."

## Interview Questions

### Q1: What are you building?

"In a sentence or two, what is this project? This helps me write the project summary 
that every agent on your team will see when they start a session."

→ Saves to: `project_name`, `project_description` in config

### Q2: Who's on the team?

"Who contributes to this repo? List the names or handles — I'll set up notes 
directories for each person. If it's just you, that's fine too."

→ Saves to: `contributors[]` — creates `docs/notes/{name}/` for each

"Do any AI agents contribute regularly? (e.g., Claude Code sessions, Cursor agent, 
Codex tasks)"

→ If yes, creates `docs/notes/agents/` with a README explaining session-based namespacing

### Q3: How do you like to work?

"Which style fits your team best?

1. **Kanban** — continuous flow, stories move through columns
2. **Sprints** — time-boxed iterations with planned capacity
3. **Lightweight** — just specs and notes, no formal story tracking

Most teams start with Kanban. You can always change later."

→ Saves to: `workflow_style` — affects status vocabulary and board layout

**Status vocabulary by style:**

| Kanban | Sprint | Lightweight |
|--------|--------|-------------|
| backlog | planned | proposed |
| ready | sprint_backlog | active |
| in_progress | in_progress | done |
| in_review | in_review | |
| done | done | |
| blocked | blocked | |

### Q4: Which AI tools does your team use?

"Check all that apply:
- [ ] Claude Code
- [ ] Cursor
- [ ] GitHub Copilot
- [ ] OpenAI Codex
- [ ] VS Code with AI extensions
- [ ] Other (specify)

I'll generate config files for each one so they all understand the same conventions."

→ Saves to: `agent_tools[]` — determines which adapter files to generate

### Q5: How strict should enforcement be?

"Three options:

**Gentle** — hooks warn but don't block. Good for solo projects or early prototypes. 
You'll see reminders but can always push through.

**Standard** (recommended for teams) — feat/fix commits need a Story: or Spec: trailer. 
Code changes need a same-day note. PR template requires a notes section.

**Strict** — everything in Standard, plus CI validates frontmatter schemas, changed 
files must match a declared spec path, and raw notes must be distilled before merge. 
Good for regulated environments or when traceability matters.

Which level?"

→ Saves to: `enforcement_level`

### Q6: Anything else I should know?

"Any naming conventions, domain-specific terminology, or workflow quirks I should 
bake into the agent instructions? For example: 'we use ticket IDs like PROJ-123' 
or 'all specs need a security review section.'"

→ Saves to: `custom_conventions[]` — appended to the agent configs

## Generation Phase

After the interview, generate files in this order:

### Step 1: Create directory scaffold

```
docs/
  specs/.gitkeep
  stories/.gitkeep (or stories/archive/.gitkeep)
  notes/{contributor-1}/.gitkeep
  notes/{contributor-2}/.gitkeep
  notes/agents/.gitkeep (if AI agents are used)
  decisions/.gitkeep
  reports/.gitkeep
.ledger/
  changes.json (empty: {"version":"1","entries":[]})
  schema.json (copy from templates/schemas/ledger.schema.json)
.agents/
  rules/ (copy rule blocks from templates/rules/)
meta/
  schemas/ (copy from templates/schemas/)
applets/ (copy dashboard.html from applets/)
scripts/ (copy automation scripts)
```

### Step 2: Generate AGENTS.md

Read `templates/AGENTS.md.template`. Fill in:
- `{{PROJECT_NAME}}` and `{{PROJECT_DESCRIPTION}}`
- `{{STATUS_VOCABULARY}}` based on workflow style
- `{{ENFORCEMENT_LEVEL}}` and corresponding rules
- `{{CUSTOM_CONVENTIONS}}` from Q6
- `{{CONTRIBUTORS}}` list

Write to project root as `AGENTS.md`.

### Step 3: Generate platform adapters

For each tool in `agent_tools[]`, read the corresponding template from 
`templates/adapters/` and generate the adapter file. Each adapter should:

1. Reference AGENTS.md as the canonical source
2. Include platform-specific formatting
3. Import or inline the relevant rule blocks from `.agents/rules/`

### Step 4: Install hooks

Ask permission: "Can I install git hooks? They'll enforce [enforcement_level] rules 
on commits. You can always disable them with `--no-verify` if needed."

If yes, copy hooks from `templates/hooks/` to `.git/hooks/` (or symlink via 
`core.hooksPath` to `.hooks/`).

### Step 5: Copy principles

Copy `principles/PRINCIPLES.md` excerpts into `.agents/rules/06-principles.md`, 
selecting principles relevant to the detected language/framework.

### Step 6: Summary

Print what was created:

```
GitSpec initialized for [project_name]

Created:
  AGENTS.md                    — canonical agent instructions
  CLAUDE.md                    — Claude Code adapter
  .cursorrules                 — Cursor adapter
  .github/copilot-instructions.md — Copilot adapter
  docs/specs/                  — requirement specifications
  docs/stories/                — user stories
  docs/notes/{contributors}/   — contributor notes
  docs/decisions/              — architecture decision records
  .ledger/changes.json         — change ledger (auto-generated)
  .agents/rules/               — append-only rule blocks
  applets/dashboard.html       — progress dashboard
  scripts/                     — automation scripts

Enforcement: [level]
Workflow: [style]

Next steps:
  1. Review AGENTS.md and customize for your project
  2. Create your first spec: `touch docs/specs/SPEC-001.md`
  3. Open the dashboard: `python scripts/serve.py`
  4. Commit everything: `git add . && git commit -m "chore: initialize GitSpec"`
```
