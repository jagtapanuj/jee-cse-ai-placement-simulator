import unittest

from app.data_loader import load_programs
from app.simulator_core import admission_bucket, compare, simulate, source_drawer


class SimulatorCoreTests(unittest.TestCase):
    def test_default_gate_is_conservative(self):
        default = simulate(rank=300, rank_type="MHT_CET_MERIT", include_partial=False)
        internal = simulate(rank=300, rank_type="MHT_CET_MERIT", include_partial=True)
        self.assertGreaterEqual(internal["counts"]["total_loaded"], default["counts"]["visible_returned"])
        self.assertEqual(default["counts"]["default_publishable_total"], 1)
        self.assertEqual(default["counts"]["hidden_pending_verification"], 14)

    def test_default_results_have_sources(self):
        default = simulate(rank=300, rank_type="MHT_CET_MERIT", include_partial=False)
        self.assertGreater(len(default["results"]), 0)
        for row in default["results"]:
            self.assertGreater(row["source_count"], 0)
            self.assertTrue(row["publish_default"])

    def test_source_drawer_for_default_row(self):
        default = simulate(rank=300, rank_type="MHT_CET_MERIT", include_partial=False)
        key = default["results"][0]["program_key"]
        drawer = source_drawer(key)
        self.assertIn("program", drawer)
        self.assertGreater(len(drawer["program_source_urls"]), 0)

    def test_bucket_logic(self):
        self.assertEqual(admission_bucket(80, 100), "SAFE_HISTORICAL")
        self.assertEqual(admission_bucket(105, 100), "LIKELY_TARGET")
        self.assertEqual(admission_bucket(125, 100), "BORDERLINE")
        self.assertEqual(admission_bucket(150, 100), "REACH")
        self.assertEqual(admission_bucket(151, 100), "UNLIKELY")
        self.assertEqual(admission_bucket(None, 100), "NEEDS_VERIFIED_CUTOFF")

    def test_include_partial_exposes_internal_rows_with_warning(self):
        internal = simulate(rank=300, rank_type="MHT_CET_MERIT", include_partial=True)
        hidden_rows = [r for r in internal["results"] if not r["publish_default"]]
        self.assertGreater(len(hidden_rows), 0)
        self.assertTrue(any("Hidden by default" in " ".join(r["warnings"]) for r in hidden_rows))

    def test_compare_honors_gate(self):
        keys = [p.program_key for p in load_programs()[:5]]
        default = compare(keys, include_partial=False)
        internal = compare(keys, include_partial=True)
        self.assertLessEqual(len(default), len(internal))
        for row in default:
            self.assertTrue(row["publish_default"])


if __name__ == "__main__":
    unittest.main()
