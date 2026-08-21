/* ONE — full-canon map caption completion pass.
 * Scope: every registered chapter map, after all 66-book data/map enrichments load.
 * It completes missing explanatory captions without inventing numbered source-map routes.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;
  const audit={maps:0,completed:0,fields:{reference:0,title:0,guide:0,imageTitle:0,places:0},routeLegendsPreserved:0};
  const clean=value=>typeof value==="string"?value.trim():"";
  const unique=items=>[...new Set(items.map(clean).filter(Boolean))];

  Object.entries(D.studyBooks).forEach(([bookNumber,book])=>{
    const bookName=clean(book?.name)||`第 ${bookNumber} 卷`;
    Object.entries(book?.chapterStudies||{}).forEach(([chapterNumber,study])=>{
      const map=study?.map;
      if(!map)return;
      audit.maps++;
      const passage=clean(study.passage)||`${bookName} ${chapterNumber}`;
      const chapterTitle=clean(study.title)||`第 ${chapterNumber} 章`;
      const places=unique(Array.isArray(map.places)?map.places:[]);
      const routes=Array.isArray(map.routes)?map.routes:[];
      let changed=false;

      if(!clean(map.reference)){map.reference=passage;audit.fields.reference++;changed=true;}
      if(!clean(map.title)){map.title=`${bookName}第 ${chapterNumber} 章地理`;audit.fields.title++;changed=true;}
      if(!clean(map.imageTitle)){map.imageTitle=clean(map.title)||`${bookName}第 ${chapterNumber} 章地圖`;audit.fields.imageTitle++;changed=true;}

      if(!clean(map.guide)){
        const placeText=places.length?`重點地名：${places.join('、')}。`:"";
        const routeText=routes.length?`下方路線圖說依原圖編號逐項對讀。`:"請配合經文辨認本章事件所在區域、相鄰地點與行程方向。";
        map.guide=`把「${chapterTitle}」放回實際地理中閱讀。${placeText}${routeText}`;
        audit.fields.guide++;changed=true;
      }

      /* Places are explanatory captions, not source-map route numbers. When a map has
       * no places list, derive only from explicit chapter background geography text;
       * never guess a place name from the image. */
      if(!places.length){
        const backgroundPlaces=unique((Array.isArray(study.background)?study.background:[])
          .map(row=>Array.isArray(row)?row[2]:"")
          .filter(text=>clean(text)));
        if(backgroundPlaces.length){map.places=backgroundPlaces;audit.fields.places++;changed=true;}
      }else map.places=places;

      /* Numbered route legends belong to the source map. Never replace an empty or
       * unknown legend with chapter-story routes: that would falsify the source map. */
      if(routes.length)audit.routeLegendsPreserved++;
      if(changed)audit.completed++;
    });
  });

  window.ONE_MAP_CAPTION_AUDIT={...audit,ok:true};
  document.documentElement.dataset.oneMapCaptions=`PASS:${audit.maps}-maps:${audit.completed}-completed`;
})();
