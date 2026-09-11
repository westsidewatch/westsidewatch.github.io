"""Candidate 01 — 4W Living Editorial River experiment (#643)."""
from __future__ import annotations
import html as html_lib, json
import design_motion_registry as motion
import codrops_site_8x5
import visual_editorial_director as ved

EDITORIAL_DIRECTOR={**ved.contract(),"source_issue":643}
_DORE="https://commons.wikimedia.org/wiki/Special:Redirect/file/016.The_Testing_of_Abraham%27s_Faith.jpg?width=2303"
_GALILEE="https://media.artmuseum.princeton.edu/iiif/3/collection/INV33869/full/max/0/default.jpg"
_CHINA="https://commons.wikimedia.org/wiki/Special:Redirect/file/Child_reading,_while_Pastor_Wang_Lieh-guang_and_missionaries_look_on.jpg?width=1024"
_PEF="https://commons.wikimedia.org/wiki/Special:Redirect/file/Survey_of_Western_Palestine_1880.17.jpg?width=3840"

# Phase-1 live editorial pool. These are candidates, not assigned slots. The
# director decides 4W affinity and capacity at render time. Later ingestion can
# replace this pool with sitewide Content Graph candidates without changing UI.
_POOL=[
ved.Candidate("watch-dawn","守望黎明","Journal · 米斯巴","在黑夜仍辨認晨光；把此刻最需要被看見的守望放到河面。",_DORE,"journal",("守望","黎明","米斯巴"),.86,.94,.91,.82),
ved.Candidate("galilee-storm","加利利海上的風暴","Visual Graph · Scripture","風浪、微小的人與遠處的光，讓觀看先於解釋。",_GALILEE,"one",("守望","光","經文"),.64,.83,.94,.74),
ved.Candidate("jerusalem-west","耶路撒冷與西地","Dawn Library · Map","1880 年巴勒斯坦勘測圖：地理本身成為守望的視野。",_PEF,"dawn-library",("守望","地圖","歷史"),.52,.68,.76,.78),
ved.Candidate("the-gate","The Gate","Journal · 門","從正在發生的事進入西望，而不是從導航開始。",_CHINA,"journal",("門","此刻","watch"),.82,.66,.78,.55),
ved.Candidate("remembered-people","被記住的人","Chinese Christian Memory","人物、教會與見證不是資料列，而是仍在說話的生命記憶。",_CHINA,"dawn-library",("人物","教會","見證","記憶","歷史"),.61,.94,.9,.92),
ved.Candidate("abraham-test","亞伯拉罕的試驗","Doré · Genesis 22","經文、事件與版畫在同一個 VisualWork 上重新相遇。",_DORE,"one",("經文","見證","生命"),.55,.87,.93,.9),
ved.Candidate("city-witness","一座城的見證","Journal · Bethel","地方、人物、時間與恩典交疊成可以被閱讀的見證。",_PEF,"journal",("見證","伯特利","歷史"),.58,.72,.7,.76),
ved.Candidate("living-water","Living Water","Church","教會世界保持安靜、簡單、克制；第二層復用已探索成立的互動方向。",_GALILEE,"church",("教會","生命","見證"),.76,.82,.84,.68),
ved.Candidate("one-outpost","ONE · 查經前哨站","ONE","從一章經文走向人物、地圖、時間、串珠與歷史背景。",_GALILEE,"one",("ONE","查經","經文","研究"),.9,.96,.86,.98),
ved.Candidate("scripture-geography","走進經文的地理","Dawn Library · PEF","古地圖不是背景；它把閱讀重新放回土地與距離。",_PEF,"one",("經文","地圖","行走","研究"),.64,.84,.82,.92),
ved.Candidate("dore-folio","Doré Folio","Writing / Research","筆記、模糊搜尋與研究結果在寫作時自然浮現。",_DORE,"dore-folio",("筆記","研究","folio"),.74,.75,.8,.86),
ved.Candidate("emmaus","以馬忤斯","Journal · Emmaus","行走、談論、忽然看見；WALK 允許內容在路上被理解。",_CHINA,"journal",("以馬忤斯","行走","walk"),.62,.8,.74,.83),
ved.Candidate("maranatha","Maranatha","Journal · 瑪拉拿","敬拜不是首頁的裝飾高潮，而是河流最後指向的盼望。",_DORE,"journal",("瑪拉拿","敬拜","盼望"),.78,.95,.93,.88),
ved.Candidate("watch-prayer","Watch Prayer","Mount of Olives","越接近禱告，流速越慢；觀看沉靜下來。",_GALILEE,"church",("禱告","安靜","worship"),.84,.9,.88,.8),
ved.Candidate("dawn-library","黎明書局","Dawn Library","5:8 書籤與書脊將在第二層形成綿延的光明城；本刀只保留世界接口。",_PEF,"dawn-library",("學習","光","黎明"),.72,.86,.79,.94),
ved.Candidate("selah","細拉","Journal · Selah","不是更多內容，而是在江河中留下可以停住的空間。",_CHINA,"journal",("細拉","安靜","敬拜"),.58,.74,.76,.72),
]

