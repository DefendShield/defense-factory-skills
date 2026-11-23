#!/usr/bin/env python3
"""Validate Defense Factory JSON artifacts against shipped schemas.

Uses jsonschema when installed; otherwise applies a stdlib required-field
and type checker sufficient for the schemas in this repository.

Examples:
  python scripts/validate_artifacts.py fixtures/sample-inventory.json
  python scripts/validate_artifacts.py fixtures/sample-validated-finding.json --schema finding
  python scripts/validate_artifacts.py --all
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = REPO_ROOT / "schemas"
FIXTURES_DIR = REPO_ROOT / "fixtures"

SCHEMA_FILES = {
    "inventory-entry": SCHEMAS_DIR / "inventory-entry.schema.json",
    "inventory": SCHEMAS_DIR / "inventory-entry.schema.json",
    "finding": SCHEMAS_DIR / "finding.schema.json",
    "ownership-assignment": SCHEMAS_DIR / "ownership-assignment.schema.json",
    "ownership": SCHEMAS_DIR / "ownership-assignment.schema.json",
    "verification-record": SCHEMAS_DIR / "verification-record.schema.json",
    "verification": SCHEMAS_DIR / "verification-record.schema.json",
}

# Heuristic auto-detect from object keys / filename
DETECT_RULES: list[tuple[str, list[str]]] = [
    ("verification-record", ["retest_method", "verifier", "merged_pr_alone_insufficient"]),
    ("ownership-assignment", ["finding_id", "sla_due", "priority", "assigned_at"]),
    ("finding", ["severity", "status", "asset_id", "source_skill"]),
    ("inventory-entry", ["asset_type", "environment", "discovered_at", "source"]),
]

TYPE_MAP = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "object": dict,
    "array": list,
}


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def detect_schema_name(data: Any, path: Path) -> str | None:
    name = path.name.lower()
    if "inventory" in name:
        return "inventory-entry"
    if "ownership" in name:
        return "ownership-assignment"
    if "verif" in name:
        return "verification-record"
    if "finding" in name:
        return "finding"

    if isinstance(data, list) and data:
        return detect_schema_name(data[0], path)
    if not isinstance(data, dict):
        return None

    best: str | None = None
    best_score = 0
    for schema_name, keys in DETECT_RULES:
        score = sum(1 for k in keys if k in data)
        if score > best_score:
            best_score = score
            best = schema_name
    return best if best_score >= 2 else None


def _check_type(value: Any, expected: str) -> bool:
    py = TYPE_MAP.get(expected)
    if py is None:
        return True
    if expected == "number" and isinstance(value, bool):
        return False
    if expected == "integer" and isinstance(value, bool):
        return False
    return isinstance(value, py)


def validate_minimal(instance: Any, schema: dict[str, Any], path: str = "$") -> list[str]:
    """Minimal draft-ish validator: type, required, enum, const, minLength, minItems, allOf/if/then."""
    errors: list[str] = []

    if "allOf" in schema:
        for i, sub in enumerate(schema["allOf"]):
            errors.extend(validate_minimal(instance, sub, f"{path}/allOf[{i}]"))

    if "if" in schema and "then" in schema:
        if_errs = validate_minimal(instance, schema["if"], f"{path}/if")
        if not if_errs:
            errors.extend(validate_minimal(instance, schema["then"], f"{path}/then"))

    expected_type = schema.get("type")
    if expected_type:
        types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_check_type(instance, t) for t in types):
            errors.append(f"{path}: expected type {expected_type}, got {type(instance).__name__}")
            return errors

    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}, got {instance!r}")

    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: value {instance!r} not in enum {schema['enum']}")

    if isinstance(instance, str) and "minLength" in schema:
        if len(instance) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength {schema['minLength']}")

    if isinstance(instance, list) and "minItems" in schema:
        if len(instance) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(instance):
                errors.extend(validate_minimal(item, item_schema, f"{path}[{i}]"))

    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"{path}: missing required property {key!r}")
        props = schema.get("properties", {})
        for key, value in instance.items():
            if key in props:
                errors.extend(validate_minimal(value, props[key], f"{path}.{key}"))

    return errors


def validate_with_jsonschema(instance: Any, schema: dict[str, Any]) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return validate_minimal(instance, schema)

    validator_cls = jsonschema.Draft202012Validator
    validator = validator_cls(schema)
    return [
        f"{'/'.join(str(p) for p in err.absolute_path) or '$'}: {err.message}"
        for err in sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    ]


def validate_one(path: Path, schema_name: str | None) -> list[str]:
    data = load_json(path)
    name = schema_name or detect_schema_name(data, path)
    if not name:
        return [f"{path}: could not auto-detect schema; pass --schema"]
    if name not in SCHEMA_FILES:
        return [f"{path}: unknown schema {name!r}"]

    schema = load_json(SCHEMA_FILES[name])

    # Inventory files may be a single entry or a list/wrapper
    if name in ("inventory-entry", "inventory"):
        if isinstance(data, list):
            errors: list[str] = []
            for i, item in enumerate(data):
                errors.extend(f"[{i}] {e}" for e in validate_with_jsonschema(item, schema))
            return errors
        if isinstance(data, dict) and "entries" in data and isinstance(data["entries"], list):
            errors = []
            for i, item in enumerate(data["entries"]):
                errors.extend(f"entries[{i}] {e}" for e in validate_with_jsonschema(item, schema))
            return errors

    return validate_with_jsonschema(data, schema)


def iter_default_targets() -> list[Path]:
    return sorted(FIXTURES_DIR.glob("*.json"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Defense Factory JSON artifacts")
    parser.add_argument("paths", nargs="*", type=Path, help="JSON file paths")
    parser.add_argument(
        "--schema",
        "-s",
        help="Schema name: finding, inventory-entry, ownership-assignment, verification-record",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all fixtures under fixtures/",
    )
    args = parser.parse_args(argv)

    paths: list[Path] = []
    if args.all or not args.paths:
        if args.all or not args.paths:
            paths = iter_default_targets()
            if not args.paths and not args.all:
                # default: if no args, validate fixtures
                pass
    if args.paths:
        paths = [p if p.is_absolute() else (Path.cwd() / p) for p in args.paths]

    if not paths:
        print("No files to validate", file=sys.stderr)
        return 2

    failed = 0
    for path in paths:
        if not path.exists():
            print(f"FAIL {path}: file not found")
            failed += 1
            continue
        try:
            errors = validate_one(path, args.schema)
        except json.JSONDecodeError as exc:
            print(f"FAIL {path}: invalid JSON ({exc})")
            failed += 1
            continue
        if errors:
            print(f"FAIL {path}")
            for err in errors:
                print(f"  - {err}")
            failed += 1
        else:
            detected = args.schema or detect_schema_name(load_json(path), path)
            print(f"OK   {path} [{detected}]")

    if failed:
        print(f"\n{failed} file(s) failed validation", file=sys.stderr)
        return 1
    print(f"\n{len(paths)} file(s) validated successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
