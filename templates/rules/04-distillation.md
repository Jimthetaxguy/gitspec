# Rule: Note Distillation

Raw notes are valuable but perishable — their meaning fades as context is forgotten. 
Distillation turns raw notes into durable organizational knowledge.

**When to distill:**
- Before merging a PR that involved non-trivial decisions
- At the end of a sprint or milestone
- When you realize a note from last week contains a decision that others should know about

**How to distill:**
1. Review your raw notes from the relevant period
2. Identify the decisions, learnings, and open questions
3. Write a cleaned summary in `docs/decisions/` using the ADR format:
   - **Context**: What situation required a decision?
   - **Decision**: What did you decide?
   - **Consequences**: What happens as a result? What trade-offs?
4. Link the ADR to relevant specs and stories via frontmatter

**For AI agents:**
When asked to distill notes, read the contributor's raw notes directory, cross-reference 
with the relevant stories and specs, and draft an ADR. Always let the human review and 
approve before committing.
