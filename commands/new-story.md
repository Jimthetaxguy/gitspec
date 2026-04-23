---
name: new-story
description: Scaffold a new GitSpec user story with auto-incremented ID and correct frontmatter
---

Create a new user story file in `docs/stories/`.

**Steps:**

1. Scan `docs/stories/` for existing `STORY-NNN.md` files. Find the highest NNN and increment by 1. If no stories exist, start at STORY-001.

2. Create `docs/stories/STORY-{NNN}.md` with this structure:

```markdown
---
id: STORY-{NNN}
title: "$ARGUMENTS"
status: backlog
owner: 
priority: medium
spec: 
blocked_by: []
acceptance:
  - ""
updated_at: {today's date YYYY-MM-DD}
---

# $ARGUMENTS

## Context

{Why this story exists — what problem it solves or what capability it adds.}

## Acceptance Criteria

- [ ] {First criterion}

## Notes

{Any relevant context, links, or constraints.}
```

3. If $ARGUMENTS is empty, ask the user: "What's the story title? One sentence describing what needs to be done."

4. After creating the file, report: "Created STORY-{NNN}: {title} at docs/stories/STORY-{NNN}.md"

5. If `scripts/build-manifest.py` or `scripts/validate-frontmatter.py` exist, mention that the user can run them to update the dashboard manifest.
