"""Portable contract tests; all offers are synthetic and no network is used.

Run from the repository root: python -m unittest discover -s tests -v
"""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "research-travel-deals" / "scripts" / "compare_trip_costs.py"
EXAMPLE = ROOT / "examples" / "family-quotes.json"
NOW_TEXT = "2026-11-14T12:00:00Z"

SPEC = importlib.util.spec_from_file_location("compare_trip_costs", SCRIPT)
comparator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(comparator)
NOW = comparator.timestamp(NOW_TEXT)


class CompareTripCostsTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def single_offer(self, index=1):
        """Use one complete offer, or an explicitly chosen example offer."""
        data = deepcopy(self.data)
        data["offers"] = [data["offers"][index]]
        return data, data["offers"][0]

    def excluded(self, data, expected_reason):
        result = comparator.compare(data, NOW)
        self.assertEqual([], result["verified_ranked"])
        self.assertEqual(1, len(result["other_offers"]))
        row = result["other_offers"][0]
        self.assertIsNone(row["cash_total"])
        self.assertIn(expected_reason, row["reasons"])
        return row

    def run_cli(self, text, now=NOW_TEXT):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "-", "--now", now],
            input=text,
            text=True,
            capture_output=True,
            check=False,
            timeout=10,
        )

    def test_complete_options_are_ranked_by_full_party_expenses(self):
        result = comparator.compare(self.data, NOW)
        ranked = result["verified_ranked"]
        self.assertEqual(
            ["synthetic-package", "synthetic-independent"],
            [row["id"] for row in ranked],
        )
        self.assertEqual(["1870.50", "1990.00"], [row["cash_total"] for row in ranked])
        self.assertEqual([1, 2], [row["rank"] for row in ranked])
        self.assertEqual(self.data["party"], ranked[0]["party"])

    def test_missing_transfers_cannot_be_treated_as_free(self):
        data, offer = self.single_offer()
        offer["components"].pop()
        row = self.excluded(data, "missing cost category: destination_transfers")
        self.assertEqual("1870.00", row["known_subtotal"])

    def test_tempting_incomplete_lead_remains_a_partial_subtotal(self):
        data, _ = self.single_offer(2)
        row = self.excluded(data, "components[3] amount is unknown")
        self.assertEqual("1350.00", row["known_subtotal"])
        self.assertIn("evidence has not reached a selected offer", row["reasons"])
        self.assertIn("components[3] is unknown", row["reasons"])

    def test_quote_for_a_different_party_is_excluded(self):
        data, offer = self.single_offer()
        offer["party"]["children_ages"] = [6]
        self.excluded(data, "party does not exactly match request")

    def test_estimated_cost_is_visible_but_not_verified(self):
        data, offer = self.single_offer()
        offer["components"][3]["status"] = "estimate"
        row = self.excluded(data, "components[3] is estimate")
        self.assertEqual("1990.00", row["known_subtotal"])

    def test_package_coverage_cannot_be_counted_twice(self):
        data, offer = self.single_offer(0)
        offer["components"].append({
            "label": "Duplicate invented hotel charge",
            "covers": ["lodging"],
            "amount": "100.00",
            "currency": "EUR",
            "status": "verified",
        })
        row = self.excluded(data, "overlapping cost category: lodging (2 components)")
        self.assertEqual("1970.50", row["known_subtotal"])

    def test_sandbox_offer_never_enters_verified_ranking(self):
        data, offer = self.single_offer()
        offer["live"] = False
        self.excluded(data, "sandbox, non-live, or live status unknown")

    def test_expired_offer_is_excluded_at_expiry_boundary(self):
        data, offer = self.single_offer()
        offer["valid_until"] = NOW_TEXT
        self.excluded(data, "offer expired")

    def test_observation_beyond_clock_tolerance_is_excluded(self):
        data, offer = self.single_offer()
        offer["observed_at"] = "2026-11-14T12:05:01Z"
        self.excluded(data, "observed_at is more than five minutes in the future")

    def test_foreign_currency_is_not_silently_converted_or_added(self):
        data, offer = self.single_offer()
        offer["components"][0]["currency"] = "USD"
        row = self.excluded(data, "components[0] currency must equal EUR; no implicit FX conversion")
        self.assertEqual("990.00", row["known_subtotal"])

    def test_decimal_totals_remain_exact_at_small_and_large_magnitudes(self):
        cases = [
            (["0.10", "0.20", "0", "0"], "0.30"),
            (["10000000000000000000000000000.01", "0.02", "0", "0"],
             "10000000000000000000000000000.03"),
        ]
        for values, expected in cases:
            with self.subTest(expected=expected):
                data, offer = self.single_offer()
                for component, value in zip(offer["components"], values):
                    component["amount"] = value
                result = comparator.compare(data, NOW)
                self.assertEqual([], result["other_offers"])
                self.assertEqual(expected, result["verified_ranked"][0]["cash_total"])

    def test_refundable_deposit_is_disclosed_separately_without_changing_rank(self):
        result = comparator.compare(self.data, NOW)
        first, second = result["verified_ranked"]
        self.assertEqual("synthetic-package", first["id"])
        self.assertEqual("1870.50", first["cash_total"])
        self.assertEqual("200.00", first["known_deposit_subtotal"])
        self.assertEqual("0", second["known_deposit_subtotal"])
        self.assertEqual(self.data["offers"][0]["refundables"], first["refundable_deposits"])

    def test_nonfinite_expenses_and_deposits_are_excluded(self):
        for field in ("components", "refundables"):
            for value in ("NaN", "Infinity", "-Infinity"):
                with self.subTest(field=field, value=value):
                    data, offer = self.single_offer(0)
                    offer[field][0]["amount"] = value
                    self.excluded(data, f"{field}[0] amount must be a nonnegative finite decimal string")

    def test_failed_hard_constraints_prevent_ranking_even_with_a_price(self):
        data, offer = self.single_offer()
        offer["constraints_ok"] = False
        row = self.excluded(data, "hard constraints failed")
        self.assertEqual("1990.00", row["known_subtotal"])

    def test_duplicate_offer_ids_are_all_excluded(self):
        data, offer = self.single_offer()
        data["offers"].append(deepcopy(offer))
        result = comparator.compare(data, NOW)
        self.assertEqual([], result["verified_ranked"])
        self.assertEqual(2, len(result["other_offers"]))
        for row in result["other_offers"]:
            self.assertIn("duplicate id", row["reasons"])
            self.assertIsNone(row["cash_total"])

    def test_cli_reads_stdin_and_emits_json_with_frozen_time(self):
        process = self.run_cli(json.dumps(self.data))
        self.assertEqual(0, process.returncode, process.stderr)
        self.assertEqual("", process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual("2026-11-14T12:00:00+00:00", result["as_of"])
        self.assertEqual("1870.50", result["verified_ranked"][0]["cash_total"])
        self.assertEqual("synthetic-cheap-lead", result["other_offers"][0]["id"])

    def test_cli_invalid_json_and_invalid_root_return_structured_errors(self):
        cases = [
            ("{", "Expecting property name"),
            ("[]", "input must be an object"),
            ('{"value": NaN}', "invalid JSON constant: NaN"),
            ('{"value": 1e999}', "JSON number is outside finite float range"),
        ]
        for text, expected in cases:
            with self.subTest(text=text):
                process = self.run_cli(text)
                self.assertEqual(2, process.returncode)
                self.assertEqual("", process.stdout)
                self.assertIn(expected, json.loads(process.stderr)["error"])

    def test_cli_requires_timezone_for_frozen_time(self):
        process = self.run_cli(json.dumps(self.data), now="2026-11-14T12:00:00")
        self.assertEqual(2, process.returncode)
        self.assertEqual("", process.stdout)
        self.assertEqual("must include timezone", json.loads(process.stderr)["error"])

    def test_unrepresentable_utc_offer_timestamps_are_excluded_without_a_traceback(self):
        extremes = ["0001-01-01T00:00:00+01:00", "9999-12-31T23:59:59-01:00"]
        for field in ("observed_at", "valid_until"):
            for value in extremes:
                with self.subTest(field=field, value=value):
                    data, offer = self.single_offer()
                    offer[field] = value
                    process = self.run_cli(json.dumps(data))
                    self.assertEqual(0, process.returncode, process.stderr)
                    self.assertEqual("", process.stderr)
                    result = json.loads(process.stdout)
                    self.assertEqual([], result["verified_ranked"])
                    self.assertEqual(1, len(result["other_offers"]))
                    row = result["other_offers"][0]
                    self.assertIsNone(row["cash_total"])
                    self.assertEqual("1990.00", row["known_subtotal"])
                    self.assertTrue(
                        any(reason.startswith(field + " ") for reason in row["reasons"]),
                        row["reasons"],
                    )

    def test_cli_accepts_maximum_valid_now_without_overflow(self):
        maximum = "9999-12-31T23:59:59.999999+00:00"
        data, offer = self.single_offer()
        offer["observed_at"] = maximum
        del offer["valid_until"]
        process = self.run_cli(json.dumps(data), now=maximum)
        self.assertEqual(0, process.returncode, process.stderr)
        self.assertEqual("", process.stderr)
        result = json.loads(process.stdout)
        self.assertEqual(maximum, result["as_of"])
        self.assertEqual([], result["other_offers"])
        self.assertEqual("1990.00", result["verified_ranked"][0]["cash_total"])


if __name__ == "__main__":
    unittest.main()
