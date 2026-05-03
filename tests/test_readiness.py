import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from app.pure_http_server import Handler
from app.readiness import readiness_report


class ReadinessTests(unittest.TestCase):
    def test_readiness_report_blocks_public_launch_currently(self):
        report = readiness_report()

        self.assertFalse(report["public_launch_ready"])
        self.assertEqual(report["data_scope"], "Maharashtra-only CSE/IT/AI/DS")
        self.assertEqual(report["summary"]["total_program_rows"], 15)
        self.assertEqual(report["summary"]["default_visible_rows"], 1)
        self.assertEqual(report["summary"]["hidden_pending_verification_rows"], 14)
        self.assertGreater(len(report["launch_blockers"]), 0)

    def test_readiness_report_keeps_hidden_rows_internal(self):
        report = readiness_report()
        hidden_blockers = [
            row for row in report["program_blockers"]
            if "hidden_pending_verification" in row["blockers"]
        ]

        self.assertEqual(len(hidden_blockers), 14)
        for row in hidden_blockers:
            self.assertFalse(row["publish_default"])

    def test_pure_http_readiness_endpoint(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urlopen(f"http://127.0.0.1:{port}/api/readiness", timeout=5) as response:
                self.assertEqual(response.status, 200)
                payload = json.loads(response.read().decode("utf-8"))
            self.assertFalse(payload["public_launch_ready"])
            self.assertIn("launch_blockers", payload)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
