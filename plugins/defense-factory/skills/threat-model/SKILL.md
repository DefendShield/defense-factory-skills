---
name: threat-model
description: Produces a concise threat model for in-scope assets during the Defense Factory prepare phase. Use after SECURITY.md exists and before or alongside inventory to prioritize discovery and validation effort.
---

# threat-model

**Phase:** Prepare / shared context  
**Style:** Blue (defensive)

## When to use

- After `define-security-policy`
- When prioritizing what to inventory and scan
- Before large `security-scan` runs

## Preconditions

1. `SECURITY.md` (or `.defense-factory/SECURITY.md`) exists and defines scope.
2. Authorization for the target system is confirmed.
3. Access to architecture docs, OpenAPI specs, IaC, or runnable services as available.

## Procedure

1. List trust boundaries: users, admins, services, data stores, identity providers, CI/CD.
2. For each in-scope asset (even if inventory is incomplete), note:
   - Assets and data classification
   - Entry points (APIs, UIs, jobs, webhooks)
   - Authn/authz mechanisms
   - High-value abuse cases (authorization bypass, injection, secret exposure, supply chain)
3. Rank threats by likelihood × impact using SECURITY.md severity language.
4. Write `.defense-factory/inventory/threat-model.md` with:
   - System summary
   - Trust boundaries
   - Threat list (id, title, assets, severity hypothesis, mitigations present/missing)
   - Discovery priorities (what `security-scan` should cover first)
5. Optionally add machine-readable priorities as JSON lines in `.defense-factory/inventory/threat-priorities.json` (`[{"threat_id","asset_hint","priority"}]`).

## Required outputs

| Path | Content |
| --- | --- |
| `.defense-factory/inventory/threat-model.md` | Human-readable threat model |
| `.defense-factory/inventory/threat-priorities.json` | Optional priority list |

## Stop / refuse

- Do not produce weaponized exploit playbooks for unauthorized targets.
- Keep abuse cases at a defensive design level unless later moving to authorized `triage-validate-finding`.

## Next phase

`build-inventory` using threat priorities to decide depth of enumeration.
