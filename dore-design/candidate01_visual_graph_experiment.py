"""Candidate 01 — 4W Living Editorial River experiment (#643)."""
from __future__ import annotations
import html as html_lib, json
import design_motion_registry as motion
import codrops_site_8x5

EDITORIAL_DIRECTOR={"schema":"dore.visual-editorial-director.v1","source_issue":643,"selection":"sitewide-highlight","classification":"4w-fuzzy-affinity","weight_meaning":"visual+reading+temporal-capacity","world_interface":"dore.world-surface/1"}
_DORE="https://commons.wikimedia.org/wiki/Special:Redirect/file/016.The_Testing_of_Abraham%27s_Faith.jpg?width=2303"
_GALILEE="https://media.artmuseum.princeton.edu/iiif/3/collection/INV33869/full/max/0/default.jpg"
_CHINA="https://commons.wikimedia.org/wiki/Special:Redirect/file/Child_reading,_while_Pastor_Wang_Lieh-guang_and_missionaries_look_on.jpg?width=1024"
_PEF="https://commons.wikimedia.org/wiki/Special:Redirect/file/Survey_of_Western_Palestine_1880.17.jpg?width=3840"
ROWS={
"WATCH":[
{"title":"守望黎明","source":"Journal · 米斯巴","deck":"在黑夜仍辨認晨光；把此刻最需要被看見的守望放到河面。","image":_DORE,"weight":3,"shape":"wide","world":"journal"},
{"title":"加利利海上的風暴","source":"Visual Graph · Scripture","deck":"風浪、微小的人與遠處的光，讓觀看先於解釋。","image":_GALILEE,"weight":2,"shape":"wide","world":"one"},
{"title":"耶路撒冷與西地","source":"Dawn Library · Map","deck":"1880 年巴勒斯坦勘測圖：地理本身成為守望的視野。","image":_PEF,"weight":1,"shape":"standard","world":"dawn-library"},
{"title":"The Gate","source":"Journal · 門","deck":"從正在發生的事進入西望，而不是從導航開始。","image":_CHINA,"weight":1,"shape":"portrait","world":"journal"}],
"WITNESS":[
{"title":"被記住的人","source":"Chinese Christian Memory","deck":"人物、教會與見證不是資料列，而是仍在說話的生命記憶。","image":_CHINA,"weight":3,"shape":"wide","world":"dawn-library"},
{"title":"亞伯拉罕的試驗","source":"Doré · Genesis 22","deck":"經文、事件與版畫在同一個 VisualWork 上重新相遇。","image":_DORE,"weight":2,"shape":"wide","world":"one"},
{"title":"一座城的見證","source":"Journal · Bethel","deck":"地方、人物、時間與恩典交疊成可以被閱讀的見證。","image":_PEF,"weight":1,"shape":"standard","world":"journal"},
{"title":"Living Water","source":"Church","deck":"教會世界保持安靜、簡單、克制；第二層復用已探索成立的互動方向。","image":_GALILEE,"weight":1,"shape":"portrait","world":"church"}],
"WALK":[
{"title":"ONE · 查經前哨站","source":"ONE","deck":"從一章經文走向人物、地圖、時間、串珠與歷史背景。","image":_GALILEE,"weight":3,"shape":"wide","world":"one"},
{"title":"走進經文的地理","source":"Dawn Library · PEF","deck":"古地圖不是背景；它把閱讀重新放回土地與距離。","image":_PEF,"weight":2,"shape":"wide","world":"one"},
{"title":"Doré Folio","source":"Writing / Research","deck":"筆記、模糊搜尋與研究結果在寫作時自然浮現。","image":_DORE,"weight":1,"shape":"standard","world":"dore-folio"},
{"title":"以馬忤斯","source":"Journal · Emmaus","deck":"行走、談論、忽然看見；WALK 允許內容在路上被理解。","image":_CHINA,"weight":1,"shape":"portrait","world":"journal"}],
"WORSHIP":[
{"title":"Maranatha","source":"Journal · 瑪拉拿","deck":"敬拜不是首頁的裝飾高潮，而是河流最後指向的盼望。","image":_DORE,"weight":3,"shape":"wide","world":"journal"},
{"title":"Watch Prayer","source":"Mount of Olives","deck":"越接近禱告，流速越慢；觀看沉靜下來。","image":_GALILEE,"weight":2,"shape":"wide","world":"church"},
{"title":"黎明書局","source":"Dawn Library","deck":"5:8 書籤與書脊將在第二層形成綿延的光明城；本刀只保留世界接口。","image":_PEF,"weight":1,"shape":"portrait","world":"dawn-library"},
{"title":"細拉","source":"Journal · Selah","deck":"不是更多內容，而是在江河中留下可以停住的空間。","image":_CHINA,"weight":1,"shape":"standard","world":"journal"}]}

