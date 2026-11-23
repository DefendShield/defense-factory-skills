---
name: fix-finding
description: Implements a verified-ready code or config fix for an owned finding in the Defense Factory Verified remediation phase. Use after ownership assignment; does not mark the finding verified—that requires verify-fix after deploy.
---

# fix-finding

**Phase:** Verified remediation (fix half)  
**Style:** Blue (defensive)

## When to use

- Validated finding has an ownership assignment
- User asks to remediate a specific finding id

## Preconditions

1. Finding status is `validated` or `remediating`.
2. Ownership assignment exists under `.defense-factory/ownership/`.
3. Authorization to modify the target repository.
4. Clear reproduction notes from validation (so the fix addresses the proven issue).

## Procedure

1. Read finding + evidence + ownership SLA.
2. Implement the minimal fix (code, config, dependency bump, or feature flag) that addresses root cause.
3. Add or update automated tests that would fail on the old behavior when feasible.
4. Open a PR or commit per project norms; record references in `.defense-factory/remediation/<finding-id>.md`:
   - Finding id
   - Change summary
   - PR URL / commit SHAs
   - Test commands run locally
   - Residual risk
5. Set finding `status` to `fixed_pending_verify` (not `verified_fixed`).
6. Explicitly note in the remediation doc: **merged PR is not remediation complete**.

## Required outputs

| Path | Notes |
| --- | --- |
| Code/config changes in the target repo | Actual fix |
| `.defense-factory/remediation/<finding-id>.md` | Remediation record |
| Updated finding JSON | `fixed_pending_verify` |

## Stop / refuse

- Do not claim `verified_fixed` from this skill.
- Do not “fix” by disabling tests or hiding scanner output without addressing the issue.
- Refuse fixes that intentionally weaken security controls without documented risk acceptance in SECURITY.md.

## Next phase

After deploy to the verification environment, run `verify-fix`.
