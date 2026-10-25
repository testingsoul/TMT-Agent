---
name: tmt-stride-catalog
description: Reference catalog of Threat Modeling Testing scenarios. STRIDE × Web/API/Database/Other systems, with stable IDs (e.g. S-API-01, E-WEB-02), Given/When/Then test scenarios, the evidence to capture, and what a test must assert to count as coverage. Use when the user asks what security tests a component should have, wants test ideas for a STRIDE category, asks what a TMT ID means, or is turning a threat model into test cases.
---

# TMT STRIDE catalog

Two references:
- `references/catalog.md`: every scenario with its ID, when it applies, what "covered" means, and grep hints. Start here.
- `references/cheatsheets/`: the original [TMT-CheatSheets](https://github.com/testingsoul/TMT-CheatSheets), organized as `<Category>/<system>.md`, with full Given/When/Then text and "Evidence to capture" / "Automation ideas".

## How to answer
- **"What tests should X have?"** Find X's system type, list the applicable IDs from `catalog.md` grouped by STRIDE, and adapt each Given/When/Then to X's real names (routes, roles, fields).
- **"Turn this threat into a test."** Match the threat to an ID, or create a `TM-NN` if none fits. Write the hypothesis as Given/When/Then, then list the three assertions it needs: **outcome**, **no side effects**, **evidence**.
- **"Explain ID Y."** Quote the row, and the scenario from the matching cheat sheet.

Every test idea should say which of the three assertions it covers. A test that shows the attack fails but checks no evidence is only `partial` coverage.
