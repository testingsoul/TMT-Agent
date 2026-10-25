# TMT Gap Report: {{project}}

_Generated {{date}} · Catalog: {{catalog}} · Threat model: {{threat_model or "none, catalog only"}}_

> If it is not tested, it is not real.

## Summary

| STRIDE | Applicable | Covered | Partial | Missing |
|---|---|---|---|---|
| Spoofing | | | | |
| Tampering | | | | |
| Repudiation | | | | |
| Information disclosure | | | | |
| Denial of service | | | | |
| Elevation of privilege | | | | |

**Top risks without a test:** the 3–5 highest-risk `missing` items, one line each.

## System under test

Components, exposure, trust boundaries, and auth mechanisms, taken from `system-profile.md`.

## Gaps (highest risk first)

### {{ID}}: {{title}} · {{component}} · risk **{{risk}}** · {{status}}

- **Where:** `path/to/route_or_config` (code locations the threat applies to)
- **Why it matters here:** one or two sentences tied to this codebase, not generic text.
- **Existing tests:** `tests/x.py::test_y` asserts the outcome but not the evidence (when partial).
- **Missing assertions:** outcome / no side effects / evidence
- **Hypothesis to test:**
  ```gherkin
  Given …
  When …
  Then …
  ```
- **Suggested home:** `tests/security/test_….py` using the project's existing fixtures `…`

## Covered (for the record)

| ID | Component | Test(s) |
|---|---|---|

## Not applicable

| ID | Reason |
|---|---|

## Next steps

1. Generate tests for the high-risk gaps: `/tmt-write-tests <IDs>`
2. Wire the gate into CI: `python scripts/tmt_gate.py tmt-report/gaps.json --fail-on high`
3. Re-run `/tmt-gap-analysis` after fixes (revalidation).
