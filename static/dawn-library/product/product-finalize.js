import { resourceManifest } from '../../js/resource-fabric-client.mjs';

const manifest=await resourceManifest();
const canonicalCount=Number(manifest?.workCount||0);
let applying=false;

function finalizeLibrarySurface(){
  if(applying)return;
  applying=true;
  try{
    // Site editorial/recommendation surfaces do not belong inside Dawn Library.
    document.querySelectorAll('.editorial-lead').forEach(node=>node.remove());

    // The moving wall is only a renderer mechanism, never a named product section.
    document.querySelectorAll('.living-shelf > h2').forEach(node=>node.remove());

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
  }finally{
    applying=false;
  }
}

finalizeLibrarySurface();
const host=document.querySelector('[data-shelves]');
if(host){
  new MutationObserver(finalizeLibrarySurface).observe(host,{childList:true,subtree:true});
}
