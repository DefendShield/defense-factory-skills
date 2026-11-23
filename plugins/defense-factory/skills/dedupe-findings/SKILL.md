---
name: dedupe-findings
description: Clusters duplicate and near-duplicate security findings after Discovery or validation in the Defense Factory Dynamic validation phase. Use before ownership assignment to reduce noise and link duplicates to a canonical finding.
---

# dedupe-findings

**Phase:** Dynamic validation  
**Style:** Blue (defensive)

## When to use

- Multiple candidates or validated findings refer to the same root cause
- Before `route-ownership` to avoid duplicate tickets

## Preconditions

1. Findings under `.defense-factory/findings/candidates/` and/or `validated/`.
2. Inventory available for asset context.

## Procedure

1. Load all findings; normalize keys: `asset_id`, `location.path`, `location.endpoint`, `cwe`, title tokens.
2. Group by similarity:
   - Same endpoint + same CWE
   - Same file sink + same issue class
   - Explicit scanner duplicate ids if present
3. Choose a **canonical** finding (prefer `validated` over `candidate`; else highest severity; else earliest `discovered_at`).
4. For each duplicate:
   - Set `status` to `duplicate`
   - Set `duplicate_of` to canonical id
   - Write to `.defense-factory/findings/duplicates/<id>.json`
5. Write a merge report `.defense-factory/findings/duplicates/_dedupe-report.md` with groups and canonical ids.
6. Validate duplicate JSON files with `python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" --schema finding`.

*`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*

## Required outputs

| Path | Notes |
| --- | --- |
| `.defense-factory/findings/duplicates/*.json` | `status=duplicate`, `duplicate_of` set |
| `.defense-factory/findings/duplicates/_dedupe-report.md` | Group summary |

## Stop / refuse

- Do not delete canonical validated evidence.
- Do not mark distinct issues as duplicates to hide risk; when unsure, keep separate.

## Next phase

`route-ownership` on canonical validated findings.
