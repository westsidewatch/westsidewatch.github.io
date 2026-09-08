from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'local'/'dore-local'/'production_actions.py'
spec=importlib.util.spec_from_file_location('dore_production_actions',PATH)
assert spec and spec.loader
production=importlib.util.module_from_spec(spec);spec.loader.exec_module(production)


class KnowledgeSubstrateControlPlaneTests(unittest.TestCase):
    def test_native_control_plane_exposes_knowledge_substrate_install(self):
        self.assertIn('knowledge.substrates.install', production.CAPABILITIES)

    def test_knowledge_install_is_bounded_to_dore_owned_installer(self):
        with tempfile.TemporaryDirectory() as td:
            repo=Path(td)/'repo'; script=repo/'local'/'dore-local'/'install-knowledge-substrates-macos.sh'
            script.parent.mkdir(parents=True); script.write_text('#!/bin/bash\n',encoding='utf-8')
            def fake_run(argv,cwd=None,timeout=120,env=None):
                if argv[:2]==['git','rev-parse']:
                    return {'argv':argv,'returncode':0,'stdout':'abc123\n','stderr':''}
                self.assertEqual(argv,['bash',str(script)])
                return {'argv':argv,'returncode':0,'stdout':'{"ok":true,"offline_core":true,"authority":false}\n','stderr':''}
            with mock.patch.object(production,'_repo',return_value=repo), mock.patch.object(production,'_sync',return_value=None), mock.patch.object(production,'_run',side_effect=fake_run):
                out=production.knowledge_substrates_install({})
            self.assertTrue(out['ok'])
            self.assertEqual(out['capability'],'knowledge.substrates.install')
            self.assertFalse(out['evidence']['authority'])


if __name__=='__main__':
    unittest.main()