def _rows():
    selected=ved.select(_POOL,per_w=4)
    rows={}
    for w,pairs in selected.items():
        rows[w]=[]
        for c,d in pairs:
            rows[w].append({"id":c.id,"title":c.title,"source":c.source,"deck":c.deck,"image":c.image,"world":c.world,"weight":d.weight,"shape":d.shape,"affinity":d.affinity,"brightness":d.brightness,"editorial_score":d.editorial_score,"editorial_reason":d.reason})
    return rows

ROWS=_rows()

STYLE=r'''<style id="candidate-01-living-editorial-river">
.living-current-band{gap:clamp(12px,1.45vw,28px)!important;align-items:center!important}.living-current-band .product{position:relative;overflow:hidden;transition:flex-grow .65s cubic-bezier(.2,.75,.2,1),transform .65s cubic-bezier(.2,.75,.2,1),opacity .4s ease,filter .4s ease;flex-basis:0!important}.living-current-band .product[data-editorial-weight="1"]{flex-grow:1!important}.living-current-band .product[data-editorial-weight="2"]{flex-grow:1.65!important}.living-current-band .product[data-editorial-weight="3"]{flex-grow:2.35!important}.living-current-band .product[data-editorial-shape="portrait"]{aspect-ratio:5/8!important;max-width:19vw}.living-current-band:has(.product.is-contemplated) .product:not(.is-contemplated){opacity:.38;filter:saturate(.65)}.living-current-band .product.is-contemplated{flex-grow:3.4!important;z-index:8;transform:scale(1.025)}.lw-editorial-tag{position:absolute;z-index:9;left:.7rem;top:.65rem;padding:.25rem .42rem;background:rgba(8,16,20,.72);color:#CEBD74;font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;pointer-events:none}.lw-inline-reader{position:absolute;z-index:10;inset:0;display:grid;grid-template-columns:minmax(38%,.72fr) minmax(0,1.28fr);background:rgba(8,16,20,.94);color:#f7f1df;opacity:0;pointer-events:none;transition:opacity .28s ease;overflow:hidden}.product.is-reading .lw-inline-reader{opacity:1;pointer-events:auto}.lw-reader-image{background-size:cover;background-position:center}.lw-reader-flow{display:flex;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;scrollbar-width:none}.lw-reader-flow::-webkit-scrollbar{display:none}.lw-reader-panel{flex:0 0 min(76%,420px);padding:clamp(16px,2vw,34px);display:flex;flex-direction:column;justify-content:flex-end;border-left:1px solid rgba(206,189,116,.25);scroll-snap-align:start}.lw-reader-panel .eyebrow{color:#CEBD74;font:600 9px/1.3 ui-monospace,monospace;letter-spacing:.14em}.lw-reader-panel h3{font:400 clamp(25px,2.6vw,46px)/.9 "Cormorant Garamond","Noto Serif TC",serif;margin:.45rem 0}.lw-reader-panel p{font:400 clamp(12px,.95vw,16px)/1.55 "Noto Serif TC",serif;margin:0}.lw-reader-panel.next{justify-content:center;color:#CEBD74}.lw-reader-panel.next:after{content:'CLICK → ENTER WORLD';font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;margin-top:1rem}@media(max-width:900px){.living-current-band .product[data-editorial-shape="portrait"]{max-width:none;aspect-ratio:8/5!important}.lw-inline-reader{grid-template-columns:1fr}.lw-reader-image{display:none}.lw-reader-panel{flex-basis:86%}}@media(prefers-reduced-motion:reduce){.living-current-band .product,.lw-inline-reader{transition:none!important}}
</style>'''

