#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,io,json,struct,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
host=load(Path(__file__).with_name('native_host.py'),'native_host_acceptance')
h=host.route_payload({'action':'native.health','__dore_transport_id':'h1'})
assert h['ok'] and h['assistant_directives'] is True
assert 'design.production.rollout' in h['production_capabilities']
# Framing remains valid for assistant-directive traffic without executing rollout.
p={'capability':'design.production.rollout','args':{},'__dore_transport_id':'x'}
raw=json.dumps(p).encode();stream=io.BytesIO(struct.pack('<I',len(raw))+raw)
assert host.read_message(stream)['capability']=='design.production.rollout'
content=(ROOT/'local/dore-companion-extension/content_script.js').read_text()
background=(ROOT/'local/dore-companion-extension/background.js').read_text()
manifest=json.loads((ROOT/'local/dore-companion-extension/manifest.json').read_text())
assert 'DORE_DIRECTIVE' in content and 'data-message-author-role="assistant"' in content
assert 'dore.directive' in background and 'design.' in background
assert manifest['version']=='2.0.0' and 'nativeMessaging' in manifest['permissions']
assert not any(str(x).startswith('http://127.0.0.1:4312') for x in manifest['permissions'])
print('DORE_A2A_ASSISTANT_DIRECTIVE_CONTROL_PLANE_PASS')
