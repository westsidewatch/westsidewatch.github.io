import unittest
from dore_core.graph.textual_bridge import build_verse_witness, bridge_edge
from dore_core.readers.original_language import TokenRecord


def tok(ref, order, language, surface, normalized, lemma, morphology, provenance):
    return TokenRecord(reference=ref, order=order, language=language, surface=surface, normalized=normalized, lemma=lemma, morphology=morphology, provenance=provenance, validation_status="pass")

class TextualBridgeTests(unittest.TestCase):
    def test_builds_ordered_hebrew_witness(self):
        tokens = [
            tok("GEN.15.6", 2, "heb", "בַּיהוָה", "ביהוה", "יהוה", "x", "oshb@test"),
            tok("GEN.15.6", 1, "heb", "וְהֶאֱמִן", "והאמין", "אמן", "x", "oshb@test"),
        ]
        witness = build_verse_witness(tokens, "GEN.15.6")
        self.assertEqual(witness.language, "heb")
        self.assertEqual(witness.lemmas, ("אמן", "יהוה"))

    def test_bridges_genesis_to_romans(self):
        source = [tok("GEN.15.6", 1, "heb", "וְהֶאֱמִן", "והאמין", "אמן", "x", "oshb@test")]
        target = [tok("ROM.4.3", 1, "grc", "ἐπίστευσεν", "ἐπίστευσεν", "πιστεύω", "V-AAI-3S", "morphgnt@test")]
        edge = {"id":"intertext.gen15_6.rom4_3","source_ref":"GEN.15.6","target_ref":"ROM.4.3","relation":"explicit_quote","claim_class":"TEXT_EXPLICIT"}
        bridge = bridge_edge(edge, source, target)
        self.assertEqual(bridge.source.lemmas, ("אמן",))
        self.assertEqual(bridge.target.lemmas, ("πιστεύω",))
        self.assertEqual(bridge.relation, "explicit_quote")

    def test_missing_reference_fails_loudly(self):
        with self.assertRaises(ValueError):
            build_verse_witness([], "GAL.3.6")

if __name__ == "__main__":
    unittest.main()
