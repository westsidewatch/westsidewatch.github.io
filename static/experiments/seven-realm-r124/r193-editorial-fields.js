/* R193: one Scripture text field; chapter outline, questions and full source-map legend. */
(()=>{
"use strict";
const esc=x=>String(x??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll('"',"&quot;");
const title=(en,zh)=>'<h3 lang="en">'+esc(en)+'<small lang="zh-Hant">'+esc(zh)+'</small></h3>';
const arr=x=>Array.isArray(x)?x:[];
function structure(s,label,rows,divisions){
 const entries=divisions?divisions.map(([a,b,en,zh])=>[a+"–"+b,zh]):arr(s?.route).filter(x=>Array.isArray(x)&&x.length>=2).map(x=>[x[0],x[1]]);
 const range=rows?.length?rows[0].n+"–"+rows[rows.length-1].n:"";
 return title("Chapter Outline","本章結構 · "+label)+'<div class="chapter-outline-scroll">'+(entries.length?'<ol class="chapter-outline">'+entries.map(x=>'<li><span class="outline-range" lang="en">'+esc(x[0])+'</span><span lang="zh-Hant">'+esc(x[1])+'</span></li>').join("")+'</ol>':'<p class="chapter-outline-empty">'+esc(label)+(range?" · "+range+"節":"")+'</p>')+'</div>';
}
function questions(s){
 const qs=arr(s?.questions).filter(x=>typeof x==="string"&&x.trim());const prepare=arr(s?.prepare).filter(x=>typeof x==="string"&&x.trim());
 const items=qs.length?qs:prepare;
 return title("Reading Guide",qs.length?"研讀問題":"讀經導引")+'<div class="chapter-questions-scroll">'+(items.length?'<ol class="chapter-questions">'+items.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ol>':'<p class="chapter-outline-empty">閱讀整章，記下經文中的人物、事件與關鍵詞。</p>')+'</div>';
}
function formatRoute(x){return Array.isArray(x)?x.map(esc).join(" · "):esc(x)}
function geography(chapterMap,forced){
 if(!chapterMap)return title("Maps & Routes","地圖與路徑");
 const catalog=window.ONE_MAP_CATALOG||{};
 const match=forced||catalog[chapterMap.mapId]||Object.values(catalog).find(x=>x.image&&x.image===chapterMap.image);
 const source=match||chapterMap;
 const image=source.image||chapterMap.image,src=source.source||chapterMap.source,caption=source.imageTitle||source.title||chapterMap.title||"";
 const legend=arr(match?.routes),local=arr(chapterMap.routes);
 const guide=String(chapterMap.guide||"").replace(/若福圖五原圖包含相應編號線路，必須逐條保留完整圖說。/g,"");
 const figure=image?'<figure class="source-map"><img src="'+esc(image)+'" alt="'+esc(caption)+'" loading="eager"><p class="image-error">原圖暫未載入 · <a href="'+esc(image)+'">查看原圖</a></p><figcaption>'+esc(caption)+(src?' · <a href="'+esc(src)+'">原圖來源</a>':'')+'</figcaption></figure>':"";
 const section=(name,items,cls)=>items.length?'<section class="map-legend-section"><h4>'+name+'</h4><ol class="'+cls+'">'+items.map(x=>'<li>'+formatRoute(x)+'</li>').join("")+'</ol></section>':"";
 const contextual=match&&String(match.title).includes("被賣")&&String(chapterMap.reference||"").includes("路加福音 24")?'<p class="map-context-note">此圖呈現受難前後的耶路撒冷背景，並非復活日往以馬忤斯的完整路線。</p>':"";
 return title("Maps & Routes","地圖與路徑")+figure+'<div class="map-reading-field"><div class="map-chapter-context">'+(chapterMap.title?'<h4>'+esc(chapterMap.title)+'</h4>':'')+(guide?'<p>'+esc(guide)+'</p>':'')+contextual+(match&&local.length?section("本章路徑",local,"chapter-map-routes"):"")+'</div>'+section(match?"原圖編號圖說":"本章路徑",match?legend:local,"map-legend")+'</div>';
}
window.EMMAUS_EDITORIAL={structure,questions,geography};
})();