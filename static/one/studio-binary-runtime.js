/* ONE Studio packed-binary runtime adapter.
 * Acceptance path for environments where approved binary bytes cannot be pushed directly.
 * Reads SAME-ORIGIN static base64 pack files, reconstructs one verified AVIF in memory,
 * and hands it to the existing cover renderer. No GitHub raw fetch, no Actions, no loader chain.
 */
(()=>{
  "use strict";
  const manifest={key:"25:3",book:25,chapter:3,mime:"image/avif",bytes:92695,parts:13,base:"/one/studio-packs/lam03/part-",source:"/one/studio-packs/lam03/manifest.json"};
  const pad=n=>String(n).padStart(3,"0");
  const decode=encoded=>{const clean=encoded.replace(/\s+/g,"");const raw=atob(clean),bytes=new Uint8Array(raw.length);for(let i=0;i<raw.length;i+=1)bytes[i]=raw.charCodeAt(i);return bytes;};
  const validAvif=bytes=>bytes.length>12&&String.fromCharCode(...bytes.slice(4,12))==="ftypavif";
  let objectUrl=null;
  const apply=()=>{
    if(!objectUrl)return;
    const study=window.ONE_DATA?.studyBooks?.[25]?.chapterStudies?.[3];
    if(study){study.illustration={...(study.illustration||{}),src:objectUrl,source:manifest.source,alt:"耶利米哀歌第三章：多雷式黑白版畫",title:"Lamentations III · ONE Studio",artist:"Westside Watch Engraving Studio · Doré continuation",origin:"ONE_STUDIO_DORE_CONTINUATION",studioAssetId:"LAM-03-DORE-STUDIO-001",assetVerified:true,packedBinary:true};}
    const title=document.querySelector("#current-book-title")?.textContent?.trim();const chapter=document.querySelector(".chapter-cover-chapter strong")?.textContent||"";
    if(title!=="耶利米哀歌"||!chapter.includes("3"))return;
    const art=document.querySelector("#chapter-cover-art"),now=document.querySelector(".now");if(art){art.src=objectUrl;art.alt="耶利米哀歌第三章：多雷式黑白版畫";art.hidden=false;}
    const engraving=`url("${objectUrl}")`;now?.style.setProperty("--chapter-engraving",engraving);document.documentElement.style.setProperty("--one-chapter-engraving",engraving);document.documentElement.dataset.oneStudioPackedBinary="25:3";
  };
  const hydrate=async()=>{try{const texts=[];for(let i=0;i<manifest.parts;i+=1){const response=await fetch(`${manifest.base}${pad(i)}.b64?v=20260820a`,{cache:"no-store"});if(!response.ok)throw new Error(`part ${i}: HTTP ${response.status}`);texts.push(await response.text());}const bytes=decode(texts.join(""));if(bytes.length!==manifest.bytes)throw new Error(`byte mismatch ${bytes.length} != ${manifest.bytes}`);if(!validAvif(bytes))throw new Error("invalid AVIF signature");objectUrl=URL.createObjectURL(new Blob([bytes],{type:manifest.mime}));apply();window.ONE_COVER_POLICY?.refreshStudioBook?.(25);apply();new MutationObserver(apply).observe(document.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["hidden","class"]});window.addEventListener("hashchange",apply);document.addEventListener("click",()=>setTimeout(apply,0),true);setInterval(apply,750);}catch(error){console.error("[ONE Studio packed binary]",error);document.documentElement.dataset.oneStudioPackedBinaryError="25:3";}};
  hydrate();
})();
