#!/usr/bin/env python3
"""Doré Design 1.6 — locked #262 front door plus the complete main-site Journal."""
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

STRUCTURE_HTML=(visual.HTML.replace('<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>','<div id="top"><b>DORÉ DESIGN 1.6 · STRUCTURE</b><button onclick="location.href=\'/editor\'">WYSIWYG</button><button onclick="location.href=\'/\'">Preview</button>'))

PREVIEW_EDIT_ENTRY='''<style>.dore-preview-edit{position:fixed;right:18px;bottom:18px;z-index:2147483647;padding:9px 12px;border:1px solid rgba(208,189,120,.7);background:rgba(7,26,40,.88);color:#f2eee4!important;text-decoration:none!important;font:10px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;backdrop-filter:blur(4px);box-shadow:0 4px 18px rgba(0,0,0,.18)}.dore-preview-edit:hover,.dore-preview-edit:focus{background:#0b2639;border-color:#d0bd78;outline:none}</style><a class="dore-preview-edit" href="/editor" aria-label="Return to Doré Design editor">Edit in Doré Design</a>'''
JOURNAL_DESIGN_NAV='''<style>.dore-journal-nav{position:fixed;right:18px;bottom:18px;z-index:2147483647;display:flex;gap:7px}.dore-journal-nav a{padding:9px 12px;border:1px solid rgba(208,189,120,.7);background:rgba(7,26,40,.9);color:#f2eee4!important;text-decoration:none!important;font:10px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;backdrop-filter:blur(4px);box-shadow:0 4px 18px rgba(0,0,0,.18)}.dore-journal-nav a:hover,.dore-journal-nav a:focus{background:#0b2639;border-color:#d0bd78;outline:none}</style><nav class="dore-journal-nav" aria-label="Doré Design journal navigation"><a href="/">Front Door</a><a href="/editor">Edit in Doré Design</a></nav>'''

def preview_html():
    html=homepage_wysiwyg.render_canvas(edit=False)
    return html.replace('</body>',PREVIEW_EDIT_ENTRY+'</body>',1)

def build_site_mirror(force=False):
    site_index=MIRROR/'index.html';journal_index=MIRROR/'journal/index.html';vol_index=MIRROR/'vol-00/index.html'
    if not force and site_index.exists() and journal_index.exists() and vol_index.exists():return {'ok':True,'rebuilt':False,'engine':'hugo','mirror':str(MIRROR)}
    hugo=shutil.which('hugo')
    if not hugo:return {'ok':False,'error':'hugo_not_found','mirror':str(MIRROR)}
    MIRROR.mkdir(parents=True,exist_ok=True)
    proc=subprocess.run([hugo,'--destination',str(MIRROR),'--cleanDestinationDir'],cwd=str(ROOT),capture_output=True,text=True,timeout=90)
    if proc.returncode!=0:return {'ok':False,'error':'hugo_build_failed','stderr':proc.stderr[-4000:],'stdout':proc.stdout[-2000:]}
    if not site_index.exists():return {'ok':False,'error':'site_mirror_missing_after_build'}
    if not journal_index.exists():return {'ok':False,'error':'journal_mirror_missing_after_build'}
    if not vol_index.exists():return {'ok':False,'error':'vol00_mirror_missing_after_build'}
    return {'ok':True,'rebuilt':True,'engine':'hugo','mirror':str(MIRROR)}

def journal_full_html():
    result=build_site_mirror(force=False)
    if not result.get('ok'):return None,result
    html=(MIRROR/'index.html').read_text(encoding='utf-8')
    return html.replace('</body>',JOURNAL_DESIGN_NAV+'</body>',1),result

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
        if path=='/':return self.send_bytes(200,preview_html().encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor':return self.send_bytes(200,homepage_wysiwyg.render_editor().encode('utf-8'),'text/html; charset=utf-8')
        if path=='/editor-canvas':return self.send_bytes(200,homepage_wysiwyg.render_canvas(edit=True).encode('utf-8'),'text/html; charset=utf-8')
        if path=='/structure-editor':return self.send_bytes(200,STRUCTURE_HTML.encode('utf-8'),'text/html; charset=utf-8')
        if path=='/asset/masthead.svg':
            p=ROOT/'static/images/westside-watch-masthead-landscape.svg'
            if p.exists():return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path=='/asset/morning-star.svg':
            p=ROOT/'static/images/westside-watch-morning-star.svg'
            if p.exists():return self.send_bytes(200,p.read_bytes(),'image/svg+xml')
        if path in ('/journal','/journal/'):
            html,result=journal_full_html()
            if not result.get('ok'):return self.out(500,result)
            return self.send_bytes(200,html.encode('utf-8'),'text/html; charset=utf-8')
        if path in ('/journal-index','/journal-index/'):
            result=build_site_mirror(force=False)
            if not result.get('ok'):return self.out(500,result)
            if self.serve_mirror('/journal/'):return
            return self.out(404,{'ok':False,'error':'journal_index_mirror_not_found'})
        if path in ('/vol-00','/vol-00/'):
            result=build_site_mirror(force=False)
            if not result.get('ok'):return self.out(500,result)
            if self.serve_mirror('/vol-00/'):return
            return self.out(404,{'ok':False,'error':'vol00_mirror_not_found'})
        if path=='/api/mirror/status':return self.out(200,{'ok':(MIRROR/'index.html').exists() and (MIRROR/'journal/index.html').exists() and (MIRROR/'vol-00/index.html').exists(),'journal':'/journal/','journal_index':'/journal-index/','vol00':'/vol-00/','mode':'full-main-site-journal-in-design','redesign':False})
        if path=='/api/preview/status':
            w=visual.base.workspace();home=next((p for p in w.get('pages',[]) if p.get('id')=='homepage'),w.get('pages',[None])[0])
            return self.out(200,{'ok':bool(home),'mode':'locked-template-shared-workspace','workspace_id':w.get('id'),'revision':w.get('revision'),'page_id':home.get('id') if home else None,'node_count':len(home.get('nodes',[])) if home else 0,'editor':'/editor','editor_canvas':'/editor-canvas','preview':'/','preview_edit_entry':True,'journal':'/journal/','journal_full_issue':True,'structure_editor':'/structure-editor'})
        if MIRROR.exists() and self.serve_mirror(path):return
        if path=='/api/health':return self.out(200,{'ok':True,'service':'dore-design','version':'1.6','workspace':'new-westside','source_of_truth':'structured-workspace','layout_source':'approved-front-door-262-locked','preview_mode':'locked-template-shared-workspace','design_direction':'watch-for-the-dawn','editor':'/editor','editor_canvas':'/editor-canvas','preview':'/','preview_edit_entry':True,'structure_editor':'/structure-editor','journal':'/journal/','journal_index':'/journal-index/','vol00_mirror':'/vol-00/','journal_mode':'full-main-site-journal-in-design','journal_source':'hugo-root-index','visual_grammar':['approved-front-door','design-locked','watch-for-the-dawn','dore-engraving','responsive-city-grid','5:8-journal','central-gate','archival-print']})
        return super().do_GET()

if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
