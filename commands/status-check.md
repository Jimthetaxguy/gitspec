---
name: status-check
description: Scan the repo for GitSpec health — orphaned TODOs, missing trailers, stale stories, spec coverage gaps
---

Run a comprehensive health check on the GitSpec project management layer.

**Steps:**

1. **Story status summary:**
   - Read all files in `docs/stories/` (excluding archive/)
   - Parse YAML frontmatter and group by status
   - Report counts: backlog, ready, in_progress, in_review, done, blocked

2. **Orphaned TODOs:**
   - Search source files (not docs/) for TODO, FIXME, HACK comments
   - Check if each has a story reference like `TODO(STORY-NNN):`
   - Report any TODOs without story references

3. **Missing commit trailers:**
   - Run `git log --oneline -20` to get recent commits
   - For any feat/fix commits, check if they have Story: or Spec: trailers
   - Report unlinked feat/fix commits

4. **Stale stories:**
   - Find stories with status `in_progress` where the linked spec or associated commits haven't been updated in >7 days
   - Report these as potentially stale

5. **Spec coverage:**
   - Read all specs in `docs/specs/`
   - For each spec, check if it has at least one linked story
   - Check if source files matching the spec's `paths:` globs contain `rnpm[impl SPEC-ID]` annotations
   - Report specs with no implementing stories or no code annotations

6. **Locked artifacts:**
   - Scan stories and specs for `locked_by:` frontmatter that isn't null
   - Check if any locks have expired (>30 minutes old)
   - Report active and expired locks

7. **Ledger health:**
   - If `.ledger/changes.json` exists, report entry count and last entry date
   - Check for any `CHG-PENDING-*` entries that haven't been finalized

**Output format:**

```
GitSpec Health Check — {date}

Stories: 3 backlog | 2 in_progress | 1 in_review | 5 done | 0 blocked
Specs: 4 active | 1 proposed | 2 implemented

Issues Found:
  - 2 TODOs without story references (src/auth/token.ts:42, src/board/render.ts:88)
  - 1 feat commit without trailer (abc1234: "add user avatar upload")
  - 1 stale story: STORY-038 (in_progress, no activity since Apr 15)
  - 1 spec with no implementation: SPEC-API-002

All Clear:
  - No expired locks
  - Ledger up to date (23 entries, last: Apr 22)
  - All active stories have linked specs
```

Present the results conversationally — highlight the issues first, then confirm what's healthy.
