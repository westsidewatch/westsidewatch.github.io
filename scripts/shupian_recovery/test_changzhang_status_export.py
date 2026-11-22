"""Local contract tests for real scanner evidence exported to the cinema testbench."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from changzhang_status_export import public_report

class ChangzhangStatusTests(unittest.TestCase):
    def test_unverified_candidates_are_not_promoted_to_playable(self):
        report={"status":"DISCOVERY_COMPLETE_UNVERIFIED","unique_catalog_ids":30,
                "media_candidate_titles":10,"unique_hls_urls":28,
                "media_samples":[{"result":{"status":"segment-bytes-sampled"}},
                                 {"result":{"status":"segment-check-failed"}}],
                "categories":{"latest_us_uk_series":{"candidate_ids":7,"metadata_matches":5}}}
        out=public_report(report)
        self.assertEqual(out["today"]["hls_sample_pass"],1)
        self.assertEqual(out["stages"]["discovery"],"PARTIAL")
        self.assertEqual(out["stages"]["ad_quality"],"SAMPLED_NOT_CERTIFIED")
        self.assertEqual(out["stages"]["playback"],"NOT_TESTED")
        self.assertEqual(out["published_playable_sources"],0)
        self.assertNotIn("candidates",out)
    def test_network_failure_not_zero_source_claim(self):
        out=public_report({"status":"INFRASTRUCTURE_OR_API_FAILURE",
                           "errors":[{"stage":"root","error":"DNS resolution failed"}]})
        self.assertEqual(out["stages"]["discovery"],"BLOCKED")
        self.assertEqual(out["today"]["failure_count"],1)
        self.assertEqual(out["fully_verified_clean"],0)

if __name__=="__main__":
    unittest.main()
