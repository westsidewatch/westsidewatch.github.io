#!/usr/bin/env python3
"""Doré Design resident product: structured workspace + Design 2.0 UI."""
import json,mimetypes,os
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
import app_visual as visual
import multiwrite_integration
multiwrite_integration.install_workspace(visual.base)
import multipage_wysiwyg,journal_wysiwyg
import multiwrite_wysiwyg
import promotion_pipeline
import design2_ui
multipage_wysiwyg.SUPPORTED.add('multiwrite-home')
_original_render_canvas=multipage_wysiwyg.render_canvas
def _render_canvas(page_id='homepage',edit=False):
    if page_id=='multiwrite-home':return multiwrite_wysiwyg.render_canvas(edit=edit)
    return _original_render_canvas(page_id,edit=edit)
multipage_wysiwyg.render_canvas=_render_canvas
multipage_wysiwyg.EDITOR_HTML=multipage_wysiwyg.EDITOR_HTML.replace("'journal-vol-00'])","'journal-vol-00','multiwrite-home'])")
multipage_wysiwyg.EDITOR_HTML=multiwrite_wysiwyg.augment_editor(multipage_wysiwyg.EDITOR_HTML)
multipage_wysiwyg.EDITOR_HTML=design2_ui.install(multipage_wysiwyg.EDITOR_HTML)
ROOT=Path(__file__).resolve().parent.parent
PACKAGE=journal_wysiwyg.PACKAGE
COORD=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()/'coordination'
STRUCTURE_HTML=visual.HTML
PREVIEW_EDIT_ENTRY='''<style>.dore-preview-edit{position:fixed;right:18px;bottom:18px;z-index:2147483647;padding:9px 12px;background:#171814dd;color:#eee!important;text-decoration:none!important;font:10px ui-monospace,monospace}</style><a class="dore-preview-edit" href="/editor?page=homepage">Edit in Doré Design</a>'''
def home_preview():return multipage_wysiwyg.render_canvas('homepage',edit=False).replace('</body>',PREVIEW_EDIT_ENTRY+'</body>',1)
def safe_file(root,request_path):
    if not root.exists():return None
    rel=request_path.lstrip('/');candidate=(root/rel).resolve();base=root.resolve()
    try:candidate.relative_to(base)
    except ValueError:return None
    if candidate.is_dir():candidate=candidate/'index.html'
    return candidate if candidate.is_file() else None
def design_asset(request_path):return safe_file(PACKAGE,request_path) or safe_file(ROOT/'static',request_path)
def read_json(path):
    try:return json.loads(path.read_text()) if path.exists() else {}
    except:return {}
def coordination_status():
    worker=read_json(COORD/'worker-state.json');daemon=read_json(COORD/'daemon-state.json');last_id=worker.get('last_task_id');task=(worker.get('tasks') or {}).get(last_id,{}) if last_id else {}
    return {'ok':bool(worker or daemon),'hardening':'1.0','daemon_health':daemon.get('status','unknown'),'last_received':last_id,'last_status':worker.get('last_task_status') or task.get('status'),'last_result':worker.get('last_result'),'last_error':worker.get('last_error')}
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
            except (ValueError,FileNotFoundError) as e:return self.out(404,{'ok':False,'error':str(e),'page_id':page_id})
            return self.send_bytes(200,html.encode(),'text/html; charset=utf-8')
        if path=='/structure-editor':return self.send_bytes(200,STRUCTURE_HTML.encode(),'text/html; charset=utf-8')
        if path in ('/journal','/journal/','/vol-00','/vol-00/'):
            try:html=multipage_wysiwyg.render_canvas('journal-vol-00',edit=False)
            except FileNotFoundError:return self.out(503,{'ok':False,'error':'editable_journal_not_imported'})
            return self.send_bytes(200,html.encode(),'text/html; charset=utf-8')
        if path=='/api/coordination/status':return self.out(200,coordination_status())
        if path=='/api/candidates':return self.out(200,promotion_pipeline.list_candidates())
        if path=='/api/multiwrite/status':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')=='multiwrite-home'),None);return self.out(200,{'ok':bool(p),'page_id':'multiwrite-home','editable':True,'semantic_design':bool(p and p.get('design')),'design':p.get('design') if p else None,'editor':'/editor?page=multiwrite-home','canvas':'/editor-canvas?page=multiwrite-home','revision':w.get('revision')})
        if path=='/api/health':
            w=visual.base.workspace();multiwrite=next((p for p in w.get('pages',[]) if p.get('id')=='multiwrite-home'),None);return self.out(200,{'ok':bool(multiwrite),'service':'dore-design','version':'2.0-ui-rebuild','workspace_id':w.get('id'),'revision':w.get('revision'),'source_of_truth':'structured-workspace','ui':'design2','editor':'/editor','multiwrite_editor':'/editor?page=multiwrite-home'})
        p=design_asset(path)
        if p:return self.send_bytes(200,p.read_bytes(),mimetypes.guess_type(str(p))[0] or 'application/octet-stream')
        return super().do_GET()
    def do_POST(self):
        if urlparse(self.path).path=='/api/candidates/judgment':
            try:
                size=int(self.headers.get('Content-Length','0'));payload=json.loads(self.rfile.read(size) or b'{}');result=promotion_pipeline.record_judgment(payload.get('candidate_id'),payload.get('decision'),payload.get('reason',''),payload.get('signals') or []);return self.out(200,result)
            except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
        return super().do_POST()
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
