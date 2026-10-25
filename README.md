# TMT-Agent

**Threat Modeling Testing, automated.** TMT-Agent is a set of skills and agents for coding assistants (Claude Code, OpenAI Codex, Gemini CLI, Cursor, GitHub Copilot, OpenCode, and any tool that reads `AGENTS.md`). They read your code and your tests, then tell you which threats from your threat model (or from STRIDE, if you don't have one) **have no test proving the control works**. It can then write those tests for you.

> If it is not tested, it is not real.

It's built on the [TMT-CheatSheets](https://github.com/testingsoul/TMT-CheatSheets), which use STRIDE as a test engine across Web, API, Database, and other systems.

## The workflow

```
threat ──► hypothesis ──► test ──► evidence ──► fix ──► revalidation
 └──── /tmt-gap-analysis ────┘└──── /tmt-write-tests ────┘└ tmt_gate.py in CI ┘
```

| Phase | Agent | Output |
|---|---|---|
| 1. Map the system | `tmt-system-mapper` | `tmt-report/system-profile.md`: components, entry points, trust boundaries, auth, sensitive data, imported threats, scenario applicability |
| 2. Inventory the tests | `tmt-test-inventory` | `tmt-report/test-inventory.md`: every security-relevant test classified by STRIDE ID, plus **false-coverage** warnings |
| 3. Find the gaps | `tmt-gap-analyst` | `tmt-report/gap-report.md` + `gaps.json`: prioritized gap matrix with Given/When/Then hypotheses |
| 4. Close the gaps | `tmt-test-writer` | Tests in your own framework. Failing tests are reported as **findings** |
| 5. Keep them closed | `scripts/tmt_gate.py` | CI fails when high-risk threats lose their tests |

Phases 1 and 2 run in parallel when the tool supports subagents. Tools without subagents run the same phases one after another, reading each role file in `agents/` as a playbook. Each phase writes its result to disk, so the output is the same either way.

### What counts as "covered"

A test only covers a scenario if it makes the three TMT assertions (from the cheat sheets' *Evidence to capture*):

1. **Outcome**: the attack is rejected (`403`, not just `!= 200`)
2. **No side effects**: state re-read and unchanged
3. **Evidence**: the audit or security event exists, without leaking secrets

A test that checks the outcome but not the evidence is `partial`. Tests that mock away the control they claim to test, are skipped, or only check the UI are flagged as false coverage.

## Supported tools

| Tool | Models | Install | Run | Subagents |
|---|---|---|---|---|
| Claude Code | Claude | plugin (below) | `/tmt-gap-analysis` | yes, parallel phases |
| OpenAI Codex | GPT / Codex | Codex plugin (below), or `install.py --target codex` | `$tmt-gap-analysis` | phases run in sequence |
| Gemini CLI | Gemini | `install.py --target gemini` | `/tmt:gap-analysis` | phases run in sequence |
| Cursor | any model in Cursor | `install.py --target cursor` | `/tmt-gap-analysis` | phases run in sequence |
| GitHub Copilot (VS Code) | any Copilot model | `install.py --target copilot` | `/tmt-gap-analysis` | phases run in sequence |
| OpenCode | any provider, incl. local models | `install.py --target opencode` | `/tmt-gap-analysis` | yes (`@tmt-system-mapper`, …) |
| Windsurf, Zed, Amp, Aider, others | any | `install.py --target agents-md` | *"run the TMT gap analysis"* | depends on the tool |

The skills and role files are the single source of truth. The installer copies them to `<project>/.tmt/` and adds small entry points that say "read `.tmt/skills/<skill>/SKILL.md` and follow it". After you update TMT-Agent, rerun the installer to refresh `.tmt/`.

## Install

### Claude Code

```bash
/plugin marketplace add testingsoul/TMT-Agent
/plugin install tmt-agent@testingsoul

# or locally while developing
claude --plugin-dir /path/to/TMT-Agent
```

### OpenAI Codex (plugin)

The repo includes a Codex manifest (`.codex-plugin/plugin.json`). To install it as a personal plugin, place the repo at `~/plugins/tmt-agent` and add this entry to `plugins` in `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "tmt-agent",
  "source": { "source": "local", "path": "./plugins/tmt-agent" },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
  "category": "Coding"
}
```

Or install it per project with `install.py --target codex`. That writes `.agents/skills/` plus `AGENTS.md`.

### Any other tool (per project)

```bash
python3 /path/to/TMT-Agent/scripts/install.py --project /path/to/your-app --target gemini,cursor
python3 /path/to/TMT-Agent/scripts/install.py --project . --target all
```

Targets: `agents-md`, `codex`, `gemini`, `cursor`, `copilot`, `opencode`, `claude` (project-level copy for teams not using the plugin), or `all`.

- The installer never overwrites a file it didn't create (use `--force` to override).
- It adds a marked block to `AGENTS.md`/`GEMINI.md` without touching the rest of the file.
- Commit the generated files so the whole team gets the commands.

## Use

Shown with Claude Code syntax. Use your tool's prefix from the table above.

```text
/tmt-gap-analysis                                  # current repo, catalog-only (auto-detects a threat model)
/tmt-gap-analysis ./services/orders --threat-model docs/orders.tm7
/tmt-gap-analysis --scope api,database --run-tests
/tmt-write-tests --risk high                       # close all high-risk gaps
/tmt-write-tests T-API-01 E-API-02                 # close specific gaps
```

In any tool you can also just ask: *"What security tests am I missing for the orders API?"* or *"What should a test for S-API-04 look like here?"* (the `tmt-stride-catalog` skill).

Analysis quality depends on the model. Smaller or local models can run the workflow, but expect weaker false-coverage detection. For those, use `--scope` to keep each run small.

**Supported threat models:** Microsoft Threat Modeling Tool (`.tm7`), OWASP Threat Dragon (`.json`), pytm, Markdown/CSV. Threats that match a catalog scenario reuse its ID. The rest become `TM-NN` custom scenarios.

## Make threat models fail builds

```yaml
# .github/workflows/tmt.yml
- name: TMT gate
  run: python3 .tmt/scripts/tmt_gate.py tmt-report/gaps.json --fail-on high   # path after install.py
```

Options: `--fail-on high|medium|low`, `--allow-partial` (only `missing` blocks), `--report-only`. Exit codes: `0` pass, `1` gaps, `2` invalid file. The script uses only the Python 3 standard library.

Commit `tmt-report/gaps.json` so the gate tracks your accepted baseline. Rerun `/tmt-gap-analysis` after each fix.

## Scenario IDs

`<STRIDE>-<SYSTEM>-<NN>`, e.g. `S-API-01` (invalid/expired token), `T-API-01` (IDOR via parameter tampering), `I-DB-04` (search index exposure: the Elasticsearch case). The full list is in [catalog.md](skills/tmt-stride-catalog/references/catalog.md).

## Layout

```
.claude-plugin/        Claude Code plugin.json, marketplace.json
.codex-plugin/         Codex plugin.json
AGENTS.md              notes for contributors (any agent)
agents/                role files: tmt-system-mapper, tmt-test-inventory, tmt-gap-analyst, tmt-test-writer
skills/
  tmt-gap-analysis/    orchestrator              (+ agents/openai.yaml for Codex)
  tmt-write-tests/     test generation           (+ agents/openai.yaml)
  tmt-stride-catalog/  catalog.md + vendored TMT-CheatSheets
templates/             gap-report.md, gaps.schema.json
scripts/
  tmt_gate.py          CI gate
  install.py           per-project installer for Codex, Gemini, Cursor, Copilot, OpenCode, AGENTS.md
tests/                 python3 -m unittest discover -s tests
```

## Updating the cheat sheets

The cheat sheets are vendored in `skills/tmt-stride-catalog/references/cheatsheets/` (upstream `eaabf3d`). After pulling upstream changes, add or adjust the matching rows in `catalog.md` so that every scenario has an ID.
