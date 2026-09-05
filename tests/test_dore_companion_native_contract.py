from __future__ import annotations
import json, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; EXT=ROOT/'local'/'dore-companion-extension'
class CompanionNativeContractTest(unittest.TestCase):
 def test_native_manifest_contract_matches_native_host(self):
  m=json.loads((EXT/'manifest.native-messaging.json').read_text());self.assertIn('nativeMessaging',m['permissions']);self.assertEqual(m['browser_specific_settings']['gecko']['id'],'dore-companion@westsidewatch.ca');self.assertEqual(m['dore_native_messaging']['host'],'ca.dore.companion')
 def test_companion_manifest(self):
  m=json.loads((EXT/'manifest.json').read_text());self.assertEqual(m['version'],'1.4.0');self.assertNotIn('applications',m);self.assertIn('nativeMessaging',m['permissions'])
 def test_transport_native_first(self):
  s=(EXT/'native_transport.js').read_text();self.assertIn('browser.runtime.connectNative(DORE_NATIVE_HOST)',s);self.assertLess(s.index('sendViaNative(payload)'),s.index('sendVia4312(payload)'))
 def test_production_design_envelope(self):
  s=(EXT/'background.js').read_text();
  for token in ['protocol: "dore.a2a/1"','action: "dispatch"','request_id: nextRequestId()','conversation_id:','session_id: sessionId','consumer_id: "design"','capability_id: "design.compose"','asset_candidate:','version: "1.4.0"'] : self.assertIn(token,s)
  self.assertIn('normalized === "/dore design"',s)
 def test_stage2_remains_diagnostic(self):
  s=(EXT/'background.js').read_text();a=s.index('if (normalized === "/dore stage2"');b=s.index('if (normalized === "/dore design"');self.assertNotIn('protocol: "dore.a2a/1"',s[a:b])
 def test_conversation_binding_and_result_surface(self):
  s=(EXT/'content_script.js').read_text();self.assertIn('function conversationId()',s);self.assertIn('conversation_id:conversationId()',s);self.assertIn('"dore:a2a-result"',s);self.assertIn('TERMINAL_HOLD_MS = 30000',s);self.assertIn('new WeakSet()',s)
 def test_installer_free_runtime(self):
  s=(EXT/'install_companion_1.command').read_text().lower();self.assertNotIn('api.openai.com',s)
if __name__=='__main__': unittest.main()
