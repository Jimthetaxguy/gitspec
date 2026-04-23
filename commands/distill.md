---
name: distill
description: Synthesize raw working notes into a cleaned ADR (Architecture Decision Record) for a given story or time period
---

Distill raw working notes into a structured Architecture Decision Record.

**Usage:** `/distill STORY-042` or `/distill` (distills recent notes)

**Steps:**

1. **Find the raw notes to distill:**
   - If $ARGUMENTS contains a STORY-NNN reference, find the story file and identify its owner. Read their recent notes from `docs/notes/{owner}/`.
   - If $ARGUMENTS is empty, scan `docs/notes/` for the most recently modified contributor directories. Read the last 3 days of notes.
   - Also check `docs/notes/agents/` for any agent session notes from the same period.

2. **Read the relevant context:**
   - Read the target story file (if specified) for its acceptance criteria and linked spec
   - Read the linked spec (if any) for the requirement context
   - Read recent git log for commits with matching Story:/Spec: trailers

3. **Synthesize the ADR:**
   - Scan existing files in `docs/decisions/` to find the next ADR number
   - Create `docs/decisions/{NNN}-{slug}.md` using this structure:

```markdown
---
id: ADR-{NNN}
title: "{Descriptive title based on the key decision found in the notes}"
status: accepted
date: {today YYYY-MM-DD}
story: STORY-{NNN}
spec: SPEC-{XXX}-{NNN}
---

# {Title}

## Context

{What situation required a decision? Synthesize from the raw notes — what was the 
contributor working on, what problems did they encounter, what options did they consider?}

## Decision

{What was decided? Distill the actual choice that was made, based on what the notes 
and commits show.}

## Consequences

{What happens as a result? What trade-offs were accepted? What follow-up work is needed?}

## Evidence

- Notes: {list the source note files}
- Commits: {list relevant commit short hashes}
- Story: STORY-{NNN}
```

4. **Present the draft to the user for review.** Never commit an ADR without human approval. Say: "Here's the distilled ADR. Review it and let me know if anything needs adjusting before I save it."

5. After the user approves, save the file and report: "Created ADR-{NNN}: {title} at docs/decisions/{NNN}-{slug}.md"
