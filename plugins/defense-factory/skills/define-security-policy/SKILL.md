---
name: define-security-policy
description: Creates or updates SECURITY.md and authorization scope for a repo in the Defense Factory prepare phase. Use when starting a defensive assessment, before inventory or scans, or when SLA/ownership rules are missing.
---

# define-security-policy

**Phase:** Prepare / shared context  
**Style:** Blue (defensive)

## When to use

- Project has no usable `SECURITY.md`
- Scope, authorization, or severity SLAs are unclear
- Before `build-inventory` or any scan/validation skill

## Preconditions

1. User intends authorized defensive work on an owned or authorized system.
2. Write access to the target repository (or a docs location they specify).
3. Prefer running `python "${CLAUDE_PLUGIN_ROOT}/scripts/init_workspace.py" --root <repo>` first so `.defense-factory/` exists.

*`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*

## Procedure

1. Locate existing policy: repo-root `SECURITY.md`, then `.defense-factory/SECURITY.md`.
2. Interview or infer from repo docs:
   - Owner / security contact
   - In-scope assets and environments
   - Explicit out-of-scope items
   - Written authorization boundaries for any dynamic testing
   - Severity → SLA mapping
3. Write or update `SECURITY.md` at repo root with sections:
   - Authorization
   - Scope (in / out)
   - Severity and SLA
   - Ownership defaults and escalation
   - Validation rules (dynamic evidence required)
   - Remediation rules (merge ≠ verified)
   - Reporting contact
4. Mirror a pointer or copy under `.defense-factory/SECURITY.md` via `${CLAUDE_PLUGIN_ROOT}/scripts/init_workspace.py` if the workspace is new.
5. Record a short changelog note in `.defense-factory/inventory/_policy_init.md` with date and author.

## Required outputs

| Path | Content |
| --- | --- |
| `SECURITY.md` | Authoritative policy |
| `.defense-factory/SECURITY.md` | Stub or pointer |
| `.defense-factory/inventory/_policy_init.md` | Init note |

## Stop / refuse

- Refuse to encode authorization for attacking third-party systems the user does not own or lack written permission to test.
- Do not invent legal authorization; require the user to state ownership or provide an authorization reference.

## Next phase

Proceed to `threat-model`, then `build-inventory`.
