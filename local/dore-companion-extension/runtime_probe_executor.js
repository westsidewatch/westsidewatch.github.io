/* Generic browser executor for Doré runtime source probing. */
const LOAD_TIMEOUT_MS=20000;
const SETTLE_MS=1600;

function sleep(ms){return new Promise(resolve=>setTimeout(resolve,ms));}
async function waitForComplete(tabId){
  const started=Date.now();
  while(Date.now()-started<LOAD_TIMEOUT_MS){
    const tab=await browser.tabs.get(tabId);
    if(tab.status==='complete')return tab;
    await sleep(180);
  }
  throw new Error('runtime source page load timeout');
}

const COLLECTOR=`(()=>{
  const abs=value=>{if(!value)return null;try{return new URL(value,document.baseURI).href}catch(_){return String(value)}};
  const videos=[...document.querySelectorAll('video')].map(node=>({src:abs(node.getAttribute('src')),currentSrc:abs(node.currentSrc),poster:abs(node.poster||node.getAttribute('poster')),type:node.getAttribute('type')||null,duration:Number.isFinite(node.duration)?node.duration:null}));
  const sources=[...document.querySelectorAll('video source,audio source,source')].map(node=>({src:abs(node.src||node.getAttribute('src')),type:node.type||node.getAttribute('type')||null,media:node.media||null}));
  const tracks=[...document.querySelectorAll('track')].map(node=>({src:abs(node.src||node.getAttribute('src')),kind:node.kind||node.getAttribute('kind')||null,srclang:node.srclang||node.getAttribute('srclang')||null,label:node.label||null}));
  const iframes=[...document.querySelectorAll('iframe')].map(node=>({src:abs(node.src||node.getAttribute('src')),title:node.title||null,allow:node.getAttribute('allow')||null}));
  const images=[...document.images].map(node=>{const text=[node.alt,node.title,node.className,node.id,node.getAttribute('aria-label')].filter(Boolean).join(' ').toLowerCase();const semanticRole=/poster|thumbnail|thumb|hero|video/.test(text)?(/poster/.test(text)?'poster':/hero/.test(text)?'hero':'thumbnail'):null;return {src:abs(node.currentSrc||node.src),role:semanticRole,videoRelated:Boolean(semanticRole),width:node.naturalWidth||null,height:node.naturalHeight||null}}).filter(item=>item.src);
  const resources=performance.getEntriesByType?performance.getEntriesByType('resource').map(entry=>({name:entry.name,initiatorType:entry.initiatorType||null,duration:entry.duration||null})):[];
  const title=document.querySelector('meta[property="og:title"]')?.content||document.querySelector('meta[name="twitter:title"]')?.content||document.title||null;
  const creator=document.querySelector('meta[name="author"]')?.content||document.querySelector('meta[property="article:author"]')?.content||null;
  const duration=videos.map(v=>v.duration).find(Number.isFinite)??null;
  return {schema:'dore.runtime-source-probe.v0',collector:'dore.runtime-source-probe.v0',url:location.href,identity:{title,creator,duration},videos,sources,tracks,iframes,images,resources,reflexPersistent:false,probeAuthority:false,rights:{rehost:false}};
})()`;

export async function collectRuntimeSnapshot(url){
  let tab=null;
  try{
    tab=await browser.tabs.create({url,active:false});
    await waitForComplete(tab.id);
    await sleep(SETTLE_MS);
    const results=await browser.tabs.executeScript(tab.id,{code:COLLECTOR,runAt:'document_idle'});
    const snapshot=Array.isArray(results)?results.find(value=>value&&typeof value==='object'):null;
    if(!snapshot)throw new Error('runtime source probe returned no snapshot');
    return snapshot;
  }finally{
    if(tab?.id!=null){try{await browser.tabs.remove(tab.id)}catch(_error){}}
  }
}
