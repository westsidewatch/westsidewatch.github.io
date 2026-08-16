/* 創世記：沒有可靠旅行地圖時不渲染地圖；沒有獨立插圖時清掉上一章殘影。 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const genesis=D?.genesis;
  const studies=genesis?.chapterStudies;
  if(!studies)return;

  ["1","5"].forEach(chapter=>{
    if(studies[chapter])studies[chapter].map=null;
  });

  Object.values(studies).forEach(study=>{
    if(study?.map&&Array.isArray(study.map.routes)&&study.map.routes.length===0){
      study.map.routes=null;
    }
  });

  /* Only a genuinely incomplete book should be unavailable.
   * Map/content audits are diagnostics: they must never make a fully loaded
   * 50-chapter Genesis disappear from the ONE cover after registration. */
  const complete=Array.from({length:50},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  if(!complete){
    if(D.studyBooks)delete D.studyBooks[1];
    document.documentElement.dataset.genesisReady="partial";
    console.error("[ONE Genesis] Book 01 unavailable because one or more chapter studies did not load.");
  }else{
    D.studyBooks=D.studyBooks||{};
    D.studyBooks[1]=genesis;
    document.documentElement.dataset.genesisReady="true";
    const mapAudit=document.documentElement.dataset.genesisMapAudit;
    const contentAudit=document.documentElement.dataset.genesisContentAudit;
    if(mapAudit!=="ok"||contentAudit!=="ok"){
      console.warn("[ONE Genesis] advisory audit warning",{mapAudit,contentAudit});
    }
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