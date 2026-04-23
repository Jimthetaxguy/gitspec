#!/usr/bin/env python3
"""
GitSpec Frontmatter Validator

Validates YAML frontmatter in story and spec files against JSON schemas.
Can be run manually or as a pre-commit hook.

Usage:
  python scripts/validate-frontmatter.py                 # Check all stories and specs
  python scripts/validate-frontmatter.py docs/specs/     # Check only specs
  python scripts/validate-frontmatter.py docs/stories/   # Check only stories
  python scripts/validate-frontmatter.py <file>          # Check a specific file
"""

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML not installed. Install with: pip install pyyaml")
    sys.exit(1)


def load_schema(schema_name):
    """Load a JSON schema from meta/schemas/."""
    schema_path = Path(f"meta/schemas/{schema_name}.schema.json")
    if not schema_path.exists():
        # Fallback to templates
        schema_path = Path(f"templates/schemas/{schema_name}.schema.json")
    if schema_path.exists():
        return json.loads(schema_path.read_text())
    return None


def extract_frontmatter(content: str):
    """Extract YAML frontmatter from Markdown file."""
    if not content.startswith("---"):
        return None, content

    lines = content.split("\n", 1)
    if len(lines) < 2:
        return None, content

    rest = lines[1]
    if "---" not in rest:
        return None, content

    end_idx = rest.index("---")
    frontmatter_text = rest[:end_idx]
    body = rest[end_idx + 3:].lstrip("\n")

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def validate_frontmatter(frontmatter, schema):
    """Validate frontmatter against a JSON schema (basic validation)."""
    if not frontmatter or not isinstance(frontmatter, dict):
        return False, "Frontmatter is not a valid YAML dict"

    errors = []

    # Check required fields
    if schema and "required" in schema:
        for required_field in schema["required"]:
            if required_field not in frontmatter:
                errors.append(f"Missing required field: {required_field}")

    # Check field types and enums
    if schema and "properties" in schema:
        for field, field_schema in schema["properties"].items():
            if field not in frontmatter:
                continue

            value = frontmatter[field]

            # Type check
            if "type" in field_schema:
                expected_type = field_schema["type"]
                if isinstance(expected_type, str):
                    type_ok = isinstance(value, type_map.get(expected_type, str))
                else:
                    # Union type
                    type_ok = any(isinstance(value, type_map.get(t, str)) for t in expected_type)
                if not type_ok and value is not None:
                    errors.append(f"Field {field}: expected {expected_type}, got {type(value).__name__}")

            # Enum check
            if "enum" in field_schema:
                if value not in field_schema["enum"]:
                    errors.append(f"Field {field}: invalid value '{value}' (allowed: {field_schema['enum']})")

            # Pattern check (for strings with regex)
            if "pattern" in field_schema and isinstance(value, str):
                if not re.match(field_schema["pattern"], value):
                    errors.append(f"Field {field}: value '{value}' does not match pattern {field_schema['pattern']}")

    return len(errors) == 0, errors if errors else None


type_map = {
    "string": str,
    "number": (int, float),
    "integer": int,
    "boolean": bool,
    "array": list,
    "object": dict,
    "null": type(None),
}


def validate_file(file_path: Path):
    """Validate a single file."""
    content = file_path.read_text()
    frontmatter, body = extract_frontmatter(content)

    if body.startswith("YAML parse error"):
        return False, [body]

    # Determine which schema to use
    if "stories" in str(file_path):
        schema = load_schema("story")
        schema_name = "story"
    elif "specs" in str(file_path):
        schema = load_schema("spec")
        schema_name = "spec"
    else:
        return True, None

    if not schema:
        return True, None  # Schema not found, skip

    is_valid, errors = validate_frontmatter(frontmatter, schema)
    return is_valid, errors


def main():
    """Validate files."""
    if len(sys.argv) > 1:
        target = Path(sys.argv[1])
        if target.is_file():
            files = [target]
        elif target.is_dir():
            files = list(target.glob("*.md"))
        else:
            print(f"Error: {target} not found")
            sys.exit(1)
    else:
        # Check all stories and specs
        files = list(Path("docs/stories").glob("*.md"))
        files += list(Path("docs/specs").glob("*.md"))
        if not files:
            print("No files to validate")
            sys.exit(0)

    failed = 0
    for file_path in sorted(files):
        is_valid, errors = validate_file(file_path)
        if is_valid:
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path}")
            if errors:
                for err in errors:
                    print(f"    {err}")
            failed += 1

    if failed > 0:
        print(f"\nValidation FAILED: {failed} file(s) with errors")
        sys.exit(1)
    else:
        print(f"\nValidation OK: {len(files)} file(s) checked")
        sys.exit(0)


if __name__ == "__main__":
    main()
