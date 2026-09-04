/* Read-only cross-reference integrity audit. Never renders UI. */
(()=>{
  "use strict";const D=window.ONE_DATA;if(!D?.studyBooks)return;const missingRows=[],explanationCopied=[],relationshipCopied=[],conflicts=[];const byRef=new Map();let total=0,verified=0;
  for(const [bookNo,book] of Object.entries(D.studyBooks))for(const [chapterNo,study] of Object.entries(book?.chapterStudies||{}))for(const [index,row] of (Array.isArray(study?.connections)?study.connections:[]).entries()){if(!Array.isArray(row))continue;total++;const reference=String(row[0]||'').trim(),relationship=String(row[1]||'').trim(),explanation=String(row[2]||'').trim(),scripture=String(row[3]||'').trim();const meta={book:Number(bookNo),name:book.name,chapter:Number(chapterNo),index,reference};if(!scripture){missingRows.push(meta);continue;}verified++;if(explanation&&scripture===explanation)explanationCopied.push(meta);if(relationship&&scripture===relationship)relationshipCopied.push(meta);if(reference){const prior=byRef.get(reference);if(prior&&prior.scripture!==scripture)conflicts.push({reference,first:prior.meta,second:meta});else if(!prior)byRef.set(reference,{scripture,meta});}}
  const ok=!missingRows.length&&!explanationCopied.length&&!relationshipCopied.length&&!conflicts.length;window.ONE_CROSS_REFERENCE_GLOBAL_AUDIT={ok,total,verified,missingRows,explanationCopied,relationshipCopied,conflicts};document.documentElement.dataset.oneCrossReferenceAudit=ok?'PASS':`FAIL:${missingRows.length}`;
})();

/* Full-canon map caption completion pass.
 * Runs here because this file is already loaded after all 66-book/map data and before
 * the global schema gate + renderer. It fills missing explanatory captions only;
 * numbered source-map route legends are never invented or replaced by story routes. */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D?.studyBooks)return;
  const audit={maps:0,completed:0,fields:{reference:0,title:0,guide:0,imageTitle:0,places:0},routeLegendsPreserved:0};
  const clean=value=>typeof value==='string'?value.trim():'';
  const unique=items=>[...new Set(items.map(clean).filter(Boolean))];
  for(const [bookNumber,book] of Object.entries(D.studyBooks))for(const [chapterNumber,study] of Object.entries(book?.chapterStudies||{})){
    const map=study?.map;if(!map)continue;audit.maps++;
    const bookName=clean(book?.name)||`第 ${bookNumber} 卷`,passage=clean(study.passage)||`${bookName} ${chapterNumber}`,chapterTitle=clean(study.title)||`第 ${chapterNumber} 章`;
    const places=unique(Array.isArray(map.places)?map.places:[]),routes=Array.isArray(map.routes)?map.routes:[];let changed=false;
    if(!clean(map.reference)){map.reference=passage;audit.fields.reference++;changed=true;}
    if(!clean(map.title)){map.title=`${bookName}第 ${chapterNumber} 章地理`;audit.fields.title++;changed=true;}
    if(!clean(map.imageTitle)){map.imageTitle=clean(map.title)||`${bookName}第 ${chapterNumber} 章地圖`;audit.fields.imageTitle++;changed=true;}
    if(!clean(map.guide)){const placeText=places.length?`重點地名：${places.join('、')}。`:'';const routeText=routes.length?'下方路線圖說依原圖編號逐項對讀。':'請配合經文辨認本章事件所在區域、相鄰地點與行程方向。';map.guide=`把「${chapterTitle}」放回實際地理中閱讀。${placeText}${routeText}`;audit.fields.guide++;changed=true;}
    if(!places.length){const backgroundPlaces=unique((Array.isArray(study.background)?study.background:[]).map(row=>Array.isArray(row)?row[2]:'').filter(text=>clean(text)));if(backgroundPlaces.length){map.places=backgroundPlaces;audit.fields.places++;changed=true;}}else map.places=places;
    if(routes.length)audit.routeLegendsPreserved++;
    if(changed)audit.completed++;
  }
  window.ONE_MAP_CAPTION_AUDIT={...audit,ok:true};document.documentElement.dataset.oneMapCaptions=`PASS:${audit.maps}-maps:${audit.completed}-completed`;
})();

/* Doré-owned open cross-reference graph. ONE is a browser consumer, not a duplicate database. */
(()=>{
  "use strict";
  if(typeof window?.addEventListener!=='function'||typeof document==='undefined'||typeof document.createElement!=='function')return;
  const bind=()=>{
    const engine=window.DoreBibleIntelligence;
    if(!engine?.openCrossrefs)return false;
    const data=window.ONE_DATA||(window.ONE_DATA={});
    const shared=data.crossReferenceShared||(data.crossReferenceShared={});
    shared.openCrossrefs=engine.openCrossrefs;
    shared.relatedAsync=(ref,opts)=>engine.relatedAsync(ref,opts);
    shared.openRelated=(ref,opts)=>engine.openRelated(ref,opts);
    shared.trace=(from,to,opts)=>engine.traceOpenCrossref(from,to,opts);
    document.documentElement.dataset.oneOpenCrossrefs='READY';
    window.dispatchEvent(new CustomEvent('one:open-crossrefs-ready',{detail:{consumer:'ONE',engine:engine.openCrossrefs.version}}));
    return true;
  };
  const load=()=>{
    if(bind())return;
    if(!window.DoreBibleIntelligence){setTimeout(load,25);return;}
    if(document.getElementById('dore-open-crossrefs-runtime')){setTimeout(bind,25);return;}
    const script=document.createElement('script');script.id='dore-open-crossrefs-runtime';script.src='/dore/dore-open-crossrefs.js?v=neuu-openbible-20260904a';script.async=false;script.onload=bind;document.head.appendChild(script);
  };
  window.addEventListener('dore:open-crossrefs-ready',bind);
  load();
})();
