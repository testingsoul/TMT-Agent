#!/usr/bin/env python3
"""TMT CI gate: fail the build when threats at or above a risk level lack a verifying test.

Usage:
    tmt_gate.py tmt-report/gaps.json --fail-on high
    tmt_gate.py tmt-report/gaps.json --fail-on medium --allow-partial
    tmt_gate.py tmt-report/gaps.json --report-only

Exit codes: 0 = pass, 1 = gaps at/above threshold, 2 = invalid gaps.json.
Standard library only, so it runs in any CI image with Python 3.8+.
"""
import argparse
import json
import re
import sys
from collections import Counter

RISKS = {"low": 1, "medium": 2, "high": 3}
STATUSES = {"covered", "partial", "missing", "not_applicable"}
STRIDE = "STRIDE"
ID_RE = re.compile(r"^([STRIDE]-(WEB|API|DB|OTH)-[A-Z0-9]+|TM-[0-9]+)$")
REQUIRED = ("id", "stride", "component", "status", "risk", "rationale")


def validate(doc):
    """Return a list of human-readable schema errors (empty when valid)."""
    if not isinstance(doc, dict):
        return ["top level must be an object"]
    errors = []
    for key in ("project", "generated", "catalog", "components", "scenarios"):
        if key not in doc:
            errors.append(f"missing top-level key '{key}'")
    component_ids = {c.get("id") for c in doc.get("components", []) if isinstance(c, dict)}
    for i, s in enumerate(doc.get("scenarios", [])):
        where = f"scenarios[{i}]"
        if not isinstance(s, dict):
            errors.append(f"{where}: must be an object")
            continue
        where = f"{where} ({s.get('id', '?')})"
        for key in REQUIRED:
            if key not in s:
                errors.append(f"{where}: missing '{key}'")
        if "id" in s and not ID_RE.match(str(s["id"])):
            errors.append(f"{where}: invalid id")
        if "stride" in s and s["stride"] not in STRIDE:
            errors.append(f"{where}: invalid stride '{s['stride']}'")
        if "status" in s and s["status"] not in STATUSES:
            errors.append(f"{where}: invalid status '{s['status']}'")
        if "risk" in s and s["risk"] not in RISKS:
            errors.append(f"{where}: invalid risk '{s['risk']}'")
        if component_ids and s.get("component") not in component_ids:
            errors.append(f"{where}: unknown component '{s.get('component')}'")
    return errors


def blocking(scenarios, fail_on, allow_partial):
    statuses = {"missing"} if allow_partial else {"missing", "partial"}
    threshold = RISKS[fail_on]
    return [
        s for s in scenarios
        if s["status"] in statuses and RISKS[s["risk"]] >= threshold
    ]


def summary(scenarios):
    counts = Counter((s["stride"], s["status"]) for s in scenarios)
    lines = ["STRIDE  covered  partial  missing  n/a"]
    for letter in STRIDE:
        row = [counts[(letter, st)] for st in ("covered", "partial", "missing", "not_applicable")]
        lines.append(f"{letter:<7} " + "  ".join(f"{n:>7}" for n in row))
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("gaps", help="path to gaps.json")
    parser.add_argument("--fail-on", choices=list(RISKS), default="high")
    parser.add_argument("--allow-partial", action="store_true",
                        help="only 'missing' scenarios block; 'partial' ones pass")
    parser.add_argument("--report-only", action="store_true",
                        help="validate and print the summary, never fail on gaps")
    args = parser.parse_args(argv)

    try:
        with open(args.gaps, encoding="utf-8") as f:
            doc = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"tmt-gate: cannot read {args.gaps}: {e}", file=sys.stderr)
        return 2

    errors = validate(doc)
    if errors:
        print("tmt-gate: invalid gaps.json", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    scenarios = doc["scenarios"]
    print(f"TMT gate · {doc['project']} · {doc['catalog']}")
    print(summary(scenarios))

    if args.report_only:
        return 0

    found = blocking(scenarios, args.fail_on, args.allow_partial)
    if not found:
        print(f"\nPASS: no untested threats at risk >= {args.fail_on}")
        return 0
    print(f"\nFAIL: {len(found)} threat(s) at risk >= {args.fail_on} without a verifying test:")
    for s in sorted(found, key=lambda s: (-RISKS[s["risk"]], STRIDE.index(s["stride"]), s["id"])):
        print(f"  [{s['risk']}] {s['id']} ({s['component']}, {s['status']}): {s.get('title', s['rationale'])}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
