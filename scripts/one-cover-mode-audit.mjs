import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root=process.cwd();
const oneDir=path.join(root,'static','one');
const indexPath=path.join(oneDir,'index.html');
const html=fs.readFileSync(indexPath,'utf8');
const noop=()=>{};
const fakeNode=()=>({hidden:false,dataset:{},style:{},classList:{add:noop,remove:noop,toggle:noop},setAttribute:noop,removeAttribute:noop,append:noop,appendChild:noop,querySelector:()=>null,querySelectorAll:()=>[],closest:()=>null,addEventListener:noop,removeEventListener:noop,textContent:'',innerHTML:''});
const documentElement=fakeNode();
const document={documentElement,body:fakeNode(),head:fakeNode(),getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],createElement:()=>fakeNode(),addEventListener:noop,removeEventListener:noop};
const context={console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,URL,URLSearchParams,localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-COVER-MODE-AUDIT'}};
context.window=context;context.globalThis=context;vm.createContext(context);

const tagRe=/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi;
const srcRe=/\bsrc=["']\.\/([^"'?]+)(?:\?[^"']*)?["']/i;
let match,executed=0;
while((match=tagRe.exec(html))){
  const full=match[0],inline=match[1].trim(),srcMatch=full.match(srcRe);
  if(srcMatch){
    const file=srcMatch[1];
    if(file==='one-app.js'||file==='one-opening-simple.js')break;
    const filePath=path.join(oneDir,file);
    if(!fs.existsSync(filePath))throw new Error(`Missing script referenced by index.html: ${file}`);
    vm.runInContext(fs.readFileSync(filePath,'utf8'),context,{filename:filePath});executed++;
  }else if(inline){vm.runInContext(inline,context,{filename:`${indexPath}:inline`});executed++;}
}

const D=context.ONE_DATA;
const policy=context.ONE_COVER_POLICY;
const canon=context.ONE_CANON_66_AUDIT;
if(!D?.studyBooks||!policy||!canon?.ok)throw new Error('Canonical ONE data / cover policy / canon audit unavailable');

const chapters=[];
const firstChapterCandidates=[];
let illustrationCovers=0;
for(const [bookKey,book] of Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0]))){
  const bookNumber=Number(bookKey);
  const total=book.chapters?.length||Object.keys(book.chapterStudies||{}).length;
  for(let chapter=1;chapter<=total;chapter++){
    const cover=policy.getCover(bookNumber,chapter);
    const coverMode=cover?'ILLUSTRATION_COVER':'BOOK_COVER';
    if(cover)illustrationCovers++;
    const row={bookNumber,book:book.name,nameEn:book.nameEn||'',chapter,coverMode,illustration:cover?{origin:cover.origin||'',title:cover.title||'',source:cover.source||''}:null};
    chapters.push(row);
    if(chapter===1&&!cover)firstChapterCandidates.push({bookNumber,book:book.name,nameEn:book.nameEn||'',chapter:1,status:'FIRST_CHAPTER_CANDIDATE'});
  }
}

if(chapters.length!==1189)throw new Error(`Expected 1189 valid cover modes, got ${chapters.length}`);
const report={
  generatedAt:new Date().toISOString(),executedScripts:executed,
  canon:{books:canon.registeredBooks,chapters:canon.registeredChapters,ok:canon.ok},
  policy:{mode:'COEXISTENCE',bookCoverIsComplete:true,illustrationIsOptional:true,firstPhase:'FIRST_CHAPTER_CANDIDATES'},
  summary:{validCoverModes:chapters.length,illustrationCovers,firstChapterCandidates:firstChapterCandidates.length},
  firstChapterCandidates
};

fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-cover-modes.json'),JSON.stringify(report,null,2));
let md=`# ONE Cover Coexistence Audit\n\n- Canon: **PASS** — ${report.canon.books}/66 books, ${report.canon.chapters}/1189 chapters\n- Valid cover modes: **${report.summary.validCoverModes}/1189**\n- Approved illustration covers: **${report.summary.illustrationCovers}**\n- Canonical book-cover mode: **valid final presentation, never a missing asset**\n- Phase-one illustration candidates: **${report.summary.firstChapterCandidates} first chapters**\n\n## Phase-one candidates\n\n| Book | Chapter | Status |\n|---|---:|---|\n`;
for(const row of firstChapterCandidates)md+=`| ${String(row.bookNumber).padStart(2,'0')} ${row.book} · ${row.nameEn} | 1 | ${row.status} |\n`;
md+='\n## Coexistence rules\n\n1. Every chapter has a valid cover presentation: illustration cover or canonical book cover.\n2. Absence of an illustration is not a warning, failure, debt or publication blocker.\n3. Approved Doré and ONE Studio illustrations remain fixed editorial assets.\n4. Phase one may propose illustrations only for first chapters that currently use book-cover mode.\n5. A proposed illustration replaces book-cover mode only after editorial approval and stable registration.\n';
fs.writeFileSync(path.join(root,'audit-output','one-cover-modes.md'),md);
console.log(md);
