import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import tmt_gate  # noqa: E402


def doc(*scenarios):
    return {
        "project": "demo",
        "generated": "2026-10-25",
        "catalog": "TMT-CheatSheets@eaabf3d",
        "components": [{"id": "api", "type": "api", "name": "Orders API"}],
        "scenarios": list(scenarios),
    }


def scenario(id_, status, risk, stride=None):
    return {"id": id_, "stride": stride or id_[0], "component": "api",
            "status": status, "risk": risk, "rationale": "r"}


class GateTest(unittest.TestCase):
    def run_gate(self, data, *args):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f)
        try:
            return tmt_gate.main([f.name, *args])
        finally:
            os.unlink(f.name)

    def test_passes_when_high_risk_covered(self):
        data = doc(scenario("S-API-01", "covered", "high"), scenario("D-API-01", "missing", "low"))
        self.assertEqual(self.run_gate(data, "--fail-on", "high"), 0)

    def test_fails_on_missing_high(self):
        self.assertEqual(self.run_gate(doc(scenario("T-API-01", "missing", "high"))), 1)

    def test_partial_blocks_unless_allowed(self):
        data = doc(scenario("E-API-02", "partial", "high"))
        self.assertEqual(self.run_gate(data), 1)
        self.assertEqual(self.run_gate(data, "--allow-partial"), 0)

    def test_threshold_includes_higher_risks(self):
        data = doc(scenario("I-API-01", "missing", "high"))
        self.assertEqual(self.run_gate(data, "--fail-on", "medium"), 1)

    def test_not_applicable_never_blocks(self):
        self.assertEqual(self.run_gate(doc(scenario("S-WEB-01", "not_applicable", "high"))), 0)

    def test_report_only_never_fails_on_gaps(self):
        self.assertEqual(self.run_gate(doc(scenario("T-API-01", "missing", "high")), "--report-only"), 0)

    def test_custom_threat_ids_accepted(self):
        self.assertEqual(self.run_gate(doc(scenario("TM-07", "missing", "high", stride="I"))), 1)

    def test_invalid_document_exits_2(self):
        bad = doc(scenario("X-API-01", "unknown", "critical", stride="Q"))
        self.assertEqual(self.run_gate(bad), 2)
        errors = tmt_gate.validate(bad)
        self.assertEqual(len(errors), 4)

    def test_unknown_component_is_an_error(self):
        s = scenario("S-API-01", "covered", "low")
        s["component"] = "ghost"
        self.assertIn("unknown component", tmt_gate.validate(doc(s))[0])


if __name__ == "__main__":
    unittest.main()
