#!/usr/bin/env python3
import unittest
from design2_commands import apply

def fixture():return{'pages':[{'id':'multiwrite-home','nodes':[{'id':'title','type':'text','text':'多寫','x':100,'y':120,'w':300,'h':50,'size':40},{'id':'body','type':'text','text':'Body','x':100,'y':240,'w':400,'h':80,'size':16},{'id':'third','type':'text','text':'Third','x':700,'y':400,'w':100,'h':40,'size':14}]}]}
class Commands(unittest.TestCase):
 def test_patch_geometry_and_text_style(self):
  w=apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'x':140,'y':150,'w':360,'size':32,'text_align':'center'}});n=w['pages'][0]['nodes'][0];self.assertEqual((n['x'],n['y'],n['w'],n['size'],n['text_align']),(140,150,360,32,'center'))
 def test_input_is_not_mutated(self):
  s=fixture();apply(s,{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'x':9}});self.assertEqual(s['pages'][0]['nodes'][0]['x'],100)
 def test_unknown_property_rejected(self):
  with self.assertRaisesRegex(ValueError,'unsupported_patch'):apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'onclick':'evil()'}})
 def test_bad_geometry_rejected(self):
  with self.assertRaises(ValueError):apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'w':0}})
 def test_patch_many_is_atomic(self):
  s=fixture()
  with self.assertRaises(ValueError):apply(s,{'op':'node.patch_many','page_id':'multiwrite-home','patches':[{'id':'title','patch':{'x':1}},{'id':'missing','patch':{'x':2}}]})
  self.assertEqual(s['pages'][0]['nodes'][0]['x'],100)
 def test_nudge_selection(self):
  w=apply(fixture(),{'op':'node.nudge','page_id':'multiwrite-home','ids':['title','body'],'dx':1,'dy':-10});self.assertEqual((w['pages'][0]['nodes'][0]['x'],w['pages'][0]['nodes'][0]['y']),(101,110))
 def test_text_command_is_data_not_markup_execution(self):
  payload='<script>alert(1)</script> 多寫';w=apply(fixture(),{'op':'node.text','page_id':'multiwrite-home','id':'title','text':payload});self.assertEqual(w['pages'][0]['nodes'][0]['text'],payload)
 def test_text_rejects_non_text_node(self):
  s=fixture();s['pages'][0]['nodes'][0]['type']='block'
  with self.assertRaisesRegex(ValueError,'not_text_node'):apply(s,{'op':'node.text','page_id':'multiwrite-home','id':'title','text':'x'})
 def test_align_center(self):
  w=apply(fixture(),{'op':'node.align','page_id':'multiwrite-home','ids':['title','body'],'edge':'center'});a,b=w['pages'][0]['nodes'][:2];self.assertEqual(a['x']+a['w']/2,b['x']+b['w']/2)
 def test_distribute_horizontal(self):
  w=apply(fixture(),{'op':'node.distribute','page_id':'multiwrite-home','ids':['title','body','third'],'axis':'horizontal'});a,b,c=w['pages'][0]['nodes'];self.assertAlmostEqual(b['x']-(a['x']+a['w']),c['x']-(b['x']+b['w']))
if __name__=='__main__':unittest.main()
