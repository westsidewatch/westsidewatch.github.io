/* Vol.00 / Twelve independent editorial contents compositions.
   A design studio, not twelve recolourings of an old table. All copy is
   read from the canonical 12-desk markup before the old folio is retired.
   Real Doré image scan, official SVG and Morning Star stay in the P2 host. */
(function(){
 "use strict";
 const page=document.getElementById("dual-stone-contents");
 const tile=document.getElementById("dual-contents");
 if(!page||!tile)return;
 const escape=s=>String(s??"").replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
 const groups=Array.from(page.querySelectorAll(".dual-movement")).map((node,i)=>({
  key:node.getAttribute("aria-label")||["WATCH","WALK","WITNESS","WORSHIP"][i],
  roman:["I","II","III","IV"][i],
  interlude:node.querySelector(".dual-movement__interlude")?.textContent.trim()||"",
  entries:Array.from(node.querySelectorAll(".dual-entry")).map(li=>{
   const col=li.querySelector(".dual-entry__column");
   const name=col?.cloneNode(true);
   name?.querySelector("small")?.remove();
   return {
    no:li.querySelector("b")?.textContent.trim()||"",
    zh:name?.textContent.trim()||"",
    en:col?.querySelector("small")?.textContent.trim()||"",
    works:Array.from(li.querySelectorAll(".dual-work")).map(el=>el.textContent.trim())
   };
  })
 }));
 if(groups.length!==4||groups.flatMap(g=>g.entries).length!==12)throw Error("P2 Contents: canonical twelve desks missing");
 const all=groups.flatMap(g=>g.entries);
 const DESIGNS=[
  {id:"01",source:"Aperture",name:"The Engraved Window",zh:"版畫之窗",glyph:[.27,.60,.055,.29,.88]},
  {id:"02",source:"COEVAL",name:"Offset Staircase",zh:"錯位階梯",glyph:[.17,.45,.06,.40,.70]},
  {id:"03",source:"Surplus",name:"Editorial Collage",zh:"編輯拼貼",glyph:[.20,.52,.07,.28,.68]},
  {id:"04",source:"L’Architecture d’Aujourd’hui",name:"Vertical Ribbons",zh:"垂直條帶",glyph:[.20,.58,.07,.26,.64]},
  {id:"05",source:"Circular 19",name:"Monumental Letterforms",zh:"字體紀念碑",glyph:[.18,.50,.075,.43,.63]},
  {id:"06",source:"Remote*Control",name:"Floating Typography",zh:"文字懸浮",glyph:[.22,.55,.055,.32,.71]},
  {id:"07",source:"The Form of Form",name:"Architectural Index",zh:"建築索引",glyph:[.19,.53,.052,.35,.67]},
  {id:"08",source:"François Girard-Meunier",name:"Swiss Counterpoint",zh:"瑞士對位",glyph:[.19,.51,.085,.37,.69]},
  {id:"09",source:"YES & NO",name:"Orbit of Four",zh:"四個軌道",glyph:[.18,.48,.07,.42,.63]},
  {id:"10",source:"Cereal",name:"Engraved Light / Quiet Gallery",zh:"版畫光跡 · 靜默畫廊",glyph:[.27,.54,.31,.34,.94]},
  {id:"11",source:"W Magazine",name:"Four Monumental Numbers",zh:"四組大數字",glyph:[.19,.51,.07,.34,.69]},
  {id:"12",source:"The Eye",name:"Bibliographic Folio",zh:"古典書目",glyph:[.25,.58,.65,.29,.56]}
 ];
 const entry=(e,style="standard")=>'<li class="p2x-entry p2x-entry--'+style+'"><span class="p2x-num">'+escape(e.no)+'</span>'+
  '<span class="p2x-entry__body"><span class="p2x-zh">'+escape(e.zh)+'</span>'+
  '<span class="p2x-en">'+escape(e.en)+'</span>'+
  (e.works.length?'<span class="p2x-works">'+e.works.map(w=>'<span>'+escape(w)+'</span>').join("")+'</span>':"")+
  '</span></li>';
 const group=(g,cls="",options={})=>'<section class="p2x-movement '+cls+'"><div class="p2x-movement__heading">'+
  '<span class="p2x-roman">'+escape(g.roman)+'</span><h3>'+escape(g.key)+'</h3></div>'+
  '<ol class="p2x-list">'+g.entries.map(e=>entry(e,options.entryStyle||"standard")).join("")+'</ol>'+
  (g.interlude?'<p class="p2x-interlude">'+escape(g.interlude)+'</p>':"")+'</section>';
 const groupList=(cls="",options={})=>groups.map(g=>group(g,cls,options)).join("");
 const opening=(no,title,details="")=>'<div class="p2x-edition"><span>WESTSIDE WATCH · VOL.00</span><span>'+escape(no)+' / 12</span></div>'+
  '<h2 class="p2x-title">'+title+'</h2>'+(details?'<p class="p2x-lede">'+details+'</p>':"");
 const renderers={
 "01":()=>'<div class="p2x-arttop"><span class="p2x-arttop__edge">GUSTAVE DORÉ / THE CITY & ITS WALLS</span>'+
   '<span class="p2x-arttop__folio">01—12</span></div>'+
   '<div class="p2x-aperture-bottom">'+opening("01","Contents<span class=p2x-dot>.</span>","四個篇章 · 十二個入口")+
   '<div class="p2x-aperture-groups">'+groupList("p2x-aperture-group")+'</div></div>',
 "02":()=>'<div class="p2x-coeval-rail"><span>VOLUME ZERO</span><b>INDEX</b><span>WESTSIDE</span></div>'+
   '<h2 class="p2x-coeval-title">Con<br><em>tents</em><i>.</i></h2>'+
   '<div class="p2x-coeval-stairs">'+groupList("p2x-stair-step",{entryStyle:"tight"})+'</div>'+
   '<span class="p2x-coeval-note">AN EDITORIAL CITY · TWELVE DESKS</span>',
 "03":()=>'<span class="p2x-surplus-ghost">00</span>'+
   '<div class="p2x-surplus-mast"><span>THE CITY / THE GATE / THE LIGHT</span><span>ISSUE NO.00</span></div>'+
   '<h2 class="p2x-surplus-title"><span>CON</span><em>TENTS</em><b>.</b></h2>'+
   '<div class="p2x-surplus-mosaic">'+groupList("p2x-surplus-panel",{entryStyle:"tight"})+'</div>'+
   '<div class="p2x-surplus-footer">西望 · JOURNAL OF THE WATCH</div>',
 "04":()=>'<div class="p2x-aa-head"><span>L’INDEX DES CITÉS</span><h2>CONTENTS</h2><span>NO. 00</span></div>'+
   '<div class="p2x-aa-strips"><div class="p2x-aa-image-strip"><span>DORÉ / ENGRAVINGS</span></div>'+
   groupList("p2x-aa-column",{entryStyle:"tight"})+'</div>'+
   '<div class="p2x-aa-bottom">FOUR MOVEMENTS <span>TWELVE CITIES</span></div>',
 "05":()=>'<span class="p2x-circular-super" aria-hidden="true">C</span><span class="p2x-circular-tail" aria-hidden="true">S.</span>'+
   '<div class="p2x-circular-top"><span>NO.00 / 2026</span><span>AN INDEX IN FOUR ACTS</span></div>'+
   '<h2 class="p2x-circular-title">Contents</h2>'+
   '<div class="p2x-circular-list">'+groupList("p2x-circular-group",{entryStyle:"tight"})+'</div>',
 "06":()=>'<span class="p2x-remote-word p2x-remote-word--one">con</span>'+
   '<span class="p2x-remote-word p2x-remote-word--two">tents.</span>'+
   '<div class="p2x-remote-identity"><span>WESTSIDE WATCH</span><span>VOLUME 00</span></div>'+
   '<div class="p2x-remote-constellation">'+groupList("p2x-remote-node",{entryStyle:"tight"})+'</div>'+
   '<span class="p2x-remote-footnote">CONSTRUCTED FROM AN ENGRAVED CITY</span>',
 "07":()=>'<div class="p2x-form-architecture"><span class="p2x-form-con">CON</span>'+
   '<span class="p2x-form-tents">TENTS</span><span class="p2x-form-period">.</span></div>'+
   '<div class="p2x-form-strap"><span>WESTSIDE / ISSUE 00</span><span>ARCHITECTURE OF A CITY</span></div>'+
   '<div class="p2x-form-index">'+groupList("p2x-form-part",{entryStyle:"tight"})+'</div>'+
   '<span class="p2x-form-margin">01 — 12</span>',
 "08":()=>'<div class="p2x-swiss-border"><span>WESTSIDE</span><span>001 / CONTENTS / 2026</span></div>'+
   '<div class="p2x-swiss-title"><span>Index / 00</span><h2>Contents.</h2><span>目錄</span></div>'+
   '<div class="p2x-swiss-quadrants">'+groupList("p2x-swiss-quadrant",{entryStyle:"tight"})+'</div>'+
   '<div class="p2x-swiss-bottom">T H E &nbsp; C I T Y &nbsp; O F &nbsp; L I G H T</div>',
 "09":()=>'<div class="p2x-orbit-diagram" aria-hidden="true"><svg viewBox="0 0 600 600" preserveAspectRatio="xMidYMid meet">'+
   '<circle cx="283" cy="287" r="235"/><circle cx="283" cy="287" r="164"/>'+
   '<circle cx="283" cy="287" r="89"/><path d="M38 300H526M283 40V535"/>'+
   '<circle cx="283" cy="52" r="6"/><circle cx="518" cy="287" r="6"/><circle cx="283" cy="522" r="6"/><circle cx="48" cy="287" r="6"/></svg></div>'+
   '<div class="p2x-orbit-head"><span>FOUR POINTS OF WATCH</span><h2>Contents.</h2></div>'+
   '<div class="p2x-orbit-locations">'+groups.map((g,i)=>'<span class="p2x-orbit-marker p2x-orbit-marker--'+i+'">'+escape(g.roman)+' / '+escape(g.key)+'</span>').join("")+'</div>'+
   '<div class="p2x-orbit-index">'+groupList("p2x-orbit-chapter",{entryStyle:"tight"})+'</div>',
 "10":()=>'<div class="p2x-cereal-gallery"><div class="p2x-cereal-edition"><span>THE CITY OF LIGHT</span><span>GUSTAVE DORÉ / ORIGINAL PLATES</span></div>'+
   '<span class="p2x-cereal-art-credit">ENGRAVED CITIES & WALLS / 1866</span></div>'+
   // Star-registered engraving: not a decorative gold slash, and not
   // 09's diagram. The star at 16% / 16.5% releases a system of hand-
   // engraved contour arcs across the entire image half. The three lines
   // frame the restored tall official Xi Wang SVG, and meet near the foot.
   '<svg class="p2x-cereal-engraving" viewBox="0 0 1000 1000" preserveAspectRatio="none" role="img" aria-label="由晨星發出的完整金色雕版線群，圍繞西望字標延伸至版畫下緣">'+
    '<defs><linearGradient id="p2x-cereal-gold" x1="0" y1="0" x2="1" y2="1">'+
      '<stop offset="0" stop-color="#e8bb73" stop-opacity=".94"/>'+
      '<stop offset=".4" stop-color="#d4a058" stop-opacity="1"/>'+
      '<stop offset=".75" stop-color="#b77e37" stop-opacity=".98"/>'+
      '<stop offset="1" stop-color="#d2a45e" stop-opacity=".78"/></linearGradient></defs>'+
    // A long left sweep and bottom embrace. Route starts at star centre.
    '<path class="p2x-etch-line p2x-etch-line--principal" d="M166 165 C165 263 145 360 165 478 C183 625 205 754 326 857 C398 919 505 932 592 896"/>'+
    // Long right arc. It is deliberately outside the title's letterforms.
    '<path class="p2x-etch-line p2x-etch-line--shadow" d="M166 165 C233 206 312 213 438 275 C556 334 585 438 585 562 C585 685 555 784 592 896"/>'+
    // Fine intermediate echo: distinct from the two framing contours.
    '<path class="p2x-etch-line p2x-etch-line--upper" d="M182 174 C249 213 315 235 427 305 C532 371 555 468 553 570 C551 672 526 786 559 843"/>'+
    '<path class="p2x-etch-glimmer" d="M166 165 C165 263 145 360 165 478 C183 625 205 754 326 857 C398 919 505 932 592 896"/>'+
    '<g class="p2x-etch-hatching">'+
      '<path d="M151 330 l-17 7 M148 353 l-16 8 M149 377 l-18 7 M152 402 l-16 8 M158 431 l-15 6 M161 454 l-15 6"/>'+
      '<path d="M183 631 l-20 6 M192 661 l-19 9 M204 695 l-20 8 M219 723 l-18 12 M242 757 l-18 13 M271 800 l-17 15"/>'+
      '<path d="M368 885 l-7 19 M395 901 l-5 19 M423 911 l-2 18 M453 916 l1 19 M483 920 l5 15 M512 916 l8 15"/>'+
      '<path d="M502 311 l14 -11 M524 336 l15 -12 M540 363 l16 -9 M559 398 l16 -8 M573 430 l17 -6 M579 460 l19 -4 M585 493 l18 -1"/>'+
      '<path d="M583 665 l18 2 M578 703 l18 5 M570 744 l18 7 M570 780 l17 9 M580 822 l16 10"/></g>'+
    '<g class="p2x-etch-witness">'+
      '<path d="M324 856 l13 -10 M438 915 l4 -15 M554 906 l-4 -17 M566 386 l14 9"/></g>'+
   '</svg>'+
   '<div class="p2x-cereal-paper">'+
    '<div class="p2x-cereal-tiny"><span>WESTSIDE WATCH / INDEX</span><span>VOL.00</span></div>'+
    '<header class="p2x-cereal-header"><h2>Contents<span class="p2x-dot">.</span></h2>'+
      '<p class="p2x-cereal-chinese">目錄 <span>FOUR MOVEMENTS / TWELVE DESKS</span></p></header>'+
    '<nav class="p2x-cereal-nav" aria-label="跳到四個目錄篇章">'+
      groups.map((g,i)=>'<button type="button" data-p2-cereal-jump="'+i+'" aria-label="跳到 '+escape(g.key)+'"><span>'+escape(g.roman)+'</span><small>'+escape(g.key)+'</small></button>').join("")+'</nav>'+
    '<div class="p2x-cereal-stack" tabindex="0" role="region" aria-label="可捲動的十二個欄目完整文章目錄">'+
     groupList("p2x-cereal-movement",{entryStyle:"standard"})+'</div>'+
    '<footer class="p2x-cereal-footer"><span>01—12 / CONTENTS</span><span class="p2x-cereal-progress" aria-live="off">SCROLL TO EXPLORE ↓</span><button class="p2x-cereal-expand" type="button" aria-label="完整目錄閱讀模式">FULL INDEX ↗</button></footer>'+
   '</div>',
 "11":()=>'<div class="p2x-w-upper"><span>WESTSIDE WATCH / JOURNAL</span>'+
   '<h2>Contents</h2><strong>00</strong></div>'+
   '<div class="p2x-w-chapters">'+groups.map((g,i)=>'<section class="p2x-w-chapter"><span class="p2x-w-huge">'+
    String(i+1).padStart(2,"0")+'</span>'+group(g,"p2x-w-mini",{entryStyle:"tight"})+'</section>').join("")+'</div>'+
   '<span class="p2x-w-bottom">VOLUME ZERO — TWELVE DESKS</span>',
 "12":()=>'<div class="p2x-eye-mast"><span>THE WESTSIDE WATCH</span><span>NO. 00</span><span>INDEX</span></div>'+
   '<div class="p2x-eye-title"><h2>Contents.</h2><span>四個篇章 / 十二個入口</span></div>'+
   '<div class="p2x-eye-register"><div class="p2x-eye-column">'+groups.slice(0,2).map(g=>group(g,"p2x-eye-group",{entryStyle:"register"})).join("")+'</div>'+
   '<div class="p2x-eye-column">'+groups.slice(2,4).map(g=>group(g,"p2x-eye-group",{entryStyle:"register"})).join("")+'</div></div>'+
   '<div class="p2x-eye-mark">00</div><div class="p2x-eye-footer">THE CITY OF LIGHT / GUSTAVE DORÉ</div>'
 };
 const params=new URLSearchParams(location.search);
 let active=DESIGNS.some(d=>d.id===params.get("variant"))?params.get("variant"):"10";
 const host=document.createElement("div");
 host.id="p2-contents-design";
 host.setAttribute("role","document");
 page.appendChild(host);
 const toolbar=document.createElement("nav");
 toolbar.className="p2-variant-toolbar";
 toolbar.setAttribute("aria-label","十二種 Contents 設計參考");
 toolbar.innerHTML='<span class="p2-variant-toolbar__label">CONTENTS STUDY <b>12</b></span>'+
  '<div class="p2-variant-toolbar__buttons">'+DESIGNS.map(d=>'<button type="button" data-p2-variant="'+d.id+'" title="'+escape(d.source+" · "+d.name)+'" aria-label="設計 '+d.id+' '+escape(d.source)+'">'+d.id+'</button>').join("")+'</div>'+
  '<span class="p2-variant-toolbar__current" aria-live="polite"></span>'+
  '<a class="p2-variant-toolbar__atlas" href="/experiments/p2-contents-twelve.html">十二版總覽</a>';
 document.querySelector(".dual-ui")?.appendChild(toolbar);
 // Reading is always possible, even in the square-constrained embedded
 // mobile P2 spread. This preserves both fixed publication page ratios.
 let reader=null,readerKeyHandler=null;
 function closeReader(){
  if(!reader)return;
  const focus=reader._returnFocus;
  reader.remove();reader=null;
  if(readerKeyHandler){document.removeEventListener("keydown",readerKeyHandler);readerKeyHandler=null}
  if(focus?.isConnected)focus.focus();
 }
 function openReader(trigger){
  closeReader();
  reader=document.createElement("div");
  reader.className="p2-cereal-reader p2x p2x--10";
  reader.setAttribute("role","dialog");
  reader.setAttribute("aria-modal","true");
  reader.setAttribute("aria-label","西望 Vol.00 完整目錄十二欄目");
  reader._returnFocus=trigger;
  reader.innerHTML='<div class="p2-cereal-reader__sheet">'+
   '<header class="p2-cereal-reader__head"><div class="p2-cereal-reader__eyebrow"><span>WESTSIDE WATCH / VOL.00</span>'+
   '<button type="button" class="p2-cereal-reader__close" aria-label="關閉完整目錄">CLOSE ×</button></div>'+
   '<h2>Contents<span class="p2x-dot">.</span></h2><p>四個篇章 · 十二個欄目 / THE CITY OF LIGHT</p></header>'+
   '<div class="p2-cereal-reader__chapters">'+groupList("p2x-cereal-movement",{entryStyle:"standard"})+'</div>'+
   '<footer class="p2-cereal-reader__tail">THE WESTSIDE WATCH · INDEX / 01–12</footer></div>';
  document.body.appendChild(reader);
  reader.querySelector(".p2-cereal-reader__close").addEventListener("click",closeReader);
  reader.addEventListener("click",e=>{if(e.target===reader)closeReader()});
  readerKeyHandler=e=>{
   if(e.key==="Escape"){e.preventDefault();closeReader()}
   if(e.key==="Tab"){
    const close=reader?.querySelector(".p2-cereal-reader__close");
    if(close){e.preventDefault();close.focus()}
   }
  };
  document.addEventListener("keydown",readerKeyHandler);
  reader.querySelector(".p2-cereal-reader__close").focus();
 }
 function select(id,history=true){
  if(!DESIGNS.some(d=>d.id===id))return;
  closeReader();
  active=id;
  const current=DESIGNS.find(d=>d.id===active);
  tile.dataset.p2Design=active;
  host.className="p2x p2x--"+active;
  host.innerHTML=renderers[active]();
  // Each variant has its own keyboard-reachable editorial reading surface.
  host.tabIndex=0;
  host.querySelectorAll(".p2x-aperture-groups,.p2x-coeval-stairs,.p2x-surplus-mosaic,.p2x-aa-strips,.p2x-aa-column,.p2x-circular-list,.p2x-remote-constellation,.p2x-form-index,.p2x-swiss-quadrants,.p2x-orbit-index,.p2x-cereal-stack,.p2x-w-chapters,.p2x-eye-register").forEach(el=>{
   el.tabIndex=0;el.setAttribute("role","region");el.setAttribute("aria-label","可捲動的十二欄目目錄");
  });
  if(active==="10"){
   const scroller=host.querySelector(".p2x-cereal-stack");
   const chapters=[...scroller.querySelectorAll(".p2x-cereal-movement")];
   const jumps=[...host.querySelectorAll("[data-p2-cereal-jump]")];
   const status=host.querySelector(".p2x-cereal-progress");
   let currentChapter=-1;
   const sync=()=>{
    let chapter=0;
    chapters.forEach((el,i)=>{if(el.offsetTop-scroller.offsetTop<=scroller.scrollTop+24)chapter=i});
    if(chapter!==currentChapter){
     currentChapter=chapter;
     jumps.forEach((b,i)=>{
      b.setAttribute("aria-current",i===chapter?"location":"false");
     });
    }
    if(status)status.textContent=scroller.scrollHeight>scroller.clientHeight+3?
       (scroller.scrollTop+scroller.clientHeight>=scroller.scrollHeight-3?
        "END / 12":"SCROLL / "+String(chapter+1).padStart(2,"0")+" OF 04"):"INDEX / COMPLETE";
   };
   host.querySelector(".p2x-cereal-expand")?.addEventListener("click",e=>openReader(e.currentTarget));
   scroller.addEventListener("scroll",sync,{passive:true});
   jumps.forEach((b,i)=>b.addEventListener("click",()=>{
    const target=chapters[i];
    const top=target.getBoundingClientRect().top-scroller.getBoundingClientRect().top+scroller.scrollTop;
    scroller.scrollTo({top,behavior:matchMedia("(prefers-reduced-motion: reduce)").matches?"instant":"smooth"});
   }));
   sync();
  }
  host.setAttribute("aria-label","Contents study "+active+" — "+current.source+" / "+current.name);
  toolbar.querySelector(".p2-variant-toolbar__current").textContent=current.source+" / "+current.zh;
  toolbar.querySelectorAll("button[data-p2-variant]").forEach(b=>{
   const selected=b.dataset.p2Variant===active;
   b.setAttribute("aria-pressed",selected?"true":"false");
   b.tabIndex=selected?0:-1;
  });
  if(history&&!document.documentElement.classList.contains("dual-embed")){
   const url=new URL(location.href);url.searchParams.set("variant",active);
   historyReplace(url);
  }
  const slider=document.getElementById("dual-progress");
  if(slider)slider.dispatchEvent(new Event("input",{bubbles:true}));
 }
 function historyReplace(url){window.history.replaceState(null,"",url)}
 toolbar.addEventListener("click",event=>{
  const b=event.target.closest("button[data-p2-variant]");
  if(b)select(b.dataset.p2Variant);
 });
 toolbar.addEventListener("keydown",event=>{
  const buttons=[...toolbar.querySelectorAll("button[data-p2-variant]")];
  const index=buttons.findIndex(b=>b.dataset.p2Variant===active);
  if(event.key==="ArrowRight"||event.key==="ArrowLeft"){
   const delta=event.key==="ArrowRight"?1:-1;
   const next=buttons[(index+delta+buttons.length)%buttons.length];
   select(next.dataset.p2Variant);next.focus();event.preventDefault();
  }
 });
 window.addEventListener("message",event=>{
  if(event.origin!==location.origin||event.data?.type!=="p2-contents-variant")return;
  select(String(event.data.variant||""),false);
 });
 window.P2ContentsTwelve={
  get active(){return active},
  get glyph(){
   // The phone composition stacks the Doré plate above the readable index.
   // Keep the official interim glyph within that art area, away from the star.
   if(active==="10" && tile.getBoundingClientRect().width<520)
    return [.24,.34,.57,.035,.94];
   return DESIGNS.find(d=>d.id===active).glyph;
  },
  get designs(){return DESIGNS.map(d=>({id:d.id,source:d.source,name:d.name,zh:d.zh}))},
  get count(){return host.querySelectorAll(".p2x-entry").length},
  select,
  get groups(){return groups.map(g=>({name:g.key,count:g.entries.length}))}
 };
 select(active,false);
})();
