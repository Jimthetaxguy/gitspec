# Build.MD Principles Catalog

> Curated best practices from leading AI companies, researchers, and builders.
> Updated via `scripts/refresh-principles.py`. Each principle cites its source,
> domain, and whether it's universal or contextual.
>
> **Universal** principles are always embedded in agent configs.
> **Contextual** principles activate based on project type during init.

---

## Universal Principles

These apply to every project, regardless of language, framework, or domain.

### U-001: Accelerate the Commodity, Focus on the Decision
**Source:** Jensen Huang / NVIDIA — "Accelerated computing" philosophy
**Domain:** workflow-design

Automate everything that doesn't require human judgment — builds, validation, ledger 
generation, manifest building, formatting, deployment. The human's job is to make 
decisions. The machine's job is to make decisions cheap to execute and easy to reverse. 
If your project management layer adds friction to the decision-making loop, it's broken.

### U-002: Iterate Fast, Ship the Vertical Slice
**Source:** Sam Altman / OpenAI — Startup velocity principles
**Domain:** workflow-design

Don't build layer by layer. Build one complete thing that works end-to-end, then improve 
it. For Build.MD: the init flow should produce a working system in 60 seconds — not a 
perfect one. A spec with three acceptance criteria and a commit with a trailer is better 
than a month of planning with no code.

### U-003: Developer Velocity Is the Leading Indicator
**Source:** Satya Nadella / Microsoft — Developer platform thesis
**Domain:** workflow-design

If the PM layer slows down the developer, developers will route around it. Every Build.MD 
convention must pass the test: "Does this make the developer faster or slower?" If slower, 
it needs to provide enough traceability value to justify the cost — and that justification 
must be explicit and understood by the team, not imposed.

### U-004: Tools Over Prompt Engineering
**Source:** Anthropic — Building Effective Agents (2025)
**Domain:** agent-design

Structured hooks, scripts, and schemas are more reliable than hoping an agent follows 
natural-language instructions. A commit-msg hook that rejects missing trailers is better 
than a CLAUDE.md line that says "please include trailers." Tools are testable, auditable, 
and consistent. Prompts are probabilistic.

### U-005: First Principles — Question Every Requirement
**Source:** Elon Musk / xAI — Engineering philosophy
**Domain:** architecture

The most dangerous requirement is the one nobody questions. Every convention in Build.MD 
should have a "why" that can be explained in one sentence. If a rule exists only because 
"that's how Jira does it," delete it. The framework is opinionated but everything is 
configurable and overridable because the best process is the one the team actually follows.

### U-006: Safety Is Not a Feature, It's the Architecture
**Source:** Dario Amodei / Anthropic — Responsible scaling philosophy
**Domain:** safety, alignment

Safety and alignment aren't bolted on after the product works — they're designed into the 
structure. In Build.MD: the change ledger is append-only (tamper-evident). Stories are 
archived, never deleted (reversible). Every feat/fix links to a spec or story (traceable). 
Hooks enforce at commit time, CI enforces at merge time (defense in depth). These aren't 
optional quality features — they're the load-bearing walls.

### U-007: The Best Documentation Is the One That Writes Itself
**Source:** Andrej Karpathy — "Software 2.0" thesis, applied to documentation
**Domain:** documentation

The change ledger is auto-generated from commit trailers. The manifest is auto-generated 
from frontmatter. The dashboard reads from Git history. The only things humans write are 
specs (intent), stories (scope), notes (context), and decisions (rationale). Everything 
else should be derived. If you have to write it twice, the system is wrong.

### U-008: Alignment Through Shared Language
**Source:** Ilya Sutskever / SSI (Safe Superintelligence Inc) — Alignment research
**Domain:** alignment, multi-agent

When multiple agents and humans work on the same codebase, alignment comes from a shared 
language — not from each agent having its own interpretation of what "done" means. The 
status vocabulary, frontmatter schemas, and commit conventions are that shared language. 
A story with `status: in_progress` means the same thing whether Claude, Cursor, Copilot, 
or a human wrote it.

### U-009: Make the Right Thing Easy and the Wrong Thing Hard
**Source:** Google — Engineering Practices, applied broadly
**Domain:** developer-experience

Don't rely on discipline. Make the default behavior correct. `build-md new-story` generates 
the right template. The commit hook catches missing trailers before they hit the repo. 
The schema validator catches invalid frontmatter before it breaks the board. Discipline 
failures are system design failures.

### U-010: Compound Returns on Context
**Source:** Jensen Huang / NVIDIA — "The more you buy, the more you save" applied to knowledge
**Domain:** documentation, institutional-memory

