# Rule: Commit Conventions

All commits follow Conventional Commits format:

```
type(scope): description

Optional body — explain why, not what.

Story: STORY-NNN
Spec: SPEC-XXX-NNN
```

**Required trailers:**
- `feat` and `fix` commits must include a `Story:` or `Spec:` trailer
- The referenced ID must correspond to an existing file in `docs/stories/` or `docs/specs/`
- Multiple trailers are allowed (one per line)

**Types and their meaning:**
- `feat` — new capability (maps to a story)
- `fix` — bug repair (maps to a story)
- `perf` — performance improvement
- `refactor` — restructuring without behavior change
- `docs` — documentation only
- `test` — adding or updating tests
- `chore` — maintenance (deps, configs)
- `style` — formatting, whitespace
- `ci` — CI/CD pipeline changes

**Breaking changes:** Add `!` after the type (`feat!:`) or include a `BREAKING CHANGE:` 
trailer in the footer.
