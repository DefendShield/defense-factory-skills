---
name: verify-fix
description: Independently retests a remediated finding after deploy for the Defense Factory Verified remediation phase. Use when a fix has shipped; a merged PR alone is never sufficient to mark remediation complete.
---

# verify-fix

**Phase:** Verified remediation (verify half)  
**Style:** Blue (defensive); authorized Red replay only to confirm fix

## When to use

- Finding is `fixed_pending_verify`
- Fix is deployed to a named environment (staging/production/lab)
- User requests closure evidence

## Preconditions

1. Remediation record exists under `.defense-factory/remediation/`.
2. Deployed version / release id is known.
3. Prefer a **verifier** different from the fix author when staffing allows.
4. Authorization still valid for retest environment.

## Procedure

1. Load original validated evidence (`reproduction_steps`).
2. Retest on the **deployed** environment using the same dynamic method (or an equivalent authorized check).
3. Capture new redacted proof under `.defense-factory/verification/<finding-id>/`.
4. Write `${CLAUDE_PLUGIN_ROOT}/schemas/verification-record.schema.json` object to `.defense-factory/verification/<id>.json` with:
   - `result`: `fixed` | `still_vulnerable` | `inconclusive` | `regressed`
   - `retest_method`
   - `evidence.summary` + `proof_artifacts` (min 1)
   - `merged_pr_alone_insufficient`: `true`
   - `remediation_ref` (PR/commit) as informational only

   *`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*
5. Update finding:
   - `verified_fixed` if `result=fixed`
   - else return to `remediating` / reopen ownership
6. Validate:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/verification/<id>.json --schema verification-record
```

## Required outputs

| Path | Schema |
| --- | --- |
| `.defense-factory/verification/<id>.json` | `verification-record` |
| `.defense-factory/verification/<finding-id>/*` | Retest proof |
| Updated finding JSON | Final status |

## Stop / refuse

- **Refuse** to mark complete based only on PR merge, green CI, or scanner silence without post-deploy retest.
- Refuse unauthorized retest targets.
- If environment is not actually deployed, result must be `inconclusive`, not `fixed`.

## Next phase

Loop complete for this finding. Feed residual issues back to `security-scan` / `fix-finding` as needed.
