# Rule: Agent Roles (Single-Writer Model)

When multiple AI agents work on this repo, they follow a single-writer model to prevent
conflicting changes. This model is compatible with human collaborators; the "agent" role
can also describe a human contributor or a dedicated CI/automation service.

## Roles

**Primary Writer** — the only agent allowed to edit files in any given scope
- Updates stories, specs, notes, ADRs, and source code
- Includes Story:/Spec: trailers in feat/fix commits
- Holds locks on artifacts it's modifying (frontmatter: `locked_by`, `locked_at`)
- Owns a continuous session until work is complete
- Handles PR author responsibilities (merging, closing, updating ledger)

**Reviewer** — reads diffs and relevant specs/stories, returns structured findings
- Does not write to the repo
- Returns findings as structured feedback (comments, not commits)
- Can be invoked mid-PR or before merge
- Validates against acceptance criteria in stories/specs

**Smart Friend** — invoked for hard architectural, security, or ambiguity decisions
- Provides advice and evidence-based recommendations
- Does not write to the repo
- Escalation path for the primary writer when stuck
- Examples: design reviews, threat modeling, API contract disputes

**Manager** — decomposes multi-spec or multi-PR work
- Maintains plan state (roadmap, dependency graph, sequencing)
- Routes review and approval
- Does not write directly unless explicitly promoted to primary writer
- Decides which agent takes primary writer role for each unit of work

## Invariants

The single-writer model enforces these invariants:

1. **No concurrent edits to the same file** — lock acquisition before edit, release after commit
2. **Every code change references a story or spec** — Story:/Spec: trailer is mandatory for feat/fix
3. **No code without documentation** — ADRs, notes, and specs must accompany significant changes
4. **Ledger is append-only** — changes.json is never edited manually; use ledger-update.py
5. **No orphaned stories** — all stories must be either done or actively assigned
6. **Lock TTL is strict** — default 30 minutes; force-unlock only via commit trailer with justification

## Lock Management

Frontmatter locking prevents agents from colliding:

```yaml
locked_by: "agent:claude-code-session-abc123"
locked_at: "2026-04-23T14:30:00Z"
```

Lock operations:
- **Acquire** — write `locked_by` and `locked_at` when starting edits
- **Check** — verify lock expiry (TTL default 30 min) before overwriting
- **Release** — clear `locked_by` and `locked_at` in the commit that closes the edit
- **Force-unlock** — use commit trailer `Lock-Override: {reason}` (audit trail)

Agents that crash mid-edit are auto-unlocked after TTL expires; no manual intervention needed.
