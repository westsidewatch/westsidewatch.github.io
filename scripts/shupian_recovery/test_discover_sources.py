"""Discovery regressions using controlled mock responses; no network required."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from discover_sources import clean_url, parse_groups, normalize_results, scan, source_probe, title_matches
from legacy_engine_core import VerificationError

class DiscoveryTests(unittest.TestCase):
    def test_multigroup_episode_recovery_and_dedup(self):
        item = {"vod_play_from":"lineA$$$lineB","vod_play_url":
                "第01集$https://media.example.com/1.m3u8#第02集$https://media.example.com/2.m3u8$$$"
                "完整版$https://media.example.com/full.mp4#bad$http://insecure.example/x.m3u8"}
        groups = parse_groups(item)
        self.assertEqual(len(groups),2)
        self.assertEqual(sum(len(g["episodes"]) for g in groups),3)
        self.assertEqual(groups[1]["episodes"][0]["format"],"mp4")

    def test_private_and_webpages_rejected(self):
        for url in ("https://localhost/test.m3u8", "https://192.168.0.1/m.m3u8",
                    "https://example.com/movies.html", "http://example.com/x.m3u8"):
            with self.subTest(url=url), self.assertRaises(VerificationError):
                clean_url(url)

    def test_maccms_provider_normalization(self):
        payload={"list":[{"vod_id":40,"vod_name":"影集 A","vod_play_url":"E1$https://cdn.example.com/a.m3u8"}]}
        result=normalize_results(payload,"影集 A","sample")
        self.assertEqual(result[0]["groups"][0]["episodes"][0]["episode"],"E1")

    def test_cycle_preserves_distinct_failures_and_no_false_certificate(self):
        providers=[{"id":"good","api":"https://api.example.com/vod"},{"id":"down","api":"https://down.example.com/vod"}]
        def fake_fetch(url):
            if "down" in url: raise TimeoutError("DNS failed")
            return {"list":[{"vod_name":"新片","vod_play_from":"a","vod_play_url":
                    "E1$https://media.example.com/a.m3u8#E2$https://media.example.com/b.m3u8"}]}
        def fake_probe(item):
            return {"format":"m3u8","manifest":"parsed","ad_cues":"none-detected",
                    "playback":"not-tested","clean":"not-certified"}
        report=scan(["新片"],providers,fetcher=fake_fetch,probe=fake_probe,max_audits=10,workers=1)
        self.assertEqual(report["works_found"],1)
        self.assertEqual(report["unique_media_candidates"],2)
        self.assertEqual(report["provider_queries_failed"],1)
        self.assertEqual(report["manifests_parsed"],2)
        self.assertEqual(report["completion"],"NOT_COMPLETED")
        self.assertFalse(any("url" in x for x in report["audits"]))

    def test_wrong_sherlock_titles_are_excluded(self):
        self.assertFalse(title_matches("夏洛克与女儿", "神探夏洛克"))
        self.assertFalse(title_matches("女神探夏洛克", "神探夏洛克"))
        self.assertTrue(title_matches("神探夏洛克 第一季", "神探夏洛克"))
        self.assertTrue(title_matches("黑镜 第一季", "黑鏡"))
        self.assertFalse(title_matches("黑鏡幕後花絮", "黑鏡"))

    def test_chinese_filename_percent_encoded(self):
        url = clean_url("https://media.example.com/第01集/index.m3u8")
        self.assertIn("%E7%AC%AC", url)
        self.assertTrue(url.endswith("index.m3u8"))

    def test_ad_marker_is_not_certified_clean(self):
        def fake_manifest(_):
            return {"master":False,"children":[],"segments":["https://example.com/seg.ts"],
                    "duration_sec":10,"ad_markers":["#EXT-X-CUE-OUT"],"encryption":[]}
        out=source_probe({"url":"https://example.com/movie.m3u8","format":"m3u8"},fake_manifest)
        self.assertEqual(out["ad_cues"],"suspected")
        self.assertEqual(out["clean"],"not-certified")

if __name__=="__main__":
    unittest.main()

# Trigger full-cycle CI on main after workflow registration.
