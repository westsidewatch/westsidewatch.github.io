#!/usr/bin/env python3
import unittest
from design2_commands import apply


def fixture():
    return {'pages':[{'id':'multiwrite-home','nodes':[
        {'id':'title','type':'text','text':'多寫','x':100,'y':120,'w':300,'size':40},
        {'id':'body','type':'text','text':'Body','x':100,'y':240,'w':400,'size':16},
    ]}]}


class Commands(unittest.TestCase):
    def test_patch_geometry_and_text_style(self):
        w=apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'x':140,'y':150,'w':360,'size':32,'text_align':'center'}})
        n=w['pages'][0]['nodes'][0]
        self.assertEqual((n['x'],n['y'],n['w'],n['size'],n['text_align']),(140,150,360,32,'center'))

    def test_input_is_not_mutated(self):
        src=fixture();apply(src,{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'x':9}})
        self.assertEqual(src['pages'][0]['nodes'][0]['x'],100)

    def test_unknown_property_rejected(self):
        with self.assertRaisesRegex(ValueError,'unsupported_patch'):
            apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'onclick':'evil()'}})

    def test_bad_geometry_rejected(self):
        with self.assertRaises(ValueError):
            apply(fixture(),{'op':'node.patch','page_id':'multiwrite-home','id':'title','patch':{'w':0}})

    def test_patch_many_is_atomic(self):
        src=fixture()
        with self.assertRaises(ValueError):
            apply(src,{'op':'node.patch_many','page_id':'multiwrite-home','patches':[{'id':'title','patch':{'x':1}},{'id':'missing','patch':{'x':2}}]})
        self.assertEqual(src['pages'][0]['nodes'][0]['x'],100)

    def test_nudge_selection(self):
        w=apply(fixture(),{'op':'node.nudge','page_id':'multiwrite-home','ids':['title','body'],'dx':1,'dy':-10})
        self.assertEqual((w['pages'][0]['nodes'][0]['x'],w['pages'][0]['nodes'][0]['y']),(101,110))
        self.assertEqual((w['pages'][0]['nodes'][1]['x'],w['pages'][0]['nodes'][1]['y']),(101,230))


if __name__=='__main__': unittest.main()
