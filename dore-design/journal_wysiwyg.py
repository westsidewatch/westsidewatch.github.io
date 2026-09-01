#!/usr/bin/env python3
"""Editable Journal / Vol.00 renderer backed by Doré workspace nodes."""
from pathlib import Path
import os
DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')).expanduser()
PACKAGE=DATA/'imports/journal-vol-00'
TEMPLATE=PACKAGE/'index.html'
PAGE_ID='journal-vol-00'

CSS='''<style id="dore-journal-editor-style">.dore-journal-bound{white-space:pre-wrap}body[data-dore-canvas="true"] .dore-journal-bound{cursor:text;outline:1px dashed transparent;outline-offset:2px}body[data-dore-canvas="true"] .dore-journal-bound:hover{outline-color:rgba(179,154,71,.72)}body[data-dore-canvas="true"] .dore-journal-bound:focus{outline:2px solid #d0bd78;background:rgba(208,189,120,.10)}.dore-journal-design-nav{position:fixed;right:18px;bottom:18px;z-index:2147483647;display:flex;gap:7px}.dore-journal-design-nav a{padding:9px 12px;border:1px solid rgba(208,189,120,.7);background:rgba(7,26,40,.9);color:#f2eee4!important;text-decoration:none!important;font:10px/1.2 ui-monospace,SFMono-Regular,Menlo,monospace;letter-spacing:.12em;text-transform:uppercase;backdrop-filter:blur(4px)}</style>'''
NAV='''<nav class="dore-journal-design-nav" aria-label="Doré Design journal navigation"><a href="/">Front Door</a><a href="/editor?page=journal-vol-00">Edit in Doré Design</a></nav>'''
JS=r'''<script id="dore-journal-editor-script">(()=>{const PAGE='journal-vol-00',edit=document.body.dataset.doreCanvas==='true';let w=null,p=null;const node=id=>p?.nodes?.find(n=>n.id===id);async function load(){w=await(await fetch('/api/workspace',{cache:'no-store'})).json();p=w.pages.find(x=>x.id===PAGE);if(!p)throw Error('journal_page_missing');document.querySelectorAll('.dore-journal-bound[data-node-id]').forEach(el=>{const n=node(el.dataset.nodeId);if(n&&n.text!==undefined)el.textContent=n.text;if(edit){el.contentEditable='true';el.spellcheck=false;el.addEventListener('focus',()=>parent.postMessage({type:'dore-select',page_id:PAGE,id:el.dataset.nodeId,field:'text',value:el.innerText},'*'))}});parent.postMessage({type:'dore-ready',page_id:PAGE,revision:w.revision},'*')}async function save(el){const id=el.dataset.nodeId,v=el.innerText;const r=await fetch('/api/workspace',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({op:'set_node',page_id:PAGE,id,patch:{text:v}})});if(!r.ok){parent.postMessage({type:'dore-error',page_id:PAGE},'*');return}w=await r.json();p=w.pages.find(x=>x.id===PAGE);parent.postMessage({type:'dore-saved',page_id:PAGE,revision:w.revision,id,field:'text',value:v},'*')}if(edit){document.addEventListener('blur',e=>{const el=e.target.closest?.('.dore-journal-bound[data-node-id]');if(el)save(el)},true);document.addEventListener('click',e=>{if(e.target.closest('a'))e.preventDefault()},true)}load().catch(err=>{console.error(err);parent.postMessage({type:'dore-error',page_id:PAGE,error:String(err)},'*')})})();</script>'''

def available():return TEMPLATE.exists()

def render_canvas(edit=False):
    if not TEMPLATE.exists():raise FileNotFoundError('editable_journal_not_imported')
    html=TEMPLATE.read_text(encoding='utf-8')
    body='<body data-dore-canvas="true" data-dore-page="journal-vol-00">' if edit else '<body data-dore-page="journal-vol-00">'
    html=html.replace('<body>',body,1)
    html=html.replace('</head>',CSS+'</head>',1)
    if not edit:html=html.replace('</body>',NAV+'</body>',1)
    return html.replace('</body>',JS+'</body>',1)
