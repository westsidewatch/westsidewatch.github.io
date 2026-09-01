#!/usr/bin/env python3
"""Doré Design 1.3 — Living Fortress homepage plus source-identical Journal/Vol.00 mirror."""
import mimetypes
import os
import shutil
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer
import app_visual as visual

ROOT=Path(__file__).resolve().parent.parent
HOMEPAGE=ROOT/'dore-design/new-westside/homepage-v2-living-fortress.html'
MIRROR=ROOT/'dore-design/.site-mirror'

EDITOR_CSS=r'''
.stage.home{background:linear-gradient(180deg,#102a43 0%,#091c2d 100%);color:#f7f3e9;isolation:isolate}
.stage.home:after{content:"";position:absolute;right:0;top:80px;width:62%;height:610px;z-index:0;background:linear-gradient(90deg,#102a43 0%,transparent 32%),linear-gradient(180deg,transparent 52%,#102a43 100%),url("https://upload.wikimedia.org/wikipedia/commons/4/4f/Dore_nwe_jeruzalem_grt.jpg") center/cover no-repeat;filter:grayscale(1) contrast(1.18);opacity:.38;mix-blend-mode:screen;pointer-events:none}
.home .masthead{z-index:4;filter:brightness(0) invert(1);opacity:.92}
.home .node{z-index:2;color:#f7f3e9}
.home .watch-kicker{top:112px!important;color:#d2bc69;letter-spacing:.14em}
.home .home-title{top:148px!important;color:#f7f3e9;font-size:70px!important;line-height:.78}
.home .home-deck{top:305px!important;color:#d2bc69}
.home .block{border:1px solid rgba(247,243,233,.3);background:rgba(9,28,45,.67);color:#f7f3e9;padding:16px;backdrop-filter:blur(1px)}
.home .block:before{height:1px;background:#d2bc69}
.home .block .eye{color:#d2bc69}
.home .block h2{font-size:30px;line-height:.94}
.home .journal-tower{left:54px!important;top:360px!important;width:390px!important;height:624px!important;background:rgba(7,22,36,.9);border-color:rgba(210,188,105,.58)}
.home .journal-tower h2{font-size:54px}
.home .one-territory{background:rgba(9,28,45,.72)}
.home .signal-territory{background:rgba(247,243,233,.92);color:#24231f}
.home .signal-territory .eye{color:#a2872a}
.home .church-territory{background:rgba(7,22,36,.82)}
.home .library-territory{background:rgba(229,222,206,.94);color:#24231f}
.home .library-territory .eye{color:#a2872a}
.home .witness-territory,.home .prayer-territory,.home .archive-territory{background:rgba(9,28,45,.72)}
.home .gatearch{left:690px;top:735px;width:130px;height:250px;z-index:3;border-color:#d2bc69;background:linear-gradient(rgba(210,188,105,.03),rgba(162,135,42,.2))}
.home .gate-mark{left:680px!important;top:930px!important;color:#d2bc69;letter-spacing:.16em;z-index:5}
.home .gate-left{left:660px!important;top:986px!important;width:48px!important;background:#d2bc69}
.home .gate-right{left:812px!important;top:986px!important;width:48px!important;background:#d2bc69}
.home .footer{left:462px!important;top:1025px!important;color:#d2bc69;letter-spacing:.12em}
.home .crenel{left:45px;right:45px;bottom:18px;background:linear-gradient(90deg,#d2bc69 0 8%,transparent 8% 11%,#d2bc69 11% 24%,transparent 24% 29%,#d2bc69 29% 42%,transparent 42% 46%,#d2bc69 46% 63%,transparent 63% 68%,#d2bc69 68% 79%,transparent 79% 84%,#d2bc69 84% 100%);opacity:.25;z-index:1}
'''

# Keep the structured editor, but make its relationship to the visual surfaces explicit.
EDITOR_HTML=(
    visual.HTML.replace(
        '<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>',
        '<div id="top"><b>DORÉ DESIGN 1.3 · STRUCTURE EDITOR</b><button onclick="location.href=\'/\'">Living Fortress</button><button onclick="location.href=\'/journal/\'">Journal Mirror</button>'
    ).replace('</style>',EDITOR_CSS+'</style>')
)


def build_site_mirror(force=False):
    """Build the CURRENT Hugo site into a private Doré Design mirror.

    This is deliberately not a redesign or reimplementation. It uses the same
    Hugo source, layouts, CSS and static assets as the main site so Journal and
    Vol.00 arrive in Doré Design at visual/source parity first.
    """
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
    """Resolve a browser path against the built site mirror without escaping it."""
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
            if not HOMEPAGE.exists():
                return self.out(500,{'ok':False,'error':'homepage_visual_missing'})
            html=HOMEPAGE.read_text(encoding='utf-8')
            html=html.replace('/images/westside-watch-masthead-landscape.svg','/asset/masthead.svg')
            html=html.replace('/images/westside-watch-morning-star.svg','/asset/morning-star.svg')
            html=html.replace('</body>','<a href="/editor" style="position:fixed;right:18px;bottom:18px;z-index:9999;background:#102a43;color:#faf9f5;border:1px solid #a2872a;padding:9px 12px;text-decoration:none;font:10px ui-monospace,monospace;letter-spacing:.12em">EDIT IN DORÉ DESIGN</a></body>')
            return self.send_bytes(200,html.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor':
            return self.send_bytes(200,EDITOR_HTML.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/asset/morning-star.svg':
            p=ROOT/'static/images/westside-watch-morning-star.svg'
            if p.exists(): return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path in ('/journal','/journal/','/vol-00','/vol-00/'):
            result=build_site_mirror(force=False)
            if not result.get('ok'):
                return self.out(500,result)
            normalized=path if path.endswith('/') else path+'/'
            if self.serve_mirror(normalized): return
            return self.out(404,{'ok':False,'error':'mirror_page_not_found','path':normalized})
        if path=='/api/mirror/status':
            return self.out(200,{
                'ok':(MIRROR/'journal/index.html').exists() and (MIRROR/'vol-00/index.html').exists(),
                'journal':'/journal/',
                'vol00':'/vol-00/',
                'mode':'source-identical-hugo-mirror',
                'redesign':False
            })
        # Once the mirror exists, let its exact CSS/JS/images/fonts and nested
        # Journal/Vol.00 routes resolve before falling back to editor assets/APIs.
        if MIRROR.exists() and self.serve_mirror(path):
            return
        if path=='/api/health':
            return self.out(200,{
                'ok':True,
                'service':'dore-design',
                'version':'1.3',
                'workspace':'new-westside',
                'default_surface':'homepage-v2-living-fortress',
                'design_direction':'A-living-fortress',
                'candidate':'homepage-v2-candidate-01',
                'editor':'/editor',
                'journal_mirror':'/journal/',
                'vol00_mirror':'/vol-00/',
                'journal_mode':'source-identical-hugo-mirror',
                'visual_grammar':['official-masthead','editorial-gravity','5:8','huarong-reflow','crenellation','central-gate','dore-engraving','archival-print','time-flow']
            })
        return super().do_GET()


if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
