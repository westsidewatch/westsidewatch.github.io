/* ONE Studio compatibility runtime.
 * Presentation-only compatibility plus an explicit, cache-busted bind for the approved
 * Lamentations 3 Studio cover. This runs after ONE_COVER_POLICY and before one-app.js,
 * so the app receives the final illustration source on first render.
 */
(()=>{
  "use strict";
  if(!document.getElementById("one-cover-no-divider")){
    const style=document.createElement("style");
    style.id="one-cover-no-divider";
    style.textContent=".chapter-cover-chapter::before{display:none!important;content:none!important;}";
    document.head.append(style);
  }
  const policy=window.ONE_COVER_POLICY?.directTestCovers?.[25]?.[3];
  const study=window.ONE_DATA?.studyBooks?.[25]?.chapterStudies?.[3];
  if(policy&&study){
    const fresh={...policy,src:"/one/studio/lamentations-03-dore-studio-v1.webp?v=20260820g",source:"/one/studio/lamentations-03-dore-studio-v1.webp",studioAssetId:"LAM-03-DORE-STUDIO-HQ-001"};
    study.illustration=fresh;
    study.studioCover={id:fresh.studioAssetId,stage:"DIRECT_BINARY",priority:"DIRECT_DORE_STUDIO",basis:"USER_APPROVED_DIRECT_ART",assetVerified:true};
    document.documentElement.dataset.oneLam03Runtime="hq-bound-20260820g";
  }
  document.documentElement.dataset.oneStudioBinaryRuntime="presentation-plus-lam03-hq-bind";
})();
