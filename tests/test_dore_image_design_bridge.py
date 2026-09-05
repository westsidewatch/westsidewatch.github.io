import unittest
from dore_core.capabilities.image_artifacts import ImageArtifactRecord
from dore_core.capabilities.image_design_bridge import design_payload,local_asset_url

class ImageDesignBridgeTests(unittest.TestCase):
 def test_generated_artifact_becomes_place_image_command(self):
  a=ImageArtifactRecord('image:abc','/tmp/out/prompt.png','0123456789abcdef0123',10,{'seed':1},{},{})
  p=design_payload(a,page_id='cover',placement={'x':72,'y':80,'w':720,'h':850},asset_url='http://127.0.0.1:8790/asset?name=prompt.png')
  self.assertEqual(p['op'],'place_image');self.assertEqual(p['page_id'],'cover')
  self.assertEqual(p['asset']['uri'],'http://127.0.0.1:8790/asset?name=prompt.png')
  self.assertEqual(p['shape']['type'],'image');self.assertEqual(p['shape']['asset_id'],'image:abc')
  self.assertTrue(p['shape']['id'].startswith('image-'))
 def test_local_asset_url_is_browser_readable_loopback(self):
  a=ImageArtifactRecord('image:x','/private/output/a b.png','h',1,{},{},{})
  self.assertEqual(local_asset_url(a),'http://127.0.0.1:8790/asset?name=a%20b.png')

if __name__=='__main__':unittest.main()
