"""Regression: distinguish inaccessible network from absence of sources."""
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine_health import diagnose

PROVIDERS=[{"id":"good","api":"https://good.example/api.php/provide/vod/"},
           {"id":"bad","api":"https://bad.example/api.php/provide/vod/"}]

def resolver(host, port):
    if host == "bad.example": raise OSError("Temporary failure in name resolution")
    return [(None, None, None, None, ("203.0.113.2", port))]

def provider_fetch(url):
    q=parse_qs(urlsplit(url).query)
    if q.get("ac") == ["list"]:
        return {"class":[{"type_id":16,"type_name":"欧美剧"}],
                "list":[{"vod_id":123,"vod_name":"A test work"}]}
    return {"list":[{"vod_id":123,"vod_name":"A test work",
                     "vod_play_from":"hls",
                     "vod_play_url":"E1$https://media.example/1.m3u8"}]}

class HealthTests(unittest.TestCase):
    def test_infrastructure_not_counted_as_empty_catalog(self):
        report=diagnose(PROVIDERS,resolve=resolver,fetch=provider_fetch)
        self.assertEqual(report["classes"]["INFRASTRUCTURE_DNS"],1)
        self.assertEqual(report["classes"]["WORKING_DISCOVERY"],1)
        self.assertEqual(report["working"],1)
    def test_missing_details_not_reported_as_dns_failure(self):
        def no_media(url):
            v=provider_fetch(url)
            if "ids=" in url: return {"list":[{"vod_id":123}]}
            return v
        report=diagnose(PROVIDERS[:1],resolve=resolver,fetch=no_media)
        self.assertEqual(report["classes"],{"DETAIL_OR_MEDIA_FAILURE":1})

if __name__=="__main__":
    unittest.main()
