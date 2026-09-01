#!/usr/bin/env python3
"""Doré Design 1.5.1 — locked #262 front door with restored editing chrome."""
import mimetypes
import os
import shutil
import subprocess
from pathlib import Path
from http.server import ThreadingHTTPServer
import app_visual as visual
import homepage_wysiwyg

ROOT=Path(__file__).resolve().parent.parent
MIRROR=ROOT/'dore-design/.site-mirror'

STRUCTURE_HTML=(visual.HTML.replace('<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>','<div id="top"><b>DORÉ DESIGN 1.5.1 · STRUCTURE</b><button onclick="location.href=\'/editor\'">WYSIWYG</button><button onclick="location.href=\'/\'">Preview</button>'))

def build_site_mirror(force=False):
    journal_index=MIRROR/'journal/index.html';vol_index=MIRROR/'vol-00/index.html'
    if not force and journal_index.exists() and vol_index.exists():return {'ok':True,'rebuilt':False,'engine':'hugo','mirror':str(MIRROR)}
    hugo=shutil.which('hugo')
    if not hugo:return {'ok':False,'error':'hugo_not_found','mirror':str(MIRROR)}
    MIRROR.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run([hugo,'--destination',str(MIRROR),'--cleanDestinationDir'],cwd=str(ROOT),capture_output=True,text=True,timeout=90)
    if proc.returncode!=0:return {'ok':False,'error':'hugo_build_failed','stderr':proc.stderr[-4000:],'stdout':proc.stdout[-2000:]}
    if not journal_index.exists():return {'ok':False,'error':'journal_mirror_missing_after_build'}
    if not vol_index.exists():return {'ok':False,'error':'vol00_mirror_missing_after_build'}
    return {'ok':True,'rebuilt':True,'engine':'hugo','mirror':str(MIRROR)}

def mirror_file_for(request_path):
    clean=request_path.split('?',1)[0].split('#',1)[0];rel=clean.lstrip('/');candidate=(MIRROR/rel).resolve();root=MIRROR.resolve()
    try:candidate.relative_to(root)
    except ValueError:return None
    if candidate.is_dir():candidate=candidate/'index.html'
    return candidate if candidate.is_file() else None

class H(visual.H):
    def send_bytes(self,status,body,ctype):
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def serve_mirror(self,path):
        p=mirror_file_for(path)
        if not p:return False
        ctype=mimetypes.guess_type(str(p))[0] or 'application/octet-stream';self.send_bytes(200,p.read_bytes(),ctype);return True
    def do_GET(self):
        path=self.path.split('?',1)[0]
        if path=='/':return self.send_bytes(200,homepage_wysiwyg.render_canvas(edit=False).encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor':return self.send_bytes(200,homepage_wysiwyg.render_editor().encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor-canvas':return self.send_bytes(200,homepage_wysiwyg.render_canvas(edit=True).encode('utf-8'),'text/html; charset=utf-8')
        if path=='/structure-editor':return self.send_bytes(200,STRUCTURE_HTML.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/asset/masthead.svg':
            p=ROOT/'static/images/westside-watch-masthead-landscape.svg'
            if p.exists():return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path=='/asset/morning-star.svg':
            p=ROOT/'static/images/westside-watch-morning-star.svg'
            if p.exists():return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path in ('/journal','/journal/','/vol-00','/vol-00/'):
            result=build_site_mirror(force=False)
            if not result.get('ok'):return self.out(500,result)
            normalized=path if path.endswith('/') else path+'/'
            if self.serve_mirror(normalized):return
            return self.out(404,{'ok':False,'error':'mirror_page_not_found','path':normalized})
        if path=='/api/mirror/status':return self.out(200,{'ok':(MIRROR/'journal/index.html').exists() and (MIRROR/'vol-00/index.html').exists(),'journal':'/journal/','vol00':'/vol-00/','mode':'source-identical-hugo-mirror','redesign':False})
        if path=='/api/preview/status':
            w=visual.base.workspace();home=next((p for p in w.get('pages',[]) if p.get('id')=='homepage'),w.get('pages',[None])[0])
            return self.out(200,{'ok':bool(home),'mode':'locked-template-shared-workspace','workspace_id':w.get('id'),'revision':w.get('revision'),'page_id':home.get('id') if home else None,'node_count':len(home.get('nodes',[])) if home else 0,'editor':'/editor','editor_canvas':'/editor-canvas','preview':'/','structure_editor':'/structure-editor'})
        if MIRROR.exists() and self.serve_mirror(path):return
        if path=='/api/health':return self.out(200,{'ok':True,'service':'dore-design','version':'1.5.1','workspace':'new-westside','source_of_truth':'structured-workspace','layout_source':'approved-front-door-262-locked','preview_mode':'locked-template-shared-workspace','design_direction':'watch-for-the-dawn','editor':'/editor','editor_canvas':'/editor-canvas','preview':'/','structure_editor':'/structure-editor','journal_mirror':'/journal/','vol00_mirror':'/vol-00/','journal_mode':'source-identical-hugo-mirror','visual_grammar':['approved-front-door','design-locked','watch-for-the-dawn','dore-engraving','responsive-city-grid','5:8-journal','central-gate','archival-print']})
        return super().do_GET()

if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
