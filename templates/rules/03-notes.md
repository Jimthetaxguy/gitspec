# Rule: Note-Taking

Working notes capture the context that code diffs can't — why you chose approach A over B, 
what you tried that didn't work, what assumptions you're making.

**For humans:**
- Write daily notes in `docs/notes/{your-name}/{YYYY-MM-DD}.md`
- Notes are append-only journals — add to today's file, don't edit yesterday's
- No formatting requirements — bullet points, stream of consciousness, whatever works

**For AI agents:**
- Write session notes in `docs/notes/agents/{agent-type}-{session-id}/{YYYY-MM-DD}.md`
- Include: what was requested, what approach you took, what you changed and why
- If you hit an unexpected problem, document it — this is the most valuable kind of note

**What belongs in notes:**
- Decisions made during implementation (and why)
- Bugs encountered and how they were resolved
- Things you tried that didn't work (save someone else the time)
- Open questions or things that need follow-up
- Links to relevant docs, issues, or conversations
