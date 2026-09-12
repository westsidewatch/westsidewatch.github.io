import unittest

from scripts.build_dawn_canonical_substrate import assert_runtime_contract, build


class DawnCanonicalSubstrateTests(unittest.TestCase):
    def setUp(self):
        self.queue = {
            'schema': 'dawn.library.10k-work-queue.v2',
            'deduplicatedWorks': 2,
            'authorityBackedWorks': 1,
            'items': [
                {
                    'queueId': 'work::openlibrary::OL1W',
                    'workId': 'OL1W',
                    'title': 'Confessions',
                    'author': 'Augustine of Hippo',
                    'authors': ['Augustine of Hippo'],
                    'languages': ['eng'],
                    'authorityIds': {'openLibraryWork': 'OL1W'},
                    'preferredEdition': 'OL1M',
                    'pointers': ['https://openlibrary.org/works/OL1W'],
                },
                {
                    'queueId': 'work::provisional::pilgrims-progress::john-bunyan',
                    'title': "The Pilgrim's Progress",
                    'author': 'John Bunyan',
                    'authors': ['John Bunyan'],
                    'languages': ['eng'],
                    'authorityIds': {},
                    'pointers': ['https://www.gutenberg.org/ebooks/39452'],
                },
            ],
        }

    def test_one_work_id_drives_both_surfaces(self):
        storefront = {
            'title': '黎明書局',
            'shelves': [{
                'id': 'theology',
                'title': 'Theology',
                'items': [{
                    'id': 'confessions-dawn',
                    'title': 'Confessions',
                    'author': 'Augustine of Hippo',
                    'identity': {'workId': '/works/OL1W'},
                    'cover': {'url': 'https://covers.openlibrary.org/b/id/1-L.jpg'},
                }],
            }],
        }
        multiwrite = {
            'title': '聖經世界',
            'items': [{
                'id': 'confessions-multiwrite',
                'work': {'title': 'Confessions', 'author': 'Augustine of Hippo'},
                'relations': ['教父'],
            }],
        }
        index, dawn, multi = build(self.queue, storefront, multiwrite)
        self.assertIn('OL1W', index['works'])
        self.assertEqual(dawn['shelves'][0]['items'][0], {'workId': 'OL1W'})
        self.assertEqual(multi['items'][0]['workId'], 'OL1W')
        self.assertEqual(set(multi['items'][0]), {'workId', 'relations'})

    def test_external_discovery_pointers_do_not_enter_runtime_index(self):
        index, dawn, multi = build(self.queue, {'shelves': []}, {'items': []})
        serialized = str({'index': index, 'dawn': dawn, 'multi': multi}).lower()
        self.assertNotIn('openlibrary.org', serialized)
        self.assertNotIn('gutenberg.org', serialized)
        self.assertIsNone(index['works']['OL1W']['readingPointer'])
        self.assertTrue(index['works']['OL1W']['cover']['pointer'].startswith('dawn://cover/'))

    def test_wikisource_is_a_hard_runtime_gate(self):
        index, dawn, multi = build(self.queue, {'shelves': []}, {'items': []})
        index['works']['OL1W']['readingPointer'] = 'https://zh.wikisource.org/wiki/Test'
        with self.assertRaisesRegex(ValueError, 'forbidden runtime dependency'):
            assert_runtime_contract(index, [dawn, multi])

    def test_surface_only_item_is_promoted_once_into_dawn_identity(self):
        storefront = {
            'shelves': [{'id': 'new', 'items': [{
                'id': 'new-dawn-book',
                'title': 'A New Dawn Book',
                'author': 'Author',
                'source': {'url': 'https://example.org/book'},
            }]}],
        }
        multiwrite = {
            'items': [{
                'id': 'same-book-in-biblical-world',
                'work': {'title': 'A New Dawn Book', 'author': 'Author'},
            }],
        }
        index, dawn, multi = build(self.queue, storefront, multiwrite)
        dawn_work_id = dawn['shelves'][0]['items'][0]['workId']
        multi_work_id = multi['items'][0]['workId']
        self.assertEqual(dawn_work_id, multi_work_id)
        self.assertIn(dawn_work_id, index['works'])
        self.assertNotIn('example.org', str(index['works'][dawn_work_id]))


if __name__ == '__main__':
    unittest.main()
