#!/usr/bin/env python3
"""Lightweight Doré Design template registry and instantiation layer."""
from __future__ import annotations
import copy,json
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
CANDIDATE_REGISTRY=ROOT/'dore-design'/'candidates'/'registry.json'


def _read_json(path,default):
    try:return json.loads(Path(path).read_text(encoding='utf-8'))
    except (OSError,ValueError):return default


def _candidate_rows():
    data=_read_json(CANDIDATE_REGISTRY,{'candidates':[]})
    rows=[]
    for item in data.get('candidates',[]):
        manifest=_read_json(ROOT/str(item.get('manifest') or ''),{})
        gate=manifest.get('promotion_gate') or {}
        if gate.get('ok') is not True:continue
        template=manifest.get('template') or {}
        rows.append({
            'id':item.get('id'),
            'name':item.get('name'),
            'source_page_id':template.get('page_id') or item.get('page_id'),
            'source_story_id':item.get('source_story_id'),
            'renderer':template.get('renderer'),
            'editable_bindings':template.get('editable_bindings') or [],
            'preview':f"/editor-canvas?page={template.get('page_id') or item.get('page_id')}",
            'status':'ready',
        })
    return rows


def list_templates():
    rows=_candidate_rows()
    return {'ok':True,'schema':'dore.design-template-registry.v1','templates':rows,'count':len(rows),'runtime':'structured-workspace','external_editor_dependency':False}


def _unique(base,used):
    if base not in used:return base
    i=2
    while f'{base}-{i}' in used:i+=1
    return f'{base}-{i}'


def register_runtime_pages(base,homepage_candidates,multipage_wysiwyg):
    w=base.workspace()
    for p in w.get('pages',[]):
        source=p.get('template_source_page_id')
        if source in homepage_candidates.PAGES:
            homepage_candidates.PAGES[p['id']]=homepage_candidates.PAGES[source]
            multipage_wysiwyg.SUPPORTED.add(p['id'])


def instantiate(base,homepage_candidates,multipage_wysiwyg,template_id,name=None):
    template=next((x for x in _candidate_rows() if x.get('id')==template_id),None)
    if not template:raise ValueError('template_not_found')
    w=base.workspace();source_id=template['source_page_id']
    source=next((p for p in w.get('pages',[]) if p.get('id')==source_id),None)
    if not source:raise ValueError('template_source_page_missing')
    page=copy.deepcopy(source)
    used={p.get('id') for p in w.get('pages',[])}
    page['id']=_unique(source_id+'-page',used)
    page['name']=str(name or template['name'] or source.get('name') or 'Template Page')[:80]
    page['template_id']=template_id
    page['template_source_page_id']=source_id
    page['template_detached']=True
    w['pages'].append(page)
    w=base.save(w)
    homepage_candidates.PAGES[page['id']]=homepage_candidates.PAGES[source_id]
    multipage_wysiwyg.SUPPORTED.add(page['id'])
    return {'ok':True,'schema':'dore.design-template-instance.v1','template_id':template_id,'page_id':page['id'],'name':page['name'],'revision':w.get('revision'),'editor':f"/editor?page={page['id']}",'canvas':f"/editor-canvas?page={page['id']}",'detached_copy':True}


CSS='''<style>.template-card{border:1px solid #b8b1a1;background:#fff;padding:9px;margin:0 0 7px}.template-card b{display:block;font-family:Arial,sans-serif}.template-meta{color:#777;font-size:9px;margin:4px 0 7px}.template-actions{display:grid;grid-template-columns:1fr 1fr;gap:5px}.template-actions button{padding:6px;border:1px solid #777;background:#242424;color:#fff;cursor:pointer;font:10px ui-monospace,monospace}.template-actions button:first-child{background:#fff;color:#222}</style>'''
PANEL='''<h3>TEMPLATES</h3><div id="templates"><div class="hint">loading templates…</div></div>'''
JS=r'''<script>(()=>{const box=document.getElementById('templates');if(!box)return;async function loadTemplates(){const j=await fetch('/api/templates',{cache:'no-store'}).then(r=>r.json());box.innerHTML='';for(const t of j.templates||[]){const c=document.createElement('div');c.className='template-card';c.innerHTML='<b>'+t.name+'</b><div class="template-meta">'+t.id+' · '+t.editable_bindings.length+' bindings</div><div class="template-actions"><button>Preview</button><button>Use template</button></div>';const [preview,use]=c.querySelectorAll('button');preview.onclick=()=>{active=t.source_page_id;supported.add(active);history.replaceState(null,'','/editor?page='+encodeURIComponent(active));load()};use.onclick=async()=>{use.disabled=true;const r=await fetch('/api/templates/instantiate',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({template_id:t.id})});const x=await r.json();if(!r.ok){use.disabled=false;document.getElementById('status').textContent='TEMPLATE FAILED · '+(x.error||r.status);return}supported.add(x.page_id);active=x.page_id;history.replaceState(null,'','/editor?page='+encodeURIComponent(active));await load();document.getElementById('status').textContent='TEMPLATE CREATED · '+x.page_id};box.appendChild(c)}}loadTemplates()})()</script>'''


def install_editor(html):
    html=html.replace('</head>',CSS+'</head>',1)
    html=html.replace('<aside class="side"><h3>', '<aside class="side">'+PANEL+'<h3>',1)
    return html.replace('</body>',JS+'</body>',1)
