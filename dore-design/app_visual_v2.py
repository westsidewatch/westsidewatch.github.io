#!/usr/bin/env python3
"""Doré Design 2.0 production resident product."""
import json,mimetypes,os
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
import app_visual as visual
# Runtime/product pages are migrations, not read-time workspace behavior. Keep the
# canonical pure reader so one explicit mutation remains exactly one revision.
_pure_workspace=visual.base.workspace
import multiwrite_integration;multiwrite_integration.install_workspace(visual.base)
import motion_prototypes;motion_prototypes.install_workspace(visual.base)
import living_water_candidate;living_water_candidate.install_workspace(visual.base)
import living_water_candidate_02;living_water_candidate_02.install_workspace(visual.base)
import living_water_candidate_03;living_water_candidate_03.install_workspace(visual.base)
import living_water_candidate_04;living_water_candidate_04.install_workspace(visual.base)
import living_water_second_layer_lab;living_water_second_layer_lab.install_workspace(visual.base)
import living_water_third_alive_lab;living_water_third_alive_lab.install_workspace(visual.base)
import design2_layer_ops;design2_layer_ops.install(visual.base)
import design2_multiwrite_cover;design2_multiwrite_cover.ensure(visual.base)
# The ensure() call above traverses every registered wrapper once and persists
# all missing runtime pages. From here onward GET/workspace is side-effect free.
visual.base.workspace=_pure_workspace
import design2_cover_render,design2_cover_interaction,design2_cover_manifest,design2_cover_acceptance,design2_closeout_acceptance
import multipage_wysiwyg,journal_wysiwyg,multiwrite_wysiwyg,promotion_pipeline,homepage_candidates,template_library
import design2_ui,design2_snap_guides,design2_layers_ui,design2_canvas_state,design2_arrange_ui,design2_cover_asset_ui,design2_typography_ui
multipage_wysiwyg.SUPPORTED.update({'multiwrite-home','multiwrite-cover',motion_prototypes.PAGE_ID,living_water_candidate.PAGE_ID,living_water_candidate_02.PAGE_ID,living_water_candidate_03.PAGE_ID,living_water_candidate_04.PAGE_ID,living_water_second_layer_lab.PAGE_ID,living_water_third_alive_lab.PAGE_ID});template_library.register_runtime_pages(visual.base,homepage_candidates,multipage_wysiwyg);_original_render_canvas=multipage_wysiwyg.render_canvas
def _render_canvas(page_id='homepage',edit=False):
    if page_id=='multiwrite-home':
        html=multiwrite_wysiwyg.render_canvas(edit=edit)
        if edit:html=design2_snap_guides.augment(html);html=design2_canvas_state.augment(html)
        return html
    if page_id=='multiwrite-cover':
        html=design2_cover_render.render(visual.base,page_id,edit=edit)
        return design2_cover_interaction.augment(html) if edit else html
    if page_id==motion_prototypes.PAGE_ID:return motion_prototypes.render_p1(edit=edit)
    if page_id==living_water_candidate.PAGE_ID:return living_water_candidate.render(edit=edit)
    if page_id==living_water_candidate_02.PAGE_ID:return living_water_candidate_02.render(edit=edit)
    if page_id==living_water_candidate_03.PAGE_ID:return living_water_candidate_03.render(edit=edit)
    if page_id==living_water_candidate_04.PAGE_ID:return living_water_candidate_04.render(edit=edit)
    if page_id==living_water_second_layer_lab.PAGE_ID:return living_water_second_layer_lab.render(edit=edit)
    if page_id==living_water_third_alive_lab.PAGE_ID:return living_water_third_alive_lab.render(edit=edit)
    return _original_render_canvas(page_id,edit=edit)
