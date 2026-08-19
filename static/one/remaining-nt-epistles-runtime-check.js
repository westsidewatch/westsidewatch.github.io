/* ONE — GLOBAL STUDY SCHEMA GATE
 * Runs after all book-data files and before one-app.js.
 * Purpose: malformed chapter data must never render as broken characters or empty shells.
 * Legacy filename retained to avoid disturbing the proven load order.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D)return;
  const warnings=[],errors=[];
  const text=value=>value==null?"":String(value);
  const row=(value,size,label,book,chapter)=>{
    if(Array.isArray(value))return Array.from({length:size},(_,i)=>text(value[i]));
    if(value==null)return Array(size).fill("");
    warnings.push(`${book} ${chapter}: ${label} row normalized from scalar`);
    return [text(value),...Array(size-1).fill("")];
  };
  const array=value=>Array.isArray(value)?value:[];

  Object.entries(D.studyBooks||{}).forEach(([number,book])=>{
    const bookName=book?.name||`Book ${number}`;
    const chapters=array(book?.chapters);
    const studies=book?.chapterStudies&&typeof book.chapterStudies==="object"?book.chapterStudies:{};
    if(!chapters.length)errors.push(`${bookName}: chapters missing`);
    if(Object.keys(studies).length!==chapters.length)errors.push(`${bookName}: chapterStudies ${Object.keys(studies).length}/${chapters.length}`);

    chapters.forEach((chapterTitle,index)=>{
      const n=index+1,key=String(n),study=studies[key];
      if(!study){errors.push(`${bookName} ${n}: study missing`);return;}
      study.title=text(study.title||chapterTitle);
      study.passage=text(study.passage||`${bookName} ${n}`);
      study.movement=text(study.movement);
      study.story=text(study.story);
      study.position=text(study.position);
      study.route=array(study.route).map(item=>row(item,2,"route",bookName,n));
      study.background=array(study.background).map(item=>row(item,3,"background",bookName,n));
      study.scout=array(study.scout).map(text);
      study.connections=array(study.connections).map(item=>row(item,3,"connections",bookName,n));
      study.harmony=array(study.harmony).map(item=>row(item,3,"harmony",bookName,n));
      study.questions=array(study.questions).map(text);
      study.prepare=array(study.prepare).map(text);

      if(study.timeline){
        study.timeline.title=text(study.timeline.title||"書卷時序");
        study.timeline.range=text(study.timeline.range||study.passage);
        study.timeline.note=text(study.timeline.note);
        study.timeline.events=array(study.timeline.events).map(item=>row(item,3,"timeline.events",bookName,n));
      }
      if(study.map){
        study.map.places=array(study.map.places).map(text);
        study.map.routes=array(study.map.routes).map(item=>row(item,3,"map.routes",bookName,n));
        if(!study.map.image||!study.map.source){
          warnings.push(`${bookName} ${n}: incomplete map suppressed`);
          delete study.map;
        }
      }
    });
  });

  /* Empty optional modules are not errors. Hide their empty rendered shells globally.
   * This keeps books with intentionally omitted harmony/cross-reference modules from
   * producing blank pages, while preserving every populated module unchanged.
   */
  const detail=document.getElementById("chapter-detail");
  const cleanEmptyOptionalModules=()=>{
    if(!detail)return;
    detail.querySelectorAll(".connection-section").forEach(section=>{
      if(!section.querySelector(".connection-grid > article"))section.hidden=true;
    });
    detail.querySelectorAll("table.harmony").forEach(table=>{
      if(!table.querySelector("tbody tr"))table.closest(".chapter-section")?.setAttribute("hidden","");
    });
  };
  if(detail){
    const observer=new MutationObserver(cleanEmptyOptionalModules);
    observer.observe(detail,{childList:true,subtree:true});
    queueMicrotask(cleanEmptyOptionalModules);
  }

  const expected={45:16,46:16,47:13,48:6,49:6,50:4,51:4,54:6,55:4,56:3,57:1,59:5,60:5,61:3,62:5,63:1,64:1,65:1};
  const missing=Object.entries(expected).filter(([n,c])=>{const b=D.studyBooks?.[n];return !b||b.chapters?.length!==c||Object.keys(b.chapterStudies||{}).length!==c;});
  window.ONE_REMAINING_NT_EPISTLES_AUDIT={expectedBooks:18,expectedChapters:100,missing:missing.map(([n])=>Number(n)),ok:missing.length===0};
  window.ONE_STUDY_SCHEMA_AUDIT={books:Object.keys(D.studyBooks||{}).length,errors,warnings,ok:errors.length===0};
  document.documentElement.dataset.remainingNtEpistlesAudit=missing.length?'FAIL:'+missing.map(([n])=>n).join(','):'PASS:18-books-100-chapters';
  document.documentElement.dataset.oneStudySchema=errors.length?`FAIL:${errors.length}`:`PASS:${Object.keys(D.studyBooks||{}).length}-books`;
  if(errors.length)console.error("ONE study schema errors",errors);
  if(warnings.length)console.warn("ONE study schema normalized warnings",warnings);
})();
