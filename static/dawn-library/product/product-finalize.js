import { resourceManifest } from '../../js/resource-fabric-client.mjs';

const manifest=await resourceManifest();
const canonicalCount=Number(manifest?.workCount||0);
const LIBRARY_TYPES=new Set(['work','book','publication','manuscript']);
let applying=false;

function resourceTypeOf(node){
  return String(node?.dataset?.resourceType||node?.dataset?.type||'').trim().toLowerCase();
}

function finalizeLibrarySurface(){
  if(applying)return;
  applying=true;
  try{
    // Site editorial/recommendation surfaces do not belong inside Dawn Library.
    document.querySelectorAll('.editorial-lead').forEach(node=>node.remove());

    // The moving wall is only a renderer mechanism, never a named product section.
    document.querySelectorAll('.living-shelf > h2').forEach(node=>node.remove());

    // Dawn Library renders publication resources only. Global Resource Fabric may
    // contain AV/maps/tools, but those belong to their own product projections.
    document.querySelectorAll('[data-resource-type],[data-type]').forEach(node=>{
      const type=resourceTypeOf(node);
      if(type&&!LIBRARY_TYPES.has(type))node.remove();
    });

    // Archive Field and Library Index share the same canonical count authority.
    document.querySelectorAll('.archive-field-head small').forEach(node=>{
      node.textContent=`LIVE ARCHIVE / ${canonicalCount.toLocaleString()} WORKS`;
    });
    document.querySelectorAll('.archive-block p strong').forEach(node=>{
      node.textContent=canonicalCount.toLocaleString();
    });

    // Remove obsolete renderer wording from work-focus navigation.
    document.querySelectorAll('.focus-close').forEach(node=>{
      if(node.textContent?.includes('館藏流'))node.textContent='返回館藏';
    });

    document.documentElement.dataset.dawnLibraryFinal='true';
    document.documentElement.dataset.dawnLibraryCountAuthority='resource-manifest';
    document.documentElement.dataset.dawnLibraryProjection='publication-only';
  }finally{
    applying=false;
  }
}

finalizeLibrarySurface();
const host=document.querySelector('[data-shelves]');
if(host){
  new MutationObserver(finalizeLibrarySurface).observe(host,{childList:true,subtree:true});
}
