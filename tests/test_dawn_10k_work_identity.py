import unittest

from scripts.discover_dawn_10k_openlibrary_works import compact


class Dawn10KWorkIdentityTests(unittest.TestCase):
    def test_openlibrary_work_is_compacted_without_book_content(self):
        item = compact({
            'key': '/works/OL123W',
            'title': 'Confessions',
            'author_name': ['Augustine of Hippo'],
            'language': ['eng', 'chi'],
            'first_publish_year': 397,
            'edition_key': ['OL456M', 'OL789M'],
            'isbn': ['9780000000001'],
            'oclc': ['12345'],
            'lccn': ['abc123'],
            'cover_i': 42,
        }, 'eng', 'Theology')
        self.assertEqual(item['workId'], 'OL123W')
        self.assertEqual(item['preferredEdition'], 'OL456M')
        self.assertEqual(item['authorityIds']['openLibraryWork'], 'OL123W')
        self.assertEqual(item['workPointer'], 'https://openlibrary.org/works/OL123W')
        self.assertEqual(item['editionPointer'], 'https://openlibrary.org/books/OL456M')
        self.assertFalse(item['contentDownloaded'])
        self.assertEqual(item['admission'], 'none')

    def test_non_work_records_are_rejected(self):
        self.assertIsNone(compact({'key': '/books/OL1M', 'title': 'Edition'}, 'eng', 'Bible'))
        self.assertIsNone(compact({'key': '/works/OL1W', 'title': ''}, 'eng', 'Bible'))

    def test_wikisource_is_not_part_of_identity_contract(self):
        item = compact({'key': '/works/OL2W', 'title': 'Bible', 'author_name': []}, 'chi', 'Bible')
        serialized = str(item).lower()
        self.assertNotIn('wikisource', serialized)
        self.assertEqual(item['provider'], 'Open Library')


if __name__ == '__main__':
    unittest.main()
