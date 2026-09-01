#!/usr/bin/env python3
"""Exact #262 front-door renderer backed by the Doré structured workspace.

The original responsive HTML remains the layout template. Both preview and editor
use this same DOM/CSS; editor mode only adds contenteditable bindings and chrome.
"""
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
TEMPLATE=ROOT/'dore-design/new-westside/homepage-v2-living-fortress.html'

BINDINGS=[
    ('<div class="hero-kicker micro">Westside Watch / 西望</div>', '<div class="hero-kicker micro dore-bound" data-node-id="watch-kicker" data-field="text">Westside Watch / 西望</div>'),
    ('<h1>WATCH<br>FOR THE <em>DAWN.</em></h1>', '<h1 class="dore-bound" data-node-id="home-title" data-field="text">WATCH<br>FOR THE <em>DAWN.</em></h1>'),
    ('<p>在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。</p>', '<p class="dore-bound" data-node-id="home-deck" data-field="text">在黑夜仍然守望，在清晨尚未來到以前保存光。文章、聖經、教會生活與研究，在同一座城中彼此照亮。</p>'),
    ('<div class="verse micro">The night is far spent,<br>the day is at hand.<br>Romans 13:12</div>', '<div class="verse micro dore-bound" data-node-id="verse" data-field="text">The night is far spent,<br>the day is at hand.<br>Romans 13:12</div>'),
    ('<strong>一個入口，四條路。</strong>', '<strong class="dore-bound" data-node-id="threshold-title" data-field="text">一個入口，四條路。</strong>'),
    ('<span class="micro">Read · Study · Gather · Remember</span>', '<span class="micro dore-bound" data-node-id="threshold-meta" data-field="text">Read · Study · Gather · Remember</span>'),
    ('<span class="eyebrow micro">Journal · Current volume</span>', '<span class="eyebrow micro dore-bound" data-node-id="journal-tower" data-field="eyebrow">Journal · Current volume</span>'),
    ('<h2>守望，<br>一座光明的城</h2>', '<h2 class="dore-bound" data-node-id="journal-tower" data-field="title">守望，<br>一座光明的城</h2>'),
    ('<p>進入本期 Journal。圖像、文字、見證與禱告在一個獨立的閱讀世界中展開。</p>', '<p class="dore-bound" data-node-id="journal-tower" data-field="body">進入本期 Journal。圖像、文字、見證與禱告在一個獨立的閱讀世界中展開。</p>'),
    ('<span class="eyebrow micro">ONE · Bible study</span>', '<span class="eyebrow micro dore-bound" data-node-id="one-territory" data-field="eyebrow">ONE · Bible study</span>'),
    ('<h2>路上，祂向我們打開聖經。</h2>', '<h2 class="dore-bound" data-node-id="one-territory" data-field="title">路上，祂向我們打開聖經。</h2>'),
    ('<p>從一章、一卷書、一條路線開始，把經文、歷史、地圖與串珠重新連起來。</p>', '<p class="dore-bound" data-node-id="one-territory" data-field="body">從一章、一卷書、一條路線開始，把經文、歷史、地圖與串珠重新連起來。</p>'),
    ('<span class="eyebrow micro">Living Water West</span>', '<span class="eyebrow micro dore-bound" data-node-id="church-territory" data-field="eyebrow">Living Water West</span>'),
    ('<h2>一座城，<br>也是一個家。</h2>', '<h2 class="dore-bound" data-node-id="church-territory" data-field="title">一座城，<br>也是一個家。</h2>'),
    ('<p>Sunday Worship · Bible Study · Prayer · Life Together</p>', '<p class="dore-bound" data-node-id="church-territory" data-field="body">Sunday Worship · Bible Study · Prayer · Life Together</p>'),
    ('<span class="eyebrow micro">Dawn Library · 黎明書局</span>', '<span class="eyebrow micro dore-bound" data-node-id="library-territory" data-field="eyebrow">Dawn Library · 黎明書局</span>'),
    ('<h2>被保存的光。</h2>', '<h2 class="dore-bound" data-node-id="library-territory" data-field="title">被保存的光。</h2>'),
    ('<p>地圖、文章、史料與研究資源逐步沉澱，成為可以再次被調用的知識。</p>', '<p class="dore-bound" data-node-id="library-territory" data-field="body">地圖、文章、史料與研究資源逐步沉澱，成為可以再次被調用的知識。</p>'),
    ('<span class="eyebrow micro">The Gate</span>', '<span class="eyebrow micro dore-bound" data-node-id="join-territory" data-field="eyebrow">The Gate</span>'),
    ('<h2>Come<br>and see.</h2>', '<h2 class="dore-bound" data-node-id="join-territory" data-field="title">Come<br>and see.</h2>'),
    ('<h3>從閱讀走向相遇。</h3>', '<h3 class="dore-bound" data-node-id="gate-copy-left" data-field="text">從閱讀走向相遇。</h3>'),
    ('<h3>從守望走向黎明。</h3>', '<h3 class="dore-bound" data-node-id="gate-copy-right" data-field="text">從守望走向黎明。</h3>'),
    ('<div class="number">12</div>', '<div class="number dore-bound" data-node-id="watch-number" data-field="text">12</div>'),
    ('黑夜已深，<br>白晝將近。', '<span class="dore-bound" data-node-id="watch-quote" data-field="text">黑夜已深，<br>白晝將近。</span>'),
    ('<cite class="micro">Romans 13:12 · Watch for the Dawn</cite>', '<cite class="micro dore-bound" data-node-id="watch-cite" data-field="text">Romans 13:12 · Watch for the Dawn</cite>'),
]

