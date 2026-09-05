#!/usr/bin/env python3
"""DORÉ DESIGN resident — 1.9.1 fallback + 2.0 workbench."""
import json,mimetypes,os
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
import app_visual as visual
import multiwrite_integration
multiwrite_integration.install_workspace(visual.base)
import design2_workspace
design2_workspace.install(visual.base)
import multipage_wysiwyg,journal_wysiwyg,multiwrite_wysiwyg,design2_inspector,design2_workbench,promotion_pipeline
multipage_wysiwyg.SUPPORTED.add('multiwrite-home')
_original_render_canvas=multipage_wysiwyg.render_canvas
def _render_canvas(page_id='homepage',edit=False):return multiwrite_wysiwyg.render_canvas(edit=edit) if page_id=='multiwrite-home' else _original_render_canvas(page_id,edit=edit)
multipage_wysiwyg.render_canvas=_render_canvas
multipage_wysiwyg.EDITOR_HTML=multipage_wysiwyg.EDITOR_HTML.replace("'journal-vol-00'])","'journal-vol-00','multiwrite-home'])")
multipage_wysiwyg.EDITOR_HTML=multiwrite_wysiwyg.augment_editor(multipage_wysiwyg.EDITOR_HTML)
multipage_wysiwyg.EDITOR_HTML=design2_inspector.augment(multipage_wysiwyg.EDITOR_HTML)
multipage_wysiwyg.EDITOR_HTML=design2_workbench.augment(multipage_wysiwyg.EDITOR_HTML)
ROOT=Path(__file__).resolve().parent.parent;PACKAGE=journal_wysiwyg.PACKAGE;COORD=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()/'coordination'
STRUCTURE_HTML=visual.HTML.replace('<div id="top"><b>DORÉ DESIGN 1.0 · NEW WESTSIDE</b>','<div id="top"><b>DORÉ DESIGN 2.0 · STRUCTURE</b><button onclick="location.href=\'/editor\'">WYSIWYG</button><button onclick="location.href=\'/\'">Preview</button>')
PREVIEW_EDIT_ENTRY='''<style>.dore-preview-edit{position:fixed;right:18px;bottom:18px;z-index:2147483647;padding:9px 12px;border:1px solid rgba(208,189,120,.7);background:rgba(7,26,40,.88);color:#f2eee4!important;text-decoration:none!important;font:10px/1.2 ui-monospace,monospace}</style><a class="dore-preview-edit" href="/editor?page=homepage">Edit in Doré Design</a>'''
def home_preview():return multipage_wysiwyg.render_canvas('homepage',edit=False).replace('</body>',PREVIEW_EDIT_ENTRY+'</body>',1)
def safe_file(root,request_path):
    if not root.exists():return None
    rel=request_path.lstrip('/');candidate=(root/rel).resolve();base=root.resolve()
    try:candidate.relative_to(base)
    except ValueError:return None
    if candidate.is_dir():candidate=candidate/'index.html'
    return candidate if candidate.is_file() else None
def design_asset(p):return safe_file(PACKAGE,p) or safe_file(ROOT/'static',p)
def read_json(p):
    try:return json.loads(p.read_text()) if p.exists() else {}
    except:return {}
def coordination_status():
    w=read_json(COORD/'worker-state.json');d=read_json(COORD/'daemon-state.json');return{'ok':bool(w or d),'hardening':'1.0','daemon_health':d.get('status','unknown'),'queue_depth':w.get('queue_depth'),'last_status':w.get('last_task_status'),'last_error':w.get('last_error')}
class H(visual.H):
    def send_bytes(self,status,body,ctype):
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        u=urlparse(self.path);path=u.path;q=parse_qs(u.query)
        if path=='/':return self.send_bytes(200,home_preview().encode(),'text/html; charset=utf-8')
        if path=='/editor':
            active=(q.get('page') or ['homepage'])[0]
            if active not in multipage_wysiwyg.SUPPORTED:active='homepage'
            return self.send_bytes(200,multipage_wysiwyg.render_editor(active).encode(),'text/html; charset=utf-8')
        if path=='/editor-canvas':
            page_id=(q.get('page') or ['homepage'])[0]
            try:html=multipage_wysiwyg.render_canvas(page_id,edit=True)
            except(ValueError,FileNotFoundError)as e:return self.out(404,{'ok':False,'error':str(e),'page_id':page_id})
            return self.send_bytes(200,html.encode(),'text/html; charset=utf-8')
        if path=='/structure-editor':return self.send_bytes(200,STRUCTURE_HTML.encode(),'text/html; charset=utf-8')
        if path in('/journal','/journal/','/vol-00','/vol-00/'):
            try:html=multipage_wysiwyg.render_canvas('journal-vol-00',edit=False)
            except FileNotFoundError:return self.out(503,{'ok':False,'error':'editable_journal_not_imported'})
            return self.send_bytes(200,html.encode(),'text/html; charset=utf-8')
        if path=='/api/coordination/status':return self.out(200,coordination_status())
        if path=='/api/candidates':return self.out(200,promotion_pipeline.list_candidates())
        if path=='/api/multiwrite/status':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')=='multiwrite-home'),None);return self.out(200,{'ok':bool(p),'page_id':'multiwrite-home','editable':True,'design2_commands':True,'revision':w.get('revision')})
        if path=='/api/health':
            w=visual.base.workspace();m=next((p for p in w.get('pages',[]) if p.get('id')=='multiwrite-home'),None);return self.out(200,{'ok':bool(m),'service':'dore-design','version':'2.0-dev-stage2','fallback':'1.9.1','source_of_truth':'structured-workspace','workbench':True,'command_palette':True,'inline_text':True,'history_navigation':True,'multiwrite_page':'multiwrite-home','revision':w.get('revision')})
        p=design_asset(path)
        if p:return self.send_bytes(200,p.read_bytes(),mimetypes.guess_type(str(p))[0] or'application/octet-stream')
        return super().do_GET()
    def _body(self,limit=65536):
        size=int(self.headers.get('Content-Length','0'))
        if size<1 or size>limit:raise ValueError('invalid_body_size')
        return json.loads(self.rfile.read(size))
    def do_POST(self):
        path=urlparse(self.path).path
        if path=='/api/design2/command':
            try:
                payload=self._body(262144);command=payload.get('command');expected=payload.get('expected_revision')
                if not design2_workspace.is_command(command):raise ValueError('unsupported_design2_command')
                w=design2_workspace.execute(visual.base,command,expected);return self.out(200,{'ok':True,'revision':w['revision'],'workspace':w})
            except Exception as e:return self.out(409 if str(e).startswith('stale_revision:') else 400,{'ok':False,'error':str(e)})
        if path=='/api/design2/history':
            try:
                p=self._body();w=design2_workspace.navigate(visual.base,p.get('direction'),p.get('revision'));return self.out(200,{'ok':True,'revision':w['revision'],'workspace':w})
            except Exception as e:return self.out(409 if str(e).startswith('stale_revision:') else 400,{'ok':False,'error':str(e)})
        if path=='/api/candidates/judgment':
            try:
                p=self._body();return self.out(200,promotion_pipeline.record_judgment(p.get('candidate_id'),p.get('decision'),p.get('reason',''),p.get('signals')or[]))
            except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
        return super().do_POST()
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
