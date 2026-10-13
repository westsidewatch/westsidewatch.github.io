#!/usr/bin/env python3
"""Protect the human-approved composed asset, including source and portrait bytes."""
import hashlib,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
manifest='static/olive/components/speaker-baseline-v1/integrity.json'
current=json.loads((root/manifest).read_text())
base=subprocess.run(['git','show','origin/main:'+manifest],cwd=root,text=True,capture_output=True)
expected=json.loads(base.stdout) if base.returncode==0 else current
if base.returncode==0 and current!=expected:
 raise SystemExit('FAIL: frozen v1 integrity manifest changed; preserve v1 and create a separately authorized variant')
for name,digest in expected.items():
 p=root/name
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:
  raise SystemExit('FAIL: protected Olive baseline changed or deleted: '+name)
for f in ['static/js/olive-editorial-rail.js','static/js/olive-journey.js']:
 s=(root/f).read_text()
 assert 'OliveSpeakerBaseline.mount' in s, f+' bypasses protected component'
 assert 'identity-en' not in s and 'englishNames' not in s, f+' reintroduces competing name overlays'
s=(root/'layouts/olive/surface-carrier.html').read_text()
assert s.count('/olive/components/speaker-baseline-v1/baseline.js')==1
records=json.loads((root/'static/olive/components/speaker-baseline-v1/names.json').read_text())
assert len(records)==12 and len({x['slug'] for x in records})==12
print('PASS: frozen bilingual composition, original sources, twelve portraits and live consumers')

# Profile transparency is independent of the immutable poster compositions.
profile_dir=root/'static/images/olive/people-transparent-v1'
if profile_dir.exists():
 originals=json.loads((profile_dir/'original-posters.json').read_text())['sha256']
 for path,digest in originals.items():
  assert hashlib.sha256((root/path).read_bytes()).hexdigest()==digest, 'Original poster overwritten: '+path
 profiles=json.loads((profile_dir/'assets.json').read_text())['records']
 assert len(profiles)==12 and len({r['id'] for r in profiles})==12, 'Twelve unique profile assets required'
 template=(root/'layouts/_default/olive-editorial.html').read_text()
 assert '.Params.portrait_profile_image | default .Params.portrait_image' in template
 for record in profiles:
  asset=root/'static'/record['url'].lstrip('/')
  png=asset.read_bytes()
  assert hashlib.sha256(png).hexdigest()==record['sha256'], 'Profile asset changed: '+record['id']
  assert png[:8]==b'\x89PNG\r\n\x1a\n' and png[25]==6, 'RGBA PNG required: '+record['id']
  page=(root/'content/olive'/(record['id']+'.md')).read_text()
  assert 'portrait_profile_image: "'+record['url']+'"' in page, 'Missing profile binding: '+record['id']
  assert 'portrait_image: "/images/olive/'+record['id']+'-editorial.png"' in page, 'Original poster binding changed: '+record['id']
 print('PASS: 12 separate RGBA profile assets; all original poster hashes and bindings preserved')
