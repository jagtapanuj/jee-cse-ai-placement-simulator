import unittest

from app.data_loader import load_program_publication_reviews, load_programs, load_publication_checks
from app.readiness import readiness_report


class ProgramPublicationReviewsTests(unittest.TestCase):
    def test_every_program_has_every_publication_check(self):
        programs = load_programs()
        checks = load_publication_checks()
        reviews = load_program_publication_reviews()

        expected_count = len(programs) * len(checks)
        self.assertEqual(len(reviews), expected_count)

        review_pairs = {(r["program_key"], r["check_key"]) for r in reviews}
        for program in programs:
            for check in checks:
                self.assertIn((program.program_key, check["check_key"]), review_pairs)

    def test_review_statuses_are_controlled_values(self):
        allowed = {"passed", "pending", "failed"}
        for review in load_program_publication_reviews():
            self.assertIn(review["status"], allowed)

    def test_readiness_report_uses_program_publication_reviews(self):
        report = readiness_report()

        self.assertEqual(report["summary"]["program_publication_review_rows"], 120)
        self.assertIn("program_publication_reviews", report)
        self.assertEqual(len(report["program_publication_reviews"]), 120)
        self.assertEqual(report["summary"]["default_visible_rows_with_all_publication_checks_passed"], 0)

        blocker_ids = {b["id"] for b in report["launch_blockers"]}
        self.assertIn("default_visible_rows_pending_publication_checks", blocker_ids)


if __name__ == "__main__":
    unittest.main()
