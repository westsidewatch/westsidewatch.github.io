"""Separates popup-site ad evidence from manifest cues and video frames."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from media_ad_origin import classify, inspect_html, inspect_hls, inspect_har

class AdOriginTests(unittest.TestCase):
    def test_site_popup_independent_of_clean_manifest(self):
        page = '<script>document.addEventListener("mousedown", trigger); localStorage.getItem("shown_at"); window.open("/jump");</script>'
        playlist="#EXTM3U\n#EXTINF:10,\nhttps://cdn.example/part.ts\n#EXT-X-ENDLIST"
        result=classify(page=page,hls=playlist)
        self.assertEqual(result["site_layer"],"SUSPECTED")
        self.assertEqual(result["manifest_layer"],"NO_MARKERS_OBSERVED")
        self.assertEqual(result["baked_in_video"],"UNDETERMINED")
    def test_hls_ad_markers_not_proof_of_site_popup(self):
        r=classify(hls="#EXTM3U\n#EXT-X-DATERANGE:ID=\"ad-break\"\n")
        self.assertEqual(r["site_layer"],"NOT_OBSERVED")
        self.assertEqual(r["manifest_layer"],"AD_MARKERS_PRESENT")
    def test_ad_network_request_not_assumed_media_file(self):
        har={"log":{"entries":[
            {"request":{"url":"https://ads.example.com/casino/popup.js"},"response":{"status":200}},
            {"request":{"url":"https://cdn.example.com/stream/index.m3u8"},"response":{"status":200}}
        ]}}
        r=classify(har=har)
        self.assertEqual(r["site_layer"],"SUSPECTED_BY_NETWORK")
        self.assertEqual(len(r["har"]["media_requests"]),1)
        self.assertEqual(r["manifest_layer"],"NOT_OBSERVED")
    def test_no_evidence_is_unknown_not_clean(self):
        r=classify()
        self.assertEqual(r["site_layer"],"NOT_OBSERVED")
        self.assertEqual(r["manifest_layer"],"NOT_OBSERVED")
        self.assertEqual(r["baked_in_video"],"UNDETERMINED")
if __name__=="__main__":
    unittest.main()
