/* P2 / Emmaus — reader-facing Biblical setting and chapter outline.
 * Published ONE data remains read-only. This panel never displays internal
 * map production instructions, missing-source caveats or book-wide movements
 * as if they were the currently selected chapter.
 */
(()=>{'use strict';
 const root=document.getElementById('emmaus'),D=window.ONE_DATA;
 if(!root||!D?.books)return;
 const $=id=>document.getElementById(id);
 const figure=$('em-context-map-figure'),image=$('em-context-map-image'),
  eyebrow=$('em-context-map-eyebrow'),credit=$('em-context-map-credit'),
  guide=$('em-context-map-guide'),places=$('em-context-map-places'),
  mapTitle=$('em-context-map-title'),mapSource=$('em-context-map-source'),
  timelineEyebrow=$('em-context-time-eyebrow'),
  timelineTitle=$('em-context-time-title'),timelineNote=$('em-context-time-note'),
  timelineEvents=$('em-context-time-events');
 if(!figure||!timelineEvents||!guide||!mapTitle)return;
 const put=(node,value)=>{if(node)node.textContent=String(value??'')};
 const add=(parent,value,tag='span')=>{
  const el=document.createElement(tag);el.textContent=String(value??'');parent.append(el);return el;
 };
 const sourceFor=n=>n===42?D.luke:n===40?D.matthew:D.studyBooks?.[n];
 // Original ONE chapter data can contain directions to map editors. That
 // prose is not audience-facing copy and must never leak into these panels.
 const internal=/原圖|圖說|圖上|福圖[一二三四五六七八九十\d]|若.{0,8}圖|編號線路|必須|應保留|後備圖|完整版|完整保存|製圖|設計|縮減|ONE\s*(?:原始|正式)|資料來源|工作台|候選位置|頁面呈現/;
 const readerCopy=value=>typeof value==='string'&&!internal.test(value)?value.trim():'';
 function paintMap(map,study,n,ch){
  const valid=map&&typeof map==='object';
  const imageURL=valid&&typeof map.image==='string'&&/^https:\/\//.test(map.image)?map.image:null;
  put(eyebrow,imageURL?'01 / BIBLICAL ATLAS':'01 / BIBLICAL SETTING');
  put(mapTitle,readerCopy(map?.title)||readerCopy(map?.imageTitle)||'經文地點');
  guide.replaceChildren();
  let paragraph='';
  if(n===42&&ch===24){
   paragraph='婦女清早前往墳墓；兩個門徒從耶路撒冷走向以馬忤斯，認出復活的耶穌後返回耶路撒冷。最後，耶穌在伯大尼附近祝福門徒。';
  }else{
   paragraph=readerCopy(map?.guide)||readerCopy(map?.preface);
   if(!paragraph&&Array.isArray(study?.route)){
    paragraph=study.route.slice(0,2).map(x=>String(x?.[1]||'')).filter(Boolean).join('；')+'。';
   }
  }
  if(paragraph)add(guide,paragraph,'p');
  places.replaceChildren();
  if(valid&&Array.isArray(map.places)){
   for(const name of [...new Set(map.places)].slice(0,6)){
    if(name&&typeof name==='string'&&!internal.test(name))add(places,name);
   }
  }
  if(mapSource){
   mapSource.hidden=!valid||!map.source;
   if(valid&&map.source){mapSource.href=map.source;mapSource.textContent='查看相關地圖 ↗';}
  }
  figure.hidden=!imageURL;
  if(imageURL){
   if(image.dataset.mapSrc!==imageURL){image.dataset.mapSrc=imageURL;image.src=imageURL;}
   image.alt=readerCopy(map.imageTitle)||readerCopy(map.title)||'聖經地理圖';
   put(credit,readerCopy(map.imageTitle)||readerCopy(map.title));
  }else{image.removeAttribute('src');image.dataset.mapSrc='';}
 }
 function paintTimeline(study,n,ch){
  timelineEvents.replaceChildren();
  const timeline=study?.timeline;
  const isChronology=Array.isArray(timeline?.events)&&timeline.events.length>0;
  // Chapter-level events take priority. Book-wide movements (the source's
  // 5-section overview of all of Luke) are NOT the outline of Luke 24.
  const events=isChronology?timeline.events:
   Array.isArray(study?.route)?study.route:[];
  put(timelineEyebrow,isChronology?'02 / BIBLICAL CHRONOLOGY':'02 / CHAPTER OUTLINE');
  put(timelineTitle,isChronology?(readerCopy(timeline.title)||'經文時序'):'本章段落');
  let note=isChronology?readerCopy(timeline.note):readerCopy(study?.movement);
  if(n===42&&ch===24)note='從空墳墓、以馬忤斯路上，到耶穌向門徒顯現及升天。';
  put(timelineNote,note);
  for(const item of events.slice(0,10)){
   if(!Array.isArray(item))continue;
   const ref=item[0],description=item[1];
   if(!ref&&!description)continue;
   const li=document.createElement('li');
   if(ref)add(li,ref,'small');
   if(description)add(li,description,'strong');
   // item[2] often contains internal labels such as "書卷結構"; no such
   // source-origin marker belongs in an editorial Bible-reading interface.
   timelineEvents.append(li);
  }
  if(!timelineEvents.childElementCount){
   const li=document.createElement('li');
   add(li,'本章經文','small');
   add(li,'請選擇經文，逐節閱讀中文和英文譯本。','strong');
   timelineEvents.append(li);
  }
 }
 let selectedKey='',lastStudy=null;
 function render(book,chapter){
  const n=Number(book),ch=Number(chapter);
  if(!Number.isInteger(n)||n<1||n>66||!Number.isInteger(ch)||ch<1)return;
  const src=sourceFor(n),study=src?.chapterStudies?.[String(ch)]||null;
  const key=n+':'+ch;
  if(key===selectedKey&&lastStudy===study)return;
  selectedKey=key;lastStudy=study;
  paintMap(study?.map,study,n,ch);
  paintTimeline(study,n,ch);
 }
 root.addEventListener('p2:one-selection',e=>render(e.detail?.book,e.detail?.chapter));
 render(Number(root.dataset.selectedBook)||42,Number(root.dataset.selectedChapter)||24);
})();
