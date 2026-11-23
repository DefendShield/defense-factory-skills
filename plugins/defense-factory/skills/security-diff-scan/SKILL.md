---
name: security-diff-scan
description: Performs change-scoped defensive discovery on a diff or PR for the Defense Factory Discovery phase. Use on pull requests or local uncommitted changes instead of a full-fleet scan.
---

# security-diff-scan

**Phase:** Discovery  
**Style:** Blue (defensive)

## When to use

- User points at a PR, branch diff, or local changes
- Faster path than `security-scan` for incremental review

## Preconditions

1. Authorization for the repository under review.
2. SECURITY.md present.
3. Ability to obtain the diff (`git diff`, `gh pr diff`, etc.).

## Procedure

1. Determine base and head (e.g. `main...HEAD`).
2. List changed paths; map to inventory `asset_id`s when possible.
3. Review the diff for:
   - AuthZ/AuthN bypass patterns
   - Injection sinks with new untrusted input
   - New secrets or credentials
   - Dangerous default configs
   - Dependency upgrades with known issues
4. Run targeted defensive tools on changed packages/files only when available.
5. Emit **candidate** findings to `.defense-factory/findings/candidates/` with:
   - `source_skill`: `security-diff-scan`
   - `location.path` set to changed files
   - Tag `diff-scan` and optional `pr_url`
6. Write `.defense-factory/findings/candidates/_diff-scan-<pr-or-sha>.md` summarizing scope and residual risk (unreviewed areas).
7. Validate JSON with `python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py"`.

*`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*

## Required outputs

| Path | Notes |
| --- | --- |
| `.defense-factory/findings/candidates/*.json` | Candidates only |
| `.defense-factory/findings/candidates/_diff-scan-*.md` | Scope report |

## Stop / refuse

- Same authorization rules as `security-scan`.
- Do not mark findings validated.
- If the diff touches systems outside authorization, stop and ask for scope clarification.

## Next phase

`triage-validate-finding` for candidates that need dynamic proof; then `dedupe-findings`.
