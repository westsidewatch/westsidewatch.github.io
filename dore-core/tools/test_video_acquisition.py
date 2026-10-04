#!/usr/bin/env python3
import importlib.util, pathlib, unittest
P=pathlib.Path(__file__).with_name("video_acquisition.py")
s=importlib.util.spec_from_file_location("video_acquisition",P); v=importlib.util.module_from_spec(s); s.loader.exec_module(v)

class Acceptance(unittest.TestCase):
    def test_direct_hls_routes_nm3u8(self):
        u="https://devstreaming-cdn.apple.com/videos/streaming/examples/bipbop_16x9/bipbop_16x9_variant.m3u8"
        self.assertTrue(v.is_manifest(u)); self.assertEqual(v.probe(u)["engine"],"N_m3u8DL-RE")
    def test_dash_routes_nm3u8(self):
        self.assertTrue(v.is_manifest("https://example.invalid/movie/manifest.mpd"))
    def test_ism_routes_nm3u8(self):
        self.assertTrue(v.is_manifest("https://example.invalid/movie.ism"))
    def test_html_manifest_discovery(self):
        html='{"src":"https:\\/\\/cdn.example.test\\/master.m3u8?token=abc"}'
        found=[m.group("url") for m in v.MANIFEST_RE.finditer(html.replace("\\/","/"))]
        self.assertEqual(found,["https://cdn.example.test/master.m3u8?token=abc"])
    def test_drm_markers_are_known(self):
        self.assertIn("widevine",v.DRM_MARKERS); self.assertIn("playready",v.DRM_MARKERS); self.assertIn("fairplay",v.DRM_MARKERS)

if __name__=="__main__": unittest.main()
