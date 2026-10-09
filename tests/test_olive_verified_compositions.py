"""Verified-photo binding never treats a missing photo as real."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from render_olive_verified_compositions import verified_assets, render

class VerifiedCompositionsTest(unittest.TestCase):
    def test_empty_registry_is_safe(self):
        self.assertEqual(verified_assets({"records":[]}),{})
    def test_unverified_asset_fails(self):
        with self.assertRaises(ValueError):
            verified_assets({"records":[{"speaker":"kou-shao-en","verified":False}]})
    def test_unsafe_path_fails(self):
        with self.assertRaises(ValueError):
            verified_assets({"records":[{"speaker":"kou-shao-en","verified":True,"licenseVerified":True,"identityVerified":True,"source":"a","license":"b","identityEvidence":"c","url":"//bad"}]})
    def test_fallback_has_no_img(self):
        page=render([{"id":"speaker:kou-shao-en","name":"寇紹恩"}],{})
        self.assertIn("PORTRAIT NOT VERIFIED",page)
        self.assertNotIn("<img",page)
    def test_twelve_speaker_fallback(self):
        import json
        from render_olive_verified_compositions import SPEAKERS
        rows=json.loads(SPEAKERS.read_text(encoding="utf-8"))["records"]
        page=render(rows,{})
        self.assertEqual(page.count("<figure>"),12)
        self.assertEqual(page.count("PORTRAIT NOT VERIFIED"),12)

if __name__=="__main__":
    unittest.main()
