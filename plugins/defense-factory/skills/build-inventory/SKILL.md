---
name: build-inventory
description: Enumerates services, repos, APIs, and related assets into schema-valid inventory files for the Defense Factory Inventory phase. Use when starting discovery or when asset ownership is unknown.
---

# build-inventory

**Phase:** Inventory  
**Style:** Blue (defensive)

## When to use

- After prepare skills (policy + optional threat model)
- Before `security-scan` / `security-diff-scan`
- When ownership routing needs accurate `asset_id`s

## Preconditions

1. Authorization / ownership confirmed per SECURITY.md.
2. `.defense-factory/` exists (`python "${CLAUDE_PLUGIN_ROOT}/scripts/init_workspace.py"`).

   *`${CLAUDE_PLUGIN_ROOT}` is set automatically by Claude Code to the plugin install directory, which holds the `scripts/`, `schemas/`, and `fixtures/` this skill uses.*
3. Read access to repos, cloud inventories, manifests, or deployment configs in scope.

## Procedure

1. Collect sources: git remotes, package manifests, Docker/K8s/IaC, API gateways, service catalogs, README deploy docs.
2. For each asset, create an entry matching `${CLAUDE_PLUGIN_ROOT}/schemas/inventory-entry.schema.json`:
   - `id` (stable, e.g. `inv-<type>-<name>`)
   - `name`, `asset_type`, `owner`, `environment`, `discovered_at`, `source`
   - Optional `urls`, `repos`, `tags`, `exposure`, `notes`
3. Write:
   - `.defense-factory/inventory/inventory.json` — `{ "entries": [ ... ] }`
   - Optionally one file per asset under `.defense-factory/inventory/entries/`
4. Validate:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/inventory/inventory.json --schema inventory-entry
```

5. Flag assets with `owner` unknown; list them for `route-ownership` later.
6. Cross-check threat-model priorities; tag high-priority assets.

## Required outputs

| Path | Schema |
| --- | --- |
| `.defense-factory/inventory/inventory.json` | `inventory-entry` (entries array) |

## Stop / refuse

- Do not scan or inventory out-of-scope third-party production systems without authorization.
- Do not store secrets (API keys, passwords) inside inventory notes.

## Next phase

`security-scan` (full) or `security-diff-scan` (change-scoped).
