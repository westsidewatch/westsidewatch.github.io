/* 創世記：沒有可靠旅行地圖時不渲染地圖；沒有獨立插圖時清掉上一章殘影。 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const genesis=D?.genesis;
  const studies=genesis?.chapterStudies;
  if(!D||!genesis||!studies)return;

  ["1","5"].forEach(chapter=>{
    if(studies[chapter])studies[chapter].map=null;
  });

  Object.values(studies).forEach(study=>{
    if(study?.map&&Array.isArray(study.map.routes)&&study.map.routes.length===0){
      study.map.routes=null;
    }
  });

  /* Genesis availability must not be coupled to diagnostics or to a single
   * chapter-batch failure. If the core book object exists, keep Book 01
   * registered so the cover can always enter the book. Missing chapter data is
   * reported separately and the chapter grid can expose only what actually
   * loaded. This prevents one bad optional module from making the whole book
   * impossible to open. */
  D.studyBooks=D.studyBooks||{};
  D.studyBooks[1]=genesis;

  const missing=[];
  for(let number=1;number<=50;number+=1){
    if(!studies[String(number)])missing.push(number);
  }
  const complete=missing.length===0;
  document.documentElement.dataset.genesisReady=complete?"true":"partial";
  if(!complete){
    console.error(`[ONE Genesis] missing chapter studies: ${missing.join(", ")}. Book 01 remains available for diagnosis and access.`);
  }

  const mapAudit=document.documentElement.dataset.genesisMapAudit;
  const contentAudit=document.documentElement.dataset.genesisContentAudit;
  if(mapAudit!=="ok"||contentAudit!=="ok"){
    console.warn("[ONE Genesis] advisory audit warning",{mapAudit,contentAudit});
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