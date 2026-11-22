"""Regression tests for the restored PARADISO verification core."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from legacy_engine_core import (
    VerificationError, validate_public_url, parse_hls,
    permit_import, merge_catalog, rank_providers
)

MEDIA = """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:10
#EXTINF:9.4,
seg-1.ts
#EXTINF:10,
seg-2.ts
#EXT-X-ENDLIST"""


class LegacyEngineTests(unittest.TestCase):
    def test_complete_hls_no_auto_approval(self):
        p = parse_hls(MEDIA, "https://media.example.com/movie/index.m3u8")
        self.assertEqual(len(p['segments']), 2)
        self.assertEqual(p['duration_sec'], 19.4)
        self.assertFalse(permit_import({'full_ad_review': 'PASS'}))

    def test_incomplete_hls_rejected(self):
        with self.assertRaises(VerificationError):
            parse_hls(MEDIA.replace('#EXT-X-ENDLIST', ''), "https://media.example.com/x.m3u8")

    def test_ad_cues_detected(self):
        p = parse_hls(MEDIA.replace('#EXTINF:10,', '#EXT-X-CUE-OUT:DURATION=30\n#EXTINF:10,'),
                      "https://media.example.com/x.m3u8")
        self.assertTrue(p['ad_markers'])

    def test_private_addresses_rejected(self):
        for url in ('http://media.example/x.m3u8', 'https://127.0.0.1/a.m3u8',
                    'https://localhost/a.m3u8', 'https://192.168.1.1/a.m3u8'):
            with self.subTest(url=url), self.assertRaises(VerificationError):
                validate_public_url(url)

    def test_authorization_required(self):
        flags = dict(id='two', whole_work_verified=True, every_episode_verified=True,
                     full_ad_review='PASS', in_site_playback='PASS',
                     all_segments_verified=True, approval='APPROVED')
        self.assertFalse(permit_import(flags))
        flags['copyright_or_usage_review'] = 'PASS'
        self.assertTrue(permit_import(flags))
        flags['known_baked_in_ads'] = True
        self.assertFalse(permit_import(flags))

    def test_merge_never_modifies_existing(self):
        existing = {'items': [{'id': 'one', 'category': '基督福音劇集'}]}
        flags = dict(id='two', whole_work_verified=True, every_episode_verified=True,
                     full_ad_review='PASS', in_site_playback='PASS',
                     all_segments_verified=True, approval='APPROVED',
                     copyright_or_usage_review='PASS')
        next_catalog, added = merge_catalog(existing, [flags, flags])
        self.assertEqual(added, ['two'])
        self.assertEqual(len(next_catalog['items']), 2)
        self.assertEqual(len(existing['items']), 1)

    def test_rank_uses_real_observations(self):
        x = rank_providers([{'provider': 'good', 'sampled': 10, 'probe_pass': 9},
                            {'provider': 'bad', 'sampled': 10, 'probe_pass': 0}])
        self.assertEqual(x[0]['provider'], 'good')
        self.assertGreater(x[0]['estimated_probe_success'], .75)


if __name__ == '__main__':
    unittest.main()
