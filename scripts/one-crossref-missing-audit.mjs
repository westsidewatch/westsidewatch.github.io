import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root=process.cwd(), oneDir=path.join(root,'static','one');
const html=fs.readFileSync(path.join(oneDir,'index.html'),'utf8');
const noop=()=>{};
const fakeNode=()=>({hidden:false,dataset:{},style:{setProperty:noop,removeProperty:noop},classList:{add:noop,remove:noop,toggle:noop,contains:()=>false},setAttribute:noop,removeAttribute:noop,append:noop,appendChild:noop,prepend:noop,querySelector:()=>null,querySelectorAll:()=>[],closest:()=>null,addEventListener:noop,removeEventListener:noop,textContent:'',innerHTML:'',set src(v){},set href(v){}});
const documentElement=fakeNode();
const document={documentElement,body:fakeNode(),head:fakeNode(),getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],createElement:()=>fakeNode(),addEventListener:noop,removeEventListener:noop};
const context={console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,URL,URLSearchParams,localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-crossref-audit'},matchMedia:()=>({matches:true}),requestAnimationFrame:(fn)=>{fn();return 1},cancelAnimationFrame:noop,fetch:async()=>({ok:false,text:async()=>''})};
context.window=context;context.globalThis=context;vm.createContext(context);
const tagRe=/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi;
const srcRe=/\bsrc=["']\.\/([^"'?]+)(?:\?[^"']*)?["']/i;
let match; const skipped=[],errors=[],executed=[];
while((match=tagRe.exec(html))){
  const full=match[0],inline=match[1].trim(),srcMatch=full.match(srcRe);
  if(srcMatch){
    const file=srcMatch[1];
    if(file==='one-app.js'||file==='one-opening-simple.js') break;
    const filePath=path.join(oneDir,file);
    if(!fs.existsSync(filePath)){skipped.push(file);continue;}
    try{vm.runInContext(fs.readFileSync(filePath,'utf8'),context,{filename:filePath});executed.push(file);}catch(e){errors.push({file,error:String(e?.message||e)});}
  }else if(inline){try{vm.runInContext(inline,context,{filename:'index:inline'});}catch(e){errors.push({file:'index:inline',error:String(e?.message||e)});}}
}
const D=context.ONE_DATA||{}; const missing=[],bad=[]; let total=0,filled=0;
for(const [bookNo,book] of Object.entries(D.studyBooks||{})){
  for(const [chapterNo,study] of Object.entries(book?.chapterStudies||{})){
    for(const [index,row] of (Array.isArray(study?.connections)?study.connections:[]).entries()){
      if(!Array.isArray(row))continue; total++;
      const reference=String(row[0]||'').trim(),relationship=String(row[1]||'').trim(),explanation=String(row[2]||'').trim(),scripture=String(row[3]||'').trim();
      if(scripture){filled++; if(scripture===explanation||scripture===relationship)bad.push({book:Number(bookNo),name:book.name,chapter:Number(chapterNo),index,reference,type:scripture===explanation?'explanationCopied':'relationshipCopied'});}
      else missing.push({book:Number(bookNo),name:book.name,chapter:Number(chapterNo),index,reference,relationship,explanation});
    }
  }
}
const uniqueMissing={}; for(const r of missing){const k=r.reference||'(blank)';(uniqueMissing[k]??=[]).push({book:r.book,name:r.name,chapter:r.chapter,index:r.index});}
const report={executed,skipped,errors,total,filled,missingCount:missing.length,badCount:bad.length,missing,bad,uniqueMissing};
fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-crossref-missing.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({total,filled,missingCount:missing.length,badCount:bad.length,uniqueMissingCount:Object.keys(uniqueMissing).length,skipped,errors},null,2));
