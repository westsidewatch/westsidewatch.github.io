"""HLS source stage-two signals must stay distinct from network sampling success."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from shupian_source_audit import ad_manifest_signals

class ManifestAdSignalTests(unittest.TestCase):
    def test_cue_markers_are_flagged(self):
        values=ad_manifest_signals(["#EXTM3U","#EXT-X-CUE-OUT:DURATION=20",
                                    "#EXTINF:10,","segment1.ts","#EXT-X-ENDLIST"])
        self.assertTrue(values["suspected"])
        self.assertEqual(len(values["markers"]),1)
    def test_promo_segment_paths_are_flagged(self):
        signals=ad_manifest_signals(["#EXTM3U","#EXTINF:10,","ads/preroll.ts",
                                     "#EXT-X-ENDLIST"])
        self.assertTrue(signals["suspected"])
        self.assertEqual(len(signals["segment_path_suspects"]),1)
    def test_no_marker_is_not_certified_clean(self):
        signals=ad_manifest_signals(["#EXTM3U","#EXTINF:10,","s01.ts","#EXT-X-ENDLIST"])
        self.assertFalse(signals["suspected"])
        self.assertIn("does not prove",signals["warning"])

if __name__=="__main__":
    unittest.main()
