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

  /* Genesis chronology follows the narrative's own eras. The primeval and patriarchal
   * sections are not assigned invented absolute years; the purpose is to show where a
   * chapter sits in the book's biblical-history movement and what immediately surrounds it.
   */
  const genesisChronology=number=>{
    let range,era,note;
    if(number<=11){range="原初史 · 創世記 1–11";era="創造、墮落、洪水與巴別";note="原初史先於族長敘事；ONE 不把創1–11轉換成無法由經文本身確證的絕對年代。";}
    else if(number<=25){range="亞伯拉罕週期 · 創世記 12–25";era="亞伯拉罕蒙召、應許、立約與後裔";note="從創12起，敘事集中於亞伯拉罕與應許之地；年代只保留族長時期的相對位置。";}
    else if(number<=36){range="以撒與雅各週期 · 創世記 26–36";era="應許傳至以撒、雅各與十二支派之父";note="本段由以撒轉向雅各一家，逐步形成以色列十二支派的家族背景。";}
    else{range="約瑟週期 · 創世記 37–50";era="約瑟下埃及、家族遷居與族長時代收束";note="約瑟故事把迦南家族帶到埃及，為出埃及記的歷史舞台作準備。";}
    const study=studies[String(number)];
    return{title:"創世記時序",range,note,events:[[range,`創世記 ${number}`,study?.title||era],["整段位置",era,"以相對敘事時序為主，不製造虛假精確年代。"]],url:"https://bibleeveryone.com/bible-timeline.php"};
  };
  for(let number=1;number<=50;number+=1){
    const study=studies[String(number)];
    if(study&&(!study.timeline||!Array.isArray(study.timeline.events)||!study.timeline.events.length))study.timeline=genesisChronology(number);
  }

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