Every spec, story, decision, and distilled note compounds. A repo with 100 ADRs is 
dramatically more valuable than one with 10 — not linearly, but exponentially, because 
each new decision can reference prior ones. The change ledger gains predictive value over 
time (you can see which specs generate the most churn). Build.MD's append-only design 
is intentional: knowledge compounds only if you never throw it away.

### U-011: Embrace Cognitive Diversity in Agent Teams
**Source:** Thinking Machines — Multi-agent coordination research
**Domain:** multi-agent, workflow-design

Different agents have different strengths. Claude is strong at reasoning and long-context. 
Cursor is fast at in-editor changes. Copilot excels at autocomplete and boilerplate. 
Build.MD doesn't try to make every agent do everything — it gives them a shared contract 
and lets each contribute where it's strongest. The AGENTS.md file is the same; the 
platform adapters optimize for each tool's interaction model.

### U-012: Minimum Viable Bureaucracy
**Source:** Ramp — Engineering velocity culture
**Domain:** workflow-design

Every process element must earn its place by reducing confusion or preventing errors that 
actually happen — not theoretically might happen. Start with the lightest enforcement 
level (gentle). Upgrade to standard when you see the specific problems it prevents. 
Go strict only when the cost of a missed trailer or undocumented decision is real and 
measured, not hypothetical.

---

## Contextual Principles — Agent & Workflow Tools

Activate when the project involves building AI agents, MCP servers, or workflow automation.

### C-AGT-001: Orchestrator-Worker for Complex Tasks
**Source:** Anthropic — Building Effective Agents; LangChain — Agent Architectures
**Domain:** agent-design

For multi-step tasks, use an orchestrator that decomposes work and delegates to specialized 
workers. Each worker has a narrow scope and clear success criteria. The orchestrator handles 
sequencing, error recovery, and result synthesis. This is how Build.MD itself works: the 
init flow is an orchestrator; the hooks, ledger script, and manifest builder are workers.

### C-AGT-002: MCP for Tool Integration
**Source:** Anthropic — Model Context Protocol (2025-2026), now under Linux Foundation
**Domain:** agent-design, interop

When building tools that multiple agents need to access, implement them as MCP servers. 
MCP is the standard for agent-tool communication — 97M+ installs as of March 2026. Every 
major AI provider ships MCP-compatible tooling. If you're building a tool that only one 
agent can use, you're building a dead end.

### C-AGT-003: Memory as Structured Files
**Source:** Anthropic — Claude Code architecture; OpenAI — Codex AGENTS.md
**Domain:** agent-design

Persistent agent memory should be stored as structured files (AGENTS.md, frontmatter YAML, 
JSON manifests) rather than conversation history. Files are versionable, searchable, and 
survive session boundaries. Chat history is ephemeral and grows unbounded.

### C-AGT-004: The Agent Is a Contributor, Not an Oracle
**Source:** Andrej Karpathy — "LLMs as a new kind of computer"
**Domain:** agent-design, alignment

AI agents should operate under the same contribution rules as human developers — same 
commit conventions, same review process, same documentation requirements. An agent that 
bypasses the PR process or writes directly to main is misaligned with the team, regardless 
of how correct its code is.

### C-AGT-005: Defensive Inference — Verify Before You Ship
**Source:** xAI / Elon Musk — "Verify everything, trust nothing"
**Domain:** agent-design, safety

Agent-generated output should be validated before it affects the world. Build.MD applies 
this through hooks (validate before commit), CI (validate before merge), and the ledger 
(audit after the fact). For agent-built features specifically: run the tests, check the 
schema, verify the frontmatter — don't assume the agent got it right just because it 
said it did.

---

## Contextual Principles — Security & Compliance

Activate for regulated domains (tax, legal, medical, financial).

### C-SEC-001: Defense in Depth for Code Contributions
**Source:** Microsoft — SDL; Anthropic — Claude safety architecture
**Domain:** security

Three layers of validation: client-side hooks (fast feedback), CI checks (authoritative 
gate), and post-merge ledger (audit trail). Any single layer can be bypassed; all three 
together create a reliable enforcement chain.

### C-SEC-002: Principle of Least Privilege for Agents
**Source:** Google DeepMind — Responsible AI Practices
**Domain:** security, agent-design

Agents should request only the permissions they need for the current task. An agent writing 
a story file doesn't need access to deployment credentials. Build.MD's locking mechanism 
(frontmatter `locked_by`) is a lightweight implementation of this — an agent claims only 
the artifact it's modifying.