def script(row_names):
 data=json.dumps({n:ROWS[n] for n in row_names},ensure_ascii=False);director=json.dumps(EDITORIAL_DIRECTOR,ensure_ascii=False);names=json.dumps(list(row_names))
 return f'''<script id="candidate-01-living-editorial-runtime">(()=>{{const DIRECTOR={director},ROWS={data},names={names};const bind=()=>{{const bands=[...document.querySelectorAll('.living-current-band')];if(bands.length<2)return false;bands.slice(0,2).forEach((band,bi)=>{{const row=ROWS[names[bi]],cards=[...band.querySelectorAll('.product')];cards.slice(0,4).forEach((card,i)=>{{const item=row[i];if(!item)return;card.dataset.editorialWeight=String(item.weight);card.dataset.editorialShape=item.shape;card.dataset.editorialWorld=item.world;card.dataset.editorialW=names[bi];card.dataset.editorialScore=String(item.editorial_score);const img=card.querySelector('img');if(img){{img.src=item.image;img.srcset='';img.alt=item.title}}const tag=document.createElement('div');tag.className='lw-editorial-tag';tag.title=item.editorial_reason;tag.textContent=names[bi]+' · '+item.source;card.appendChild(tag);const reader=document.createElement('div');reader.className='lw-inline-reader';reader.innerHTML=`<div class="lw-reader-image"></div><div class="lw-reader-flow"><section class="lw-reader-panel"><span class="eyebrow">${{names[bi]}} · ${{item.source}}</span><h3>${{item.title}}</h3><p>${{item.deck}}</p></section><section class="lw-reader-panel next"><span class="eyebrow">SECOND LAYER</span><h3>${{item.world}}</h3><p>第一層只定義進入接口；各內容世界的沉浸動效不在本刀展開。</p></section></div>`;reader.querySelector('.lw-reader-image').style.backgroundImage=`url("${{item.image}}")`;card.appendChild(reader);let timer=0;card.addEventListener('mouseenter',()=>{{card.classList.add('is-contemplated');timer=setTimeout(()=>card.classList.add('is-reading'),500)}});card.addEventListener('mouseleave',()=>{{clearTimeout(timer);card.classList.remove('is-reading','is-contemplated')}});card.addEventListener('click',ev=>{{if(!card.classList.contains('is-reading'))return;ev.preventDefault();ev.stopImmediatePropagation();window.parent.postMessage({{type:'dore-world-enter',interface:DIRECTOR.world_interface,world:item.world,w:names[bi],title:item.title,source:item.source,editorial_score:item.editorial_score}},'*')}},true)}})}});document.documentElement.dataset.visualEditorialDirector=DIRECTOR.schema;return true}};if(!bind()){{const o=new MutationObserver(()=>{{if(bind())o.disconnect()}});o.observe(document.documentElement,{{childList:true,subtree:true}})}}}})();</script>'''

def focus_screen(screen_no,labels):
 row_names=("WATCH","WITNESS") if screen_no==2 else ("WALK","WORSHIP")
 doc=motion._install_living_current(codrops_site_8x5.render(edit=False));doc=doc.replace('</head>',motion._CANDIDATE_FOCUS_EMBED_STYLE+STYLE+'</head>',1);doc=doc.replace('</body>',motion._movement_labels_script(labels)+script(row_names)+'</body>',1);srcdoc=html_lib.escape(doc,quote=True)
 return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s" data-editorial-director="%s"><iframe title="4W Living Editorial River %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,EDITORIAL_DIRECTOR['schema'],screen_no-1,srcdoc)

def install(current):
 motion._candidate_focus_screen=focus_screen
