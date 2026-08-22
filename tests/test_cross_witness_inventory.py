import json
import tempfile
import unittest
from pathlib import Path
from dore_core.language.base import LanguageUnit, TextWitness
from dore_core.language.inventory import write_inventory
from dore_core.language.adapters.lxx_textfabric import LXXTextFabricAdapter

class CrossWitnessInventoryTests(unittest.TestCase):
    def test_inventory_excludes_source_specific_refs_from_canonical_count(self):
        witness=TextWitness('w','grc','x','source','snap')
        units=[
            LanguageUnit('w','bible.ref.GEN.1.1',1,'a','a','grc',(),('p',)),
            LanguageUnit('w','lxx.ref.WISDOM.1.1',1,'b','b','grc',(),('p',)),
        ]
        with tempfile.TemporaryDirectory() as d:
            payload=write_inventory(Path(d)/'i.json',witness,units)
        self.assertEqual(payload['canonical_ref_count'],1)
        self.assertEqual(payload['book_ids'],['GEN'])
        self.assertEqual(payload['source_specific_ref_count'],1)

    def test_lxx_common_abbreviations_map_to_shared_canon(self):
        cases={'Gen':'GEN','Exod':'EXO','1Sam':'1SA','1Kgs':'1KI','Ps':'PSA','Isa':'ISA','Zech':'ZEC'}
        for source,canon in cases.items():
            self.assertEqual(LXXTextFabricAdapter._ref(source,1,1),f'bible.ref.{canon}.1.1')

    def test_lxx_non_protestant_book_stays_source_specific(self):
        self.assertTrue(LXXTextFabricAdapter._ref('Wisdom',1,1).startswith('lxx.ref.'))

if __name__=='__main__': unittest.main()
