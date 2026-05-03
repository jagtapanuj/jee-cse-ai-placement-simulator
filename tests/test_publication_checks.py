import unittest

from app.data_loader import load_publication_checks
from app.readiness import readiness_report


class PublicationChecksTests(unittest.TestCase):
    def test_publication_checks_exist_for_v1_gate(self):
        checks = load_publication_checks()
        self.assertGreaterEqual(len(checks), 8)

        required = [c for c in checks if c["required_for_v1"].lower() == "yes"]
        self.assertEqual(len(required), len(checks))

        keys = {c["check_key"] for c in checks}
        expected = {
            "source_urls_present",
            "cutoff_verified",
            "placement_denominator_verified",
            "fee_verified",
            "salary_basis_verified",
            "confidence_threshold_met",
            "last_verified_present",
            "manual_review_complete",
        }
        self.assertTrue(expected.issubset(keys))

    def test_readiness_report_includes_publication_checks(self):
        report = readiness_report()
        self.assertIn("publication_checks", report)
        self.assertEqual(report["summary"]["publication_check_rows"], 8)
        self.assertEqual(report["summary"]["required_publication_checks"], 8)


if __name__ == "__main__":
    unittest.main()
