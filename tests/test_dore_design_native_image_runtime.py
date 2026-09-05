import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DESIGN=ROOT/'dore-design'
sys.path.insert(0,str(DESIGN))
spec=importlib.util.spec_from_file_location('dore_design_workspace',DESIGN/'app_workspace.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

class NativeImageRuntimeTests(unittest.TestCase):
 def base(self):
  w=mod.default_workspace();w['assets']={};return w
 def test_place_image_is_normal_workspace_mutation(self):
  w=self.base();mod.save=lambda x,snapshot_before=True:x
  payload={'op':'place_image','page_id':'cover','asset':{'id':'image:abc','kind':'image','uri':'/api/image/asset?name=abc.png','sha256':'abc'},'shape':{'id':'image-cover','type':'image','asset_id':'image:abc','x':72.0,'y':80.0,'w':720.0,'h':850.0,'fit':'cover','role':'editorial-image','rotation':0.0}}
  out=mod.mutate(w,payload)
  self.assertIn('image:abc',out['assets'])
  node=next(n for n in mod.page(out,'cover')['nodes'] if n['id']=='image-cover')
  self.assertEqual(node['type'],'image');self.assertEqual(node['asset_id'],'image:abc')
  self.assertEqual(mod.validate(out),[])
 def test_svg_export_renders_native_image(self):
  w=self.base();w['assets']['image:abc']={'id':'image:abc','kind':'image','uri':'/asset/abc.png','sha256':'abc'}
  mod.page(w,'cover')['nodes'].append({'id':'image-cover','type':'image','asset_id':'image:abc','x':0,'y':0,'w':1200,'h':930,'fit':'cover','rotation':0})
  svg=mod.page_svg(w,'cover')
  self.assertIn('<image ',svg);self.assertIn('href="/asset/abc.png"',svg);self.assertIn('preserveAspectRatio="xMidYMid slice"',svg)
 def test_missing_asset_is_rejected(self):
  w=self.base();mod.page(w,'cover')['nodes'].append({'id':'bad-image','type':'image','asset_id':'missing','x':0,'y':0,'w':100,'h':100,'fit':'cover'})
  self.assertTrue(any(x.startswith('image_asset:') for x in mod.validate(w)))
 def test_browser_runtime_resolves_asset_to_img(self):
  self.assertIn("n.type==='image'",mod.HTML);self.assertIn("w.assets?.[n.asset_id]",mod.HTML);self.assertIn("im.style.objectFit=n.fit||'cover'",mod.HTML)

if __name__=='__main__':unittest.main()