multipage_wysiwyg.render_canvas=_render_canvas
multipage_wysiwyg.EDITOR_HTML=multipage_wysiwyg.EDITOR_HTML.replace("'journal-vol-00'])","'journal-vol-00','multiwrite-home','multiwrite-cover'])")
for installer in (multiwrite_wysiwyg.augment_editor,design2_ui.install,design2_layers_ui.install,design2_arrange_ui.install,design2_cover_asset_ui.install,design2_typography_ui.install,template_library.install_editor,motion_prototypes.install_editor,living_water_candidate.install_editor,living_water_candidate_02.install_editor,living_water_candidate_03.install_editor,living_water_candidate_04.install_editor,living_water_second_layer_lab.install_editor,living_water_third_alive_lab.install_editor):multipage_wysiwyg.EDITOR_HTML=installer(multipage_wysiwyg.EDITOR_HTML)
ROOT=Path(__file__).resolve().parent.parent;PACKAGE=journal_wysiwyg.PACKAGE;COORD=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()/'coordination';STRUCTURE_HTML=visual.HTML
PREVIEW_EDIT_ENTRY='''<style>.dore-preview-edit{position:fixed;right:18px;bottom:18px;z-index:2147483647;padding:9px 12px;background:#171814dd;color:#eee!important;text-decoration:none!important;font:10px ui-monospace,monospace;letter-spacing:.12em}</style><a class="dore-preview-edit" href="/editor?page=homepage">Edit in Doré Design</a>'''
def home_preview():return multipage_wysiwyg.render_canvas('homepage',edit=False).replace('</body>',PREVIEW_EDIT_ENTRY+'</body>',1)
def safe_file(root,request_path):
    if not root.exists():return None
    candidate=(root/request_path.lstrip('/')).resolve();base=root.resolve()
    try:candidate.relative_to(base)
    except ValueError:return None
    if candidate.is_dir():candidate=candidate/'index.html'
    return candidate if candidate.is_file() else None
def design_asset(p):return safe_file(PACKAGE,p) or safe_file(ROOT/'static',p)
def read_json(path):
    try:return json.loads(path.read_text()) if path.exists() else {}
    except:return {}
def coordination_status():
    worker=read_json(COORD/'worker-state.json');daemon=read_json(COORD/'daemon-state.json');last_id=worker.get('last_task_id');task=(worker.get('tasks') or {}).get(last_id,{}) if last_id else {}
    return {'ok':bool(worker or daemon),'hardening':'1.0','daemon_health':daemon.get('status','unknown'),'last_received':last_id,'last_status':worker.get('last_task_status') or task.get('status'),'last_result':worker.get('last_result'),'last_error':worker.get('last_error')}
