"""Regression tests for the isolated synthetic read-only CLI."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).parent
CLI = HERE / "refund_status_cli.py"
FIXTURES = HERE / "fixtures"


class RefundStatusCliTests(unittest.TestCase):
    def invoke(self, case_id: str, fixture: str, *extra: str) -> tuple[subprocess.CompletedProcess[str], dict]:
        completed = subprocess.run(
            [sys.executable, str(CLI), case_id, str(FIXTURES / fixture), *extra],
            check=False,
            capture_output=True,
            text=True,
        )
        return completed, json.loads(completed.stdout)

    def assert_error(self, payload: dict, code: str) -> None:
        self.assertEqual(payload["error"]["code"], code)
        self.assertNotIn("result", payload)

    def test_normal_result_contains_full_evidence_envelope(self) -> None:
        completed, payload = self.invoke("case_synth_001", "valid.json")
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(
            set(payload),
            {"result", "semanticDefinitionVersion", "sourceEvidence", "freshness", "accessDecision"},
        )
        self.assertEqual(payload["result"]["refundStatus"], "approved")
        self.assertEqual(
            set(payload["freshness"]),
            {"observedAt", "asOf", "expiresAt", "status"},
        )
        self.assertTrue(payload["accessDecision"]["allowed"])

    def test_missing_id_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_missing", "valid.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "refund_case_not_found")

    def test_stale_evidence_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_001", "stale.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "evidence_outside_freshness_window")

    def test_as_of_before_observed_at_fails_closed(self) -> None:
        completed, payload = self.invoke(
            "case_synth_001",
            "valid.json",
            "--as-of",
            "2026-08-27T23:59:59Z",
        )
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "evidence_outside_freshness_window")

    def test_missing_source_id_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_001", "missing_source_id.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "invalid_source_evidence")

    def test_missing_source_kind_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_001", "missing_source_kind.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "invalid_source_evidence")

    def test_denied_access_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_denied", "denied.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "access_denied")

    def test_unsupported_version_fails_closed(self) -> None:
        completed, payload = self.invoke("case_synth_001", "unsupported.json")
        self.assertNotEqual(completed.returncode, 0)
        self.assert_error(payload, "unsupported_semantic_definition")


if __name__ == "__main__":
    unittest.main()
