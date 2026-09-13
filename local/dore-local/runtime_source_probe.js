/* Doré Runtime Source Probe v0
 * Provider-neutral, request-scoped browser evidence collector.
 * It never downloads, stores, rehosts, or declares source authority.
 */
(function(global){
  'use strict';
  function attrs(node,names){const out={};for(const name of names){const value=node?.getAttribute?.(name);if(value)out[name]=value;}return out;}
  function abs(value){if(!value)return null;try{return new URL(value,document.baseURI).href;}catch{return String(value);}}
  function videos(){return [...document.querySelectorAll('video')].map(node=>({
    src:abs(node.getAttribute('src')), currentSrc:abs(node.currentSrc), poster:abs(node.poster||node.getAttribute('poster')), type:node.getAttribute('type')||null,
    duration:Number.isFinite(node.duration)?node.duration:null
  }));}
  function sources(){return [...document.querySelectorAll('video source,audio source,source')].map(node=>({src:abs(node.src||node.getAttribute('src')),type:node.type||node.getAttribute('type')||null,media:node.media||null}));}
  function tracks(){return [...document.querySelectorAll('track')].map(node=>({src:abs(node.src||node.getAttribute('src')),kind:node.kind||node.getAttribute('kind')||null,srclang:node.srclang||node.getAttribute('srclang')||null,label:node.label||null}));}
  function iframes(){return [...document.querySelectorAll('iframe')].map(node=>({src:abs(node.src||node.getAttribute('src')),title:node.title||null,allow:node.getAttribute('allow')||null}));}
  function images(){
    return [...document.images].map(node=>{
      const text=[node.alt,node.title,node.className,node.id,node.getAttribute('aria-label')].filter(Boolean).join(' ').toLowerCase();
      const semanticRole=/poster|thumbnail|thumb|hero|video/.test(text)?(/poster/.test(text)?'poster':/hero/.test(text)?'hero':'thumbnail'):null;
      return {src:abs(node.currentSrc||node.src),role:semanticRole,videoRelated:!!semanticRole,width:node.naturalWidth||null,height:node.naturalHeight||null};
    }).filter(item=>item.src);
  }
  function resources(){
    if(!global.performance?.getEntriesByType)return [];
    return global.performance.getEntriesByType('resource').map(entry=>({name:entry.name,initiatorType:entry.initiatorType||null,duration:entry.duration||null}));
  }
  function identity(){
    const title=document.querySelector('meta[property="og:title"]')?.content||document.querySelector('meta[name="twitter:title"]')?.content||document.title||null;
    const creator=document.querySelector('meta[name="author"]')?.content||document.querySelector('meta[property="article:author"]')?.content||null;
    const duration=videos().map(v=>v.duration).find(Number.isFinite)??null;
    return {title,creator,duration};
  }
  function collect(){return {schema:'dore.runtime-source-probe.v0',collector:'dore.runtime-source-probe.v0',url:location.href,identity:identity(),videos:videos(),sources:sources(),tracks:tracks(),iframes:iframes(),images:images(),resources:resources(),reflexPersistent:false,probeAuthority:false,rights:{rehost:false}};}
  global.DoreRuntimeSourceProbe={collect};
})(typeof window!=='undefined'?window:globalThis);
