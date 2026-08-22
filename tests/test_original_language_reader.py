import unittest
from dore_core.readers.original_language import parse_morphgnt_line, validate_token, iter_oshb_words

class OriginalLanguageReaderTests(unittest.TestCase):
    def test_matthew_1_1_greek_token(self):
        token = parse_morphgnt_line("610101 N- ----NSF- Βίβλος Βίβλος βίβλος", 1)
        self.assertEqual(token.canonical_ref_id, "bible.ref.MAT.1.1")
        self.assertEqual(token.surface, "Βίβλος")
        self.assertEqual(token.analyses[-1].value, "βίβλος")
        self.assertEqual(validate_token(token), [])

    def test_missing_textual_provenance_fails(self):
        token = parse_morphgnt_line("610101 N- ----NSF- Βίβλος Βίβλος βίβλος", 1)
        token.textual_source_id = ""
        self.assertIn("missing_textual_provenance", validate_token(token))

    def test_daniel_does_not_default_to_hebrew(self):
        xml = '''<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"><osisText><div><chapter><verse osisID="Dan.2.4"><w lemma="x" morph="x">אֱדַיִן</w></verse></chapter></div></osisText></osis>'''
        token = next(iter_oshb_words(xml, "DAN"))
        self.assertEqual(token.language, "und")
        self.assertEqual(token.validation_status, "warn")

if __name__ == "__main__":
    unittest.main()
