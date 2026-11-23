---
name: route-ownership
description: Assigns accountable owners and SLAs to validated findings for the Defense Factory Ownership phase. Use after validation and deduplication when fix responsibility must be explicit.
---

# route-ownership

**Phase:** Ownership  
**Style:** Blue (defensive)

## When to use

- Validated findings exist and need owners
- Inventory `owner` fields and SECURITY.md contacts are available

## Preconditions

1. Canonical validated findings in `.defense-factory/findings/validated/`.
2. SECURITY.md severity → SLA mapping.
3. Team/person directory or CODEOWNERS / inventory owners.

## Procedure

1. For each validated finding (skip duplicates):
   - Resolve owner from inventory `asset_id` → `owner`, else CODEOWNERS for `location.path`, else SECURITY.md default contact.
2. Map severity to priority and `sla_due`:
   - critical → `p0`, high → `p1`, medium → `p2`, low/info → `p3`
   - Compute `sla_due` from SECURITY.md remediation targets using UTC dates.
3. Create assignment per `${CLAUDE_PLUGIN_ROOT}/schemas/ownership-assignment.schema.json`.

   *`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*
4. Optionally open a tracker issue; store `tracker_url`.
5. Write `.defense-factory/ownership/<assignment-id>.json`.
6. Update finding `owner` field and set `status` to `remediating` when accepted.
7. Validate:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/ownership/<id>.json --schema ownership-assignment
```

## Required outputs

| Path | Schema |
| --- | --- |
| `.defense-factory/ownership/*.json` | `ownership-assignment` |
| Updated finding JSON | `owner` set |

## Stop / refuse

- Do not assign ownership for unauthorized/out-of-scope findings; close the loop with policy instead.
- Do not leave `owner` as an empty string; use an explicit escalation contact.

## Next phase

`fix-finding` by the assigned owner (agent-assisted).
