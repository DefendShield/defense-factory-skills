---
name: triage-validate-finding
description: Dynamically reproduces finding candidates with authorization and writes validated findings for the Defense Factory Dynamic validation phase. Static-only results stay candidates; refuse unauthorized Red testing.
---

# triage-validate-finding

**Phase:** Dynamic validation  
**Style:** Blue triage + **authorized Red** reproduction only

## When to use

- Candidates exist under `.defense-factory/findings/candidates/`
- User requests confirmation before ownership or fix work
- Never use to attack unauthorized systems

## Preconditions

1. Explicit ownership or **written authorization** referenced in SECURITY.md or a ticket id.
2. Safe environment for reproduction (prefer staging/lab over production).
3. Candidate JSON files present and schema-valid.

## Procedure

1. Load candidate; confirm `asset_id` is in-scope.
2. Record `authorization_ref` (SECURITY.md section + ticket/email id).
3. Attempt **minimal dynamic reproduction** sufficient to prove impact:
   - Authorized requests, config checks, or controlled exploit **replay** against owned/authorized targets only
   - Capture redacted request/response or logs under `.defense-factory/findings/validated/<id>/`
4. Decision:
   - **Validated:** set `status` to `validated`, `evidence.dynamic` to `true`, include `reproduction_steps`, `observed_behavior`, `expected_behavior`, `proof_artifacts`, `authorization_ref`
   - **False positive:** set `status` to `false_positive` with short rationale; keep under candidates or move to `findings/duplicates/` with note
   - **Cannot reproduce:** leave as candidate; document attempts in a sibling `.md` file—**do not** mark validated
5. Write validated file to `.defense-factory/findings/validated/<id>.json`.
6. Validate:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/findings/validated/<id>.json --schema finding
```

*`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*

## Required outputs

| Path | Rule |
| --- | --- |
| `.defense-factory/findings/validated/<id>.json` | Must include dynamic evidence |
| `.defense-factory/findings/validated/<id>/*` | Redacted proof artifacts |

## Stop / refuse

- **Refuse** reproduction against systems lacking ownership or written authorization.
- **Refuse** to mark validated when only static analyzer output exists.
- Do not expand into unrelated offensive tooling development.

## Next phase

`dedupe-findings`, then `route-ownership`.
