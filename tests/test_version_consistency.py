from pathlib import Path
import unittest

from app.simulator_core import data_quality_summary, simulate
from app.version import APP_VERSION, DATA_VERSION, DATA_SCOPE, version_payload


class VersionConsistencyTests(unittest.TestCase):
    def test_version_payload_has_expected_beta_scope(self):
        payload = version_payload()
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["app_version"], APP_VERSION)
        self.assertEqual(payload["data_version"], DATA_VERSION)
        self.assertIn("Maharashtra", DATA_SCOPE)

    def test_core_payloads_use_central_data_version(self):
        self.assertEqual(data_quality_summary()["data_version"], DATA_VERSION)
        self.assertEqual(simulate(rank=300, rank_type="MHT_CET_MERIT")["data_version"], DATA_VERSION)

    def test_old_patch_version_strings_are_removed_from_source(self):
        forbidden = [
            "maharashtra" + "-v6-localapp-v8-patch",
            "Local" + " App v7",
        ]

        roots = [Path("app"), Path("docs"), Path("frontend"), Path("tests"), Path("README.md")]
        files = []
        for root in roots:
            if root.is_file():
                files.append(root)
            elif root.exists():
                files.extend(
                    p for p in root.rglob("*")
                    if p.is_file()
                    and "__pycache__" not in p.parts
                    and ".git" not in p.parts
                    and p.suffix.lower() in {".py", ".md", ".html", ".js", ".css"}
                )

        for path in files:
            text = path.read_text(encoding="utf-8")
            for value in forbidden:
                self.assertNotIn(value, text, f"{path} still contains old version string: {value}")


if __name__ == "__main__":
    unittest.main()
