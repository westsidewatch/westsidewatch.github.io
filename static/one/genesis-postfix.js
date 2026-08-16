/* 創世記：沒有可靠旅行地圖時不渲染地圖；沒有獨立插圖時清掉上一章殘影。 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const studies=D?.genesis?.chapterStudies;
  if(!studies)return;

  ["1","5"].forEach(chapter=>{
    if(studies[chapter])studies[chapter].map=null;
  });

  Object.values(studies).forEach(study=>{
    if(study?.map&&Array.isArray(study.map.routes)&&study.map.routes.length===0){
      study.map.routes=null;
    }
  });

  const complete=Array.from({length:50},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  const mapAudit=document.documentElement.dataset.genesisMapAudit;
  const contentAudit=document.documentElement.dataset.genesisContentAudit;
  if(!complete||mapAudit!=="ok"||contentAudit!=="ok"){
    if(D.studyBooks)delete D.studyBooks[1];
    document.documentElement.dataset.genesisReady="partial";
    console.error("[ONE Genesis] fail-closed: Book 01 was not exposed because chapter/map/content audit is incomplete.");
  }

  const clearStaleArtwork=()=>{
    const detail=document.getElementById("chapter-detail");
    if(!detail||detail.dataset.book!=="1")return;
    const study=studies[String(detail.dataset.chapter||"")];
    if(study?.illustration)return;
    const now=document.querySelector(".now"),cover=document.getElementById("chapter-cover-art"),credit=document.getElementById("chapter-art-credit");
    now?.style.removeProperty("--chapter-engraving");
    document.documentElement.style.removeProperty("--one-chapter-engraving");
    if(cover){cover.removeAttribute("src");cover.alt="";cover.hidden=true;}
    if(credit){credit.removeAttribute("href");credit.textContent="";credit.hidden=true;}
  };

  document.addEventListener("DOMContentLoaded",()=>{
    const detail=document.getElementById("chapter-detail");
    if(!detail)return;
    const observer=new MutationObserver(clearStaleArtwork);
    observer.observe(detail,{attributes:true,attributeFilter:["data-book","data-chapter"]});
    clearStaleArtwork();
  });
})();