#!/usr/bin/env python3
"""Initialize a .defense-factory workspace for Defense Factory skills.

Creates directory layout and a SECURITY.md stub (or a pointer to repo-root SECURITY.md).

Examples:
  python scripts/init_workspace.py
  python scripts/init_workspace.py --root C:\\temp\\my-app
  python scripts/init_workspace.py --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

DIRS = [
    "inventory",
    "findings/candidates",
    "findings/validated",
    "findings/duplicates",
    "ownership",
    "remediation",
    "verification",
]

SECURITY_STUB = """# Security policy (workspace)

This file was created by `scripts/init_workspace.py` from
[defense-factory-skills](https://github.com/kenhuangus/defense-factory-skills).

## Authorization

- Testing and remediation apply only to systems the operator owns or has
  **written authorization** to assess.
- Unauthorized offensive testing, exploit development, or access against
  third-party systems is refused.

## Scope

- In-scope assets: (list inventory ids / repos / environments)
- Out-of-scope: (list explicitly)

## Severity and SLA (edit to match your org)

| Severity | Initial response | Remediation target |
|----------|------------------|--------------------|
| critical | 4 hours          | 7 days             |
| high     | 1 business day   | 14 days            |
| medium   | 3 business days  | 30 days            |
| low      | 5 business days  | 90 days            |

## Ownership defaults

- Default security contact:
- Escalation path:

## Validation rules

- A finding is **validated** only with dynamic reproduction evidence.
- Static scanner output alone is a **candidate**, not validated.
- A merged PR is **not** remediation complete; post-deploy retest is required
  (see `verify-fix` skill).

## Related root policy

If this repository already has `SECURITY.md` at the repo root, treat that
document as authoritative and keep this workspace copy aligned.
"""

POINTER_TEMPLATE = """# Security policy pointer

Authoritative policy: `{rel_path}`

This workspace uses the repository-root SECURITY.md. Do not diverge local rules
without updating the root file.
"""


def plan_actions(root: Path, force_stub: bool) -> list[tuple[str, Path, str | None]]:
    """Return list of (action, path, content_or_none)."""
    base = root / ".defense-factory"
    actions: list[tuple[str, Path, str | None]] = []
    actions.append(("mkdir", base, None))
    for rel in DIRS:
        actions.append(("mkdir", base / rel, None))

    security_path = base / "SECURITY.md"
    root_security = root / "SECURITY.md"
    if root_security.is_file() and not force_stub:
        try:
            rel = root_security.relative_to(base)
        except ValueError:
            rel = Path("..") / "SECURITY.md"
        content = POINTER_TEMPLATE.format(rel_path=rel.as_posix())
        actions.append(("write", security_path, content))
    else:
        actions.append(("write", security_path, SECURITY_STUB))
    return actions


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize .defense-factory workspace")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Project root (default: current directory)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned actions without writing",
    )
    parser.add_argument(
        "--force-stub",
        action="store_true",
        help="Always write SECURITY stub even if root SECURITY.md exists",
    )
    args = parser.parse_args(argv)

    root = args.root.resolve()
    if not root.is_dir():
        print(f"Root is not a directory: {root}", file=sys.stderr)
        return 2

    actions = plan_actions(root, force_stub=args.force_stub)
    for action, path, content in actions:
        if action == "mkdir":
            if args.dry_run:
                print(f"MKDIR {path}")
            else:
                path.mkdir(parents=True, exist_ok=True)
                print(f"MKDIR {path}")
        elif action == "write":
            assert content is not None
            if path.exists() and not args.force_stub:
                if args.dry_run:
                    print(f"SKIP  {path} (exists)")
                else:
                    print(f"SKIP  {path} (exists)")
                continue
            if args.dry_run:
                print(f"WRITE {path} ({len(content)} bytes)")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                print(f"WRITE {path}")

    print("Done." if not args.dry_run else "Dry-run complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
