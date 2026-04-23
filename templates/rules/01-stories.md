# Rule: Story Authoring

When creating or modifying user stories in `docs/stories/`:

1. Every story file must have YAML frontmatter with at minimum: `id`, `title`, `status`, `owner`
2. Story IDs follow the pattern `STORY-NNN` (sequential, never reused)
3. Status values must come from the project's status vocabulary (defined in AGENTS.md)
4. Acceptance criteria are checkboxes in Markdown: `- [ ] Criterion`
5. When a story is done, move it to `docs/stories/archive/` — never delete it
6. Link stories to specs via the `spec:` frontmatter field when applicable
7. If you're an AI agent, set `locked_by` in frontmatter while editing, clear it when done
