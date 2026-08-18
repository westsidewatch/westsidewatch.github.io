/* Revelation integrity audit: validation only; never mutates study content or blocks publication for missing generated plates. */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const R=D?.studyBooks?.[66]||D?.revelation;
  const S=R?.chapterStudies||{};
  const report={
    book:66,
    expectedChapters:22,
    registered:Boolean(D?.studyBooks?.[66]),
    chapterCount:Object.keys(S).length,
    missing:[],
    invalidCore:[],
    invalidConnections:[],
    invalidTimeline:[],
    originalLocked:[],
    studioFixed:[],
    missingPlates:[],
    connectionCount:0
  };

  for(let n=1;n<=22;n+=1){
    const c=S[String(n)];
    if(!c){report.missing.push(n);continue;}

    ["title","passage","movement","story","position"].forEach(key=>{
      if(!String(c[key]||"").trim())report.invalidCore.push({chapter:n,field:key});
    });
    if(!Array.isArray(c.route)||!c.route.length)report.invalidCore.push({chapter:n,field:"route"});
    if(!Array.isArray(c.background)||!c.background.length)report.invalidCore.push({chapter:n,field:"background"});
    if(!Array.isArray(c.scout)||!c.scout.length)report.invalidCore.push({chapter:n,field:"scout"});
    if(!Array.isArray(c.questions)||!c.questions.length)report.invalidCore.push({chapter:n,field:"questions"});

    const links=Array.isArray(c.connections)?c.connections:[];
    if(!links.length)report.invalidConnections.push({chapter:n,reason:"empty"});
    links.forEach((x,i)=>{
      report.connectionCount+=1;
      if(!Array.isArray(x)||x.length!==3||!String(x[0]||"").trim()||!String(x[1]||"").trim()||!String(x[2]||"").trim()){
        report.invalidConnections.push({chapter:n,index:i,reason:"shape"});
      }
    });

    if(c.timeline){
      const t=c.timeline;
      const ok=typeof t==="object"&&!Array.isArray(t)&&String(t.title||"").trim()&&String(t.range||"").trim()&&Array.isArray(t.events)&&t.events.length;
      if(!ok)report.invalidTimeline.push(n);
    }

    if(c.doreCover?.stage==="CANONICAL_MASTER"&&c.illustration)report.originalLocked.push(n);
    else if(c.studioCover?.stage==="FIXED_GENERATED"&&c.illustration)report.studioFixed.push(n);
    else if(!c.illustration)report.missingPlates.push(n);
  }

  report.ok=report.registered&&report.chapterCount===22&&!report.missing.length&&!report.invalidCore.length&&!report.invalidConnections.length&&!report.invalidTimeline.length;
  report.publicationReady=report.ok;
  report.illustrationComplete=report.missingPlates.length===0;
  R.audit=report;

  document.documentElement.dataset.revelationAudit=report.ok?"pass":"fail";
  document.documentElement.dataset.revelationPublicationReady=report.publicationReady?"true":"false";
  document.documentElement.dataset.revelationMissingPlates=report.missingPlates.join(",");

  if(!report.ok)console.error("[ONE Revelation audit]",report);
  else console.info(`[ONE Revelation audit] pass: 22 chapters, ${report.connectionCount} connections; ${report.missingPlates.length} missing plates are non-blocking`);
})();
