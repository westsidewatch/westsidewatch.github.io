"""Offline regression for dedicated Changzhang specialist sweep."""
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

sys.path.insert(0,str(Path(__file__).resolve().parent))
from changzhang_sweep import scan, category_tree, endpoint

CLASSES = [
    {"type_id":4,"type_pid":0,"type_name":"电视剧"},
    {"type_id":401,"type_pid":4,"type_name":"欧美剧"},
    {"type_id":5,"type_pid":0,"type_name":"动漫"},
    {"type_id":501,"type_pid":5,"type_name":"日韩动漫"},
    {"type_id":1,"type_pid":0,"type_name":"电影"},
    {"type_id":101,"type_pid":1,"type_name":"剧情片"},
    {"type_id":601,"type_pid":0,"type_name":"基督教电影"},
]
RECORDS = {
 "401":{"vod_id":100,"vod_name":"The UK TV Series","type_name":"欧美剧","vod_year":"2026","vod_area":"英国"},
 "501":{"vod_id":200,"vod_name":"New Anime","type_name":"日韩动漫","vod_year":"2026","vod_area":"日本"},
 "1":{"vod_id":300,"vod_name":"Classic Film","type_name":"电影","vod_year":"1991","vod_area":"美国"},
 "101":{"vod_id":301,"vod_name":"Old Film","type_name":"剧情片","vod_year":"1970","vod_area":"英国"},
 "601":{"vod_id":400,"vod_name":"Jesus Movie","type_name":"基督教电影","vod_year":"2010","vod_area":"美国"},
}
BY_ID={str(x["vod_id"]):x for x in RECORDS.values()}

def mock_fetch(url):
    q=parse_qs(urlsplit(url).query)
    ac=q.get("ac",[""])[0]
    if "ids" in q:
        result=[]
        for ident in q["ids"][0].split(","):
            if ident in BY_ID:
                record=dict(BY_ID[ident])
                record["vod_play_from"]="changzhangm3u8"
                record["vod_play_url"]="第1集$https://media.example/"+ident+"/ep1.m3u8#第2集$https://media.example/"+ident+"/ep2.m3u8"
                result.append(record)
        return {"list":result}
    if "t" in q:
        item=RECORDS.get(q["t"][0])
        return {"class":CLASSES,"list":[item] if item else [],
                "pagecount":1,"total":1 if item else 0}
    if q.get("wd"):
        return {"list":[],"pagecount":1}
    return {"class":CLASSES,"list":[],"pagecount":1,"total":100}

class ChangzhangSweepTests(unittest.TestCase):
    def test_type_tree_includes_children(self):
        ids, direct=category_tree(CLASSES,"classic_films")
        self.assertIn("1",ids)
        self.assertIn("101",ids)
    def test_all_four_categories_same_sweep(self):
        result=scan(fetch=mock_fetch,max_pages=2,page_size=20,
                    detail_batch=2,probe_count=0,current_year=2026)
        self.assertEqual(len(result["categories"]),4)
        self.assertEqual(result["status"],"DISCOVERY_COMPLETE_UNVERIFIED")
        self.assertEqual(result["unique_catalog_ids"],5)
        self.assertEqual(result["details_received"],5)
        self.assertEqual(result["media_candidate_titles"],5)
        self.assertEqual(result["unique_hls_urls"],10)
        self.assertTrue(all(v["candidate_ids"]>0 for v in result["categories"].values()))
        self.assertEqual(result["categories"]["latest_us_uk_series"]["metadata_matches"],1)
        self.assertEqual(result["categories"]["japanese_anime"]["metadata_matches"],1)
        self.assertEqual(result["categories"]["classic_films"]["metadata_matches"],2)
        self.assertEqual(result["categories"]["gospel_media"]["metadata_matches"],1)
    def test_probe_is_one_episode_per_distinct_title(self):
        seen=[]
        def fake_probe(url):
            seen.append(url)
            return {"status":"segment-bytes-sampled","sampled_segments":[{"http":206}]}
        result=scan(fetch=mock_fetch,probe=fake_probe,probe_count=5,
                    max_pages=1,page_size=20,current_year=2026)
        self.assertEqual(len(result["media_samples"]),5)
        self.assertEqual(len({x["title"] for x in result["media_samples"]}),5)
        self.assertEqual(result["benchmark"]["current_segment_probe_pass"],5)
        self.assertFalse(result["benchmark"]["comparable"])
        self.assertEqual(result["certified_ad_free"],0)
    def test_dns_failure_does_not_claim_no_sources(self):
        def dead(url):raise OSError("getaddrinfo: NameResolutionError")
        r=scan(fetch=dead,max_pages=1,probe_count=0)
        self.assertEqual(r["status"],"INFRASTRUCTURE_OR_API_FAILURE")
        self.assertNotIn("media_candidate_titles",r)
        self.assertTrue(r["errors"])

if __name__=="__main__":
    unittest.main()
