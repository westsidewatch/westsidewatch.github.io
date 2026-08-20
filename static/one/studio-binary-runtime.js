/* ONE Studio direct-binary runtime for Lamentations 3.
 * Uses the verified binary AVIF already committed in /static/one/studio/.
 * No Base64 text decoding, Blob URLs, or workflow dependency.
 */
(()=>{
  "use strict";
  if(!document.getElementById("one-cover-no-divider")){
    const style=document.createElement("style");
    style.id="one-cover-no-divider";
    style.textContent=".chapter-cover-chapter::before{display:none!important;content:none!important;}";
    document.head.append(style);
  }

  const bookNumber=25;
  const chapterNumber=3;
  const src="/one/studio/lamentations-03-dore-studio-v2.avif?v=20260820i";
  const source="/one/studio/lamentations-03-dore-studio-v2.avif";
  const study=window.ONE_DATA?.studyBooks?.[bookNumber]?.chapterStudies?.[chapterNumber];
  const policy=window.ONE_COVER_POLICY?.directTestCovers?.[bookNumber]?.[chapterNumber];
  if(!study){
    document.documentElement.dataset.oneLam03Runtime="missing-study";
    return;
  }

  const art={
    ...(policy||{}),
    src,
    source,
    alt:"耶利米哀歌第三章：多雷式黑白版畫",
    title:"Lamentations III · ONE Studio",
    artist:"Westside Watch Engraving Studio · Doré continuation",
    origin:"ONE_STUDIO_DORE_CONTINUATION",
    palette:"MONOCHROME_ENGRAVING",
    studioAssetId:"LAM-03-DORE-STUDIO-002",
    fixedStatus:"DIRECT_BINARY",
    master:"ONE-STUDIO-DIRECT-BINARY",
    assetVerified:true,
    directBinary:true
  };

  const apply=()=>{
    study.illustration={...art};
    study.studioCover={id:art.studioAssetId,stage:"DIRECT_BINARY",priority:"DIRECT_DORE_STUDIO",basis:"USER_APPROVED_DIRECT_ART",assetVerified:true};

    const title=document.getElementById("current-book-title")?.textContent?.trim();
    const chapter=document.querySelector(".chapter-cover-chapter strong")?.textContent||"";
    if(title!=="耶利米哀歌"||!chapter.includes("3"))return;

    const cover=document.getElementById("chapter-cover-art");
    const now=document.querySelector(".now");
    if(cover){
      if(cover.getAttribute("src")!==src)cover.src=src;
      cover.alt=art.alt;
      cover.hidden=false;
    }
    const engraving=`url("${src}")`;
    now?.style.setProperty("--chapter-engraving",engraving);
    document.documentElement.style.setProperty("--one-chapter-engraving",engraving);
    document.documentElement.dataset.oneLam03Runtime="direct-avif-ready-20260820i";
  };

  apply();
  document.addEventListener("DOMContentLoaded",apply,{once:true});
  window.addEventListener("hashchange",apply);
  document.addEventListener("click",()=>setTimeout(apply,0),true);
  new MutationObserver(apply).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["hidden","class"]});
  document.documentElement.dataset.oneStudioBinaryRuntime="lam03-direct-avif";
})();
