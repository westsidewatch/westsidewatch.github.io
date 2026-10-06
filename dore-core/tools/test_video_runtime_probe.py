#!/usr/bin/env python3
import importlib.util, pathlib, unittest
P=pathlib.Path(__file__).with_name("video_runtime_probe.py")
spec=importlib.util.spec_from_file_location("vrp",P); vrp=importlib.util.module_from_spec(spec); spec.loader.exec_module(vrp)
class RuntimeProbeContract(unittest.TestCase):
    def test_url_detection(self):
        self.assertEqual(vrp.media_kind("https://cdn/x.m3u8"),"hls")
        self.assertEqual(vrp.media_kind("https://cdn/x.mpd"),"dash")
        self.assertEqual(vrp.media_kind("https://cdn/x.ism/Manifest"),"mss")
    def test_mime_detection_without_suffix(self):
        self.assertEqual(vrp.media_kind("https://cdn/api?id=1","application/vnd.apple.mpegurl"),"hls")
        self.assertEqual(vrp.media_kind("https://cdn/api?id=2","application/dash+xml"),"dash")
    def test_non_media(self):
        self.assertIsNone(vrp.media_kind("https://example.com/page","text/html"))
if __name__=="__main__": unittest.main()
