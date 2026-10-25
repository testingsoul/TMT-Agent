---
name: tmt-write-tests
description: Closes Threat Modeling Testing gaps by generating executable security tests (Given/When/Then, asserting outcome, no side effects, and evidence) in the project's own test framework, then runs them and reports which ones expose missing controls. Use after a TMT gap analysis, or when the user asks to write tests for specific STRIDE scenarios or TMT IDs like T-API-01.
---

# TMT: write the missing tests

**Arguments** (all optional): `[IDs...|--risk high] [--report tmt-report/gaps.json]`

## Paths
- `KIT` = two directories above this file. That's the plugin root, or `.tmt/` when installed into a project.
- `CATALOG` = `KIT/skills/tmt-stride-catalog/references/catalog.md`
- `ROLE` = `KIT/agents/tmt-test-writer.md`
- `GAPS` = the `--report` argument, or `tmt-report/gaps.json` in the current project

## Steps

1. If `GAPS` doesn't exist, run the `tmt-gap-analysis` skill first, or ask the user whether to do that.

2. **Select scenarios.** Use the explicit IDs if given, else `--risk <level>`, else every `missing` and `partial` scenario with risk `high`. If the selection has more than 10 entries, show the list and confirm before writing.

3. **Write the tests.** Group the selected scenarios into batches by component and test file. For each batch, follow `ROLE` with inputs `TARGET`, `CATALOG`, `GAPS`, `IDS`, and `INVENTORY=tmt-report/test-inventory.md`.
   - **Subagents available** (Claude Code `tmt-agent:tmt-test-writer`, OpenCode `@tmt-test-writer`, or any tool that can spawn them): give one subagent per batch. Batches that touch different files can run in parallel. Batches that share a file must run one after another.
   - **No subagents:** do the batches yourself, one at a time, following `ROLE`.

4. **Update the record.** For each ID now covered by a passing test, set `status: covered` in `gaps.json` and add the test to `tests`. A failing test that exposes a missing control leaves the status `partial` and gets a `rationale` note saying what the test exposed.

5. **Report.** Give the user:
   - **Findings first**: tests that fail because the control is missing or broken. These are probable vulnerabilities. For each, give the ID, the test, what happened, and the expected behavior.
   - tests added and passing (now protected against regressions)
   - expected failures marking missing evidence mechanisms (e.g. no audit log)
   - the command to rerun the new tests, and the suggestion to gate CI with `python3 KIT/scripts/tmt_gate.py tmt-report/gaps.json --fail-on high`

Never weaken an assertion to turn a failing security test green.
