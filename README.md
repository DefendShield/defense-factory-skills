# Defense Factory marketplace

A Claude Code plugin marketplace that lists one plugin, **`defense-factory`** — authorized
defensive-security workflow skills (inventory → scan → validate → own → fix → verify).

```bash
claude plugin marketplace add "C:/Users/sabar/OneDrive/Desktop/DefenseFactory/plugin"
claude plugin install defense-factory@defense-factory-skills
```

- Marketplace manifest: [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)
- Plugin: [`plugins/defense-factory/`](plugins/defense-factory/) (see its [README](plugins/defense-factory/README.md))

Adapted for Claude from [Ken Huang's `defense-factory-skills`](https://github.com/kenhuangus/defense-factory-skills) (MIT).
Not official OpenAI software; not affiliated with or endorsed by OpenAI.
