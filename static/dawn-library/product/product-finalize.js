import { resourceManifest } from '../../js/resource-fabric-client.mjs';
import { createDawnCoverStream } from './cover-stream.js';

const manifest=await resourceManifest();
const canonicalCount=Number(manifest?.workCount||0);
const LIBRARY_TYPES=new Set(['work','book','publication','manuscript']);
let applying=false;

function resourceTypeOf(node){
  return String(node?.dataset?.resourceType||node?.dataset?.type||'').trim().toLowerCase();
}

function ensureCollectionSurface(){
  const lower=document.querySelector('#library-lower');
  if(!lower||document.querySelector('#dawn-cover-collection'))return;
  const right=lower.querySelector('.lower-right')||lower.lastElementChild;
  if(!right)return;
  const old=right.querySelector('.index-block');
  const surface=document.createElement('section');
  surface.id='dawn-cover-collection';
  surface.className='dawn-cover-collection';
  surface.setAttribute('aria-label','黎明書局館藏封面預覽');
  surface.innerHTML=`<header class="dawn-cover-collection__head"><div><span>COLLECTION SURFACE</span><strong>${canonicalCount.toLocaleString()} Works</strong></div><p>館藏封面按需浮現；完整 layout 與挑選動效留待全站重建。</p></header><div id="dawn-cover-stream" class="dawn-cover-collection__stream"></div>`;
  old?.replaceWith(surface);
  if(!document.querySelector('#dawn-cover-collection-style')){
    const style=document.createElement('style');style.id='dawn-cover-collection-style';style.textContent=`
      .dawn-cover-collection{min-height:0;flex:1;display:flex;flex-direction:column;padding-top:18px}
      .dawn-cover-collection__head{display:flex;justify-content:space-between;gap:24px;align-items:end;padding:0 0 14px;border-bottom:1px solid rgba(80,65,38,.18)}
      .dawn-cover-collection__head span{display:block;font:500 .52rem/1.2 Arial,sans-serif;letter-spacing:.16em;color:#8c6818}
      .dawn-cover-collection__head strong{display:block;margin-top:4px;font:400 clamp(1.5rem,2vw,2.5rem)/1 'Cormorant Garamond',serif}
      .dawn-cover-collection__head p{max-width:25rem;margin:0;font-size:.68rem;line-height:1.55;color:#756e62}
      .dawn-cover-collection__stream{position:relative;min-height:0;flex:1;overflow:auto;padding-top:16px}
      .dawn-cover-stream__status{position:sticky;top:0;z-index:3;width:max-content;margin-left:auto;padding:4px 7px;background:rgba(244,239,229,.92);font:500 .5rem/1 Arial,sans-serif;letter-spacing:.12em;color:#756e62}
      .dawn-cover-stream__rail{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:clamp(10px,1.2vw,20px) clamp(8px,1vw,16px);align-items:start}
      .dawn-cover-stream__work{min-width:0;border:0;background:none;padding:0;text-align:left;cursor:pointer;color:inherit}
      .dawn-cover-stream__work img,.dawn-cover-stream__fallback{display:block;width:100%;aspect-ratio:2/3;object-fit:cover;background:linear-gradient(145deg,#e8dfce,#d8c99d);border:1px solid rgba(80,65,38,.14)}
      .dawn-cover-stream__work span span{display:block}.dawn-cover-stream__work strong{display:block;margin-top:7px;font-size:.66rem;font-weight:400;line-height:1.25}.dawn-cover-stream__work small{display:block;margin-top:3px;font-size:.55rem;line-height:1.3;color:#756e62}
      .dawn-cover-stream__sentinel{height:2px}.dawn-cover-stream__work:focus-visible{outline:1px solid #8c6818;outline-offset:4px}
      @media(max-width:900px){.dawn-cover-collection__head{align-items:start;flex-direction:column}.dawn-cover-collection__stream{overflow:visible}.dawn-cover-stream__rail{grid-template-columns:repeat(3,minmax(0,1fr))}}
    `;document.head.appendChild(style);
  }
  createDawnCoverStream(surface.querySelector('#dawn-cover-stream'),{onSelect:item=>{
    window.dispatchEvent(new CustomEvent('dawn:cover-select',{detail:item}));
    document.querySelector('#library-top')?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
  }}).then(stream=>{surface.dataset.coverStream='ready';surface.dataset.coverWorkCount=String(stream.root.workCount)}).catch(error=>{surface.dataset.coverStream='failed';console.error('[Dawn Library] cover stream failed',error)});
}

function finalizeLibrarySurface(){
  if(applying)return;
  applying=true;
  try{
    document.querySelectorAll('.editorial-lead').forEach(node=>node.remove());
    document.querySelectorAll('.living-shelf > h2').forEach(node=>node.remove());
    document.querySelectorAll('[data-resource-type],[data-type]').forEach(node=>{
      const type=resourceTypeOf(node);
      if(type&&!LIBRARY_TYPES.has(type))node.remove();
    });
    document.querySelectorAll('.archive-field-head small').forEach(node=>{node.textContent=`LIVE ARCHIVE / ${canonicalCount.toLocaleString()} WORKS`;});
    document.querySelectorAll('.archive-block p strong').forEach(node=>{node.textContent=canonicalCount.toLocaleString();});
    document.querySelectorAll('.focus-close').forEach(node=>{if(node.textContent?.includes('館藏流'))node.textContent='返回館藏';});
    ensureCollectionSurface();
    document.documentElement.dataset.dawnLibraryFinal='true';
    document.documentElement.dataset.dawnLibraryCountAuthority='resource-manifest';
    document.documentElement.dataset.dawnLibraryProjection='publication-only';
  }finally{applying=false}
}

finalizeLibrarySurface();
const host=document.querySelector('[data-shelves]');
if(host)new MutationObserver(finalizeLibrarySurface).observe(host,{childList:true,subtree:true});
