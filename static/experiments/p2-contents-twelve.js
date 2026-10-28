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
  {id:"10",source:"Cereal",name:"Quiet Gallery",zh:"靜默畫廊",glyph:[.32,.66,.09,.26,.83]},
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
 "10":()=>'<div class="p2x-cereal-gallery"><div class="p2x-cereal-edition">THE CITY OF LIGHT <span>VOL. 00</span></div>'+
   '<span class="p2x-cereal-art-credit">GUSTAVE DORÉ<br>1866 / ORIGINAL PLATES</span></div>'+
   '<div class="p2x-cereal-paper"><span class="p2x-cereal-tiny">INDEX / WESTSIDE WATCH</span>'+
   '<h2>Contents.</h2><span class="p2x-cereal-chinese">目錄 · 十二個入口</span>'+
   '<div class="p2x-cereal-stack">'+groupList("p2x-cereal-movement",{entryStyle:"tight"})+'</div></div>',
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
 let active=DESIGNS.some(d=>d.id===params.get("variant"))?params.get("variant"):"01";
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
 function select(id,history=true){
  if(!DESIGNS.some(d=>d.id===id))return;
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
  get glyph(){return DESIGNS.find(d=>d.id===active).glyph},
  get designs(){return DESIGNS.map(d=>({id:d.id,source:d.source,name:d.name,zh:d.zh}))},
  get count(){return host.querySelectorAll(".p2x-entry").length},
  select,
  get groups(){return groups.map(g=>({name:g.key,count:g.entries.length}))}
 };
 select(active,false);
})();
