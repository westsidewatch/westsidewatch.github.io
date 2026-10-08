import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import refresh_dawn_bulk_corpus as refresh


class DawnBulkRefreshTests(unittest.TestCase):
    def run_refresh(self, items, added=0, content_downloaded=False):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / 'data'
            data.mkdir()
            source = {
                'contentDownloaded': content_downloaded,
                'policy': {'wikisourceForbidden': True},
                'metrics': {'works': 13163, 'chineseMatchedWorksAdded': added},
            }
            queue = {
                'deduplicatedWorks': 12251, 'authorityBackedWorks': 12180,
                # A stale aggregate must not conceal missing Chinese holdings.
                'languageSignals': {'chi': 2945}, 'items': items,
            }
            for name, value in (
                ('dawn-10k-openlibrary-works.json', source),
                ('dawn-10k-work-queue.json', queue),
                ('dawn-resource-queue.json', {'resourceCount': 12323}),
            ):
                (data / name).write_text(json.dumps(value), encoding='utf-8')
            output = io.StringIO()
            with patch.object(refresh, 'ROOT', root), \
                    patch.object(refresh, 'discover'), patch.object(refresh, 'run'), \
                    contextlib.redirect_stdout(output):
                self.assertEqual(refresh.main(), 0)
            return json.loads(output.getvalue())

    def test_existing_chinese_holdings_pass_without_new_discoveries(self):
        report = self.run_refresh([
            {'languages': ['chi', 'eng'], 'matchedLanguage': 'chi'},
            {'languages': [], 'matchedLanguage': 'chi'},
            {'languages': ['eng']},
        ])
        self.assertEqual(report['chineseWorks'], 2)
        self.assertEqual(report['chineseMatchedWorksAdded'], 0)

    def test_new_discoveries_do_not_mask_empty_admitted_holdings(self):
        with self.assertRaisesRegex(SystemExit, 'Chinese corpus empty'):
            self.run_refresh([{'languages': ['eng']}], added=5)

    def test_empty_queue_fails_despite_stale_language_summary(self):
        with self.assertRaisesRegex(SystemExit, 'Chinese corpus empty'):
            self.run_refresh([])

    def test_media_download_policy_remains_a_hard_failure(self):
        with self.assertRaisesRegex(SystemExit, 'bulk corpus must remain metadata-only'):
            self.run_refresh([{'languages': ['chi']}], content_downloaded=True)


if __name__ == '__main__':
    unittest.main()
