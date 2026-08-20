/* ONE Studio binary runtime bridge.
 * Reconstructs verified text-staged binary assets in-browser when the repository connector
 * cannot persist binary files directly. Keep this generic and remove individual manifests
 * after canonical binary assets are committed.
 */
(()=>{
  "use strict";
  const manifests=[{
    key:"25:3",
    book:25,
    chapter:3,
    mime:"image/avif",
    bytes:92695,
    parts:13,
    base:"https://raw.githubusercontent.com/westsidewatch/westsidewatch.github.io/ad83a77c921f97e309e072b406a501d4e414fef9/.dore-upload/lam03-hq/part-",
    source:"https://github.com/westsidewatch/westsidewatch.github.io/tree/main/.dore-upload/lam03-hq"
  }];
  const urls=window.ONE_STUDIO_RUNTIME_ASSETS=window.ONE_STUDIO_RUNTIME_ASSETS||{};
  const pad=n=>String(n).padStart(3,"0");
  const decode=encoded=>{
    const clean=encoded.replace(/\s+/g,"");
    const raw=atob(clean),bytes=new Uint8Array(raw.length);
    for(let i=0;i<raw.length;i+=1)bytes[i]=raw.charCodeAt(i);
    return bytes;
  };
  const validAvif=bytes=>bytes.length>12&&String.fromCharCode(...bytes.slice(4,12))==="ftypavif";
  const activeKey=()=>{
    const title=document.querySelector("#current-book-title")?.textContent?.trim();
    const chapter=document.querySelector(".chapter-cover-chapter strong")?.textContent||"";
    if(title==="耶利米哀歌"&&/第\s*3\s*章/.test(chapter))return "25:3";
    return null;
  };
  const applyActive=()=>{
    const key=activeKey(),url=key&&urls[key];
    if(!url)return;
    const art=document.querySelector("#chapter-cover-art"),now=document.querySelector(".now");
    if(art){art.src=url;art.alt="耶利米哀歌第三章：多雷式黑白版畫";art.hidden=false;}
    const engraving=`url("${url}")`;
    now?.style.setProperty("--chapter-engraving",engraving);
    document.documentElement.style.setProperty("--one-chapter-engraving",engraving);
    document.documentElement.dataset.oneStudioRuntimeApplied=key;
  };
  const hydrate=async manifest=>{
    try{
      const parts=await Promise.all(Array.from({length:manifest.parts},async(_,i)=>{
        const response=await fetch(`${manifest.base}${pad(i)}.b64`,{cache:"no-store",mode:"cors"});
        if(!response.ok)throw new Error(`part ${i}: HTTP ${response.status}`);
        return response.text();
      }));
      const bytes=decode(parts.join(""));
      if(bytes.length!==manifest.bytes)throw new Error(`byte mismatch ${bytes.length} != ${manifest.bytes}`);
      if(manifest.mime==="image/avif"&&!validAvif(bytes))throw new Error("invalid AVIF signature");
      const url=URL.createObjectURL(new Blob([bytes],{type:manifest.mime}));
      urls[manifest.key]=url;
      const study=window.ONE_DATA?.studyBooks?.[manifest.book]?.chapterStudies?.[manifest.chapter];
      if(study?.illustration){study.illustration.src=url;study.illustration.source=manifest.source;study.illustration.assetVerified=true;study.illustration.runtimeBinary=true;}
      document.documentElement.dataset.oneStudioRuntimeBinary=manifest.key;
      applyActive();
    }catch(error){
      console.error("[ONE Studio binary runtime]",manifest.key,error);
      document.documentElement.dataset.oneStudioRuntimeBinaryError=manifest.key;
    }
  };
  const observer=new MutationObserver(()=>applyActive());
  const startObserver=()=>{const root=document.querySelector(".now")||document.body;if(root)observer.observe(root,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:["src","hidden"]});};
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",startObserver,{once:true});else startObserver();
  document.addEventListener("click",()=>queueMicrotask(applyActive),true);
  manifests.forEach(hydrate);
})();