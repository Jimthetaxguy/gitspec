# Rule: Source Code Annotations

When implementing specs, annotate source code with traceability markers so that the
relationship between code and specs is explicit and machine-scannable. The `build-graph.py`
script uses these annotations to build the full traceability graph.

## Annotation Format

Annotations use the `rnpm[kind SPEC-ID]` format (short for "repo-native project metadata").
The prefix is chosen for searchability and collision avoidance.

```python
# Python example
def refresh_auth_token():
    # rnpm[impl SPEC-AUTH-003]
    token = get_fresh_token()
    return token

# Test example
def test_token_expiry():
    # rnpm[verify SPEC-AUTH-003]
    token = old_token()
    assert not is_valid(token)
```

Supported annotation kinds:

| Kind | Meaning | Example |
|---|---|---|
| `impl` | This code implements the spec | `// rnpm[impl SPEC-AUTH-003]` |
| `verify` | This test verifies the spec | `// rnpm[verify SPEC-AUTH-003]` |
| `risk` | This code has a known risk related to the spec | `// rnpm[risk SPEC-AUTH-003]` |
| `depends` | This code depends on the spec | `// rnpm[depends SPEC-AUTH-003]` |
| `workaround` | Temporary workaround for spec constraints | `// rnpm[workaround SPEC-AUTH-003]` |

## Syntax by Language

The annotation format is the same across all languages; only comment syntax differs:

```python
# Python
# rnpm[impl SPEC-AUTH-003]

// JavaScript / TypeScript / Java / C / C++
// rnpm[impl SPEC-AUTH-003]

-- SQL / Lua
-- rnpm[impl SPEC-AUTH-003]

<!-- HTML / XML -->
<!-- rnpm[impl SPEC-AUTH-003] -->

# Bash / Shell / Makefile
# rnpm[impl SPEC-AUTH-003]
```

## Placement Guidelines

Place annotations:
- **On the line before** the relevant code block, or
- **On the same line** (end-of-line comment) for short statements, or
- **Above a function/class definition** if the entire unit implements the spec

Example:

```python
# rnpm[impl SPEC-AUTH-003]
class TokenRefreshHandler:
    def handle_refresh(self, old_token):
        # rnpm[verify SPEC-AUTH-003]
        new_token = self.refresh(old_token)
        assert new_token.issued_at > old_token.issued_at
        return new_token
```

## Graph Building

The `scripts/build-graph.py` script scans all source files and extracts these annotations:

```bash
python scripts/build-graph.py
# Output: .ledger/graph.json with nodes and edges
```

The resulting graph includes:
- Story and spec nodes
- Change (commit) nodes from the ledger
- Annotation nodes (file:line locations)
- Edges showing relationships: implements, verifies, depends, risks, workarounds

## Maintenance

When a spec changes or is deprecated:
1. Run `grep -r "SPEC-AUTH-003" src/` to find all related annotations
2. Review each annotation and decide:
   - Keep (spec still applies): no change
   - Update (spec evolved): revise the annotation
   - Remove (spec deprecated): delete the annotation
3. Include spec change details in the commit message (Story:/Spec: trailers)

Annotations are first-class citizens in code reviews — treat them the same as tests
or documentation. If a reviewer questions a `risk` annotation, add a comment block
explaining the risk.
