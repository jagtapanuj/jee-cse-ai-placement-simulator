import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen

from app.data_loader import load_programs
from app.pure_http_server import Handler


class PureHttpServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def get_json(self, path):
        with urlopen(f"http://127.0.0.1:{self.port}{path}", timeout=5) as response:
            self.assertEqual(response.status, 200)
            return json.loads(response.read().decode("utf-8"))

    def test_compare_endpoint_honors_default_publish_gate(self):
        keys = ",".join(p.program_key for p in load_programs()[:5])
        payload = self.get_json(f"/api/compare?program_keys={keys}")

        self.assertIn("programs", payload)
        self.assertGreater(len(payload["programs"]), 0)
        for row in payload["programs"]:
            self.assertTrue(row["publish_default"])

    def test_compare_endpoint_can_include_partial_for_internal_testing(self):
        keys = ",".join(p.program_key for p in load_programs()[:5])
        default_payload = self.get_json(f"/api/compare?program_keys={keys}")
        internal_payload = self.get_json(f"/api/compare?program_keys={keys}&include_partial=true")

        self.assertGreaterEqual(len(internal_payload["programs"]), len(default_payload["programs"]))


if __name__ == "__main__":
    unittest.main()
