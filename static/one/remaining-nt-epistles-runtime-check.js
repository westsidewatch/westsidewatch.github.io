/* ONE — GLOBAL STUDY SCHEMA + 66-BOOK RELEASE GATE
 * Runs after all book-data files and before one-app.js.
 * Purpose: malformed or missing book/chapter data must never render as broken characters,
 * undefined labels, invalid Scripture URLs, empty shells, or a falsely complete canon.
 * Legacy filename retained to avoid disturbing the proven load order.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;if(!D)return;
  const warnings=[],errors=[];
  const text=value=>value==null?"":String(value);
  const array=value=>Array.isArray(value)?value:[];
  const warn=(book,chapter,message)=>warnings.push(`${book}${chapter?` ${chapter}`:""}: ${message}`);
  const row=(value,size,label,book,chapter)=>{
    if(Array.isArray(value))return Array.from({length:size},(_,i)=>text(value[i]));
    if(value==null)return Array(size).fill("");
    warn(book,chapter,`${label} row normalized from scalar`);
    return [text(value),...Array(size-1).fill("")];
  };

  Object.entries(D.studyBooks||{}).forEach(([number,book])=>{
    if(!book||typeof book!=="object"){errors.push(`Book ${number}: volume missing`);return;}
    const bookName=text(book.name)||`Book ${number}`;

    /* Renderer-facing volume contract. Preserve legacy aliases safely, but record drift. */
    if(!book.name){book.name=bookName;warn(bookName,null,"name normalized");}
    if(!book.nameEn){book.nameEn=text(book.en);if(book.nameEn)warn(bookName,null,"nameEn normalized from legacy en");}
    if(!book.nameEn)errors.push(`${bookName}: nameEn missing`);
    if(!book.zhCode){book.zhCode=text(book.code);if(book.zhCode)warn(bookName,null,"zhCode normalized from code");}
    if(!book.enCode){book.enCode=text(book.code);if(book.enCode)warn(bookName,null,"enCode normalized from code");}
    if(!book.zhCode||!book.enCode)errors.push(`${bookName}: Scripture code missing`);
    if(!book.summary){book.summary=bookName;warn(bookName,null,"summary fallback applied");}
    book.meta=array(book.meta);
    if(!book.meta.length){book.meta=[["位置",`第 ${number} 卷`],["核心線索","逐章研讀"]];warn(bookName,null,"meta fallback applied");}
    book.meta=book.meta.map(item=>row(item,2,"meta",bookName,null));
    if(!Array.isArray(book.movements)||!book.movements.length){
      if(Array.isArray(book.structure)&&book.structure.length){
        book.movements=book.structure.map((item,index)=>[String(index+1).padStart(2,"0"),text(item?.range),text(item?.title)]);
        warn(bookName,null,"movements normalized from legacy structure");
      }else{
        book.movements=[["01","全卷","逐章研讀"]];
        warn(bookName,null,"movements fallback applied");
      }
    }else book.movements=book.movements.map(item=>row(item,3,"movements",bookName,null));

    const chapters=array(book.chapters);
    const studies=book.chapterStudies&&typeof book.chapterStudies==="object"?book.chapterStudies:{};
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
      study.connections=array(study.connections).map(item=>row(item,4,"connections",bookName,n));
      study.harmony=array(study.harmony).map(item=>row(item,3,"harmony",bookName,n));
      study.questions=array(study.questions).map(text);
      study.prepare=array(study.prepare).map(text);

      if(study.timeline){
        study.timeline.title=text(study.timeline.title||"書卷時序");
        study.timeline.range=text(study.timeline.range||study.passage);
        study.timeline.note=text(study.timeline.note);
        study.timeline.events=array(study.timeline.events).map(item=>row(item,3,"timeline.events",bookName,n));
        study.timeline.url=text(study.timeline.url||"https://bibleeveryone.com/bible-timeline.php");
      }
      if(study.map){
        study.map.reference=text(study.map.reference||study.passage);
        study.map.title=text(study.map.title||`${bookName}地理`);
        study.map.guide=text(study.map.guide||"按經文明示辨認本章地理位置與路線。");
        study.map.imageTitle=text(study.map.imageTitle||study.map.title);
        study.map.preface=text(study.map.preface);
        study.map.places=array(study.map.places).map(text);
        study.map.routes=array(study.map.routes).map(item=>row(item,3,"map.routes",bookName,n));
        if(!study.map.image||!study.map.source){
          warn(bookName,n,"incomplete map suppressed");
          delete study.map;
        }
      }
    });
  });

  /* Empty optional modules are not errors. Hide their empty rendered shells globally. */
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

  /* Legacy 18-epistle audit retained for regression history. */
  const expectedEpistles={45:16,46:16,47:13,48:6,49:6,50:4,51:4,54:6,55:4,56:3,57:1,59:5,60:5,61:3,62:5,63:1,64:1,65:1};
  const missingEpistles=Object.entries(expectedEpistles).filter(([n,c])=>{const b=D.studyBooks?.[n];return !b||b.chapters?.length!==c||Object.keys(b.chapterStudies||{}).length!==c;});
  window.ONE_REMAINING_NT_EPISTLES_AUDIT={expectedBooks:18,expectedChapters:100,missing:missingEpistles.map(([n])=>Number(n)),ok:missingEpistles.length===0};
  document.documentElement.dataset.remainingNtEpistlesAudit=missingEpistles.length?'FAIL:'+missingEpistles.map(([n])=>n).join(','):'PASS:18-books-100-chapters';

  /* Canonical Protestant 66-book release gate. A future book batch cannot claim
   * completion merely because its files exist: every canonical book and all 1,189
   * chapters must be registered before the shared renderer starts. */
  const canonicalChapterCounts={1:50,2:40,3:27,4:36,5:34,6:24,7:21,8:4,9:31,10:24,11:22,12:25,13:29,14:36,15:10,16:13,17:10,18:42,19:150,20:31,21:12,22:8,23:66,24:52,25:5,26:48,27:12,28:14,29:3,30:9,31:1,32:4,33:7,34:3,35:3,36:3,37:2,38:14,39:4,40:28,41:16,42:24,43:21,44:28,45:16,46:16,47:13,48:6,49:6,50:4,51:4,52:5,53:3,54:6,55:4,56:3,57:1,58:13,59:5,60:5,61:3,62:5,63:1,64:1,65:1,66:22};
  const canonFailures=[];
  let registeredChapters=0;
  Object.entries(canonicalChapterCounts).forEach(([number,expectedCount])=>{
    const book=D.studyBooks?.[number],chapterCount=book?.chapters?.length||0,studyCount=Object.keys(book?.chapterStudies||{}).length;
    registeredChapters+=chapterCount;
    if(!book)canonFailures.push(`${number}:missing`);
    else if(chapterCount!==expectedCount||studyCount!==expectedCount)canonFailures.push(`${number}:${chapterCount}/${studyCount}/${expectedCount}`);
  });
  const extraBooks=Object.keys(D.studyBooks||{}).map(Number).filter(number=>!canonicalChapterCounts[number]);
  if(extraBooks.length)warn("Canon",null,`non-canonical studyBooks registered: ${extraBooks.join(",")}`);
  canonFailures.forEach(failure=>errors.push(`Canon 66: ${failure}`));
  const canonOk=canonFailures.length===0&&Object.keys(canonicalChapterCounts).length===66&&registeredChapters===1189;
  window.ONE_CANON_66_AUDIT={expectedBooks:66,expectedChapters:1189,registeredBooks:Object.keys(canonicalChapterCounts).filter(n=>D.studyBooks?.[n]).length,registeredChapters,failures:canonFailures,extraBooks,ok:canonOk};
  document.documentElement.dataset.oneCanon66=canonOk?'PASS:66-books-1189-chapters':`FAIL:${canonFailures.join(',')||registeredChapters+'-chapters'}`;

  window.ONE_STUDY_SCHEMA_AUDIT={books:Object.keys(D.studyBooks||{}).length,errors,warnings,canon66:window.ONE_CANON_66_AUDIT,ok:errors.length===0&&canonOk};
  document.documentElement.dataset.oneStudySchema=(errors.length||!canonOk)?`FAIL:${errors.length||canonFailures.length}`:`PASS:66-books-1189-chapters`;
  if(errors.length)console.error("ONE study schema errors",errors);
  if(warnings.length)console.warn("ONE study schema normalized warnings",warnings);
})();