SHARED_CSS=r'''
.dore-bound{white-space:pre-line}
'''

EDITOR_CSS=r'''
body[data-dore-editor="true"]{padding-top:44px}
.dore-editbar{position:fixed;left:0;right:0;top:0;height:44px;z-index:10000;background:#171717;color:#f2eee4;display:flex;align-items:center;gap:8px;padding:0 12px;font:11px ui-monospace,SFMono-Regular,Menlo,monospace;box-shadow:0 1px 0 #000}
.dore-editbar strong{letter-spacing:.08em}.dore-editbar a,.dore-editbar button{color:#f2eee4;background:#303030;border:1px solid #555;padding:6px 9px;text-decoration:none;font:inherit;cursor:pointer}.dore-editbar .state{margin-left:auto;color:#d0bd78}
body[data-dore-editor="true"] .dore-bound{cursor:text;outline:1px dashed transparent;outline-offset:4px}
body[data-dore-editor="true"] .dore-bound:hover{outline-color:rgba(179,154,71,.7)}
body[data-dore-editor="true"] .dore-bound:focus{outline:2px solid #d0bd78;background:rgba(208,189,120,.08)}
'''

CLIENT_JS=r'''
<script>
(()=>{
 const edit=document.body.dataset.doreEditor==='true';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 let workspace=null,home=null;
 function node(id){return home?.nodes?.find(n=>n.id===id)}
 function paint(el,value,id){
   value=String(value??'');
   if(id==='home-title'){
     const lines=value.split(/\n+/).filter(Boolean);
     el.innerHTML=lines.map((x,i)=>i===lines.length-1?'<em>'+esc(x)+'</em>':esc(x)).join('<br>');
   }else{
     el.textContent=value;
   }
 }
 async function load(){
   const r=await fetch('/api/workspace',{cache:'no-store'}); workspace=await r.json();
   home=workspace.pages.find(p=>p.id==='homepage')||workspace.pages[0];
   document.querySelectorAll('[data-node-id]').forEach(el=>{
     const n=node(el.dataset.nodeId),field=el.dataset.field||'text';
     if(n && n[field]!==undefined)paint(el,n[field],n.id);
     if(edit){el.contentEditable='true';el.spellcheck=false;}
   });
   const st=document.getElementById('dore-state');if(st)st.textContent='workspace r'+workspace.revision+' · exact #262 layout';
 }
 async function save(el){
   const id=el.dataset.nodeId,field=el.dataset.field||'text';
   let value=el.innerText.replace(/\n{3,}/g,'\n\n').trim();
   const r=await fetch('/api/workspace',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({op:'set_node',page_id:'homepage',id,patch:{[field]:value}})});
   if(!r.ok){document.getElementById('dore-state').textContent='SAVE FAILED';return}
   workspace=await r.json();home=workspace.pages.find(p=>p.id==='homepage')||workspace.pages[0];paint(el,value,id);
   document.getElementById('dore-state').textContent='saved · r'+workspace.revision;
 }
 if(edit){
   document.addEventListener('blur',e=>{const el=e.target.closest?.('[data-node-id]');if(el)save(el)},true);
   document.addEventListener('click',e=>{if(e.target.closest('.portal,.gate-mark') && !e.target.closest('.dore-editbar'))e.preventDefault()},true);
 }
 load().catch(e=>{const st=document.getElementById('dore-state');if(st)st.textContent='workspace load failed';console.error(e)});
})();
</script>
'''


def render(edit=False):
    html=TEMPLATE.read_text(encoding='utf-8')
    html=html.replace('/images/westside-watch-masthead-landscape.svg','/asset/masthead.svg')
    html=html.replace('/images/westside-watch-morning-star.svg','/asset/morning-star.svg')
    for old,new in BINDINGS:
        html=html.replace(old,new)
    html=html.replace('</style>',SHARED_CSS+(EDITOR_CSS if edit else '')+'</style>',1)
    if edit:
        html=html.replace('<body>','<body data-dore-editor="true">',1)
        bar='<div class="dore-editbar"><strong>DORÉ DESIGN 1.5 · WYSIWYG</strong><a href="/">Preview</a><a href="/structure-editor">Structure</a><a href="/journal/">Journal Mirror</a><span id="dore-state" class="state">loading workspace…</span></div>'
        html=html.replace('<main class="shell"',bar+'<main class="shell"',1)
    html=html.replace('</body>',CLIENT_JS+'</body>',1)
    return html
