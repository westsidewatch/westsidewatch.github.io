/* ONE canonical illustration cleanup for every currently loaded book.
 * Runs after book data/registries and before the audit/renderer.
 * This is deliberately cross-book: legacy book files may keep their content,
 * while this layer removes systemic illustration misuse without book patches.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;

  const DIRECT_ONLY=new Set(["historical","generated"]);
  const normalize=(volume,chapter,art)=>{
    if(!art||typeof art!=="object"||!art.src)return null;
    const expected=Number(volume.number)<=39?"OT":"NT";
    const type=art.type||art.kind||(art.generated||art.aiGenerated?"generated":"historical");
    const relation=art.relation||"direct";
    if(!DIRECT_ONLY.has(type))return null;
    if(relation!=="direct")return null;
    if(art.testament&&art.testament!==expected)return null;
    return {
      ...art,
      type,
      kind:type,
      relation:"direct",
      testament:expected,
      morningStar:Boolean(art.morningStar),
      artist:art.artist||(type==="generated"?"ONE Studio":"Historical engraving"),
      alt:String(art.alt||`${volume.name}第 ${chapter} 章插圖`),
      title:String(art.title||`${volume.name} ${chapter}`)
    };
  };

  Object.values(D.studyBooks).forEach(volume=>{
    if(!volume?.chapterStudies)return;
    const seen=new Set();
    const pending=[];
    Object.entries(volume.chapterStudies).forEach(([chapter,study])=>{
      if(!study)return;
      const art=normalize(volume,chapter,study.illustration);
      delete study.illustration;
      if(!art){pending.push(Number(chapter));return;}
      /* Repeating one picture across multiple chapters is not a canonical cover.
       * Keep the first direct occurrence only; later chapters wait for their own art.
       */
      if(seen.has(art.src)){pending.push(Number(chapter));return;}
      seen.add(art.src);
      study.illustration=art;
    });
    volume.pendingGeneratedIllustrations=[...new Set([
      ...(Array.isArray(volume.pendingGeneratedIllustrations)?volume.pendingGeneratedIllustrations:[]),
      ...pending
    ])].filter(Number.isFinite).sort((a,b)=>a-b);
  });
})();