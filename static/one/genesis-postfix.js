/* Genesis compatibility layer — content/registry only.
 * Chapter illustrations are owned exclusively by ONE_COVER_POLICY.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const genesis=D?.genesis;
  const studies=genesis?.chapterStudies;
  if(!studies)return;

  ["1","5"].forEach(chapter=>{if(studies[chapter])studies[chapter].map=null;});
  Object.values(studies).forEach(study=>{if(study?.map&&Array.isArray(study.map.routes)&&study.map.routes.length===0)study.map.routes=null;});

  /* HKBS Chinese Scripture keeps the official dual-window page. */
  const useDualWindowHKBS=root=>{
    const scope=root?.querySelectorAll?root:document;
    scope.querySelectorAll('a[href*="rcuv.hkbs.org.hk/CUNP1/"], iframe[data-src*="rcuv.hkbs.org.hk/CUNP1/"], iframe[src*="rcuv.hkbs.org.hk/CUNP1/"]').forEach(node=>{
      for(const attribute of ["href","data-src","src"]){
        const value=node.getAttribute(attribute);
        if(value?.includes("rcuv.hkbs.org.hk/CUNP1/"))node.setAttribute(attribute,value.replace("/CUNP1/","/CUNP1s/"));
      }
    });
  };
  const scriptureObserver=new MutationObserver(records=>{
    records.forEach(record=>record.addedNodes.forEach(node=>{
      if(node.nodeType===1){
        useDualWindowHKBS(node);
        if(node.matches?.('a[href*="rcuv.hkbs.org.hk/CUNP1/"], iframe[data-src*="rcuv.hkbs.org.hk/CUNP1/"], iframe[src*="rcuv.hkbs.org.hk/CUNP1/"]'))useDualWindowHKBS(node.parentElement||document);
      }
    }));
  });
  scriptureObserver.observe(document.documentElement,{childList:true,subtree:true});
  useDualWindowHKBS(document);

  /* Shared registry guard retained because it protects already-loaded books. */
  const registry=(D.studyBooks&&typeof D.studyBooks==="object")?D.studyBooks:{};
  const descriptor=Object.getOwnPropertyDescriptor(D,"studyBooks");
  if(!descriptor||descriptor.configurable!==false){
    Object.defineProperty(D,"studyBooks",{
      enumerable:true,configurable:false,
      get(){return registry;},
      set(next){if(next&&typeof next==="object")Object.assign(registry,next);}
    });
  }
  D.registerStudyBook=(number,book)=>{
    const key=Number(number);
    if(!Number.isInteger(key)||key<1||key>66||!book){console.warn("[ONE Registry] invalid study book registration",{number,book});return false;}
    registry[key]=book;return true;
  };

  const complete=Array.from({length:50},(_,index)=>Boolean(studies[String(index+1)])).every(Boolean);
  const registerGenesis=()=>{D.registerStudyBook(1,genesis);document.documentElement.dataset.genesisReady=complete?"true":"partial";};
  registerGenesis();

  const mapAudit=document.documentElement.dataset.genesisMapAudit;
  const contentAudit=document.documentElement.dataset.genesisContentAudit;
  if(!complete||mapAudit!=="ok"||contentAudit!=="ok")console.warn("[ONE Genesis] advisory audit warning",{complete,mapAudit,contentAudit});

  const syncGenesisCoverEntry=()=>{
    registerGenesis();
    const item=document.querySelector('.cover-book[data-book="1"]');
    if(!item)return;
    item.classList.add("has-study");item.classList.remove("forthcoming");item.setAttribute("aria-label","第 1 卷，創世記，可開始查考");
  };
  document.addEventListener("DOMContentLoaded",()=>{syncGenesisCoverEntry();useDualWindowHKBS(document);});
})();