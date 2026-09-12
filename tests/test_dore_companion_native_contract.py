from __future__ import annotations
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; EXT=ROOT/'local'/'dore-companion-extension'; LOCAL=ROOT/'local'/'dore-local'
# Book Intelligence is an explicitly declared site capability, not an open-ended bridge.

class CompanionNativeContractTest(unittest.TestCase):
 def test_native_manifest_contract_matches_native_host(self):
  m=json.loads((EXT/'manifest.native-messaging.json').read_text());self.assertIn('nativeMessaging',m['permissions']);self.assertEqual(m['browser_specific_settings']['gecko']['id'],'dore-companion@westsidewatch.ca');self.assertEqual(m['dore_native_messaging']['host'],'ca.dore.companion')
 def test_companion_manifest(self):
  m=json.loads((EXT/'manifest.json').read_text());self.assertEqual(m['version'],'2.0.0');self.assertNotIn('applications',m);self.assertIn('nativeMessaging',m['permissions'])
  site=[x for x in m['content_scripts'] if 'site_bridge.js' in x.get('js',[])];self.assertEqual(len(site),1);self.assertEqual(site[0]['matches'],['https://westsidewatch.github.io/*'])
 def test_transport_native_first(self):
  s=(EXT/'native_transport.js').read_text();self.assertIn('browser.runtime.connectNative(DORE_NATIVE_HOST)',s);self.assertLess(s.index('sendViaNative(payload)'),s.index('sendVia4312(payload)'))
 def test_production_design_envelope(self):
  s=(EXT/'background.js').read_text()
  for token in ['protocol:"dore.a2a/1"','action:"dispatch"','request_id:nextRequestId()','conversation_id:','session_id:sessionId','consumer_id:"design"','capability_id:"design.compose"','asset_candidate:','version:"2.0.0"']:
   self.assertIn(token,s)
  self.assertIn('n==="/dore design"',s)
 def test_stage2_remains_diagnostic(self):
  s=(EXT/'background.js').read_text();a=s.index('n==="/dore stage2"');b=s.index('n==="/dore design"');self.assertNotIn('action:"dispatch"',s[a:b])
 def test_conversation_binding_and_result_surface(self):
  s=(EXT/'content_script.js').read_text();self.assertIn('function conversationId()',s);self.assertIn('conversation_id:conversationId()',s);self.assertIn('DORÉ_LOCAL_RESULT',s);self.assertIn('TERMINAL_HOLD_MS=30000',s);self.assertIn('new WeakSet()',s)
 def test_assistant_directive_allowlist_is_bounded(self):
  s=(EXT/'background.js').read_text();self.assertIn('ASSISTANT_DIRECTIVE_ALLOWLIST',s);self.assertIn('"knowledge.substrates.install"',s);self.assertIn('"system.self-maintain"',s);self.assertNotIn('capability.startsWith("knowledge.")',s);self.assertNotIn('capability.startsWith("system.")',s)
 def test_site_capability_bridge_is_bounded_to_declared_site_capabilities(self):
  bg=(EXT/'background.js').read_text();bridge=(EXT/'site_bridge.js').read_text()
  self.assertIn('SITE_CAPABILITY_ALLOWLIST=new Set(["context.fuzzy-search","publishing.book-intelligence"])',bg);self.assertIn('message.type==="dore.site-capability"',bg);self.assertIn('caller_product:',bg)
  self.assertIn("const FUZZY_CAPABILITY='context.fuzzy-search'",bridge);self.assertIn("const BOOK_CAPABILITY='publishing.book-intelligence'",bridge)
  self.assertIn("'dore:context-fuzzy-search'",bridge);self.assertIn("'dore:context-fuzzy-search-result'",bridge);self.assertIn("limit:5",bridge)
  self.assertIn("'dore:book-intelligence'",bridge);self.assertIn("'dore:book-intelligence-result'",bridge);self.assertIn("await send(BOOK_CAPABILITY,args,'multiwrite')",bridge)
  for forbidden in ('QMD','Concord','SWORD','OpenAI'):
   self.assertNotIn(forbidden,bridge)
 def test_installer_free_runtime(self):
  s=(EXT/'install_companion_1.command').read_text().lower();self.assertNotIn('api.openai.com',s)
 def test_native_snapshot_binds_real_worktree_for_git_actions(self):
  s=(LOCAL/'install_native_messaging.sh').read_text();self.assertIn('export DORE_REPO_ROOT=',s);self.assertIn('export DORE_WORKTREE=',s);self.assertIn('/westsidewatch.github.io',s);self.assertIn('.git',s)
 def test_self_maintenance_is_bounded_and_reversible(self):
  host=(LOCAL/'native_host.py').read_text();action=(LOCAL/'self_maintenance_action.py').read_text();bootstrap=(LOCAL/'bootstrap-self-maintenance.command').read_text()
  self.assertIn('_load("self_maintenance_action")',host);self.assertIn('MAINTENANCE.execute',host);self.assertIn('system.self-maintain',action)
  self.assertNotIn('shell=True',action);self.assertIn('git branch "$SAFE_BRANCH" "$OLD_HEAD"',bootstrap);self.assertIn('git rebase --abort',bootstrap);self.assertIn('working tree is not clean',bootstrap)

if __name__=='__main__': unittest.main()
