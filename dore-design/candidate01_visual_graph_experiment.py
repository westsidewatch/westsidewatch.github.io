"""Candidate 01 — 4W Living Editorial River experiment (#643)."""
from __future__ import annotations
import html as html_lib, json
import design_motion_registry as motion
import codrops_site_8x5
import visual_editorial_director as ved
import sitewide_editorial_candidates as sitewide

EDITORIAL_DIRECTOR={**ved.contract(),"source_issue":643}
SITEWIDE=sitewide.load()
_POOL=SITEWIDE.candidates


def _rows():
    selected=ved.select(_POOL,per_w=4)
    rows={}
    for w,pairs in selected.items():
        rows[w]=[]
        for c,d in pairs:
            rows[w].append({
                "id":c.id,"title":c.title,"source":c.source,"deck":c.deck,
                "image":c.image,"world":c.world,"weight":d.weight,"shape":d.shape,
                "affinity":d.affinity,"brightness":d.brightness,
                "editorial_score":d.editorial_score,"editorial_reason":d.reason,
                "provenance":SITEWIDE.provenance.get(c.id,{}),
            })
    return rows

ROWS=_rows()

STYLE=r'''<style id="candidate-01-living-editorial-river">
.living-current-band{gap:clamp(12px,1.45vw,28px)!important;align-items:center!important}.living-current-band .product{position:relative;overflow:hidden;transition:flex-grow .65s cubic-bezier(.2,.75,.2,1),transform .65s cubic-bezier(.2,.75,.2,1),opacity .4s ease,filter .4s ease;flex-basis:0!important}.living-current-band .product[data-editorial-weight="1"]{flex-grow:1!important}.living-current-band .product[data-editorial-weight="2"]{flex-grow:1.65!important}.living-current-band .product[data-editorial-weight="3"]{flex-grow:2.35!important}.living-current-band .product[data-editorial-shape="portrait"]{aspect-ratio:5/8!important;max-width:19vw}.living-current-band:has(.product.is-contemplated) .product:not(.is-contemplated){opacity:.38;filter:saturate(.65)}.living-current-band .product.is-contemplated{flex-grow:3.4!important;z-index:8;transform:scale(1.025)}.lw-editorial-tag{position:absolute;z-index:9;left:.7rem;top:.65rem;padding:.25rem .42rem;background:rgba(8,16,20,.72);color:#CEBD74;font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;pointer-events:none}.lw-inline-reader{position:absolute;z-index:10;inset:0;display:grid;grid-template-columns:minmax(38%,.72fr) minmax(0,1.28fr);background:rgba(8,16,20,.94);color:#f7f1df;opacity:0;pointer-events:none;transition:opacity .28s ease;overflow:hidden}.product.is-reading .lw-inline-reader{opacity:1;pointer-events:auto}.lw-reader-image{background-size:cover;background-position:center}.product[data-editorial-has-visual="false"] .lw-inline-reader{grid-template-columns:1fr}.product[data-editorial-has-visual="false"] .lw-reader-image{display:none}.lw-reader-flow{display:flex;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;scrollbar-width:none}.lw-reader-flow::-webkit-scrollbar{display:none}.lw-reader-panel{flex:0 0 min(76%,420px);padding:clamp(16px,2vw,34px);display:flex;flex-direction:column;justify-content:flex-end;border-left:1px solid rgba(206,189,116,.25);scroll-snap-align:start}.lw-reader-panel .eyebrow{color:#CEBD74;font:600 9px/1.3 ui-monospace,monospace;letter-spacing:.14em}.lw-reader-panel h3{font:400 clamp(25px,2.6vw,46px)/.9 "Cormorant Garamond","Noto Serif TC",serif;margin:.45rem 0}.lw-reader-panel p{font:400 clamp(12px,.95vw,16px)/1.55 "Noto Serif TC",serif;margin:0}.lw-reader-panel.next{justify-content:center;color:#CEBD74}.lw-reader-panel.next:after{content:'CLICK → ENTER WORLD';font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;margin-top:1rem}@media(max-width:900px){.living-current-band .product[data-editorial-shape="portrait"]{max-width:none;aspect-ratio:8/5!important}.lw-inline-reader{grid-template-columns:1fr}.lw-reader-image{display:none}.lw-reader-panel{flex-basis:86%}}@media(prefers-reduced-motion:reduce){.living-current-band .product,.lw-inline-reader{transition:none!important}}
</style>'''


