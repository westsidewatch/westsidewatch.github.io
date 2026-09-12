import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from dore_core.capabilities.zotero_reconciliation import ZoteroTranslationAdapter


class _Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        if self.path not in ('/search', '/web') or not body.strip():
            self.send_response(400)
            self.end_headers()
            return
        payload = [{
            'itemType': 'book',
            'title': 'The Confessions',
            'creators': [{'firstName': 'Saint', 'lastName': 'Augustine'}],
            'date': '1997',
            'publisher': 'Vintage',
            'ISBN': '0385472579',
            'url': 'https://example.invalid/confessions',
            'libraryCatalog': 'Test Catalog',
        }]
        raw = json.dumps(payload).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, format, *args):
        pass


class DawnZoteroReconciliationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('127.0.0.1', 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join(timeout=2)

    def test_identifier_translation_maps_to_stable_identity(self):
        result = ZoteroTranslationAdapter(self.base).search_identifier('0385472579')
        self.assertEqual(len(result), 1)
        item = result[0]
        self.assertEqual(item.source, 'zotero-translation-server')
        self.assertEqual(item.item_type, 'book')
        self.assertEqual(item.title, 'The Confessions')
        self.assertEqual(item.creators, ('Saint Augustine',))
        self.assertEqual(item.authority_ids, {'isbn': '0385472579'})

    def test_web_translation_uses_same_normalized_identity_contract(self):
        result = ZoteroTranslationAdapter(self.base).translate_web('https://example.invalid/confessions')
        self.assertEqual(result[0].publisher, 'Vintage')
        self.assertEqual(result[0].library_catalog, 'Test Catalog')

    def test_empty_input_never_hits_provider(self):
        adapter = ZoteroTranslationAdapter(self.base)
        self.assertEqual(adapter.search_identifier(''), [])
        self.assertEqual(adapter.translate_web('   '), [])


if __name__ == '__main__':
    unittest.main()
