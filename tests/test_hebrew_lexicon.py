import unittest
from dore_core.lexicon.hebrew import parse_oshb_lexical_value, resolve_oshb_lexeme

class HebrewLexiconTests(unittest.TestCase):
    def test_preserves_prefix_and_raw_value(self):
        prefixes, lexical_id = parse_oshb_lexical_value("c/539")
        self.assertEqual(prefixes, ("c",))
        self.assertEqual(lexical_id, "539")
        item = resolve_oshb_lexeme("c/539", "snapshot-test")
        self.assertEqual(item.raw_value, "c/539")
        self.assertEqual(item.lexeme, "אמן")
        self.assertEqual(item.status, "resolved")

    def test_resolves_genesis_15_6_seed(self):
        expected = {"539":"אמן", "3068":"יהוה", "2803":"חשב", "6666":"צדקה"}
        for lexical_id, lexeme in expected.items():
            self.assertEqual(resolve_oshb_lexeme(lexical_id, "snapshot-test").lexeme, lexeme)

    def test_unknown_identifier_stays_unresolved(self):
        item = resolve_oshb_lexeme("999999", "snapshot-test")
        self.assertIsNone(item.lexeme)
        self.assertEqual(item.status, "unresolved")

if __name__ == "__main__":
    unittest.main()
