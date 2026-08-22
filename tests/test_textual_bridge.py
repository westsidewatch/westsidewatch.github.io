import unittest
from dore_core.graph.textual_bridge import build_verse_witness, bridge_edge
from dore_core.readers.original_language import TokenRecord, Analysis


def tok(ref, order, language, surface, normalized, lemma, morphology, source, snapshot):
    book, chapter, verse = ref.split(".")
    return TokenRecord(
        token_id=f"test.{ref}.{order}",
        canonical_ref_id=f"bible.ref.{book}.{int(chapter)}.{int(verse)}",
        source_native_ref=ref,
        witness_id="witness.test",
        language=language,
        order=order,
        surface=surface,
        normalized=normalized,
        analyses=[Analysis("lemma", lemma, source), Analysis("morphology", morphology, source)],
        textual_source_id=source,
        corpus_snapshot=snapshot,
        validation_status="pass",
    )

class TextualBridgeTests(unittest.TestCase):
    def test_builds_ordered_hebrew_witness(self):
        tokens = [
            tok("GEN.15.6", 2, "he", "בַּיהוָה", None, "יהוה", "x", "source.oshb", "oshb@test"),
            tok("GEN.15.6", 1, "he", "וְהֶאֱמִן", None, "אמן", "x", "source.oshb", "oshb@test"),
        ]
        witness = build_verse_witness(tokens, "GEN.15.6")
        self.assertEqual(witness.language, "he")
        self.assertEqual(witness.lemmas, ("אמן", "יהוה"))

    def test_bridges_genesis_to_romans(self):
        source = [tok("GEN.15.6", 1, "he", "וְהֶאֱמִן", None, "אמן", "x", "source.oshb", "oshb@test")]
        target = [tok("ROM.4.3", 1, "grc", "ἐπίστευσεν", "ἐπίστευσεν", "πιστεύω", "V-AAI-3S", "source.morphgnt", "morphgnt@test")]
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
