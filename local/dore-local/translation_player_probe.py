#!/usr/bin/env python3
import json
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[2]
item = json.loads((root/'cinema/data/translation-source.v0.json').read_text())['items'][0]
url = item['providerProbeUrl']
req = Request(url, headers={'User-Agent':'Mozilla/5.0','Accept':'text/html,*/*'})
with urlopen(req, timeout=30) as response:
    body = response.read(65536).decode('utf-8', errors='replace')
    print('FINAL_URL=' + response.geturl())
    print('STATUS=' + str(getattr(response, 'status', 200)))
    print('BODY_BEGIN=' + body[:4000].replace('\n',' '))