def script(row_names):
    data=json.dumps({n:ROWS[n] for n in row_names},ensure_ascii=False);director=json.dumps(EDITORIAL_DIRECTOR,ensure_ascii=False);names=json.dumps(list(row_names))
    return f'''<script id="candidate-01-living-editorial-runtime">(()=>{{const DIRECTOR={director},ROWS={data},names={names};const bind=()=>{{const bands=[...document.querySelectorAll('.living-current-band')];if(bands.length<2)return false;bands.slice(0,2).forEach((band,bi)=>{{const row=ROWS[names[bi]],cards=[...band.querySelectorAll('.product')];cards.slice(0,4).forEach((card,i)=>{{const item=row[i];if(!item)return;const hasVisual=Boolean(item.image);card.dataset.editorialWeight=String(item.weight);card.dataset.editorialShape=item.shape;card.dataset.editorialWorld=item.world;card.dataset.editorialW=names[bi];card.dataset.editorialScore=String(item.editorial_score);card.dataset.editorialHasVisual=String(hasVisual);const img=card.querySelector('img');if(img&&hasVisual){{img.src=item.image;img.srcset='';img.alt=item.title}}const tag=document.createElement('div');tag.className='lw-editorial-tag';tag.title=item.editorial_reason;tag.textContent=names[bi]+' · '+item.source;card.appendChild(tag);const reader=document.createElement('div');reader.className='lw-inline-reader';reader.innerHTML=`<div class="lw-reader-image"></div><div class="lw-reader-flow"><section class="lw-reader-panel"><span class="eyebrow">${{names[bi]}} · ${{item.source}}</span><h3>${{item.title}}</h3><p>${{item.deck}}</p></section><section class="lw-reader-panel next"><span class="eyebrow">SECOND LAYER</span><h3>${{item.world}}</h3><p>第一層只定義進入接口；各內容世界的沉浸動效不在本刀展開。</p></section></div>`;if(hasVisual)reader.querySelector('.lw-reader-image').style.backgroundImage=`url("${{item.image}}")`;card.appendChild(reader);let timer=0;card.addEventListener('mouseenter',()=>{{card.classList.add('is-contemplated');timer=setTimeout(()=>card.classList.add('is-reading'),500)}});card.addEventListener('mouseleave',()=>{{clearTimeout(timer);card.classList.remove('is-reading','is-contemplated')}});card.addEventListener('click',ev=>{{if(!card.classList.contains('is-reading'))return;ev.preventDefault();ev.stopImmediatePropagation();window.parent.postMessage({{type:'dore-world-enter',interface:DIRECTOR.world_interface,world:item.world,w:names[bi],title:item.title,source:item.source,editorial_score:item.editorial_score}},'*')}},true)}})}});document.documentElement.dataset.visualEditorialDirector=DIRECTOR.schema;return true}};if(!bind()){{const o=new MutationObserver(()=>{{if(bind())o.disconnect()}});o.observe(document.documentElement,{{childList:true,subtree:true}})}}}})();</script>'''


def focus_screen(screen_no,labels):
    row_names=("WATCH","WITNESS") if screen_no==2 else ("WALK","WORSHIP")
    doc=motion._install_living_current(codrops_site_8x5.render(edit=False));doc=doc.replace('</head>',motion._CANDIDATE_FOCUS_EMBED_STYLE+STYLE+'</head>',1);doc=doc.replace('</body>',motion._movement_labels_script(labels)+script(row_names)+'</body>',1);srcdoc=html_lib.escape(doc,quote=True)
    return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s" data-editorial-director="%s"><iframe title="4W Living Editorial River %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,EDITORIAL_DIRECTOR['schema'],screen_no-1,srcdoc)


def install(current):
    motion._candidate_focus_screen=focus_screen
