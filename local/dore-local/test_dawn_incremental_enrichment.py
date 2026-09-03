import unittest
from dawn_library_enrichment import enrich
from dawn_incremental_enrichment import incremental_enrich
class IncrementalTest(unittest.TestCase):
 def test_delta_only_and_repeat_zero(self):
  first=enrich();existing=first['sources'][:32];ids={str(x.get('id') or x.get('url')) for x in existing};delta=incremental_enrich(ids,[first['knowledge_id']]);self.assertGreaterEqual(delta['source_count'],8);self.assertFalse(ids&{x['id'] for x in delta['sources']});self.assertGreaterEqual(delta['source_family_count'],6);self.assertTrue(delta['provenance_preserved']);self.assertTrue(delta['rights_preserved']);self.assertEqual(incremental_enrich(ids|{x['id'] for x in delta['sources']})['source_count'],0)
if __name__=='__main__':unittest.main()