class H(visual.H):
    def send_bytes(self,status,body,ctype):self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        u=urlparse(self.path);path=u.path;q=parse_qs(u.query)
        if path=='/':return self.send_bytes(200,home_preview().encode(),'text/html; charset=utf-8')
        if path=='/editor':
            template_library.register_runtime_pages(visual.base,homepage_candidates,multipage_wysiwyg)
            active=(q.get('page') or ['homepage'])[0];active=active if active in multipage_wysiwyg.SUPPORTED else 'homepage';return self.send_bytes(200,multipage_wysiwyg.render_editor(active).encode(),'text/html; charset=utf-8')
        if path=='/editor-canvas':
            template_library.register_runtime_pages(visual.base,homepage_candidates,multipage_wysiwyg);page_id=(q.get('page') or ['homepage'])[0]
            try:return self.send_bytes(200,multipage_wysiwyg.render_canvas(page_id,edit=True).encode(),'text/html; charset=utf-8')
            except (ValueError,FileNotFoundError) as e:return self.out(404,{'ok':False,'error':str(e),'page_id':page_id})
        if path=='/structure-editor':return self.send_bytes(200,STRUCTURE_HTML.encode(),'text/html; charset=utf-8')
        if path in ('/journal','/journal/','/vol-00','/vol-00/'):
            try:return self.send_bytes(200,multipage_wysiwyg.render_canvas('journal-vol-00',edit=False).encode(),'text/html; charset=utf-8')
            except FileNotFoundError:return self.out(503,{'ok':False,'error':'editable_journal_not_imported'})
        if path=='/api/coordination/status':return self.out(200,coordination_status())
        if path=='/api/candidates':return self.out(200,promotion_pipeline.list_candidates())
        if path=='/api/templates':return self.out(200,template_library.list_templates())
        if path=='/api/design2/multiwrite-cover':return self.out(200,design2_cover_manifest.status(visual.base))
        if path=='/api/design2/multiwrite-cover/acceptance':return self.out(200,design2_cover_acceptance.check(visual.base))
        if path=='/api/design2/closeout':return self.out(200,design2_closeout_acceptance.check(visual.base))
        if path=='/api/multiwrite/status':
            w=visual.base.workspace();home=next((x for x in w.get('pages',[]) if x.get('id')=='multiwrite-home'),None);cover=next((x for x in w.get('pages',[]) if x.get('id')=='multiwrite-cover'),None);return self.out(200,{'ok':bool(home and cover),'page_id':'multiwrite-home','cover_page_id':'multiwrite-cover','editable':True,'editor':'/editor?page=multiwrite-home','cover_editor':'/editor?page=multiwrite-cover','revision':w.get('revision')})
        if path=='/api/motion/prototypes':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==motion_prototypes.PAGE_ID),None);return self.out(200,{'ok':bool(p),'count':1 if p else 0,'page_id':motion_prototypes.PAGE_ID,'editor':'/editor?page='+motion_prototypes.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/design-candidates/living-water-01':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_candidate.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_candidate.PAGE_ID,'editor':'/editor?page='+living_water_candidate.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/design-candidates/living-water-02':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_candidate_02.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_candidate_02.PAGE_ID,'editor':'/editor?page='+living_water_candidate_02.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/design-candidates/living-water-03':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_candidate_03.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_candidate_03.PAGE_ID,'editor':'/editor?page='+living_water_candidate_03.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/design-candidates/living-water-04':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_candidate_04.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_candidate_04.PAGE_ID,'editor':'/editor?page='+living_water_candidate_04.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/motion/second-layer':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_second_layer_lab.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_second_layer_lab.PAGE_ID,'editor':'/editor?page='+living_water_second_layer_lab.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/motion/third-alive':
            w=visual.base.workspace();p=next((x for x in w.get('pages',[]) if x.get('id')==living_water_third_alive_lab.PAGE_ID),None);return self.out(200,{'ok':bool(p),'page_id':living_water_third_alive_lab.PAGE_ID,'editor':'/editor?page='+living_water_third_alive_lab.PAGE_ID,'experiment':(p or {}).get('design_experiment')})
        if path=='/api/health':
            w=visual.base.workspace();close=design2_closeout_acceptance.check(visual.base);templates=template_library.list_templates();return self.out(200,{'ok':close['ok'],'service':'dore-design','version':'2.0-production','workspace_id':w.get('id'),'revision':w.get('revision'),'source_of_truth':'structured-workspace','ui':'design2','interaction':'direct-manipulation+resize+snap+guides+multiselect','layers':'atomic-zorder+visibility+lock','inspector':'geometry+arrange+cover-image+typography','arrange':'align+distribute+spacing+atomic-zorder+group','assets':'frame+local-image+cover-art+8mb-guard','typography':'family+size+weight+color+leading+tracking+align','multiwrite_cover':'editable-direct-manipulation+resize+image-tools+type-tools','motion_lab':{'count':3,'p1':motion_prototypes.PAGE_ID,'second_layer':living_water_second_layer_lab.PAGE_ID,'third_alive':living_water_third_alive_lab.PAGE_ID},'design_candidates':{'living_water_01':living_water_candidate.PAGE_ID,'living_water_02':living_water_candidate_02.PAGE_ID,'living_water_03':living_water_candidate_03.PAGE_ID,'living_water_04':living_water_candidate_04.PAGE_ID},'templates':{'count':templates['count'],'registry':templates['schema'],'instantiate':'detached-structured-workspace-copy','external_editor_dependency':False},'batch':'atomic-batch-set+atomic-zorder','closeout':close,'editor':'/editor','multiwrite_editor':'/editor?page=multiwrite-home','multiwrite_cover_editor':'/editor?page=multiwrite-cover','motion_p1_editor':'/editor?page='+motion_prototypes.PAGE_ID,'living_water_01_editor':'/editor?page='+living_water_candidate.PAGE_ID,'living_water_02_editor':'/editor?page='+living_water_candidate_02.PAGE_ID,'living_water_03_editor':'/editor?page='+living_water_candidate_03.PAGE_ID,'living_water_04_editor':'/editor?page='+living_water_candidate_04.PAGE_ID,'second_layer_editor':'/editor?page='+living_water_second_layer_lab.PAGE_ID,'third_alive_editor':'/editor?page='+living_water_third_alive_lab.PAGE_ID})
        p=design_asset(path)
        if p:return self.send_bytes(200,p.read_bytes(),mimetypes.guess_type(str(p))[0] or 'application/octet-stream')
        return super().do_GET()
    def do_POST(self):
        path=urlparse(self.path).path
        if path=='/api/templates/instantiate':
            try:size=int(self.headers.get('Content-Length','0'));payload=json.loads(self.rfile.read(size) or b'{}');return self.out(200,template_library.instantiate(visual.base,homepage_candidates,multipage_wysiwyg,payload.get('template_id'),payload.get('name')))
            except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
        if path=='/api/candidates/judgment':
            try:size=int(self.headers.get('Content-Length','0'));payload=json.loads(self.rfile.read(size) or b'{}');return self.out(200,promotion_pipeline.record_judgment(payload.get('candidate_id'),payload.get('decision'),payload.get('reason',''),payload.get('signals') or []))
            except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
        return super().do_POST()
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
