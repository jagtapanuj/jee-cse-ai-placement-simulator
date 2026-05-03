from pathlib import Path
import unittest


FRONTEND_DIR = Path("frontend")


class StaticFrontendTests(unittest.TestCase):
    def test_html_files_do_not_contain_known_corruption_markers(self):
        bad_patterns = [
            "<p Review",
            'class="ey class=',
            "</head>\n<body>\n  <main class=\"shell\">\n    <section class=\"hero\">\n      <p class=\"ey class=",
        ]

        html_files = sorted(FRONTEND_DIR.glob("*.html"))
        self.assertGreater(len(html_files), 0, "No frontend HTML files found.")

        for path in html_files:
            text = path.read_text(encoding="utf-8")
            for pattern in bad_patterns:
                self.assertNotIn(pattern, text, f"{path} contains corruption marker: {pattern}")

    def test_html_files_have_single_document_shell(self):
        html_files = sorted(FRONTEND_DIR.glob("*.html"))
        self.assertGreater(len(html_files), 0, "No frontend HTML files found.")

        for path in html_files:
            text = path.read_text(encoding="utf-8").lower()
            self.assertEqual(text.count("<!doctype html>"), 1, f"{path} should contain one doctype.")
            self.assertEqual(text.count("<html"), 1, f"{path} should contain one opening html tag.")
            self.assertEqual(text.count("</html>"), 1, f"{path} should contain one closing html tag.")
            self.assertEqual(text.count("<head>"), 1, f"{path} should contain one head tag.")
            self.assertEqual(text.count("</head>"), 1, f"{path} should contain one closing head tag.")
            self.assertEqual(text.count("<body>"), 1, f"{path} should contain one body tag.")
            self.assertEqual(text.count("</body>"), 1, f"{path} should contain one closing body tag.")

    def test_review_page_required_elements_exist(self):
        path = FRONTEND_DIR / "review.html"
        text = path.read_text(encoding="utf-8")

        required_snippets = [
            '<section id="programSummary"',
            '<section id="publicationReview"',
            'data-check="cutoff_verified"',
            'data-check="rank_type_verified"',
            'data-check="placement_denominator_verified"',
            'id="reviewNotes"',
            'id="lastCheckedDate"',
            'id="saveReviewBtn"',
            'id="exportReviewBtn"',
            'id="clearReviewBtn"',
            'id="sourceEvidence"',
            '<script src="review.js"></script>',
        ]

        for snippet in required_snippets:
            self.assertIn(snippet, text, f"review.html missing required snippet: {snippet}")

    def test_review_page_consumes_publication_review_api(self):
        html = (FRONTEND_DIR / "review.html").read_text(encoding="utf-8")
        js = (FRONTEND_DIR / "review.js").read_text(encoding="utf-8")

        self.assertIn("publication-review API", html)
        self.assertIn("/api/publication-review/", js)
        self.assertIn("renderPublicationReview", js)
        self.assertIn("can_publish_default", js)
        self.assertIn("all_required_checks_passed", js)
        self.assertIn("pending_or_failed_check_keys", js)
        self.assertIn("publication_checks", js)
        self.assertIn("A row remains internal unless every required v1.0 publication check passes", html)


if __name__ == "__main__":
    unittest.main()
