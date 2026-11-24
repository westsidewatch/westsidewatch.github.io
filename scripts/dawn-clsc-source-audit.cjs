#!/usr/bin/env node
/** Inspect Yale/HKBU CLSC page HTML and discover per-title PDF links.
 * Read-only source audit; do not infer a URL from a title or ID.
 */
const fs=require('node:fs');
const site='https://adhoc.yalepages.org/Collections/HKBU/CLSC/index.html';
const expected=[
 '住在主裏面','慕牧師木鐸記','基督證道論','怎樣禱告',
 '教會古史節要','門徒的祈禱','瑞士牧童'
];
(async()=>{
 const response=await fetch(site,{headers:{'User-Agent':'DawnLibraryProvenanceAudit/1.0 (public research)'}});
 const html=await response.text();
 const scripts={};
 const scriptNames=[...html.matchAll(/<script\b[^>]*src=["']([^"']+)/gi)].map(m=>m[1]);
 for(const name of scriptNames){
  const scriptUrl=new URL(name,site).href;
  const reply=await fetch(scriptUrl);
  const data=await reply.text();
  scripts[name]={url:scriptUrl,http:reply.status,bytes:data.length,
   head:data.slice(0,1800),
   hits:Object.fromEntries(expected.map(title=>{
    const i=data.indexOf(title);
    return [title,i>=0?data.slice(Math.max(0,i-200),i+500):'NOT_FOUND'];
   })),
   pdfs:[...data.matchAll(/[A-Za-z0-9_%-]+\.pdf/g)].slice(0,12).map(x=>x[0])};
  fs.mkdirSync('artifacts/dawn-clsc',{recursive:true});
  fs.writeFileSync('artifacts/dawn-clsc/'+name.replace(/[^A-Za-z0-9_.-]/g,'_'),data);
 }
 const out={url:site,http:response.status,bytes:html.length,
  siteScripts:scriptNames,scripts,
  pdfHrefs:[...html.matchAll(/href=["']([^"']+\.pdf[^"']*)["']/gi)].map(m=>m[1]).slice(0,25),
  titleContext:Object.fromEntries(expected.map(title=>{
   const i=html.indexOf(title);
   return [title,i>=0?html.slice(Math.max(0,i-450),i+750):'NOT_IN_STATIC_HTML'];
  })),
  lines:html.slice(0,1600)};
 fs.mkdirSync('artifacts/dawn-clsc', {recursive:true});
 fs.writeFileSync('artifacts/dawn-clsc/source-audit.json',JSON.stringify(out,null,2)+'\n');
 console.log(JSON.stringify({status:response.status,bytes:html.length,
  scripts:out.siteScripts,sourcePdfMatches:Object.entries(scripts).map(([name,r])=>({name,bytes:r.bytes,pdfs:r.pdfs,hits:r.hits})),pdfs:out.pdfHrefs.length,
  matchedTitles:Object.entries(out.titleContext).filter(([_,v])=>v!=='NOT_IN_STATIC_HTML').map(([k])=>k),
  samples:Object.entries(out.titleContext).slice(0,3)}));
 if(!response.ok)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
