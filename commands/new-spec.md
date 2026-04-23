---
name: new-spec
description: Scaffold a new GitSpec requirement spec with structured frontmatter
---

Create a new specification file in `docs/specs/`.

**Steps:**

1. Ask the user (if not provided via $ARGUMENTS):
   - "What domain does this spec belong to?" (e.g., AUTH, BOARD, API, UI)
   - "What's the spec title?"

2. Scan `docs/specs/` for existing `SPEC-{DOMAIN}-NNN.md` files in the given domain. Find the highest NNN and increment by 1. If none exist for this domain, start at 001.

3. Create `docs/specs/SPEC-{DOMAIN}-{NNN}.md` with this structure:

```markdown
---
id: SPEC-{DOMAIN}-{NNN}
title: "$TITLE"
status: proposed
owner: 
stories: []
decision_records: []
paths: []
acceptance:
  - ""
updated_at: {today's date YYYY-MM-DD}
---

# $TITLE

## Requirement

{What the system must do. Be specific and testable.}

## Rationale

{Why this requirement exists. What problem it solves.}

## Acceptance Criteria

- [ ] {First criterion}

## Paths

Files expected to implement this spec:
- `src/...`

## Open Questions

- {Any unresolved decisions or dependencies}
```

4. After creating, report: "Created SPEC-{DOMAIN}-{NNN}: {title}"
