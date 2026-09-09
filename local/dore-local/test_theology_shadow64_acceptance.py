#!/usr/bin/env python3
from __future__ import annotations
import ast
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
SCRIPT=ROOT/"theology-shadow64-acceptance.py"
ACTION=ROOT/"theology_training_action.py"

class Shadow64AcceptanceBoundsTest(unittest.TestCase):
    def test_script_is_fixed_and_shadow_only(self):
        text=SCRIPT.read_text(encoding="utf-8")
        self.assertIn('MODEL="mlx-community/gemma-4-e4b-it-4bit"',text)
        self.assertIn('"mode":"shadow_only"',text)
        self.assertIn('"production_default_changed":False',text)
        self.assertIn('"adapter_fused_into_base":False',text)
        self.assertIn('"canonical_ingest":False',text)
        self.assertIn('"paid_api_required":False',text)
        self.assertIn('env["HF_HUB_OFFLINE"]="1"',text)
        self.assertIn('env["TRANSFORMERS_OFFLINE"]="1"',text)
        self.assertIn('no caller arguments accepted',text)

    def test_fixed_eight_distinct_shadow_prompts(self):
        tree=ast.parse(SCRIPT.read_text(encoding="utf-8"))
        cases=None
        for node in tree.body:
            if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="CASES" for t in node.targets):
                cases=ast.literal_eval(node.value)
        self.assertIsNotNone(cases)
        self.assertEqual(len(cases),8)
        self.assertEqual(len({x["id"] for x in cases}),8)
        self.assertTrue(all(x["prompt"] and x["groups"] for x in cases))

    def test_action_surface_is_fixed(self):
        text=ACTION.read_text(encoding="utf-8")
        self.assertIn('"theology.shadow.acceptance64"',text)
        self.assertIn('"theology-shadow64-acceptance.py",3900',text)
        self.assertNotIn('shell=True',text)

if __name__=="__main__": unittest.main()
