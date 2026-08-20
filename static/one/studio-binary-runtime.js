/* ONE Studio compatibility runtime.
 * The historical Lamentations 3 asset was committed as Base64 text under a .webp name.
 * Decode that payload once in-browser into a real image/webp Blob, then hand the Blob URL
 * to ONE before/after the normal chapter renderer as needed.
 */
(()=>{
  "use strict";
  if(!document.getElementById("one-cover-no-divider")){
    const style=document.createElement("style");
    style.id="one-cover-no-divider";
    style.textContent=".chapter-cover-chapter::before{display:none!important;content:none!important;}";
    document.head.append(style);
  }

  const bookNumber=25,chapterNumber=3;
  const encodedAsset="/one/studio/lamentations-03-dore-studio-v1.webp?v=20260820h";
  const sourceAsset="/one/studio/lamentations-03-dore-studio-v1.webp";
  const policy=window.ONE_COVER_POLICY?.directTestCovers?.[bookNumber]?.[chapterNumber];
  const study=window.ONE_DATA?.studyBooks?.[bookNumber]?.chapterStudies?.[chapterNumber];
  if(!policy||!study){
    document.documentElement.dataset.oneLam03Runtime="missing-study";
    return;
  }

  const base={...policy,source:sourceAsset,studioAssetId:"LAM-03-DORE-STUDIO-HQ-001"};
  study.illustration={...base,src:encodedAsset};
  study.studioCover={id:base.studioAssetId,stage:"DIRECT_BINARY",priority:"DIRECT_DORE_STUDIO",basis:"USER_APPROVED_DIRECT_ART",assetVerified:true};

  const applyDecoded=url=>{
    const art={...base,src:url};
    study.illustration=art;
    const cover=document.getElementById("chapter-cover-art");
    const now=document.querySelector(".now");
    const engraving=`url("${url}")`;
    if(cover&&document.getElementById("current-book-title")?.textContent?.includes("耶利米哀歌")){
      cover.src=url;
      cover.alt=art.alt||"耶利米哀歌第三章：多雷式黑白版畫";
      cover.hidden=false;
      now?.style.setProperty("--chapter-engraving",engraving);
      document.documentElement.style.setProperty("--one-chapter-engraving",engraving);
    }
    document.querySelectorAll(".chapter-illustration img").forEach(img=>{
      if(document.title.includes("耶利米哀歌 3"))img.src=url;
    });
    document.documentElement.dataset.oneLam03Runtime="decoded-webp-ready-20260820h";
  };

  fetch(encodedAsset,{cache:"no-store"})
    .then(response=>{if(!response.ok)throw new Error(`HTTP ${response.status}`);return response.text();})
    .then(text=>{
      const base64=text.replace(/\s+/g,"");
      const raw=atob(base64);
      const bytes=new Uint8Array(raw.length);
      for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
      if(raw.slice(0,4)!=="RIFF"||raw.slice(8,12)!=="WEBP")throw new Error("Decoded payload is not WEBP");
      const url=URL.createObjectURL(new Blob([bytes],{type:"image/webp"}));
      window.ONE_LAM03_HQ_OBJECT_URL=url;
      applyDecoded(url);
    })
    .catch(error=>{
      document.documentElement.dataset.oneLam03Runtime=`decode-failed:${String(error.message||error)}`;
      console.error("ONE Lamentations 3 WebP decode failed",error);
    });

  document.documentElement.dataset.oneStudioBinaryRuntime="lam03-base64-webp-decoder";
})();
