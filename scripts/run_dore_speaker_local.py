#!/usr/bin/env python3
"""One-shot autonomous local speaker proof. Run on Mac mini; no ChatGPT connection needed.
Prepares job, dispatches via EXISTING local dore.a2a/1 Gateway, stores JSON response.
No publish. Explicitly blocks reusing a request ID for changed parameters.
"""
import argparse,json,uuid,urllib.request,urllib.error
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def dispatch(speaker,request_id,url,output,dry_run=False):
 if not url.startswith('http://127.0.0.1:') and not url.startswith('http://localhost:'):
  raise ValueError('Local loopback Gateway only')
 payload={'protocol':'dore.a2a/1','action':'dispatch','request_id':request_id,
          'conversation_id':'speaker-engineering','session_id':'mac-mini','consumer_id':'design',
          'capability_id':'design.speaker-cover.render','payload':{'speaker':speaker,'dry_run':dry_run}}
 out=Path(output);out.mkdir(parents=True,exist_ok=True)
 reqpath=out/'request.json'
 if reqpath.exists() and json.loads(reqpath.read_text())!=payload:
  raise ValueError('Existing request_id payload mismatch; refusing changed replay')
 reqpath.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
 req=urllib.request.Request(url,json.dumps(payload).encode(),{'Content-Type':'application/json'},method='POST')
 try:
  with urllib.request.urlopen(req,timeout=1800) as response:
   raw=response.read(2_000_000)
   result=json.loads(raw)
 except urllib.error.HTTPError as exc:
  body=exc.read(4096).decode(errors='replace')
  (out/'error.txt').write_text(f'HTTP {exc.code}: {body}')
  raise
 (out/'gateway-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 return result
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--speaker',default='david-pawson')
 p.add_argument('--gateway',default='http://127.0.0.1:4312/a2a')
 p.add_argument('--request-id',default=None)
 p.add_argument('--output',default='local/dore-speaker-runs')
 p.add_argument('--dry-run',action='store_true')
 a=p.parse_args()
 rid=a.request_id or 'dore-'+uuid.uuid4().hex
 dest=Path(a.output)/rid
 result=dispatch(a.speaker,rid,a.gateway,dest,a.dry_run)
 print(json.dumps({'request_id':rid,'response_file':str(dest/'gateway-result.json'),'gateway_result':result},ensure_ascii=False))
if __name__=='__main__':main()
