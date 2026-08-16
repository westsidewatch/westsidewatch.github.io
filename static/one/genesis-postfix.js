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

  /* ONE study-book registry guard.
   * Book bundles may add registrations, but assigning D.studyBooks must never
   * replace registrations that earlier bundles already installed. */
  const registry=(D.studyBooks&&typeof D.studyBooks==="object")?D.studyBooks:{};
  const descriptor=Object.getOwnPropertyDescriptor(D,"studyBooks");
  if(!descriptor||descriptor.configurable!==false){
    Object.defineProperty(D,"studyBooks",{
      enumerable:true,
      configurable:false,
      get(){return registry;},
      set(next){
        if(next&&typeof next==="object")Object.assign(registry,next);
      }
    });
  }
  D.registerStudyBook=(number,book)=>{
    const key=Number(number);
    if(!Number.isInteger(key)||key<1||key>66||!book){
      console.warn("[ONE Registry] invalid study book registration",{number,book});
      return false;
    }
    registry[key]=book;
    return true;
  };

  /* Keep Genesis registered whenever its study object exists.
   * Completeness and map/content audits are diagnostics only: they must never
   * remove Book 01 from the ONE cover or block the open-book flow. */
  const complete=Array.from({length:50},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  const registerGenesis=()=>{
    D.registerStudyBook(1,genesis);
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
    syncGenesisCoverEntry();
    const detail=document.getElementById("chapter-detail");
    const cover=document.getElementById("chapter-cover-art");
    if(cover){
      const restoreCoverVisibility=()=>{
        if(cover.hasAttribute("src")&&cover.getAttribute("src"))cover.hidden=false;
      };
      const coverObserver=new MutationObserver(restoreCoverVisibility);
      coverObserver.observe(cover,{attributes:true,attributeFilter:["src"]});
      restoreCoverVisibility();
    }
    if(!detail)return;
    const observer=new MutationObserver(clearStaleArtwork);
    observer.observe(detail,{attributes:true,attributeFilter:["data-book","data-chapter"]});
    clearStaleArtwork();
  });
})();