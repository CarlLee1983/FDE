import copy
import importlib.util
import json
import unittest
from pathlib import Path


EXAMPLE_DIR = Path(__file__).resolve().parents[1]
MODULE_PATH = EXAMPLE_DIR / "scripts" / "recommend_replenishment.py"
SPEC = importlib.util.spec_from_file_location("recommend_replenishment", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def fixture(name: str):
    return json.loads((EXAMPLE_DIR / "fixtures" / name).read_text(encoding="utf-8"))


class ReplenishmentRecommendationTests(unittest.TestCase):
    def test_normal_candidate_is_rounded_to_moq_and_pack(self):
        result = MODULE.recommend(fixture("replenishment-snapshot.json"))
        candidate = result["result"]["items"][0]
        self.assertEqual(candidate["status"], "candidate")
        self.assertEqual(candidate["projectedStockAtArrival"], 0)
        self.assertEqual(candidate["shortfall"], 60)
        self.assertEqual(candidate["quantity"], 120)

    def test_no_candidate_when_arrival_stock_exceeds_safety_stock(self):
        result = MODULE.recommend(fixture("replenishment-snapshot.json"))
        self.assertEqual(result["result"]["items"][1]["status"], "no-candidate")

    def test_boundary_equal_to_safety_stock_is_not_a_candidate(self):
        result = MODULE.recommend(fixture("replenishment-snapshot.json"))
        boundary = result["result"]["items"][2]
        self.assertEqual(boundary["projectedStockAtArrival"], 50)
        self.assertEqual(boundary["status"], "no-candidate")

    def test_invalid_item_abstains_only_that_item(self):
        snapshot = fixture("replenishment-snapshot.json")
        invalid_item = copy.deepcopy(snapshot["items"][0])
        invalid_item["sku"] = "SKU-BAD"
        invalid_item["onHand"] = -1
        snapshot["items"].append(invalid_item)
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["status"], "candidates-with-abstentions")
        self.assertEqual(result["result"]["items"][-1], {"sku": "SKU-BAD", "status": "abstained", "reasonCodes": ["invalid-onHand"]})

    def test_stale_required_source_abstains_entire_snapshot(self):
        result = MODULE.recommend(fixture("stale-replenishment-snapshot.json"))
        self.assertEqual(result["result"]["status"], "abstained")
        self.assertIn("stale-source:inventory-snapshot", result["result"]["reasonCodes"])

    def test_access_not_allowed_abstains_entire_snapshot(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["accessDecision"]["decision"] = "missing"
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["status"], "abstained")
        self.assertEqual(result["result"]["reasonCodes"], ["access-not-allowed"])
        self.assertEqual(result["freshness"]["status"], "fresh")

    def test_invalid_review_period_abstains_entire_snapshot(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["policy"]["reviewPeriod"]["end"] = "2026-08-26"
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["status"], "abstained")
        self.assertEqual(result["result"]["reasonCodes"], ["invalid-review-period"])

    def test_output_is_read_only_and_replayable(self):
        snapshot = fixture("replenishment-snapshot.json")
        self.assertEqual(MODULE.recommend(copy.deepcopy(snapshot)), MODULE.recommend(copy.deepcopy(snapshot)))
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["semanticDefinitionVersion"], snapshot["semanticDefinitionVersion"])
        self.assertFalse(result["writeBack"]["permitted"])
        self.assertFalse(result["writeBack"]["attempted"])
        self.assertFalse(result["accessDecision"]["enterpriseAuthorization"])
        self.assertEqual(result["result"]["items"][0]["uncertainty"]["status"], "unassessed")

    def test_only_confirmed_inbound_before_arrival_offsets_shortfall(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["items"] = [copy.deepcopy(snapshot["items"][0])]
        snapshot["items"][0]["inboundBeforeArrival"] = 60
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["items"][0]["status"], "no-candidate")

    def test_fractional_non_finite_and_out_of_range_values_abstain(self):
        for field, value in (("packSize", 2.5), ("dailyDemand", float("nan")), ("onHand", MODULE.MAX_QUANTITY + 1)):
            with self.subTest(field=field):
                snapshot = fixture("replenishment-snapshot.json")
                snapshot["items"] = [copy.deepcopy(snapshot["items"][0])]
                snapshot["items"][0][field] = value
                item = MODULE.recommend(snapshot)["result"]["items"][0]
                self.assertEqual(item["status"], "abstained")
                self.assertEqual(item["reasonCodes"], [f"invalid-{field}"])

    def test_derived_quantity_out_of_range_abstains(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["items"] = [copy.deepcopy(snapshot["items"][0])]
        snapshot["items"][0].update({"onHand": 0, "dailyDemand": MODULE.MAX_QUANTITY, "leadTime": 2})
        item = MODULE.recommend(snapshot)["result"]["items"][0]
        self.assertEqual(item["status"], "abstained")
        self.assertEqual(item["reasonCodes"], ["calculation-out-of-range"])

    def test_unknown_policy_version_abstains(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["policy"]["policyVersion"] = "unknown-policy@99"
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["reasonCodes"], ["unsupported-policy-version"])

    def test_duplicate_source_is_conflicting_not_order_dependent(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["sourceEvidence"].append(copy.deepcopy(snapshot["sourceEvidence"][0]))
        result = MODULE.recommend(snapshot)
        self.assertIn("conflicting-source:inventory-snapshot", result["result"]["reasonCodes"])
        self.assertEqual(result["freshness"]["status"], "unacceptable")

    def test_malformed_source_time_is_unverifiable(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["sourceEvidence"][0]["observedAt"] = "not-a-time"
        result = MODULE.recommend(snapshot)
        self.assertIn("unverifiable-source:inventory-snapshot", result["result"]["reasonCodes"])
        self.assertEqual(result["freshness"]["status"], "unverifiable")

    def test_duplicate_sku_abstains_entire_snapshot(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["items"].append(copy.deepcopy(snapshot["items"][0]))
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["status"], "abstained")
        self.assertEqual(result["result"]["reasonCodes"], ["duplicate-sku:SKU-CANDIDATE"])

    def test_as_of_requires_utc_z_to_bound_review_date(self):
        snapshot = fixture("replenishment-snapshot.json")
        snapshot["asOf"] = "2026-08-27T00:00:00+08:00"
        result = MODULE.recommend(snapshot)
        self.assertEqual(result["result"]["status"], "abstained")
        self.assertEqual(result["result"]["reasonCodes"], ["invalid-asOf"])


if __name__ == "__main__":
    unittest.main()
