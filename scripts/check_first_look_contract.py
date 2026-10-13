#!/usr/bin/env python3
"""Protect approved screens and boundaries while seven-realm acceptance continues."""
from pathlib import Path
import hashlib,json,re,sys
root=Path(__file__).resolve().parents[1]
def read(p): return (root/p).read_text()
def require(ok,message):
 if not ok: raise SystemExit('FAIL: '+message)
freeze=json.loads(read('static/first-look/home-freeze.v1.json'))['sha256']
for path,digest in freeze.items():
 content=read('layouts/partials/watch-home.html').split('<section class="sites-home-hero"',1)[1] if path=='home_first_three_screens' else None
 if path=='home_first_three_screens':
  content=('<section class="sites-home-hero"'+content).split('<div class="sites-home-realms"')[0].encode()
 else:
  content=(root/path).read_bytes()
 require(hashlib.sha256(content).hexdigest()==digest,'frozen homepage composition changed: '+path)
home=read('layouts/partials/watch-home.html')
require(len(re.findall('data-fl-realm-frame=',home))==7,'seven actual realm stages required')
for route in ['church','journal','emmaus','olive','dawn-library','cinema','daylight-cafe']:
 require(f'src="/{route}/?first-look=embed"' in home,'missing realm content: '+route)
require(home.count('first-look-host.js')==1,'one parent adapter required')
corpus=json.loads(read('static/first-look/scripture.v1.json'))
js=read('static/js/westside-first-look.js')
embedded=json.loads(js.split('const corpus=',1)[1].split(';\n const aliases=',1)[0])
require(corpus==embedded,'scripture runtime diverges from canonical verified corpus')
require(corpus['timezone']=='America/Toronto','Toronto owns daily date')
require(len(corpus['identities'])==7 and all(v['verified'] for v in corpus['verses']),'verified realm scripture missing')
require('stage.after(band)' in js and 'aria-pressed' in js,'scripture must stay outside media with a pause control')
require("e.origin===location.origin&&e.source===parent" in js,'child message origin/source validation missing')
require("event.origin!==location.origin" in read('static/js/first-look-host.js') and 'contentWindow===event.source' in read('static/js/first-look-host.js'),'parent message validation missing')
book=read('layouts/dawn-library/list.html')
require('sites-product-frame' not in book and 'data-fl-book-reading' in book,'book must expose actual reading without physical spread')
life=read('layouts/daylight-cafe/portal.html')
require(all(s in life for s in ['生活工具','拾字','Habakkuk','/calligraphy/remote-probe.html','westsidewatch/Westside-Stories']),'independent tool entries missing from Life')
require('vol-00' not in life,'Life tool entries must not depend on Vol.00')
print('PASS: frozen first three screens, seven shared stages, scripture authority, message boundaries, digital reader and independent Life tools')
print('NOT A COMPLETION GATE: approved Magazine columns and runtime audiovisual/accessibility evidence remain separate acceptance requirements.')
