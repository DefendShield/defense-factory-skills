---
name: security-scan
description: Runs authorized defensive discovery across inventoried assets and writes finding candidates for the Defense Factory Discovery phase. Use for baseline or periodic scans, not for unauthorized offensive testing.
---

# security-scan

**Phase:** Discovery  
**Style:** Blue (defensive)

## When to use

- Inventory exists under `.defense-factory/inventory/`
- Full or periodic discovery is requested
- Prefer `security-diff-scan` instead when only a PR/diff is in scope

## Preconditions

1. Written authorization / ownership for targets in SECURITY.md.
2. Inventory entries with ids for assets to scan.
3. Tooling available in the environment (language scanners, dependency audit, secret scanners, config linters). Use what the repo already supports; do not install malware or attack frameworks.

## Procedure

1. Read inventory and threat priorities; select in-scope assets.
2. Run **defensive** checks only, for example:
   - Dependency vulnerability audit (`npm audit`, `pip-audit`, etc. as applicable)
   - Secret scanning on repo contents
   - SAST / linters the project already uses
   - Misconfiguration checks on IaC the user owns
3. For each issue, write a **candidate** finding (`status: "candidate"`) per `${CLAUDE_PLUGIN_ROOT}/schemas/finding.schema.json` **without** claiming validation.

*`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*

4. Save each file to `.defense-factory/findings/candidates/<id>.json`.
5. Add a run log `.defense-factory/findings/candidates/_scan-run-<timestamp>.md` listing tools, versions, commands, and asset ids.
6. Validate candidates:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/findings/candidates/<id>.json --schema finding
```

## Required outputs

| Path | Notes |
| --- | --- |
| `.defense-factory/findings/candidates/*.json` | `status=candidate` |
| `.defense-factory/findings/candidates/_scan-run-*.md` | Tooling log |

## Stop / refuse

- Refuse unauthorized offensive scanning of third-party systems.
- Do not set `status` to `validated` from this skill.
- Do not produce weaponized exploit payloads; record location and descriptive risk only.

## Next phase

`triage-validate-finding` for dynamic confirmation; optionally `dedupe-findings` if volume is high.
