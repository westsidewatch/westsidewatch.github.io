import unittest

from scripts.build_dawn_10k_work_queue import contains_forbidden_wikisource as discovery_forbidden
from scripts.build_dawn_10k_work_queue import language_priority
from scripts.build_dawn_canonical_substrate import canonical_from_queue
from scripts.build_dawn_source_capability_map import build as build_capability_map


class DawnCollectionGrowthGateTests(unittest.TestCase):
    def test_discovery_rejects_provider_marker_without_wikisource_url(self):
        row = {
            'title': 'Legacy candidate',
            'provider': 'zh-wikisource',
            'sourceUrl': 'https://example.org/legacy-copy',
        }
        self.assertTrue(discovery_forbidden(row))

    def test_discovery_rejects_any_wikisource_hostname(self):
        self.assertTrue(discovery_forbidden({'sourceUrl': 'https://en.wikisource.org/wiki/Test'}))
        self.assertTrue(discovery_forbidden({'sourceUrl': 'https://zh.wikisource.org/wiki/Test'}))

    def test_chinese_promotion_precedes_english_without_granting_admission(self):
        chinese = {'queueId': 'work::zh', 'languages': ['zho'], 'admission': 'none'}
        english = {'queueId': 'work::en', 'languages': ['eng'], 'admission': 'none'}
        ordered = sorted([english, chinese], key=lambda item: (language_priority(item), item['queueId']))
        self.assertEqual([item['queueId'] for item in ordered], ['work::zh', 'work::en'])
        self.assertEqual([item['admission'] for item in ordered], ['none', 'none'])

    def test_final_canonical_admission_rejects_stale_provider_marker(self):
        stale = {
            'queueId': 'work::legacy::stale',
            'title': 'Legacy candidate',
            'author': 'Unknown',
            'provider': 'zh-wikisource',
            'pointers': ['https://example.org/legacy-copy'],
        }
        with self.assertRaisesRegex(ValueError, 'forbidden Wikisource source at final canonical admission'):
            canonical_from_queue(stale)

    def test_capability_projection_rejects_provider_marker_even_after_url_is_cleaned(self):
        storefront = {
            'shelves': [{
                'id': 'test',
                'items': [{
                    'id': 'legacy-source',
                    'source': {'provider': 'zh-wikisource', 'url': 'https://example.org/legacy-copy'},
                }],
            }],
        }
        identity_map = {
            'schema': 'dore.source-identity-admission.v1',
            'claims': {
                'legacy-source': {
                    'canonicalWorkId': 'dawn:legacy-source',
                    'sourcePointer': 'https://example.org/legacy-copy',
                    'sourceAuthority': 'zh-wikisource',
                    'status': 'admitted',
                },
            },
        }
        result = build_capability_map(storefront, identity_map)
        self.assertEqual(result['blockedCount'], 1)
        self.assertEqual(result['claims']['legacy-source']['status'], 'blocked')
        self.assertEqual(result['claims']['legacy-source']['reason'], 'source-policy-deny')


if __name__ == '__main__':
    unittest.main()
