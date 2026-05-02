import unittest
from app.data_loader import load_programs, load_sources


class DataQualityTests(unittest.TestCase):
    def test_all_programs_have_keys_and_sources(self):
        for program in load_programs():
            self.assertTrue(program.program_key)
            self.assertTrue(program.college)
            self.assertTrue(program.program)
            self.assertGreater(len(program.source_url_list()), 0, program.program_key)

    def test_publish_default_requires_pilot_verified_status(self):
        for program in load_programs():
            if program.publish_default:
                self.assertEqual(program.data_quality_status, "PILOT_SCORE_READY_VERIFIED")
                self.assertTrue(program.internal_job_score_v3 is not None)

    def test_source_register_urls_present(self):
        for source in load_sources():
            self.assertTrue(source.get("url"), source)
            self.assertTrue(source.get("source_type"), source)
            self.assertTrue(source.get("use_status"), source)


if __name__ == "__main__":
    unittest.main()
