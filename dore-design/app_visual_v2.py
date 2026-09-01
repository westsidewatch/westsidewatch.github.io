#!/usr/bin/env python3
"""Doré Design 1.4 — editor workspace is the single source of truth for preview."""
import mimetypes
import os
import shutil
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer
import app_visual as visual

ROOT=Path(__file__).resolve().parent.parent
MIRROR=ROOT/'dore-design/.site-mirror'

EDITOR_CSS=r'''
.stage.home{background:#f2eee4;color:#1e211f;isolation:isolate}
.stage.home:before{opacity:.08}
.stage.home:after{content:"";position:absolute;left:500px;right:0;top:96px;height:600px;z-index:0;background:linear-gradient(90deg,#0b2639 0%,rgba(11,38,57,.92) 12%,rgba(11,38,57,.38) 68%,rgba(7,26,40,.68) 100%),linear-gradient(180deg,rgba(7,26,40,.06),rgba(7,26,40,.55)),url("https://upload.wikimedia.org/wikipedia/commons/4/4f/Dore_nwe_jeruzalem_grt.jpg") 55% 40%/cover no-repeat;filter:grayscale(1) contrast(1.12) brightness(.8);pointer-events:none}
.home .masthead{left:64px!important;top:32px!important;width:1072px!important;height:62px!important;z-index:6;filter:none;opacity:.82;border-bottom:1px solid rgba(30,33,31,.22)}
.home .node{z-index:3;color:#1e211f}
.home .brand,.home .brand-zh,.home .h-rule{display:none}
.home .watch-kicker{color:#b39a47!important;letter-spacing:.16em;z-index:5}
.home .home-title{color:#f2eee4!important;font-size:88px!important;line-height:.72!important;letter-spacing:-.045em;z-index:5;text-shadow:0 1px 1px rgba(0,0,0,.12)}
.home .home-deck{color:rgba(242,238,228,.9)!important;line-height:1.45!important;z-index:5}
.home .verse{color:#d0bd78!important;line-height:1.5!important;letter-spacing:.12em;text-align:right;z-index:5}
.home .hero-rule{background:rgba(242,238,228,.32)!important;z-index:5}
.home .threshold-title{color:#1e211f!important}
.home .threshold-meta{color:#8c7a3d!important;letter-spacing:.15em;text-align:right}
.home .block{border:1px solid rgba(30,33,31,.22);padding:26px;background:#e7e0d2;color:#1e211f;overflow:hidden;display:flex;flex-direction:column;justify-content:flex-end;box-shadow:none}
.home .block:before{height:1px;background:#b39a47;width:28%}
.home .block .eye{color:#a2872a;letter-spacing:.14em}
.home .block h2{font-size:42px;line-height:.9;margin:18px 0 10px;font-weight:400}
.home .block p{font-size:15px;line-height:1.55}
.home .journal-tower{background:#0b2639;color:#f2eee4;border-color:#0b2639}
.home .journal-tower:after{content:"";position:absolute;inset:0;z-index:0;background:linear-gradient(180deg,rgba(7,26,40,.1),rgba(7,26,40,.95)),url("https://upload.wikimedia.org/wikipedia/commons/4/4f/Dore_nwe_jeruzalem_grt.jpg") 35% 50%/cover no-repeat;filter:grayscale(1) contrast(1.08);opacity:.46;pointer-events:none}
.home .journal-tower>*{position:relative;z-index:1}
.home .journal-tower .eye{color:#d0bd78}
.home .journal-tower h2{font-size:66px;max-width:5.2em}
.home .journal-tower p{font-size:17px;color:rgba(242,238,228,.8);max-width:22em}
.home .one-territory{background:#e7e0d2}
.home .one-territory h2{font-size:48px;max-width:10em}
.home .church-territory{background:#071a28;color:#f2eee4;border-color:#071a28}
.home .church-territory .eye{color:#d0bd78}
.home .church-territory p{color:rgba(242,238,228,.75)}
.home .library-territory{background:#ded6c4}
.home .join-territory{background:#b39a47;color:#071a28;border-color:#b39a47}
.home .join-territory:before{background:#071a28}
.home .join-territory .eye{color:#071a28}
.home .gate-copy-left,.home .gate-copy-right{color:#f2eee4!important;z-index:5}
.home .gate-copy-right{text-align:right}
.home .gatearch{left:520px!important;top:1645px!important;width:160px!important;height:185px!important;z-index:4;border:1px solid #d0bd78;border-bottom:0;border-radius:100px 100px 0 0;background:linear-gradient(180deg,rgba(208,189,120,.02),rgba(208,189,120,.13))}
.home .gate-mark{color:#d0bd78!important;letter-spacing:.18em;text-align:center;z-index:5}
.home .gate-left,.home .gate-right{background:#d0bd78!important;z-index:5}
.home .watch-number{color:#b39a47!important;font-size:128px!important;line-height:.7!important}
.home .watch-quote{color:#0b2639!important;font-size:54px!important;line-height:1.02!important}
.home .watch-cite,.home .footer{color:#a2872a!important;letter-spacing:.14em}
.home .footer-rule{background:rgba(30,33,31,.22)!important}
.home .crenel{display:none}
.home:has(.gate-copy-left):after{box-shadow:0 980px 0 0 #0b2639}
'''

