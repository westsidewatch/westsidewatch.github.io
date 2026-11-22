"""Tests for selecting only qualified, distinct HLS candidates for browser playback."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from changzhang_browser_probe import sample_candidates

class BrowserSelection(unittest.TestCase):
    def test_excludes_ad_suspects_failed_bytes_and_duplicate_titles(self):
        x={"media_samples":[
            {"title":"A","episode":"1","url":"https://cdn.example/a.m3u8",
             "result":{"status":"segment-bytes-sampled","ad_signals":{"suspected":False}}},
            {"title":"B","episode":"1","url":"https://cdn.example/b.m3u8",
             "result":{"status":"segment-bytes-sampled","ad_signals":{"suspected":True}}},
            {"title":"A","episode":"2","url":"https://cdn.example/a2.m3u8",
             "result":{"status":"segment-bytes-sampled"}},
            {"title":"C","episode":"1","url":"https://cdn.example/c.m3u8",
             "result":{"status":"segment-check-failed"}},
            {"title":"D","episode":"1","url":"https://cdn.example/d.m3u8",
             "result":{"status":"segment-bytes-sampled"}}
        ]}
        out=sample_candidates(x,limit=3)
        self.assertEqual([v["title"] for v in out],["A","D"])
    def test_invalid_network_urls_never_enter_browser(self):
        x={"media_samples":[{"title":"Local","url":"https://127.0.0.1/test.m3u8",
                             "result":{"status":"segment-bytes-sampled"}}]}
        self.assertEqual(sample_candidates(x),[])

if __name__=="__main__":
    unittest.main()
