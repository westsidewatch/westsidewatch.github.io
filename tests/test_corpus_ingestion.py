import unittest
from dore_core.readers.corpus_ingestion import ingest_morphgnt, ingest_oshb, assert_lossless

class CorpusIngestionTests(unittest.TestCase):
    def test_greek_multiple_tokens_lossless(self):
        lines = [
            "010101 N- ----NSF- Βίβλος Βίβλος Βίβλος βίβλος",
            "010101 N- ----GSF- γενέσεως γενέσεως γενέσεως γένεσις",
        ]
        tokens, report = ingest_morphgnt(lines)
        self.assertEqual(len(tokens), 2)
        self.assertEqual(tokens[0].order, 1)
        self.assertEqual(tokens[1].order, 2)
        assert_lossless(report)

    def test_oshb_lossless_and_aramaic_warning_visible(self):
        xml = '''<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"><osisText><div><chapter><verse osisID="Dan.2.4"><w lemma="x" morph="x">אֱדַיִן</w><w lemma="y" morph="y">מַלְּלוּ</w></verse></chapter></div></osisText></osis>'''
        tokens, report = ingest_oshb(xml, "DAN")
        self.assertEqual(report.emitted_tokens, 2)
        self.assertEqual(report.warnings, 2)
        self.assertTrue(all(t.language == "und" for t in tokens))
        assert_lossless(report)

    def test_invalid_record_blocks_lossless_gate(self):
        _, report = ingest_morphgnt(["not-a-valid-record"])
        with self.assertRaises(AssertionError):
            assert_lossless(report)

if __name__ == "__main__":
    unittest.main()
