import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

EXAMPLE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXAMPLE / "scripts"))
import replay_account_reconciliation as replay  # noqa: E402


def fixture(relative):
    return json.loads((EXAMPLE / relative).read_text(encoding="utf-8"))


class ReplayTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = fixture("evidence/reconciliation-snapshot.json")
        self.semantics = fixture("artifacts/semantic-definitions.json")
        self.decision = fixture("artifacts/decision-service.json")
        self.access = fixture("evidence/local-access-decision.json")

    def invoke(self, **kwargs):
        return replay.replay(copy.deepcopy(kwargs.get("snapshot", self.snapshot)), copy.deepcopy(kwargs.get("semantics", self.semantics)), copy.deepcopy(kwargs.get("decision", self.decision)), copy.deepcopy(kwargs.get("access", self.access)), kwargs.get("as_of", replay.DEFAULT_AS_OF), kwargs.get("actor", replay.DEFAULT_ACTOR), kwargs.get("scenario", replay.DEFAULT_SCENARIO))

    def totals(self, snapshot):
        snapshot["controlTotals"] = {"bankRecordCount": len(snapshot["bankTransactions"]), "bankAmountMinor": sum(r["amountMinor"] for r in snapshot["bankTransactions"]), "ledgerRecordCount": len(snapshot["ledgerEntries"]), "ledgerAmountMinor": sum(r["amountMinor"] for r in snapshot["ledgerEntries"])}

    def test_exact_and_unmatched_golden_contract(self):
        self.assertEqual(self.invoke(), fixture("expected/read-only-result.json"))
        result = self.invoke()
        self.assertEqual(result["result"]["exactMatches"][0]["reference"], "PAY-100")
        self.assertEqual([item["reason"] for item in result["result"]["humanReviewQueue"]], ["amount-mismatch", "unmatched", "unmatched"])

    def test_multiple_candidates_abstain_to_human_queue(self):
        snapshot = copy.deepcopy(self.snapshot)
        duplicate_key = dict(snapshot["bankTransactions"][0], transactionId="TX-101")
        snapshot["bankTransactions"].append(duplicate_key)
        self.totals(snapshot)
        result = self.invoke(snapshot=snapshot)
        queue = result["result"]["humanReviewQueue"]
        self.assertEqual(queue[0]["reason"], "ambiguous-multiple-candidates-abstained")
        self.assertEqual(result["result"]["exactMatches"], [])

    def test_stale_access_denied_and_access_mismatch_fail_closed(self):
        cases = []
        cases.append({"as_of": "2026-08-28T10:01:00Z"})
        denied = copy.deepcopy(self.access); denied["permissions"]["reconciliation"] = "denied"; cases.append({"access": denied})
        cases.append({"actor": "not-the-bound-subject"})
        future_access = copy.deepcopy(self.access); future_access["evaluatedAt"] = "2026-08-28T09:16:00Z"; cases.append({"access": future_access})
        expired_access = copy.deepcopy(self.access); expired_access["validUntil"] = "2026-08-28T09:14:00Z"; cases.append({"access": expired_access})
        revoked_access = copy.deepcopy(self.access); revoked_access["status"] = "revoked"; cases.append({"access": revoked_access})
        malformed_access = copy.deepcopy(self.access); malformed_access["freshnessPolicy"] = "invalid"; malformed_access["subject"] = []; malformed_access["permissions"] = None; cases.append({"access": malformed_access})
        for kwargs in cases:
            with self.subTest(kwargs=kwargs):
                result = self.invoke(**kwargs)
                self.assertEqual(result["result"], {"exactMatches": [], "humanReviewQueue": []})
                self.assertTrue(result["contractFailures"])

    def test_invalid_duplicate_ids_totals_and_contract_drift_fail_closed(self):
        invalid = copy.deepcopy(self.snapshot); invalid["bankTransactions"][0]["amountMinor"] = 12.5
        invalid_date = copy.deepcopy(self.snapshot); invalid_date["bankTransactions"][0]["bookingDate"] = "2026-07-not-a-date"
        invalid_id = copy.deepcopy(self.snapshot); invalid_id["bankTransactions"][0]["transactionId"] = []
        invalid_currency = copy.deepcopy(self.snapshot); invalid_currency["currency"] = "123"
        for record in invalid_currency["bankTransactions"] + invalid_currency["ledgerEntries"]: record["currency"] = "123"
        duplicate = copy.deepcopy(self.snapshot); duplicate["ledgerEntries"].append(dict(duplicate["ledgerEntries"][0])); self.totals(duplicate)
        totals = copy.deepcopy(self.snapshot); totals["controlTotals"]["bankAmountMinor"] += 1
        semantic_drift = copy.deepcopy(self.semantics); semantic_drift["version"] = "9.9.9"
        malformed_semantics = copy.deepcopy(self.semantics); malformed_semantics["definitions"][0]["id"] = []
        decision_drift = copy.deepcopy(self.decision); decision_drift["rule"] = "silently accept fuzzy matches"
        for kwargs in ({"snapshot": invalid}, {"snapshot": invalid_date}, {"snapshot": invalid_id}, {"snapshot": invalid_currency}, {"snapshot": duplicate}, {"snapshot": totals}, {"semantics": semantic_drift}, {"semantics": malformed_semantics}, {"decision": decision_drift}):
            with self.subTest(kwargs=kwargs):
                result = self.invoke(**kwargs)
                self.assertEqual(result["result"], {"exactMatches": [], "humanReviewQueue": []})
                self.assertTrue(result["contractFailures"])

    def test_deterministic_and_no_write(self):
        tracked = [EXAMPLE / "evidence/reconciliation-snapshot.json", EXAMPLE / "expected/read-only-result.json"]
        before = [hashlib.sha256(path.read_bytes()).digest() for path in tracked]
        first, second = self.invoke(), self.invoke()
        self.assertEqual(first, second)
        self.assertFalse(first["writeBack"])
        self.assertEqual(before, [hashlib.sha256(path.read_bytes()).digest() for path in tracked])


if __name__ == "__main__":
    unittest.main()