/* ONE — 66-BOOK / 1,189-CHAPTER QUALITY MATRIX
 * Read-only second-layer audit. It never mutates study content and therefore cannot
 * change book availability, chapter rendering, illustration allocation, or navigation.
 * Structural failures remain release-blocking; content-quality gaps are surfaced as
 * warnings so Canon Complete can be improved systematically without hiding gaps.
 */
(()=>{
  "use strict";
  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;
  const schema=window.ONE_STUDY_SCHEMA_AUDIT||{};
  const canonical=window.ONE_CANON_66_AUDIT||{};
  const coverPolicy=window.ONE_COVER_POLICY;
  const books=[];
  const chapters=[];
  const failures=[];
  const warnings=[];
  const counts={books:0,chapters:0,pass:0,warning:0,fail:0,validCovers:0,illustrationCovers:0,withTimeline:0,missingTimeline:0,withMap:0,withConnections:0,withQuestions:0,withPreparation:0};
  const nonEmpty=value=>typeof value==="string"&&value.trim().length>0;
  const hasRows=value=>Array.isArray(value)&&value.length>0;
  const issue=(level,bookNumber,chapter,message)=>({level,bookNumber:Number(bookNumber),chapter:Number(chapter)||null,message});

  Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([bookNumber,book])=>{
    if(!book||typeof book!=="object")return;
    counts.books++;
    const bookIssues=[];
    const bookStats={number:Number(bookNumber),name:book.name||`Book ${bookNumber}`,nameEn:book.nameEn||"",chapters:Array.isArray(book.chapters)?book.chapters.length:0,pass:0,warning:0,fail:0,validCovers:0,illustrationCovers:0,withTimeline:0,missingTimeline:0,withMap:0};
    Object.entries(book.chapterStudies||{}).sort((a,b)=>Number(a[0])-Number(b[0])).forEach(([chapterNumber,study])=>{
      counts.chapters++;
      const local=[];
      const fail=message=>{const row=issue("FAIL",bookNumber,chapterNumber,message);local.push(row);failures.push(row);};
      const warn=message=>{const row=issue("WARNING",bookNumber,chapterNumber,message);local.push(row);warnings.push(row);};

      if(!study||typeof study!=="object")fail("chapter study object missing");
      else{
        if(!nonEmpty(study.title))fail("chapter title missing");
        if(!nonEmpty(study.passage))fail("passage missing");
        if(!nonEmpty(study.story))warn("chapter story is empty");
        if(!nonEmpty(study.position))warn("chapter position/context is empty");
        if(!hasRows(study.background))warn("background module is empty");
        if(!hasRows(study.scout))warn("observation/scout module is empty");
        if(!hasRows(study.questions))warn("questions module is empty"); else counts.withQuestions++;
        if(!hasRows(study.prepare))warn("preparation module is empty"); else counts.withPreparation++;
        if(hasRows(study.connections))counts.withConnections++;
        if(study.map)counts.withMap++;

        const timelineEvents=study.timeline?.events;
        if(study.timeline&&hasRows(timelineEvents))counts.withTimeline++;
        else warn("biblical chronology missing or has no events");

        const cover=study.illustration||coverPolicy?.getCover?.(Number(bookNumber),Number(chapterNumber));
        counts.validCovers++;
        if(cover?.src){
          counts.illustrationCovers++;
          if(!cover.origin)warn("cover exists but origin metadata is missing");
        }

        if(study.map&&(!study.map.image||!study.map.source))fail("map survived runtime gate without image/source pair");
      }

      const level=local.some(item=>item.level==="FAIL")?"FAIL":local.length?"WARNING":"PASS";
      if(level==="FAIL"){counts.fail++;bookStats.fail++;}
      else if(level==="WARNING"){counts.warning++;bookStats.warning++;}
      else{counts.pass++;bookStats.pass++;}
      if(study?.timeline&&hasRows(study.timeline.events))bookStats.withTimeline++;else bookStats.missingTimeline++;
      if(study?.map)bookStats.withMap++;
      const cover=study?.illustration||coverPolicy?.getCover?.(Number(bookNumber),Number(chapterNumber));
      bookStats.validCovers++;
      if(cover?.src)bookStats.illustrationCovers++;
      chapters.push({bookNumber:Number(bookNumber),book:bookStats.name,chapter:Number(chapterNumber),title:study?.title||"",level,issues:local,coverMode:cover?.src?'ILLUSTRATION_COVER':'BOOK_COVER',modules:{cover:true,illustration:Boolean(cover?.src),timeline:Boolean(study?.timeline&&hasRows(study.timeline.events)),map:Boolean(study?.map),connections:hasRows(study?.connections),questions:hasRows(study?.questions),prepare:hasRows(study?.prepare)}});
    });
    if(!book.nameEn)bookIssues.push("English book name missing");
    if(!book.zhCode||!book.enCode)bookIssues.push("Scripture code incomplete");
    bookStats.issues=bookIssues;
    books.push(bookStats);
  });

  counts.missingTimeline=counts.chapters-counts.withTimeline;
  const structuralOk=Boolean(schema.ok&&canonical.ok&&counts.books===66&&counts.chapters===1189&&failures.length===0);
  const summary={status:structuralOk?(warnings.length?"WARNING":"PASS"):"FAIL",structuralOk,generatedAt:new Date().toISOString(),counts,schemaErrors:Array.isArray(schema.errors)?schema.errors.slice():[],schemaWarnings:Array.isArray(schema.warnings)?schema.warnings.slice():[],canonicalFailures:Array.isArray(canonical.failures)?canonical.failures.slice():[],failures,warnings};
  window.ONE_GLOBAL_QUALITY_AUDIT={summary,books,chapters};
  document.documentElement.dataset.oneGlobalQuality=`${summary.status}:${counts.pass}-pass-${counts.warning}-warning-${counts.fail}-fail`;
  if(summary.status==="FAIL")console.error("ONE global quality audit",summary);
  else if(summary.status==="WARNING")console.warn("ONE global quality audit",summary);
  else console.info("ONE global quality audit",summary);
})();
