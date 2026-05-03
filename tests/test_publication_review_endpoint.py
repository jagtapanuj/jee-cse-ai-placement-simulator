import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from app.publication_review import publication_review
from app.pure_http_server import Handler


class PublicationReviewEndpointTests(unittest.TestCase):
    def test_publication_review_for_default_row_is_not_publishable_yet(self):
        payload = publication_review("PROG-V5-004")

        self.assertEqual(payload["program"]["program_key"], "PROG-V5-004")
        self.assertEqual(payload["summary"]["required_checks"], 8)
        self.assertFalse(payload["summary"]["all_required_checks_passed"])
        self.assertFalse(payload["summary"]["can_publish_default"])
        self.assertIn("manual_review_complete", payload["pending_or_failed_check_keys"])

    def test_publication_review_for_hidden_row_is_not_publishable(self):
        payload = publication_review("PROG-V5-001")

        self.assertEqual(payload["program"]["program_key"], "PROG-V5-001")
        self.assertFalse(payload["program"]["publish_default"])
        self.assertFalse(payload["summary"]["can_publish_default"])
        self.assertGreater(payload["summary"]["pending_or_failed_required_checks"], 0)

    def test_pure_http_publication_review_endpoint(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://127.0.0.1:{port}/api/publication-review/PROG-V5-004", timeout=5) as response:
                self.assertEqual(response.status, 200)
                payload = json.loads(response.read().decode("utf-8"))

            self.assertEqual(payload["program"]["program_key"], "PROG-V5-004")
            self.assertIn("checks", payload)
            self.assertEqual(len(payload["checks"]), 8)
            self.assertFalse(payload["summary"]["can_publish_default"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
