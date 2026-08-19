/* ONE Pentateuch cover runtime sync.
 * Guarantees audited Doré mappings for books 2–5 are visible to the canonical
 * registry and re-applied after all book data/app scripts have settled.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!D||!R)return;

  const syncRegistry=()=>{
    R.maps=R.maps||{};
    [2,3,4,5].forEach(bookNumber=>{
      const mapping=D.studyBooks?.[bookNumber]?.canonicalDoreMapping;
      if(mapping&&typeof mapping==="object") R.maps[bookNumber]={...mapping};
    });
  };

  const refresh=()=>{
    syncRegistry();
    const policy=window.ONE_COVER_POLICY;
    if(!policy)return;
    [2,3,4,5].forEach(bookNumber=>policy.applyBook?.(bookNumber));
    policy.applyAll?.();

    /* If the current chapter is one of the newly loaded Pentateuch books,
     * force the visible cover element to the canonical resolver result now.
     */
    const currentBook=Number(D.current?.book);
    const currentChapter=Number(D.current?.nextChapter||1);
    if(currentBook>=2&&currentBook<=5){
      const art=policy.getCover?.(currentBook,currentChapter);
      const img=document.getElementById("chapter-cover-art");
      const credit=document.getElementById("chapter-art-credit");
      if(img){
        if(art?.src){img.src=art.src;img.alt=art.alt||"";img.hidden=false;}
        else{img.removeAttribute("src");img.alt="";img.hidden=true;}
      }
      if(credit){
        if(art?.source){credit.href=art.source;credit.textContent=art.title||"Gustave Doré";credit.hidden=false;}
        else credit.hidden=true;
      }
    }
    document.documentElement.dataset.pentateuchCoverSync="ready";
  };

  syncRegistry();
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",()=>setTimeout(refresh,0),{once:true});
  else setTimeout(refresh,0);
  window.addEventListener("load",()=>setTimeout(refresh,0),{once:true});
})();
