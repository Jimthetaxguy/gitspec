---
name: pr-prep
description: Prepare a pull request — distill notes, generate PR description with notes cleanup section, validate trailers
---

Prepare everything needed for a clean GitSpec-compliant pull request.

**Usage:** `/pr-prep` (operates on current branch vs main)

**Steps:**

1. **Identify the PR scope:**
   - Run `git log main..HEAD --oneline` to see all commits on this branch
   - Extract Story: and Spec: trailers from all commits
   - Identify the stories and specs this PR touches

2. **Check trailer compliance:**
   - Verify all feat/fix commits have Story: or Spec: trailers
   - If any are missing, warn the user and suggest amending

3. **Distill notes (if needed):**
   - Check `docs/notes/` for raw notes created during this branch's timeframe
   - If raw notes exist but no corresponding cleaned note or ADR was created, offer to run the distillation flow
   - If distillation is needed and the user agrees, follow the `/distill` command flow

4. **Generate PR description:**

```markdown
## Summary

{1-3 sentence summary based on the commit messages and story titles}

## Stories

{List each story touched, with status}
- STORY-NNN: {title} ({status})

## Specs Affected

- SPEC-XXX-NNN: {title}

## Changes

{Bulleted list of what changed, derived from commit subjects}

## Notes Cleanup

{If ADRs were created during distillation, link them here}
- ADR-NNN: {title} — docs/decisions/{NNN}-{slug}.md

{If no distillation was needed}
- No new decisions documented (routine implementation)

## Checklist

- [ ] All feat/fix commits have Story:/Spec: trailers
- [ ] Raw notes distilled into ADR (if applicable)
- [ ] Frontmatter valid (`python scripts/validate-frontmatter.py`)
- [ ] Ledger updated (`python scripts/ledger-update.py`)
```

5. **Present to user:** Show the generated PR description and ask: "Does this look right? I can adjust the summary or add details before you create the PR."

6. **Optionally create the PR:** If the user says "go ahead" or "create it", use `gh pr create` with the generated title and body.
