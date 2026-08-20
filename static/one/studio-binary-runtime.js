/* ONE Studio direct-binary runtime adapter.
 * Production acceptance path: approved Studio artwork is a real same-origin AVIF file
 * committed under /static/one/studio/. No base64 reconstruction, Blob URL, or Actions dependency.
 */
(()=>{
  "use strict";
  const asset={
    key:"25:3",
    book:25,
    chapter:3,
    src:"/one/studio/lamentations-03-dore-studio-v2.avif?v=20260820b",
    source:"/one/studio/lamentations-03-dore-studio-v2.avif",
    alt:"耶利米哀歌第三章：多雷式黑白版畫",
    title:"Lamentations III · ONE Studio",
    artist:"Westside Watch Engraving Studio · Doré continuation",
    studioAssetId:"LAM-03-DORE-STUDIO-002"
  };

  const apply=()=>{
    const study=window.ONE_DATA?.studyBooks?.[asset.book]?.chapterStudies?.[asset.chapter];
    if(study){
      study.illustration={
        ...(study.illustration||{}),
        src:asset.src,
        source:asset.source,
        alt:asset.alt,
        title:asset.title,
        artist:asset.artist,
        origin:"ONE_STUDIO_DORE_CONTINUATION",
        studioAssetId:asset.studioAssetId,
        assetVerified:true,
        directBinary:true
      };
    }

    const title=document.querySelector("#current-book-title")?.textContent?.trim();
    const chapter=document.querySelector(".chapter-cover-chapter strong")?.textContent||"";
    if(title!=="耶利米哀歌"||!chapter.includes("3"))return;

    const art=document.querySelector("#chapter-cover-art");
    const now=document.querySelector(".now");
    if(art){
      if(art.getAttribute("src")!==asset.src) art.src=asset.src;
      art.alt=asset.alt;
      art.hidden=false;
    }
    const engraving=`url("${asset.src}")`;
    now?.style.setProperty("--chapter-engraving",engraving);
    document.documentElement.style.setProperty("--one-chapter-engraving",engraving);
    document.documentElement.dataset.oneStudioDirectBinary=asset.key;
  };

  const boot=()=>{
    apply();
    window.ONE_COVER_POLICY?.refreshStudioBook?.(asset.book);
    apply();
    new MutationObserver(apply).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["hidden","class"]});
    window.addEventListener("hashchange",apply);
    document.addEventListener("click",()=>setTimeout(apply,0),true);
    setInterval(apply,750);
  };

  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",boot,{once:true});
  else boot();
})();
