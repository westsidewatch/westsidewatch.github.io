import json
import shutil
import subprocess
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "static" / "dore" / "dore-multiwrite-bible-study.js"
MULTIWRITE_HOST = ROOT / "static" / "multiwrite" / "bible-study.js"
MULTIWRITE_BOOK = ROOT / "static" / "multiwrite" / "book.js"
ONE_HOST = ROOT / "static" / "one" / "one-bi3-embedded.js"


class MultiwriteBibleStudyUIContractTests(unittest.TestCase):
    def test_prepare_ui_stays_on_dore_product_contract(self):
        source = UI.read_text(encoding="utf-8")
        self.assertIn('capability: "context.fuzzy-search"', source)
        self.assertIn('mode: "prepare"', source)
        self.assertIn('host: config.host || "multiwrite"', source)
        self.assertIn('embedded: Boolean(config.embedded)', source)
        self.assertNotIn("QMD", source)
        self.assertNotIn("Concord", source)
        self.assertNotIn("SWORD", source)
        self.assertNotIn("OpenAI", source)

    def test_ui_exposes_only_bi1_study_actions(self):
        source = UI.read_text(encoding="utf-8")
        self.assertIn('new Set(["keep", "flow", "present"])', source)
        self.assertIn("canonical_reference", source)
        self.assertIn("evidence_status", source)
        self.assertIn("source_ref", source)

    def test_multiwrite_host_persists_study_document_without_provider_leakage(self):
        source = MULTIWRITE_HOST.read_text(encoding="utf-8")
        self.assertIn("studyDocuments", source)
        self.assertIn("dore.study-document.v1", source)
        self.assertIn("host: 'multiwrite'", source)
        self.assertIn("embedded: false", source)
        self.assertIn("context.fuzzy-search", source)
        self.assertIn("doc.flow", source)
        self.assertIn("doc.kept", source)
        for forbidden in ("QMD", "Concord", "SWORD", "OpenAI"):
            self.assertNotIn(forbidden, source)

    def test_multiwrite_book_and_study_host_share_schema_version(self):
        book = MULTIWRITE_BOOK.read_text(encoding="utf-8")
        study = MULTIWRITE_HOST.read_text(encoding="utf-8")
        self.assertIn("const DB_VERSION = 3", book)
        self.assertIn("const DB_VERSION = 3", study)
        self.assertIn("const STUDY_STORE = 'studyDocuments'", book)
        self.assertIn("createObjectStore(STUDY_STORE", book)

    def test_one_host_uses_same_prepare_controller_and_embedded_context(self):
        source = ONE_HOST.read_text(encoding="utf-8")
        self.assertIn("studyDocuments", source)
        self.assertIn("dore.study-document.v1", source)
        self.assertIn("host:'one'", source)
        self.assertIn("embedded:true", source)
        self.assertIn("context.fuzzy-search", source)
        self.assertIn("DoreMultiwriteBibleStudy", source)
        self.assertIn("doc.flow", source)
        self.assertIn("doc.kept", source)
        for forbidden in ("QMD", "Concord", "SWORD", "OpenAI"):
            self.assertNotIn(forbidden, source)

    @unittest.skipUnless(shutil.which("node"), "Node is required for JS behavior acceptance")
    def test_prepare_search_preserves_context_and_dispatches_typed_action(self):
        script = textwrap.dedent(
            f"""
            const ui = require({json.dumps(str(UI))});
            const seen = [];
            const actions = [];
            const controller = ui.createPrepareController({{
              host: 'one',
              embedded: true,
              search: async (query, context) => {{
                seen.push({{query, context}});
                return {{results: [{{
                  id: 'r1',
                  title: '馬太福音 6:34',
                  snippet: '所以，不要為明天憂慮。',
                  canonical_reference: 'Matt.6.34',
                  source_ref: 'scripture:Matt.6.34',
                  evidence_status: 'canonical',
                  actions: ['keep', 'flow', 'present', 'unknown']
                }}]}};
              }},
              onAction: payload => actions.push(payload)
            }});
            (async () => {{
              await controller.search('一天的憂慮一天當就夠了');
              if (!controller.dispatchAction('flow')) process.exit(2);
              const state = controller.getState();
              const output = {{seen, actions, state: {{
                host: state.host,
                mode: state.mode,
                embedded: state.embedded,
                resultActions: state.results[0].actions,
                canonicalReference: state.results[0].canonicalReference
              }}}};
              console.log(JSON.stringify(output));
            }})().catch(error => {{ console.error(error); process.exit(1); }});
            """
        )
        run = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
        payload = json.loads(run.stdout)
        self.assertEqual(payload["seen"][0]["context"]["capability"], "context.fuzzy-search")
        self.assertEqual(payload["seen"][0]["context"]["host"], "one")
        self.assertEqual(payload["seen"][0]["context"]["mode"], "prepare")
        self.assertTrue(payload["seen"][0]["context"]["embedded"])
        self.assertEqual(payload["seen"][0]["context"]["lane"], "explicit")
        self.assertEqual(payload["state"]["resultActions"], ["keep", "flow", "present"])
        self.assertEqual(payload["state"]["canonicalReference"], "Matt.6.34")
        self.assertEqual(payload["actions"][0]["action"], "flow")
        self.assertEqual(payload["actions"][0]["canonical_reference"], "Matt.6.34")
        self.assertEqual(payload["actions"][0]["evidence_status"], "canonical")


if __name__ == "__main__":
    unittest.main()