### C-SEC-003: Immutable Audit Trail
**Source:** Harvey AI — Legal engineering practices; ToltIQ — Tax compliance workflows
**Domain:** compliance, traceability

In regulated domains, the ability to prove *who changed what, when, and why* is non-negotiable. 
The change ledger, combined with Git history and commit trailers, provides this. Stories 
are never deleted. ADRs are never overwritten. Superseded entries are marked, not removed. 
The entire history is reconstructable from `git log`.

### C-SEC-004: Privacy by Architecture
**Source:** OpenAI — Privacy Filter (Apr 2026); SSI — Safety-first design
**Domain:** security, privacy

When agents process repository data, ensure PII and secrets don't leak into logs, 
manifests, or generated reports. Build.MD's ledger captures file paths and summaries, 
not file contents. The dashboard reads frontmatter metadata, not document bodies. 
For sensitive projects, consider running the OpenAI Privacy Filter as a pre-commit 
step on generated documentation.

---

## Contextual Principles — Rapid Prototyping

Activate for startups, hackathons, solo projects, and early-stage exploration.

### C-RAP-001: Ship the Vertical Slice First
**Source:** Replit — Rapid development practices
**Domain:** workflow-design

Build one complete feature touching every layer (data → logic → UI) before polishing any 
single layer. For Build.MD: create one spec, one story, one commit with a trailer, and 
open the dashboard — before writing the CI pipeline or the distillation workflow.

### C-RAP-002: Concessions Are Temporary, Architecture Is Permanent
**Source:** Ramp — Engineering culture
**Domain:** architecture

Move fast, but know what's cheap to fix later (hardcoded values, missing tests, rough UI) 
vs what's expensive (wrong data models, coupled architectures, no traceability). Build.MD's 
frontmatter schemas and commit conventions are the architecture — get those right early. 
The dashboard layout and report formatting are concessions — iterate on those later.

### C-RAP-003: Automate the Feedback Loop
**Source:** Sakana AI — AI Scientist v2; Meta FAIR — Research practices
**Domain:** rapid-iteration

Structure exploration as hypothesis → experiment → measurement → conclusion. The change 
ledger enables this naturally: each feat/fix commit is an experiment; the spec's acceptance 
criteria are the hypothesis; the test suite is the measurement; the ADR is the conclusion.

---

## Contextual Principles — Research & Knowledge Work

Activate for research projects, data analysis, document-heavy workflows.

### C-RES-001: Distillation Is the Differentiator
**Source:** Hebbia — Knowledge management patterns
**Domain:** documentation, research

Raw notes accumulate fast and become unreadable. The distillation step — synthesizing raw 
notes into a structured ADR — is where knowledge becomes institutional. Build.MD enforces 
this at PR time (standard/strict enforcement) because without enforcement, distillation 
is the first thing teams skip under pressure.

### C-RES-002: Benchmark Before Optimizing
**Source:** Meta FAIR — Systems research practices; Andrej Karpathy — ML engineering
**Domain:** research, performance

Measure before you optimize. Profile before you refactor. The ledger's change frequency 
data can tell you which specs generate the most churn (and therefore need the most 
attention). Intuition is unreliable; the data is in the repo.

---

## Refresh Metadata

```yaml
last_refreshed: 2026-04-23
version: 2.0.0
principle_count: 24
sources_checked:
  - anthropic.com/engineering (Dario Amodei, Building Effective Agents)
  - openai.com (Sam Altman, Agents SDK, Privacy Filter, Codex)
  - nvidia.com (Jensen Huang, accelerated computing philosophy)
  - x.ai (Elon Musk, Grok, first-principles engineering)
  - ai.google.dev (Google DeepMind, Gemma, responsible AI)
  - meta.com/ai (Meta FAIR, Llama, open-source research)
  - microsoft.com (Satya Nadella, Copilot, developer velocity)
  - langchain.com (agent architectures, tool use patterns)
  - cursor.com (agent best practices, .mdc rules)
  - replit.com (rapid prototyping, deployment)
  - ramp.com/engineering (engineering velocity, MVB)
  - sakana.ai (AI Scientist, evolutionary methods)
  - harvey.ai (legal AI workflows, precision)
  - toltiq.com (tax technology, compliance)
  - hebbia.ai (knowledge management, RAG)
  - ssi.inc (Ilya Sutskever, Safe Superintelligence, alignment)
  - karpathy.ai (Andrej Karpathy, Software 2.0, LLM engineering)
  - thinkingmachines.dev (multi-agent coordination research)
next_refresh_due: 2026-05-23
```
