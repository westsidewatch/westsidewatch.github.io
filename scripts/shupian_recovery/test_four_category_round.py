"""Four obligatory buckets, dynamic years, broad scans, and failure isolation."""
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from four_category_round import BUCKETS, bucket_queries, round_scan

PROVIDERS = [
    {"id": "A", "api": "https://provider-a.example/provide/vod/"},
    {"id": "B", "api": "https://provider-b.example/provide/vod/"}
]

def dummy_fetch(url):
    query=parse_qs(urlsplit(url).query)
    page=int(query.get("pg",["1"])[0])
    keyword=query.get("wd", ["catalog"])[0]
    if "ids" in query:
        return {"list":[{"vod_id":query["ids"][0],"vod_name":"Studio sample",
                         "vod_play_from":"primary",
                         "vod_play_url":"全集$https://media.example/whole.m3u8"}]}
    return {"list":[{"vod_id":f"{keyword}-p{page}", "vod_name":keyword,
                     "vod_play_from":"primary"}]}

class FourCategories(unittest.TestCase):
    def test_all_four_categories_mandatory(self):
        self.assertEqual(list(BUCKETS),[
            "latest_us_uk_series","japanese_anime","classic_films","gospel_media"
        ])
    def test_dynamic_year_and_multilingual_fuzzy(self):
        us=bucket_queries("latest_us_uk_series",year=2026)
        self.assertIn("美剧 2026",us)
        self.assertIn("英剧 2025",us)
        self.assertIn("British TV",us)
        self.assertIn("日本动漫 2026",bucket_queries("japanese_anime",year=2026))
        self.assertIn("Christian film",bucket_queries("gospel_media",year=2026))
    def test_every_bucket_every_provider_and_every_page(self):
        report=round_scan(PROVIDERS,year=2026,pages=2,fetch=dummy_fetch)
        self.assertEqual(report["totals"]["categories"],4)
        for bucket in report["categories"].values():
            self.assertEqual(bucket["provider_count"],2)
            self.assertEqual(bucket["probe_count"],2*(len(bucket["queries"])+1)*2)
            self.assertGreater(bucket["candidate_count"],0)
            self.assertEqual(bucket["error_count"],0)
            self.assertTrue(any(x["detail_hydrated"] for x in bucket["probes"]))
    def test_independent_provider_failure(self):
        def one_bad(url):
            if "provider-a" in url:
                raise OSError("provider down")
            return dummy_fetch(url)
        report=round_scan(PROVIDERS,year=2026,pages=1,fetch=one_bad)
        self.assertEqual(report["totals"]["categories"],4)
        self.assertGreater(report["totals"]["errors"],0)
        self.assertTrue(all(c["candidate_count"]>0 for c in report["categories"].values()))

if __name__=="__main__":
    unittest.main()
