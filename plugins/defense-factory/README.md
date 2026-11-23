# Defense Factory (Claude Code plugin)

Authorized **defensive** security workflow skills for Claude Code — mapping findings from inventory
through verified remediation. Use only on systems you own or have **written authorization** to test.

> Adapted for Claude from [Ken Huang's `defense-factory-skills`](https://github.com/kenhuangus/defense-factory-skills) (MIT).
> **Not official OpenAI software** — illustrative skills inspired by publicly described OpenAI Defense
> Factory concepts; not affiliated with, endorsed by, or part of OpenAI.

## Skills (10)

| Phase | Skills |
| --- | --- |
| Prepare | `define-security-policy`, `threat-model` |
| Inventory | `build-inventory` |
| Discovery | `security-scan`, `security-diff-scan` |
| Dynamic validation | `triage-validate-finding`, `dedupe-findings` |
| Ownership | `route-ownership` |
| Verified remediation | `fix-finding`, `verify-fix` |

Once the plugin is enabled, each skill is namespaced under it, e.g. `/defense-factory:threat-model`,
or it triggers automatically when a task matches its description.

## Install

This directory's parent (`plugin/`) is a marketplace that lists this plugin. Point Claude Code at it:

```bash
claude plugin marketplace add "C:/Users/sabar/OneDrive/Desktop/DefenseFactory/plugin"
claude plugin install defense-factory@defense-factory-skills
```

Or load it directly, without a marketplace, for local use or development:

```bash
claude --plugin-dir "C:/Users/sabar/OneDrive/Desktop/DefenseFactory/plugin/plugins/defense-factory"
```

To host it for others, push the `plugin/` directory to a git repository; teammates then run
`claude plugin marketplace add <owner>/<repo>` followed by the install command above.

## Bundled tooling

The plugin bundles `scripts/` (workspace init + artifact validation), `schemas/` (artifact JSON
schemas), and `fixtures/` (sample artifacts). Skills reference these via `${CLAUDE_PLUGIN_ROOT}`,
which Claude Code resolves to the plugin's install directory automatically — no path setup needed.
A command a skill runs looks like:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/validate_artifacts.py" .defense-factory/findings/validated/<id>.json --schema finding
```

Workspace artifacts are written under `.defense-factory/` in the repository you are assessing.

## Hard rules (all skills)

- Refuse unauthorized offensive work and exploit development for systems the user does not own or
  lacks written authorization to test.
- Validation requires reproduction evidence; static-only is not validated.
- A merged PR is not remediation complete; verification requires post-deploy retest.

## License

MIT © 2026 Ken Huang (original `defense-factory-skills`) and Sabareesh VK (Claude adaptation).
See [LICENSE](LICENSE).
