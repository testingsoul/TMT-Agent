# Working on TMT-Agent

This repo is the source of a Threat Modeling Testing kit that runs in several coding agents.
The instructions are written once and exposed to each tool through thin entry points.

## Source of truth
- `skills/*/SKILL.md`: the workflows (gap analysis, write tests, catalog). Keep them tool-neutral. Say "subagent if available, otherwise do it yourself", and never depend on one vendor's tool names.
- `agents/*.md`: one role file per phase. Claude Code loads them as subagents, and other tools read them as playbooks. The front matter is Claude Code's. Keep the body self-contained.
- `skills/tmt-stride-catalog/references/catalog.md`: scenario IDs. Never renumber an existing ID, because `gaps.json` files in user repos reference them.
- `templates/gaps.schema.json` and `scripts/tmt_gate.py` must agree. Change both together.

## Per-tool packaging
- Claude Code: `.claude-plugin/plugin.json` + `marketplace.json` (skills/ and agents/ are auto-discovered)
- Codex: `.codex-plugin/plugin.json` + `skills/*/agents/openai.yaml`
- Everything else: `scripts/install.py` generates entry points into a target project

Skill front matter may only use `name`, `description`, `license`, `allowed-tools`, `metadata`, which Codex's validator enforces. Put usage and argument docs in the body.

## Checks
```bash
python3 -m unittest discover -s tests
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .   # if Codex is installed
```
