/* ONE Canon Index — shared read-only data layer for Atlas, Scripture Graph and Search.
 * One identity model: 66 books / 1,189 chapters. This module never mutates ONE_DATA.
 * Consumers must use chapter ids and URLs from this index rather than inventing local identities.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA,policy=window.ONE_COVER_POLICY;
  if(!D?.studyBooks||!policy)return;

  const flat=value=>{
    if(value==null)return[];
    if(typeof value==="string"||typeof value==="number")return[String(value)];
    if(Array.isArray(value))return value.flatMap(flat);
    if(typeof value==="object")return Object.values(value).flatMap(flat);
    return[];
  };
  const uniq=list=>[...new Set(list.filter(Boolean))];
  const clean=value=>String(value??"").replace(/\s+/g," ").trim();
  const normalize=value=>clean(value).toLocaleLowerCase("zh-Hant").normalize("NFKC");
  const mapId=map=>{
    if(Number.isInteger(map?.mapId))return map.mapId;
    const text=`${map?.source||""} ${map?.imageTitle||""}`;
    const m=text.match(/(?:m_id=|[（(])(\d{3})(?:[）)]|\b)/);
    return m?Number(m[1]):null;
  };

  const bookMeta=new Map();
  const aliases=[];
  for(const [key,book] of Object.entries(D.studyBooks)){
    const n=Number(key),meta={number:n,name:clean(book.name),nameEn:clean(book.nameEn),code:clean(book.enCode||book.code),zhCode:clean(book.zhCode||book.code)};
    bookMeta.set(n,meta);
    uniq([meta.name,meta.nameEn,meta.code,meta.zhCode]).filter(x=>x.length>=2).forEach(alias=>aliases.push({alias,normalized:normalize(alias),bookNumber:n}));
  }
  aliases.sort((a,b)=>b.normalized.length-a.normalized.length);

  const parseReferenceText=text=>{
    const source=clean(text);if(!source)return[];
    const out=[];
    for(const item of aliases){
      const escaped=item.alias.replace(/[.*+?^${}()|[\]\\]/g,"\\$&");
      const re=new RegExp(`${escaped}\\s*(\\d{1,3})(?::(\\d{1,3})(?:[–—-](\\d{1,3}))?)?`,"gi");
      let m;
      while((m=re.exec(source))){
        const chapter=Number(m[1]);const book=D.studyBooks[item.bookNumber];
        if(!book||chapter<1||chapter>(book.chapters?.length||0))continue;
        out.push({bookNumber:item.bookNumber,chapter,verseStart:m[2]?Number(m[2]):null,verseEnd:m[3]?Number(m[3]):null,raw:m[0]});
      }
    }
    return uniq(out.map(r=>JSON.stringify(r))).map(s=>JSON.parse(s));
  };

  const records=[],byId=Object.create(null),placeIndex=Object.create(null),mapIndex=Object.create(null),edges=[];
  const addPlace=(place,id)=>{const key=clean(place);if(!key)return;(placeIndex[key]||(placeIndex[key]=[])).push(id);};
  const addMap=(id,chapterId)=>{if(!id)return;(mapIndex[String(id)]||(mapIndex[String(id)]=[])).push(chapterId);};

  for(const [bookKey,book] of Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0]))){
    const bookNumber=Number(bookKey),meta=bookMeta.get(bookNumber),total=book.chapters?.length||0;
    for(let chapter=1;chapter<=total;chapter++){
      const study=book.chapterStudies?.[String(chapter)]||{};
      const id=`${String(bookNumber).padStart(2,"0")}:${String(chapter).padStart(3,"0")}`;
      const url=`/one/?book=${bookNumber}&chapter=${chapter}`;
      const places=uniq((study.map?.places||[]).map(clean));
      const currentMapId=mapId(study.map);
      const connections=flat(study.connections).map(clean).filter(Boolean);
      const harmony=flat(study.harmony).map(clean).filter(Boolean);
      const crossReferenceText=uniq([...connections,...harmony]);
      const references=uniq(crossReferenceText.flatMap(parseReferenceText).map(r=>JSON.stringify(r))).map(s=>JSON.parse(s));
      const cover=policy.getCover(bookNumber,chapter);
      const searchParts=[meta?.name,meta?.nameEn,meta?.code,chapter,study.title,study.passage,study.movement,study.story,study.position,...flat(study.background),...flat(study.scout),...connections,...harmony,...places,study.map?.title,study.map?.imageTitle,study.timeline?.title,study.timeline?.range,...flat(study.timeline?.events)];
      const record={
        id,bookNumber,book:meta?.name||book.name||"",bookEn:meta?.nameEn||book.nameEn||"",code:meta?.code||"",chapter,
        title:clean(study.title||book.chapters?.[chapter-1]||`第 ${chapter} 章`),passage:clean(study.passage||`${meta?.name||book.name} ${chapter}`),url,
        movement:clean(study.movement),story:clean(study.story),position:clean(study.position),
        places,map:study.map?{mapId:currentMapId,title:clean(study.map.title||study.map.imageTitle),source:study.map.source||"",image:study.map.image||""}:null,
        timeline:study.timeline?{title:clean(study.timeline.title),range:clean(study.timeline.range)}:null,
        connections:crossReferenceText,references,
        cover:cover?{origin:cover.origin||"",doreId:cover.doreId||null,studioAssetId:cover.studioAssetId||null,title:cover.title||"",src:cover.src||""}:null,
        modules:{map:Boolean(study.map),timeline:Boolean(study.timeline?.events?.length),connections:crossReferenceText.length>0,cover:Boolean(cover)},
        searchText:normalize(searchParts.join(" "))
      };
      records.push(record);byId[id]=record;places.forEach(place=>addPlace(place,id));addMap(currentMapId,id);
      references.forEach(ref=>{const targetId=`${String(ref.bookNumber).padStart(2,"0")}:${String(ref.chapter).padStart(3,"0")}`;if(targetId!==id)edges.push({source:id,target:targetId,type:"SCRIPTURE_REFERENCE",raw:ref.raw});});
    }
  }

  Object.values(placeIndex).forEach(list=>list.splice(0,list.length,...uniq(list)));
  Object.values(mapIndex).forEach(list=>list.splice(0,list.length,...uniq(list)));
  const edgeSeen=new Set();const graphEdges=edges.filter(edge=>{const key=`${edge.source}>${edge.target}:${edge.type}`;if(edgeSeen.has(key))return false;edgeSeen.add(key);return Boolean(byId[edge.source]&&byId[edge.target]);});
  const adjacency=Object.create(null);for(const edge of graphEdges){(adjacency[edge.source]||(adjacency[edge.source]=[])).push(edge);}

  const search=(query,options={})=>{
    const q=normalize(query);if(!q)return[];
    const terms=q.split(/\s+/).filter(Boolean);const limit=Math.max(1,Math.min(Number(options.limit)||30,200));
    const bookFilter=options.bookNumber?Number(options.bookNumber):null;const placeFilter=clean(options.place||"");
    return records.filter(r=>(!bookFilter||r.bookNumber===bookFilter)&&(!placeFilter||r.places.includes(placeFilter))).map(r=>{
      let score=0;const title=normalize(r.title),book=normalize(`${r.book} ${r.bookEn} ${r.code}`),passage=normalize(r.passage);
      if(title.includes(q))score+=12;if(book.includes(q))score+=10;if(passage.includes(q))score+=9;if(r.places.some(p=>normalize(p).includes(q)))score+=8;
      for(const term of terms)if(r.searchText.includes(term))score+=2;
      if(terms.every(term=>r.searchText.includes(term)))score+=5;
      return{record:r,score};
    }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.record.bookNumber-b.record.bookNumber||a.record.chapter-b.record.chapter).slice(0,limit).map(x=>({...x.record,score:x.score}));
  };
  const chaptersForPlace=place=>(placeIndex[clean(place)]||[]).map(id=>byId[id]);
  const chaptersForMap=id=>(mapIndex[String(Number(id))]||[]).map(chapterId=>byId[chapterId]);
  const neighbors=(id,direction="out")=>{
    if(direction==="in")return graphEdges.filter(e=>e.target===id).map(e=>({...e,chapter:byId[e.source]}));
    return(adjacency[id]||[]).map(e=>({...e,chapter:byId[e.target]}));
  };
  if(records.length!==1189)throw new Error(`[ONE Canon Index] expected 1189 chapter records, got ${records.length}`);
  const indexedIds=new Set(records.map(r=>r.id));if(indexedIds.size!==1189)throw new Error('[ONE Canon Index] duplicate chapter identity');

  window.ONE_CANON_INDEX=Object.freeze({
    mode:"ONE_CANON_INDEX_1189",version:"2026-08-19-v1",records:Object.freeze(records),byId,bookMeta,placeIndex,mapIndex,graphEdges:Object.freeze(graphEdges),
    get:(bookNumber,chapter)=>byId[`${String(Number(bookNumber)).padStart(2,"0")}:${String(Number(chapter)).padStart(3,"0")}`]||null,
    search,chaptersForPlace,chaptersForMap,neighbors,parseReferenceText,
    stats:Object.freeze({books:66,chapters:records.length,places:Object.keys(placeIndex).length,maps:Object.keys(mapIndex).length,graphEdges:graphEdges.length,searchable:records.filter(r=>r.searchText).length})
  });
  document.documentElement.dataset.oneCanonIndex=`PASS:1189:${Object.keys(placeIndex).length}-places:${graphEdges.length}-edges`;
})();
