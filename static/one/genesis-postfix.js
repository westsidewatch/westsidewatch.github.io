/* 創世記：註冊保護、逐章 Doré 插圖與 ONE 經文版面修復。 */
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

  /* Every published Genesis chapter must carry an explicit illustration.
   * There is deliberately no fallback artwork: each chapter is mapped to the
   * closest matching Genesis plate from Gustave Doré's 1866 Bible series. */
  const plates={
    1:["001.The Creation of Light.jpg","The Creation of Light"],
    2:["002.The Creation of Eve.jpg","The Creation of Eve"],
    3:["003.Adam and Eve Are Driven out of Eden.jpg","Adam and Eve Are Driven out of Eden"],
    4:["004.Cain and Abel Offer Their Sacrifices.jpg","Cain and Abel Offer Their Sacrifices"],
    5:["005.Cain Slays Abel.jpg","Cain Slays Abel"],
    6:["006.The World Is Destroyed by Water.jpg","The World Is Destroyed by Water"],
    7:["007.The Great Flood.jpg","The Great Flood"],
    8:["008.A Dove Is Sent Forth from the Ark.jpg","A Dove Is Sent Forth from the Ark"],
    9:["009.Noah Curses Ham and Canaan.jpg","Noah Curses Ham and Canaan"],
    10:["010.The Tower of Babel.jpg","The Tower of Babel"],
    11:["011.Abraham Goes to the Land of Canaan.jpg","Abraham Goes to the Land of Canaan"],
    12:["012.Abraham and the Three Angels.jpg","Abraham and the Three Angels"],
    13:["013.Lot Flees as Sodom and Gomorrah Burn.jpg","Lot Flees as Sodom and Gomorrah Burn"],
    14:["014.Abraham Sends Hagar and Ishmael Away.jpg","Abraham Sends Hagar and Ishmael Away"],
    15:["015.Hagar and Ishmael in the Wilderness.jpg","Hagar and Ishmael in the Wilderness"],
    16:["016.The Testing of Abraham's Faith.jpg","The Testing of Abraham's Faith"],
    17:["017.The Burial of Sarah.jpg","The Burial of Sarah"],
    18:["018.Eliezer and Rebekah at the Well.jpg","Eliezer and Rebekah at the Well"],
    19:["019.The Meeting of Isaac and Rebekah.jpg","The Meeting of Isaac and Rebekah"],
    20:["020.Isaac Blesses Jacob.jpg","Isaac Blesses Jacob"],
    21:["021.Jacob's Dream.jpg","Jacob's Dream"],
    22:["022.Jacob Tends Laban's Flocks and Meets Rachel.jpg","Jacob Tends Laban's Flocks and Meets Rachel"],
    23:["023.Jacob Prays for Protection.jpg","Jacob Prays for Protection"],
    24:["024.Jacob Wrestles with the Angel.jpg","Jacob Wrestles with the Angel"],
    25:["025.Jacob and Esau Meet.jpg","Jacob and Esau Meet"],
    26:["026.Joseph Is Sold by His Brothers.jpg","Joseph Is Sold by His Brothers"],
    27:["027.Joseph Interprets Pharaoh's Dream.jpg","Joseph Interprets Pharaoh's Dream"],
    28:["028.Joseph Reveals Himself to His Brothers.jpg","Joseph Reveals Himself to His Brothers"],
    29:["029.Jacob Goes to Egypt.jpg","Jacob Goes to Egypt"]
  };
  const chapterPlate=[
    1,2,3,4,5,6,7,8,9,9,
    10,11,11,11,11,14,12,12,13,12,
    14,16,17,18,19,19,20,21,22,22,
    22,24,25,25,21,25,26,26,26,27,
    27,27,27,28,28,29,29,28,29,29
  ];
  const illustrationFor=plateNumber=>{
    const plate=plates[plateNumber];
    if(!plate)return null;
    const [filename,title]=plate;
    return {
      src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(filename)}`,
      source:`https://commons.wikimedia.org/wiki/File:${filename.replaceAll(" ","_")}`,
      title,
      alt:`古斯塔夫・多雷版畫：${title}`
    };
  };
  chapterPlate.forEach((plateNumber,index)=>{
    const study=studies[String(index+1)];
    const illustration=illustrationFor(plateNumber);
    if(study&&illustration)study.illustration=illustration;
  });
  const missingIllustrations=Array.from({length:50},(_,index)=>index+1).filter(chapter=>!studies[String(chapter)]?.illustration);
  if(missingIllustrations.length){
    console.error("[ONE Genesis] published chapters missing illustrations",missingIllustrations);
  }

  /* Give the HKBS Chinese page the full ONE reading width on desktop so its own
   * responsive layout can return to the two-column scripture presentation.
   * English NIV remains directly below it; mobile is unchanged as a single column. */
  const scriptureLayout=document.createElement("style");
  scriptureLayout.dataset.oneScriptureWidth="full";
  scriptureLayout.textContent=`
    @media (min-width:651px){
      .scripture-reading__pages{grid-template-columns:minmax(0,1fr)!important}
      .scripture-reading__pages article+article{border-left:0!important;border-top:1px solid var(--line)!important}
      .scripture-reading iframe{width:100%!important}
    }
  `;
  document.head.append(scriptureLayout);

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

  document.addEventListener("DOMContentLoaded",()=>{
    syncGenesisCoverEntry();
    const cover=document.getElementById("chapter-cover-art");
    if(cover){
      const restoreCoverVisibility=()=>{
        if(cover.hasAttribute("src")&&cover.getAttribute("src"))cover.hidden=false;
      };
      const coverObserver=new MutationObserver(restoreCoverVisibility);
      coverObserver.observe(cover,{attributes:true,attributeFilter:["src"]});
      restoreCoverVisibility();
    }
  });
})();