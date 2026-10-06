#!/usr/bin/env python3
import importlib.util, pathlib, sys, unittest
from unittest.mock import patch

P=pathlib.Path(__file__).with_name("video_acquisition.py")\nsys.path.insert(0,str(P.parent))
spec=importlib.util.spec_from_file_location("video_acquisition",P)
va=importlib.util.module_from_spec(spec); spec.loader.exec_module(va)

class RuntimeFallbackIntegration(unittest.TestCase):
    def test_probe_uses_runtime_after_yt_and_static_fail(self):
        runtime={"ok":True,"engine":"playwright-runtime","title":"fixture","webpage_url":"https://example.test/watch","manifests":[{"url":"https://cdn.example.test/master.m3u8","kind":"hls","content_type":"application/vnd.apple.mpegurl","headers":{"referer":"https://example.test/"}}]}
        with patch.object(va,"yt_probe",side_effect=RuntimeError("yt failed")), patch.object(va,"discover_manifests",return_value=[]), patch.object(va,"runtime_probe",return_value=runtime):
            got=va.probe("https://example.test/watch")
        self.assertEqual(got["engine"],"N_m3u8DL-RE")
        self.assertEqual(got["webpage_url"],"https://cdn.example.test/master.m3u8")
        self.assertEqual(got["manifest_candidates"],["https://cdn.example.test/master.m3u8"])
        self.assertEqual(got["runtime"]["engine"],"playwright-runtime")

    def test_probe_preserves_primary_error_when_runtime_finds_nothing(self):
        primary=RuntimeError("yt failed")
        with patch.object(va,"yt_probe",side_effect=primary), patch.object(va,"discover_manifests",return_value=[]), patch.object(va,"runtime_probe",return_value={"ok":False,"manifests":[]}):
            with self.assertRaisesRegex(RuntimeError,"yt failed"):
                va.probe("https://example.test/watch")

    def test_static_manifest_still_precedes_runtime(self):
        with patch.object(va,"yt_probe",side_effect=RuntimeError("yt failed")), patch.object(va,"discover_manifests",return_value=["https://cdn.example.test/static.m3u8"]), patch.object(va,"runtime_probe") as rp:
            got=va.probe("https://example.test/watch")
        rp.assert_not_called()
        self.assertEqual(got["manifest_candidates"],["https://cdn.example.test/static.m3u8"])

if __name__=="__main__": unittest.main()
