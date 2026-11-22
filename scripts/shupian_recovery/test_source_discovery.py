"""Broad discovery regression: no single-title restriction, no first-result truncation."""
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_discovery import search, variants, play_groups, similarity

PROVIDERS = [
    {"id": "one", "api": "https://provider-one.example/api.php/provide/vod/"},
    {"id": "two", "api": "https://provider-two.example/api.php/provide/vod/"}
]

def fake_fetch(url):
    args = parse_qs(urlsplit(url).query)
    p = int(args["pg"][0])
    wd = args.get("wd", [""])[0]
    title = "神探夏洛克" if wd else "公開目錄作品"
    # Each page returns a different work and source group with two episodes.
    return {"list": [{"vod_id": f"{p}-{wd}", "vod_name": title,
             "vod_play_from": "hls$$$mp4",
             "vod_play_url": (
                "第01集$https://media.example/ep1.m3u8#第02集$https://media.example/ep2.m3u8"
                "$$$完整版$https://media.example/movie.mp4"
             )}]}

class BroadDiscovery(unittest.TestCase):
    def test_titles_and_aliases(self):
        self.assertEqual(variants("Sherlock / 神探夏洛克 Season 1", ["神探夏洛克"]),
                         ["Sherlock / 神探夏洛克 Season 1","Sherlock / 神探夏洛克",
                          "Sherlock","神探夏洛克 Season 1","神探夏洛克"])
        self.assertEqual(similarity("神探夏洛克", ["Sherlock", "神探夏洛克"]), 1.0)

    def test_preserves_all_episodes_and_formats(self):
        x = fake_fetch("https://example.com/?pg=1")["list"][0]
        groups = play_groups(x)
        self.assertEqual(len(groups), 2)
        self.assertEqual(len(groups[0]["episodes"]), 2)
        self.assertEqual(groups[1]["episodes"][0]["format"], "mp4")

    def test_all_providers_all_pages_and_broad_discovery(self):
        report=search(PROVIDERS,["神探夏洛克"],pages=2,discover=True,fetch=fake_fetch)
        self.assertEqual(len(report["probes"]),8)
        self.assertEqual(len(report["candidates"]),8)
        self.assertEqual(report["errors"],[])
        self.assertIn("(broad)",[x["query"] for x in report["probes"]])

    def test_broad_only_needs_no_target_title(self):
        report=search(PROVIDERS,pages=3,discover=True,fetch=fake_fetch)
        self.assertEqual(len(report["probes"]),6)
        self.assertEqual(len(report["candidates"]),6)

    def test_provider_failure_does_not_abort_other_providers(self):
        def sometimes_fail(url):
            if "provider-one" in url: raise OSError("simulated outage")
            return fake_fetch(url)
        report=search(PROVIDERS,["片名"],pages=2,fetch=sometimes_fail)
        self.assertEqual(len(report["errors"]),2)
        self.assertEqual(len(report["candidates"]),2)

if __name__=="__main__":
    unittest.main()
