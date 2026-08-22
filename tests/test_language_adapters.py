import unittest
from dore_core.language.base import TextWitness, validate_units
from dore_core.language.adapters import OSHBAdapter, MorphGNTAdapter


class LanguageAdapterMigrationTests(unittest.TestCase):
    def test_oshb_adapter_preserves_core_evidence(self):
        xml = '''<osis xmlns="http://www.bibletechnologies.net/2003/OSIS/namespace"><osisText><div><chapter><verse osisID="Gen.15.6"><w lemma="c/539" morph="HC/Vhp3ms">וְהֶאֱמִן</w></verse></chapter></div></osisText></osis>'''
        witness = TextWitness("witness.oshb.wlc", "he", "WLC/OSHB", "source.oshb", "3d15126f")
        units = tuple(OSHBAdapter().ingest((xml, "GEN"), witness))
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0].canonical_ref_id, "bible.ref.GEN.15.6")
        self.assertIn(("lemma", "c/539"), units[0].analyses)
        self.assertTrue(units[0].provenance)

    def test_morphgnt_adapter_preserves_core_evidence(self):
        text = "010101 N- ----NSF- Βίβλος Βίβλος Βίβλος βίβλος"
        witness = TextWitness("witness.sblgnt", "grc", "SBLGNT/MorphGNT", "source.sblgnt", "aaed91e5")
        units = tuple(MorphGNTAdapter().ingest(text, witness))
        self.assertEqual(len(units), 1)
        self.assertEqual(units[0].canonical_ref_id, "bible.ref.MAT.1.1")
        self.assertIn(("lemma", "βίβλος"), units[0].analyses)
        self.assertFalse(validate_units(units, witness))

if __name__ == "__main__":
    unittest.main()
