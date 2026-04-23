# Contributing to Build.MD

Thank you for considering a contribution. Build.MD is a small, opinionated project. To keep it that way, please read this before opening a pull request.

## What belongs in Build.MD

**Yes:**
- Fixes to the installer, hooks, or helper scripts.
- New platform adapters (new AI agents or editors that need their own config format).
- New slash commands that map directly to the documented layers.
- Clarifications and corrections to SKILL.md or README.md.
- Additional schema validators or rule templates.

**No (open a discussion first):**
- New layers in the nine-layer architecture.
- New runtime dependencies (Python packages, Node modules, shell libraries).
- External service integrations (Jira, Linear, Slack, etc.). Build.MD is repo-native by design.
- Telemetry, analytics, or any network call during install.

## Workflow

1. **Open an issue first** for anything larger than a typo or a one-file fix. A short discussion up front saves everyone a round-trip on design.
2. **Fork and branch.** Work on a topic branch named `feat/...`, `fix/...`, or `docs/...`.
3. **Dogfood the tool.** If you change `install.sh`, run `./scripts/install.sh /tmp/test-repo --dry-run` and then a real install into a scratch repo before opening the PR.
4. **Run the smoke test.** `bash ci/smoke.sh` should pass locally.
5. **Open a PR** against `main`. Reference the issue in the description.

## Commit style

We eat our own dog food. Commit messages follow the same convention Build.MD installs for its users:

```
<type>: <short imperative summary>

<optional body explaining what changed and why>

Story: STORY-001
```

Valid types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `ci`.

`Story:` and `Spec:` trailers are optional on this repo until we have a story backlog of our own, but they're welcome.

## Code standards

- **Bash:** `set -euo pipefail`. `shellcheck scripts/*.sh templates/hooks/*` should pass.
- **Python:** Python 3.9+ standard library only. No `pip install`. Keep scripts self-contained.
- **Markdown:** YAML frontmatter where the schema requires it. Line length is not enforced — prioritize readability.

## What a good PR looks like

- One logical change per PR.
- Tests or a smoke-test update if the change is non-trivial.
- Documentation updated in the same PR (don't land code without docs).
- A PR description that explains the motivation, not just the diff.

## Code of conduct

Be direct, be kind, assume good faith. Reviewers will do the same. Disagreements about design are normal and should stay focused on the artifact under review, not the person who wrote it.

## Licensing

By contributing, you agree that your contributions will be licensed under the MIT License (see `LICENSE`).