EDITOR_HTML=(
    visual.HTML.replace(
        '<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>',
        '<div id="top"><b>DORÉ DESIGN 1.4 · STRUCTURE EDITOR</b><button onclick="location.href=\'/\'">Preview</button><button onclick="location.href=\'/journal/\'">Journal Mirror</button>'
    ).replace('</style>',EDITOR_CSS+'</style>')
)

PREVIEW_CSS=r"""
html,body{height:auto;min-height:100%;background:#071a28}
#top,.side{display:none!important}
.app{height:auto!important;display:block!important}
.stagewrap{min-height:100vh;padding:28px;overflow:auto;display:flex;align-items:flex-start;justify-content:center;background:#071a28}
.stage{margin:0 auto}
.stage .node{pointer-events:none!important;cursor:default!important}
.preview-edit{position:fixed;right:18px;bottom:18px;z-index:9999;background:#0b2639;color:#f2eee4;border:1px solid #b39a47;padding:9px 12px;text-decoration:none;font:10px ui-monospace,monospace;letter-spacing:.12em}
@media(max-width:700px){.stagewrap{padding:0;justify-content:flex-start}}
"""

PUBLIC_HTML=(
    EDITOR_HTML
    .replace('<body>','<body class="preview">')
    .replace('</style>',PREVIEW_CSS+'</style>',1)
    .replace('</body>','<a class="preview-edit" href="/editor">EDIT IN DORÉ DESIGN</a></body>')
)

def build_site_mirror(force=False):
    journal_index=MIRROR/'journal/index.html'
    vol_index=MIRROR/'vol-00/index.html'
    if not force and journal_index.exists() and vol_index.exists():
        return {'ok':True,'rebuilt':False,'engine':'hugo','mirror':str(MIRROR)}
    hugo=shutil.which('hugo')
    if not hugo:
        return {'ok':False,'error':'hugo_not_found','mirror':str(MIRROR)}
    MIRROR.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run(
        [hugo,'--destination',str(MIRROR),'--cleanDestinationDir'],
        cwd=str(ROOT),capture_output=True,text=True,timeout=90
    )
    if proc.returncode!=0:
        return {'ok':False,'error':'hugo_build_failed','stderr':proc.stderr[-4000:],'stdout':proc.stdout[-2000:]}
    if not journal_index.exists():
        return {'ok':False,'error':'journal_mirror_missing_after_build'}
    if not vol_index.exists():
        return {'ok':False,'error':'vol00_mirror_missing_after_build'}
    return {'ok':True,'rebuilt':True,'engine':'hugo','mirror':str(MIRROR)}

def mirror_file_for(request_path):
    clean=request_path.split('?',1)[0].split('#',1)[0]
    rel=clean.lstrip('/')
    candidate=(MIRROR/rel).resolve()
    root=MIRROR.resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    if candidate.is_dir():
        candidate=candidate/'index.html'
    if candidate.is_file():
        return candidate
    return None

class H(visual.H):
    def send_bytes(self,status,body,ctype):
        self.send_response(status)
        self.send_header('Content-Type',ctype)
        self.send_header('Cache-Control','no-store')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_mirror(self,path):
        p=mirror_file_for(path)
        if not p:
            return False
        ctype=mimetypes.guess_type(str(p))[0] or 'application/octet-stream'
        self.send_bytes(200,p.read_bytes(),ctype)
        return True

    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/':
            return self.send_bytes(200,PUBLIC_HTML.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor':
            return self.send_bytes(200,EDITOR_HTML.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/asset/morning-star.svg':
            p=ROOT/'static/images/westside-watch-morning-star.svg'
            if p.exists():
                return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path in ('/journal','/journal/','/vol-00','/vol-00/'):
            result=build_site_mirror(force=False)
            if not result.get('ok'):
                return self.out(500,result)
            normalized=path if path.endswith('/') else path+'/'
            if self.serve_mirror(normalized):
                return
            return self.out(404,{'ok':False,'error':'mirror_page_not_found','path':normalized})
        if path=='/api/mirror/status':
            return self.out(200,{
                'ok':(MIRROR/'journal/index.html').exists() and (MIRROR/'vol-00/index.html').exists(),
                'journal':'/journal/',
                'vol00':'/vol-00/',
                'mode':'source-identical-hugo-mirror',
                'redesign':False
            })
        if path=='/api/preview/status':
            w=visual.base.workspace()
            home=next((p for p in w.get('pages',[]) if p.get('id')=='homepage'),w.get('pages',[None])[0])
            return self.out(200,{
                'ok':bool(home),
                'mode':'same-workspace-same-renderer',
                'workspace_id':w.get('id'),
                'revision':w.get('revision'),
                'page_id':home.get('id') if home else None,
                'node_count':len(home.get('nodes',[])) if home else 0,
                'editor':'/editor',
                'preview':'/'
            })
        if MIRROR.exists() and self.serve_mirror(path):
            return
        if path=='/api/health':
            return self.out(200,{
                'ok':True,
                'service':'dore-design',
                'version':'1.4',
                'workspace':'new-westside',
                'source_of_truth':'structured-workspace',
                'default_surface':'workspace-homepage-preview',
                'preview_mode':'same-workspace-same-renderer',
                'design_direction':'watch-for-the-dawn',
                'editor':'/editor',
                'preview':'/',
                'journal_mirror':'/journal/',
                'vol00_mirror':'/vol-00/',
                'journal_mode':'source-identical-hugo-mirror',
                'visual_grammar':['approved-front-door','watch-for-the-dawn','dore-engraving','editorial-gravity','5:8','asymmetric-portals','central-gate','archival-print']
            })
        return super().do_GET()

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
