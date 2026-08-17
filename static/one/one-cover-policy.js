/* ONE canonical cover policy — SOLE runtime illustration writer.
 * Load order is explicit in index.html:
 * one-dore-cover-registry.js -> one-dore-assets-241.js -> one-dore-round3-maps.js -> this file -> one-app.js.
 * No document.write, no fallback search, no secondary writer.
 *
 * Priority: P1 ORIGINAL_LOCKED > P2 OFFICIAL_PARALLEL > P3 HISTORICAL_MATCH >
 * P4 TYPOLOGY > P5 SEMANTIC_EXPANSION > P6 DEUTEROCANON_EXPANSION > P7 VISUAL_DIVERSITY.
 * P1 is immutable. Existing pages never outrank source correspondence.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const R=window.ONE_DORE_COVER_REGISTRY;
  if(!D||!R?.files||!R?.maps)return;

  const parseMap=raw=>{
    if(!raw)return {};
    if(typeof raw==="object")return raw;
    return Object.fromEntries(String(raw).split(",").filter(Boolean).map(pair=>{
      const [chapter,id]=pair.split(":");
      return [String(Number(chapter)),Number(id)];
    }));
  };

  const makeArt=id=>{
    const file=R.files?.[id];
    if(!file)return null;
    const title=R.titles?.[id]||`Doré plate ${String(id).padStart(3,"0")}`;
    return {
      src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=1280`,
      alt:`古斯塔夫・多雷版畫：${title}`,
      title,
      source:R.gallery||"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations",
      artist:"Gustave Doré",
      doreId:String(id).padStart(3,"0"),
      master:"ONE-DORE-241-MASTER-MAPPING"
    };
  };

  const clearLegacyCovers=()=>{
    Object.values(D.studyBooks||{}).forEach(book=>{
      Object.values(book?.chapterStudies||{}).forEach(study=>{
        if(!study||typeof study!=="object")return;
        delete study.illustration;
        delete study.illustrations;
        delete study.coverIllustration;
        delete study.coverImage;
      });
    });
  };

  const applyBook=bookNumber=>{
    const book=D.studyBooks?.[Number(bookNumber)];
    if(!book)return {applied:0,unresolved:[]};
    const mapping=parseMap(R.maps?.[Number(bookNumber)]??R.maps?.[String(bookNumber)]);
    let applied=0;
    const unresolved=[];
    Object.values(book.chapterStudies||{}).forEach(study=>{
      if(!study||typeof study!=="object")return;
      delete study.illustration;delete study.illustrations;delete study.coverIllustration;delete study.coverImage;
    });
    Object.entries(mapping).forEach(([chapter,id])=>{
      const study=book.chapterStudies?.[chapter];
      if(!study)return;
      const art=makeArt(Number(id));
      study.doreCover={id:String(id).padStart(3,"0"),title:R.titles?.[id],stage:"CANONICAL_MASTER",assetVerified:Boolean(art)};
      if(art){study.illustration=art;applied+=1;}else unresolved.push(`${bookNumber}:${chapter}:${String(id).padStart(3,"0")}`);
    });
    return {applied,unresolved};
  };

  const applyAll=()=>{
    clearLegacyCovers();
    let applied=0;const unresolved=[];
    Object.keys(D.studyBooks||{}).forEach(bookNumber=>{const result=applyBook(bookNumber);applied+=result.applied;unresolved.push(...result.unresolved);});
    R.appliedVerifiedAssets=applied;R.unresolvedAssets=unresolved;
    document.documentElement.dataset.oneCoverPolicy="canonical-master-only";
    document.documentElement.dataset.oneCoverApplied=String(applied);
    document.documentElement.dataset.oneCoverUnresolved=unresolved.join(",");
    return {applied,unresolved};
  };

  window.ONE_COVER_POLICY={
    mode:"CANONICAL_MASTER_ONLY",
    legacyCoverRulesEnabled:false,
    originalDoréPlacementLocked:true,
    builtPagesHavePriority:false,
    allocationPriority:Object.freeze({ORIGINAL_LOCKED:1,OFFICIAL_PARALLEL:2,HISTORICAL_MATCH:3,TYPOLOGY:4,SEMANTIC_EXPANSION:5,DEUTEROCANON_EXPANSION:6,VISUAL_DIVERSITY:7}),
    clearLegacyCovers,applyBook,applyAll,
    registerBookMapping(bookNumber,mapping){R.maps[Number(bookNumber)]=mapping;return applyBook(Number(bookNumber));},
    getCover(bookNumber,chapter){const mapping=parseMap(R.maps?.[Number(bookNumber)]??R.maps?.[String(bookNumber)]);const id=Number(mapping[String(Number(chapter))]);return id?makeArt(id):null;}
  };

  applyAll();
})();