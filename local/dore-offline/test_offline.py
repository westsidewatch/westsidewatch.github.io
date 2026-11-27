import functools
import http.server
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.request
import offline
import vendor_dependencies as vendor

class OfflineTest(unittest.TestCase):
    def test_vendor_localizes_css_and_nested_fonts(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            font = "https://fonts.gstatic.com/test/example.woff2"
            (root / "index.html").write_text('<script src="' + vendor.GSAP + '"></script><link href="' + vendor.GOOGLE.replace('&','&amp;') + '">')
            payloads = {vendor.GSAP: b"/* gsap */", vendor.GOOGLE: ('@font-face{src:url(' + font + ')}').encode(), font:b"font"}
            result = vendor.localize(root, get=payloads.__getitem__)
            self.assertEqual(set(result), set(payloads))
            self.assertNotIn("https://", (root/"index.html").read_text())
            css = (root / result[vendor.GOOGLE]["path"].lstrip("/")).read_text()
            self.assertIn(result[font]["path"], css)
            self.assertFalse(vendor.allowed("https://example.com/a.woff2"))

    def test_church_quality_is_limited_to_known_knobs(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            path = root / 'p2/church-tour.js'
            path.parent.mkdir()
            source = 'renderer.setPixelRatio(Math.min(devicePixelRatio || 1, 1.5));\nsun.shadow.mapSize.set(2048, 2048);\nconst camera = unchanged;'
            path.write_text(source)
            self.assertEqual(offline.configure_church_quality(root)['status'], 'configured')
            changed = path.read_text()
            self.assertIn('doreClassic ? 1 : 1.5', changed)
            self.assertIn('doreClassic ? 1024 : 2048', changed)
            self.assertIn('const camera = unchanged;', changed)
            self.assertEqual(offline.configure_church_quality(root)['status'], 'renderer_contract_changed')
            self.assertEqual(path.read_text(), changed)

    def test_snapshot_and_local_server(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            commit = "a" * 40
            snap = root / "versions" / commit
            site = snap / "site"
            for name in offline.ROUTES:
                p = site / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("one-app.js" if name == "one/index.html" else "ok")
            (site / offline.ROUTES[-1]).write_text(json.dumps({"records": [0] * 12}))
            (site / "index.html").write_text('<a href="https://westsidewatch.github.io/one/">one</a><img src="https://example.org/test.jpg">')
            (site / "clip.webm").write_bytes(b"0123456789")
            audit = offline.localize_and_audit(site)
            self.assertIn("example.org", audit["external_url_mentions"])
            self.assertIn(offline.ORIGIN, (site / "index.html").read_text())
            offline.atomic_json(snap / "manifest.json", {"commit": commit, "files": offline.manifest(site)})
            offline.activate(root, commit)
            self.assertEqual(offline.active(root), snap)
            portable = root / "Portable"
            with patch.object(offline, 'build_portable_runtime') as build:
                offline.export_portable(root, portable)
                build.assert_called_once()
            self.assertEqual(offline.verify(offline.active(portable / "portable-data"))["commit"], commit)
            self.assertTrue((portable / "Launch.command").stat().st_mode & 0o100)
            with self.assertRaises(ValueError):
                offline.export_portable(root, portable)
            handler = functools.partial(offline.Handler, directory=str(site))
            with http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
                thread = threading.Thread(target=server.serve_forever, daemon=True)
                thread.start()
                try:
                    url = "http://127.0.0.1:%d/clip.webm" % server.server_port
                    req = urllib.request.Request(url, headers={"Range": "bytes=2-5"})
                    with urllib.request.urlopen(req) as r:
                        self.assertEqual(r.status, 206)
                        self.assertEqual(r.read(), b"2345")
                        self.assertIn("connect-src 'self'", r.headers["Content-Security-Policy"])
                finally:
                    server.shutdown()
                    thread.join()
            (site / "clip.webm").write_bytes(b"modified")
            with self.assertRaises(ValueError):
                offline.verify(snap)

if __name__ == "__main__":
    unittest.main()
