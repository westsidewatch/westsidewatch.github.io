"""Discovery regressions using controlled mock responses; no network required."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from discover_sources import clean_url, parse_groups, normalize_results, scan, source_probe, title_matches, probe_segment
from legacy_engine_core import VerificationError
from source_lifecycle import (url_fingerprint, path_fingerprint, episode_key,
                              source_evidence, failure_class, sanitized_error)
from urllib.error import HTTPError

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

    def test_targeted_rescan_prefers_previous_episode(self):
        providers=[{"id":"sample","api":"https://api.example.com/vod"}]
        def fake_fetch(_):
            return {"list":[{"vod_name":"新片","vod_play_url":
                "E1$https://media.example.com/one.m3u8#E2$https://media.example.com/two.m3u8"}]}
        collected=[]
        def fake_probe(candidate):
            collected.append(candidate["episode"])
            return {"format":"m3u8","manifest":"parsed","ad_cues":"none-detected",
                    "playback":"not-tested","clean":"not-certified"}
        report=scan(["新片"],providers,fetcher=fake_fetch,probe=fake_probe,
                    max_audits=1,focus={("sample","新片","E2")},workers=1)
        self.assertEqual(collected,["E2"])
        self.assertEqual(report["audited"],1)

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

    def test_segment_media_signatures_without_network(self):
        class Response:
            status = 206
            headers = {"Content-Type": "video/mp2t"}
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, limit):
                packet = bytearray(376)
                packet[0] = 0x47
                packet[188] = 0x47
                return bytes(packet)
        out = probe_segment("https://media.example.com/part.ts",
                            opener=lambda request, timeout: Response())
        self.assertTrue(out["ok"])
        self.assertEqual(out["signature"], "mpeg-ts")

    def test_health_tracks_recovery_and_regression(self):
        providers=[{"id":"source","api":"https://api.example.com/vod"}]
        def fetch(_):
            return {"list":[{"vod_name":"新片","vod_play_url":"E1$https://media.example.com/a.m3u8"}]}
        from source_lifecycle import url_fingerprint, path_fingerprint
        prior={"manifest":"failed","source_fingerprint":url_fingerprint("https://media.example.com/a.m3u8"),
               "source_path_fingerprint":path_fingerprint("https://media.example.com/a.m3u8"),
               "health_checks":3,"health_pass":1}
        def good(_):
            return {"manifest":"parsed","segment_sample":"pass","ad_cues":"none-detected",
                    "format":"m3u8","playback":"requires-in-site-browser-test","clean":"not-certified"}
        report=scan(["新片"],providers,fetcher=fetch,probe=good,workers=1,
                    previous_audits={episode_key("source","新片","E1"):prior})
        a=report["audits"][0]
        self.assertEqual(a["url_comparison"],"same_exact_url")
        self.assertEqual(a["status_transition"],"recovered")
        self.assertEqual((a["health_checks"],a["health_pass"]),(4,2))
        self.assertEqual(report["recovered_count"],1)
        self.assertEqual(report["regressed_count"],0)
        self.assertLess(a["sample_reliability"],1.0)

    def test_parsed_manifest_with_failed_segments_is_not_healthy(self):
        providers=[{"id":"source","api":"https://api.example.com/vod"}]
        def fetch(_):
            return {"list":[{"vod_name":"新片","vod_play_url":"E1$https://media.example.com/a.m3u8"}]}
        key=episode_key("source","新片","E1")
        prior={"manifest":"parsed","segment_sample":"pass",
               "health_checks":2,"health_pass":2}
        def broken_segments(_):
            return {"format":"m3u8","manifest":"parsed","segment_sample":"failed",
                    "ad_cues":"none-detected","playback":"not-tested","clean":"not-certified"}
        result=scan(["新片"],providers,fetcher=fetch,probe=broken_segments,
                    workers=1,max_audits=1,previous_audits={key:prior})
        audit=result["audits"][0]
        self.assertEqual(audit["manifest"],"parsed")
        self.assertEqual(result["manifests_parsed"],1)
        self.assertEqual(result["segment_sample_pass"],0)
        self.assertEqual(audit["status_transition"],"regressed")
        self.assertEqual((audit["health_checks"],audit["health_pass"]),(3,2))
        self.assertEqual(result["stable_healthy_count"],0)

    def test_manifest_success_clears_contradictory_http_failure(self):
        providers=[{"id":"sample","api":"https://sample.example.com/vod"}]
        def fetch(_):
            return {"list":[{"vod_name":"新片","vod_play_url":"E1$https://media.example.com/a.m3u8"}]}
        def probe(_):
            return {"format":"m3u8","manifest":"parsed",
                    "error":"HTTPError: HTTP Error 404: Not Found",
                    "failure_class":"http_404_missing_or_masked",
                    "ad_cues":"none-detected","playback":"not-tested","clean":"not-certified"}
        report=scan(["新片"],providers,fetcher=fetch,probe=probe,workers=1,max_audits=1)
        self.assertEqual(report["manifests_parsed"],1)
        self.assertEqual(report["http_404_count"],0)
        self.assertNotIn("error",report["audits"][0])
        self.assertNotIn("failure_class",report["audits"][0])

    def test_url_identity_changes_without_leaking_signed_url(self):
        a="https://media.example.com/film/master.m3u8?token=one"
        b="https://media.example.com/film/master.m3u8?token=two"
        self.assertNotEqual(url_fingerprint(a),url_fingerprint(b))
        self.assertEqual(path_fingerprint(a),path_fingerprint(b))
        result=source_evidence({"url":b},{"source_fingerprint":url_fingerprint(a),
                                          "source_path_fingerprint":path_fingerprint(a)})
        self.assertEqual(result["url_comparison"],"same_path_changed_url")
        self.assertNotIn("token",str(result))
        self.assertEqual(source_evidence({"url":b})["url_comparison"],"no_comparable_baseline")

    def test_http_failure_classification_and_error_redaction(self):
        def error(code): return HTTPError("https://host.example.com/a.m3u8?secret=abc",
                                         code,"failure",{},None)
        self.assertEqual(failure_class(error(404)),"http_404_missing_or_masked")
        self.assertEqual(failure_class(error(403)),"http_access_restricted")
        self.assertEqual(failure_class(error(503)),"http_temporary_server_error")
        self.assertNotIn("secret=abc",sanitized_error(str(error(403))))

    def test_failing_source_is_retained_and_alternate_audited(self):
        providers=[{"id":"a","api":"https://a.example.com/vod"},
                   {"id":"b","api":"https://b.example.com/vod"}]
        def fetch(url):
            provider="a" if "a.example" in url else "b"
            return {"list":[{"vod_name":"新片 第一季",
                              "vod_play_url":"第01集$https://media.example.com/"+provider+".m3u8"}]}
        calls=[]
        def probe(candidate):
            calls.append(candidate["provider"])
            if candidate["provider"]=="a":
                return {"format":"m3u8","manifest":"failed","failure_class":"http_404_missing_or_masked",
                        "ad_cues":"unknown","clean":"not-certified","playback":"not-tested"}
            return {"format":"m3u8","manifest":"parsed","ad_cues":"none-detected",
                    "clean":"not-certified","playback":"not-tested"}
        focus={("a","新片 第一季","第01集")}
        prev={episode_key("a","新片 第一季","第01集"):
              {"manifest":"failed","source_fingerprint":"deadbeef",
               "source_path_fingerprint":"deadbeef"}}
        result=scan(["新片"],providers,fetcher=fetch,probe=probe,max_audits=2,
                    workers=1,focus=focus,previous_audits=prev)
        self.assertEqual(calls,["a","b"])
        self.assertEqual(result["alternative_candidates_audited"],1)
        self.assertEqual(result["http_404_count"],1)
        self.assertEqual(result["manifests_parsed"],1)
        self.assertEqual(result["audits"][0]["url_comparison"],"different_url")
        self.assertTrue(all("url" not in x for x in result["audits"]))

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