STYLE=r'''<style id="candidate-01-living-editorial-river">
.living-current-band{gap:clamp(12px,1.45vw,28px)!important;align-items:center!important}.living-current-band .product{position:relative;overflow:hidden;transition:flex-grow .65s cubic-bezier(.2,.75,.2,1),transform .65s cubic-bezier(.2,.75,.2,1),opacity .4s ease,filter .4s ease;flex-basis:0!important}.living-current-band .product[data-editorial-weight="1"]{flex-grow:1!important}.living-current-band .product[data-editorial-weight="2"]{flex-grow:1.65!important}.living-current-band .product[data-editorial-weight="3"]{flex-grow:2.35!important}.living-current-band .product[data-editorial-shape="portrait"]{aspect-ratio:5/8!important;max-width:19vw}.living-current-band:has(.product.is-contemplated) .product:not(.is-contemplated){opacity:.38;filter:saturate(.65)}.living-current-band .product.is-contemplated{flex-grow:3.4!important;z-index:8;transform:scale(1.025)}.lw-editorial-tag{position:absolute;z-index:9;left:.7rem;top:.65rem;padding:.25rem .42rem;background:rgba(8,16,20,.72);color:#CEBD74;font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;pointer-events:none}.lw-inline-reader{position:absolute;z-index:10;inset:0;display:grid;grid-template-columns:minmax(38%,.72fr) minmax(0,1.28fr);background:rgba(8,16,20,.94);color:#f7f1df;opacity:0;pointer-events:none;transition:opacity .28s ease;overflow:hidden}.product.is-reading .lw-inline-reader{opacity:1;pointer-events:auto}.lw-reader-image{background-size:cover;background-position:center}.lw-reader-flow{display:flex;overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x proximity;scrollbar-width:none}.lw-reader-flow::-webkit-scrollbar{display:none}.lw-reader-panel{flex:0 0 min(76%,420px);padding:clamp(16px,2vw,34px);display:flex;flex-direction:column;justify-content:flex-end;border-left:1px solid rgba(206,189,116,.25);scroll-snap-align:start}.lw-reader-panel .eyebrow{color:#CEBD74;font:600 9px/1.3 ui-monospace,monospace;letter-spacing:.14em}.lw-reader-panel h3{font:400 clamp(25px,2.6vw,46px)/.9 "Cormorant Garamond","Noto Serif TC",serif;margin:.45rem 0}.lw-reader-panel p{font:400 clamp(12px,.95vw,16px)/1.55 "Noto Serif TC",serif;margin:0}.lw-reader-panel.next{justify-content:center;color:#CEBD74}.lw-reader-panel.next:after{content:'CLICK → ENTER WORLD';font:600 9px/1 ui-monospace,monospace;letter-spacing:.12em;margin-top:1rem}@media(max-width:900px){.living-current-band .product[data-editorial-shape="portrait"]{max-width:none;aspect-ratio:8/5!important}.lw-inline-reader{grid-template-columns:1fr}.lw-reader-image{display:none}.lw-reader-panel{flex-basis:86%}}@media(prefers-reduced-motion:reduce){.living-current-band .product,.lw-inline-reader{transition:none!important}}
</style>'''

def script(row_names):
 data=json.dumps({n:ROWS[n] for n in row_names},ensure_ascii=False);director=json.dumps(EDITORIAL_DIRECTOR,ensure_ascii=False);names=json.dumps(list(row_names))
 return f'''<script id="candidate-01-living-editorial-runtime">(()=>{{const DIRECTOR={director},ROWS={data},names={names};const bind=()=>{{const bands=[...document.querySelectorAll('.living-current-band')];if(bands.length<2)return false;bands.slice(0,2).forEach((band,bi)=>{{const row=ROWS[names[bi]],cards=[...band.querySelectorAll('.product')];cards.slice(0,4).forEach((card,i)=>{{const item=row[i];if(!item)return;card.dataset.editorialWeight=String(item.weight);card.dataset.editorialShape=item.shape;card.dataset.editorialWorld=item.world;card.dataset.editorialW=names[bi];const img=card.querySelector('img');if(img){{img.src=item.image;img.srcset='';img.alt=item.title}}const tag=document.createElement('div');tag.className='lw-editorial-tag';tag.textContent=names[bi]+' · '+item.source;card.appendChild(tag);const reader=document.createElement('div');reader.className='lw-inline-reader';reader.innerHTML=`<div class="lw-reader-image"></div><div class="lw-reader-flow"><section class="lw-reader-panel"><span class="eyebrow">${{names[bi]}} · ${{item.source}}</span><h3>${{item.title}}</h3><p>${{item.deck}}</p></section><section class="lw-reader-panel next"><span class="eyebrow">SECOND LAYER</span><h3>${{item.world}}</h3><p>第一層只定義進入接口；各內容世界的沉浸動效不在本刀展開。</p></section></div>`;reader.querySelector('.lw-reader-image').style.backgroundImage=`url("${{item.image}}")`;card.appendChild(reader);let timer=0;card.addEventListener('mouseenter',()=>{{card.classList.add('is-contemplated');timer=setTimeout(()=>card.classList.add('is-reading'),500)}});card.addEventListener('mouseleave',()=>{{clearTimeout(timer);card.classList.remove('is-reading','is-contemplated')}});card.addEventListener('click',ev=>{{if(!card.classList.contains('is-reading'))return;ev.preventDefault();ev.stopImmediatePropagation();window.parent.postMessage({{type:'dore-world-enter',interface:DIRECTOR.world_interface,world:item.world,w:names[bi],title:item.title,source:item.source}},'*')}},true)}})}});document.documentElement.dataset.visualEditorialDirector=DIRECTOR.schema;return true}};if(!bind()){{const o=new MutationObserver(()=>{{if(bind())o.disconnect()}});o.observe(document.documentElement,{{childList:true,subtree:true}})}}}})();</script>'''

def focus_screen(screen_no,labels):
 row_names=("WATCH","WITNESS") if screen_no==2 else ("WALK","WORSHIP")
 doc=motion._install_living_current(codrops_site_8x5.render(edit=False));doc=doc.replace('</head>',motion._CANDIDATE_FOCUS_EMBED_STYLE+STYLE+'</head>',1);doc=doc.replace('</body>',motion._movement_labels_script(labels)+script(row_names)+'</body>',1);srcdoc=html_lib.escape(doc,quote=True)
 return '<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="%s" data-editorial-director="%s"><iframe title="4W Living Editorial River %s" loading="eager" srcdoc="%s"></iframe></section>'%(screen_no,EDITORIAL_DIRECTOR['schema'],screen_no-1,srcdoc)

def install(current):
 motion._candidate_focus_screen=focus_screen
