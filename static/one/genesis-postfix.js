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

  /* Keep Genesis registered whenever its study object exists.
   * Completeness and map/content audits are diagnostics only: they must never
   * remove Book 01 from the ONE cover or block the open-book flow. */
  const complete=Array.from({length:50},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  const registerGenesis=()=>{
    D.studyBooks=D.studyBooks||{};
    D.studyBooks[1]=genesis;
    document.documentElement.dataset.genesisReady=complete?"true":"partial";
  };
  registerGenesis();

  const mapAudit=document.documentElement.dataset.genesisMapAudit;
  const contentAudit=document.documentElement.dataset.genesisContentAudit;
  if(!complete||mapAudit!=="ok"||contentAudit!=="ok"){
    console.warn("[ONE Genesis] advisory audit warning",{complete,mapAudit,contentAudit});
  }

  const syncGenesisCoverEntry=()=>{
    registerGenesis();
    const item=document.querySelector('.cover-book[data-book="1"]');
    if(!item)return;
    item.classList.add("has-study");
    item.classList.remove("forthcoming");
    item.setAttribute("aria-label","第 1 卷，創世記，可開始查考");
  };

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
    /* Some later book bundles rebuild D.studyBooks. Reconcile Genesis after every
     * synchronous bundle has loaded, then align the already-rendered cover item. */
    syncGenesisCoverEntry();
    const detail=document.getElementById("chapter-detail");
    if(!detail)return;
    const observer=new MutationObserver(clearStaleArtwork);
    observer.observe(detail,{attributes:true,attributeFilter:["data-book","data-chapter"]});
    clearStaleArtwork();
  });
})();