#!/usr/bin/env python3
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parent
SERVER=(ROOT/"theology-live-canary-server.py").read_text(encoding="utf-8")
ACCEPT=(ROOT/"theology-live-canary-acceptance.py").read_text(encoding="utf-8")
WORKFLOW=(ROOT.parent.parent/".github"/"workflows"/"dore-theology-live-canary.yml").read_text(encoding="utf-8")

class TheologyLiveCanaryTest(unittest.TestCase):
    def test_server_reuses_real_handler_on_localhost(self):
        self.assertIn('import dore_local as dl',SERVER)
        self.assertIn('ThreadingHTTPServer(("127.0.0.1",PORT),dl.H)',SERVER)
        self.assertIn('dl.ollama=mlx_inference',SERVER)
        self.assertIn('PORT=int(os.environ.get("DORE_THEOLOGY_CANARY_PORT","8791"))',SERVER)
        self.assertNotIn('8788',SERVER)

    def test_model_and_adapter_are_fixed(self):
        self.assertIn('MODEL="mlx-community/gemma-4-e4b-it-4bit"',SERVER)
        self.assertIn('"n64-recovery"/"adapter"',SERVER)
        self.assertIn('ADAPTER_FILE=ADAPTER_DIR/"adapter.safetensors"',SERVER)
        self.assertIn('HF_HUB_OFFLINE',SERVER)
        self.assertIn('TRANSFORMERS_OFFLINE',SERVER)
        self.assertIn('"production_default_changed":False',SERVER)

    def test_acceptance_hits_real_chat_route(self):
        self.assertIn('BASE="http://127.0.0.1:8791"',ACCEPT)
        self.assertIn('BASE+"/chat"',ACCEPT)
        self.assertIn('"handler":"dore_local.H"',ACCEPT)
        self.assertIn('"production_default_changed":False',ACCEPT)
        self.assertIn('"adapter_fused_into_base":False',ACCEPT)
        self.assertIn('"canonical_ingest":False',ACCEPT)

    def test_live_scorer_is_bilingual_without_lowering_threshold(self):
        self.assertIn('"Scripture","Bible","聖經","經文","神的話"',ACCEPT)
        self.assertIn('"revelation","authority","啟示","權威"',ACCEPT)
        self.assertIn('hits/total>=0.80',ACCEPT)
        self.assertIn('"bilingual_scoring":True',ACCEPT)

    def test_unrelated_cases_use_isolated_conversations(self):
        self.assertIn('cid=f"theology-live-{RUN_ID}-{c[\'id\']}"',ACCEPT)
        self.assertIn('"conversation_id":cid',ACCEPT)
        self.assertIn('"isolated_conversations":True',ACCEPT)
        self.assertNotIn('CID="theology-live-"',ACCEPT)

    def test_workflow_is_owner_only_bounded_and_self_hosted(self):
        self.assertIn("github.event.issue.user.login == github.repository_owner",WORKFLOW)
        self.assertIn("github.event.issue.title == '[DORÉ THEOLOGY CANARY] run'",WORKFLOW)
        self.assertIn('runs-on: [self-hosted, macOS, dore]',WORKFLOW)
        self.assertIn('timeout-minutes: 25',WORKFLOW)
        self.assertIn('http://127.0.0.1:8791/health',WORKFLOW)

if __name__=="__main__": unittest.main()
