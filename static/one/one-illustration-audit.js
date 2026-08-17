/* ONE cross-book illustration audit.
 * Runs after all book data/registries are loaded and before one-app.js.
 * Purpose: enforce shared illustration metadata and catch systemic problems
 * without making book-specific renderer patches.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;

  const issues=[];
  const report=(level,book,chapter,code,message,extra={})=>{
    const item={level,book,chapter,code,message,...extra};
    issues.push(item);
    const fn=level==="error"?console.error:level==="warn"?console.warn:console.info;
    fn(`[ONE illustration audit] ${book} ${chapter||""} ${code}: ${message}`,extra);
  };

  const expectedTestament=number=>Number(number)<=39?"OT":"NT";
  const normalizeType=art=>{
    if(art.type==="historical"||art.type==="generated")return art.type;
    if(art.generated===true||art.aiGenerated===true)return "generated";
    if(art.artist||art.source)return "historical";
    return "generated";
  };

  Object.entries(D.studyBooks).forEach(([number,volume])=>{
    if(!volume?.chapterStudies)return;
    const testament=expectedTestament(number);
    const seen=new Map();

    Object.entries(volume.chapterStudies).forEach(([chapter,study])=>{
      const art=study?.illustration;
      if(!art)return;

      if(!art.src||typeof art.src!=="string"){
        report("error",volume.name,chapter,"missing-src","Illustration metadata has no usable src; removing visual only.");
        delete study.illustration;
        return;
      }

      art.type=normalizeType(art);
      art.testament=art.testament||testament;
      art.morningStar=Boolean(art.morningStar);
      art.alt=String(art.alt||`${volume.name}第 ${chapter} 章插圖`);
      art.title=String(art.title||`${volume.name} ${chapter}`);

      if(art.type==="historical"){
        art.artist=String(art.artist||"Historical engraving");
        if(!art.source)report("warn",volume.name,chapter,"historical-no-source","Historical illustration has no source URL.",{src:art.src});
      }else if(art.type==="generated"){
        art.artist=String(art.artist||"ONE Studio");
      }

      if(art.testament!==testament){
        report("error",volume.name,chapter,"testament-mismatch",`Expected ${testament} art but metadata says ${art.testament}; removing visual only.`,{src:art.src,title:art.title});
        delete study.illustration;
        return;
      }

      const prior=seen.get(art.src);
      if(prior){
        report("warn",volume.name,chapter,"duplicate-src",`Same illustration is also used in chapter ${prior}. Reuse requires an explicit same-event justification.`,{src:art.src,previousChapter:prior});
      }else seen.set(art.src,chapter);

      if(art.relation==="related"){
        report("warn",volume.name,chapter,"related-not-direct","Related historical art is not automatically canonical chapter art; review against the mother rule.",{src:art.src,title:art.title});
      }
    });
  });

  const errors=issues.filter(item=>item.level==="error").length;
  const warnings=issues.filter(item=>item.level==="warn").length;
  window.ONE_ILLUSTRATION_AUDIT={issues,errors,warnings,ranAt:new Date().toISOString()};
  document.documentElement.dataset.oneIllustrationAudit=errors?"errors":warnings?"warnings":"clean";
})();