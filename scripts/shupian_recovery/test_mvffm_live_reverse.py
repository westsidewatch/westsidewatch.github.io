"""Reverse-engineering observability regressions, without network access."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from mvffm_live_reverse import safe_url_parts, validate_target, summarize_trace, INJECT

class TestMvffmLiveReverse(unittest.TestCase):
    def test_original_site_is_first_class(self):
        self.assertEqual(safe_url_parts("https://www.mvffm.net/drama/420952/?token=secret"),
                         {"host":"www.mvffm.net","path":"/drama/420952/"})
    def test_legacy_fingerprints_in_runtime_instrumentation(self):
        for signature in ('"mousedown"', 'shown_at', 'window.open', 'iframe-created',
                          'Storage.prototype.getItem', 'Storage.prototype.setItem'):
            self.assertIn(signature, INJECT)
    def test_popup_and_media_recorded_separately(self):
        report={"target_host":"www.mvffm.net",
                "browser_events":[{"kind":"window-open"},{"kind":"ad-timer-read"}],
                "navigations":[{"host":"casino.example","path":"/redirect"}],
                "requests":[{"host":"media.example","media_candidate":True},
                            {"host":"ads.example","media_candidate":False}]}
        summary=summarize_trace(report)
        self.assertEqual(summary["status"],"PAGE_AD_BEHAVIOR_OBSERVED")
        self.assertEqual(summary["cross_origin_navigations"],1)
        self.assertEqual(summary["media_request_count"],1)
    def test_no_events_not_certified_clean(self):
        report={"target_host":"www.mvffm.net"}
        s=summarize_trace(report)
        self.assertEqual(s["status"],"NO_POPUP_OBSERVED_IN_THIS_RUN")
        self.assertIn("does not certify",s["limitation"])
    def test_no_local_or_insecure_network_targets(self):
        for u in ("http://www.mvffm.net/", "https://127.0.0.1/",
                  "https://localhost/", "https://10.0.0.10/"):
            with self.subTest(url=u), self.assertRaises(ValueError):
                validate_target(u)
        self.assertEqual(validate_target("https://www.mvffm.net/drama/420952/"),
                         "https://www.mvffm.net/drama/420952/")

if __name__=="__main__":
    unittest.main()
