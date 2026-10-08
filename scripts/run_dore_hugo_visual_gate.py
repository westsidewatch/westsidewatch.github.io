#!/usr/bin/env python3
"""Build a Doré Hugo proof and capture it via a local HTTP server.

Requires hugo, Playwright Python and installed Chromium. Does not download,
modify production content, publish or claim visual QA acceptance.
"""
import argparse,functools,http.server,json,shutil,subprocess,threading
from pathlib import Path
from capture_dore_editorial_screenshots import capture

def build(repo,overlay,out):
 repo=Path(repo).resolve();overlay=Path(overlay).resolve();out=Path(out).resolve()
 content=overlay/'content';asset=overlay/'static'
 if not (repo/'hugo.toml').is_file():raise FileNotFoundError(repo/'hugo.toml')
 if not content.is_dir():raise FileNotFoundError(content)
 if not asset.is_dir():raise FileNotFoundError(asset)
 if not shutil.which('hugo'):raise RuntimeError('hugo executable unavailable')
 out.mkdir(parents=True,exist_ok=True)
 cmd=['hugo','--source',str(repo),'--contentDir',str(content),
      '--destination',str(out/'public'),'--cleanDestinationDir']
 subprocess.run(cmd,cwd=repo,check=True)
 for file in asset.rglob('*'):
  if file.is_file():
   target=out/'public'/file.relative_to(asset)
   target.parent.mkdir(parents=True,exist_ok=True)
   shutil.copy2(file,target)
 pages=list(content.rglob('dore-proof.md'))
 if len(pages)!=1:raise ValueError('Expected exactly one dore-proof.md')
 route=pages[0].parent.parent.name
 html=out/'public'/route/'dore-proof'/'index.html'
 if not html.is_file():raise FileNotFoundError('Hugo did not render proof: '+str(html))
 return html,out/'public'
def run(repo,overlay,out):
 html,root=build(repo,overlay,out)
 handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(root))
 server=http.server.ThreadingHTTPServer(('127.0.0.1',0),handler)
 thread=threading.Thread(target=server.serve_forever,daemon=True)
 thread.start()
 try:
  url='http://127.0.0.1:'+str(server.server_port)+'/'+html.relative_to(root).as_posix()
  result=capture(url,Path(out)/'screenshots')
  result['hugo_proof_route']=html.relative_to(root).as_posix()
  return result
 finally:
  server.shutdown();server.server_close();thread.join(timeout=5)
def main():
 p=argparse.ArgumentParser()
 p.add_argument('--repo',default='.')
 p.add_argument('--overlay',required=True)
 p.add_argument('--out',default='local/dore-hugo-proof-run')
 a=p.parse_args()
 r=run(a.repo,a.overlay,a.out)
 print(json.dumps({'screenshots':len(r['screenshots']),'route':r['hugo_proof_route']}))
if __name__=='__main__':main()
