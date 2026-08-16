/* Isaiah integrity audit: validation only; does not mutate study content. */
(() => {
  "use strict";
  const D=window.ONE_DATA,I=D?.isaiah,S=I?.chapterStudies||{};
  const report={chapters:66,missing:[],invalidConnections:[],missingContext:[],connectionCount:0};
  for(let n=1;n<=66;n+=1){
    const c=S[String(n)];
    if(!c){report.missing.push(n);continue;}
    if(!Array.isArray(c.timeline)||!c.timeline.length||!Array.isArray(c.geography)||!c.geography.length)report.missingContext.push(n);
    const links=Array.isArray(c.connections)?c.connections:[];
    if(!links.length)report.invalidConnections.push({chapter:n,reason:"empty"});
    links.forEach((x,i)=>{
      report.connectionCount+=1;
      if(!Array.isArray(x)||x.length!==3||!String(x[0]||"").trim()||!String(x[1]||"").trim()||!String(x[2]||"").trim())report.invalidConnections.push({chapter:n,index:i,reason:"shape"});
    });
  }
  report.ok=!report.missing.length&&!report.invalidConnections.length&&!report.missingContext.length;
  I.audit=report;
  document.documentElement.dataset.isaiahAudit=report.ok?"pass":"fail";
  if(!report.ok)console.error("[ONE Isaiah audit]",report);else console.info(`[ONE Isaiah audit] pass: 66 chapters, ${report.connectionCount} connections`);
})();