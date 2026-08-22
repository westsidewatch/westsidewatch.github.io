import unittest
from dore_core.readers.original_language import (
    parse_morphgnt_line,
    validate_token,
    iter_oshb_words,
    resolve_ot_language,
)

class OriginalLanguageReaderTests(unittest.TestCase):
    def test_matthew_1_1_greek_token(self):
        token = parse_morphgnt_line("010101 N- ----NSF- Βίβλος Βίβλος βίβλος βίβλος", 1)
        self.assertEqual(token.canonical_ref_id, "bible.ref.MAT.1.1")
        self.assertEqual(token.surface, "Βίβλος")
        self.assertEqual(token.normalized, "βίβλος")
        self.assertEqual(token.analyses[-1].value, "βίβλος")
        self.assertEqual(validate_token(token), [])

    def test_revelation_mapping_exists(self):
        token = parse_morphgnt_line("270101 N- ----NSF- Ἀποκάλυψις Ἀποκάλυψις ἀποκάλυψις ἀποκάλυψις", 1)
        self.assertEqual(token.canonical_ref_id, "bible.ref.REV.1.1")

    def test_missing_textual_provenance_fails(self):
        token = parse_morphgnt_line("010101 N- ----NSF- Βίβλος Βίβλος βίβλος βίβλος", 1)
        token.textual_source_id = ""
        self.assertIn("missing_textual_provenance", validate_token(token))

    def test_daniel_2_4_boundary_stays_unresolved(self):
        self.assertEqual(resolve_ot_language("DAN", 2, 4), ("und", "warn"))

    def test_daniel_2_5_is_aramaic(self):
        self.assertEqual(resolve_ot_language("DAN", 2, 5), ("arc", "pass"))

    def test_daniel_8_1_returns_to_hebrew(self):
        self.assertEqual(resolve_ot_language("DAN", 8, 1), ("he", "pass"))

    def test_ezra_aramaic_boundaries(self):
        self.assertEqual(resolve_ot_language("EZR", 4, 8), ("arc", "pass"))
        self.assertEqual(resolve_ot_language("EZR", 6, 18), ("arc", "pass"))
        self.assertEqual(resolve_ot_language("EZR", 6, 19), ("he", "pass"))
        self.assertEqual(resolve_ot_language("EZR", 7, 12), ("arc", "pass"))
        self.assertEqual(resolve_ot_language("EZR", 7, 27), ("he", "pass"))

    def test_daniel_reader_does_not_default_to_hebrew(self):
        xml = '''<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"><osisText><div><chapter><verse osisID="Dan.2.4"><w lemma="x" morph="x">אֱדַיִן</w></verse></chapter></div></osisText></osis>'''
        token = next(iter_oshb_words(xml, "DAN"))
        self.assertEqual(token.language, "und")
        self.assertEqual(token.validation_status, "warn")

if __name__ == "__main__":
    unittest.main()
