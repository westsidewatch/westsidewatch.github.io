import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root = process.cwd();
const oneDir = path.join(root, 'static', 'one');
const indexPath = path.join(oneDir, 'index.html');
const html = fs.readFileSync(indexPath, 'utf8');

const noop = () => {};
const fakeNode = () => ({hidden:false,dataset:{},style:{},classList:{add:noop,remove:noop,toggle:noop},setAttribute:noop,removeAttribute:noop,append:noop,appendChild:noop,querySelector:()=>null,querySelectorAll:()=>[],closest:()=>null,addEventListener:noop,removeEventListener:noop,textContent:'',innerHTML:''});
const documentElement = fakeNode();
const document = {documentElement,body:fakeNode(),head:fakeNode(),getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],createElement:()=>fakeNode(),addEventListener:noop,removeEventListener:noop};
const context = {console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,URL,URLSearchParams,localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-CI'}};
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

const canon=context.ONE_CANON_66_AUDIT,schema=context.ONE_STUDY_SCHEMA_AUDIT,quality=context.ONE_GLOBAL_QUALITY_AUDIT;
if(!canon||!schema||!quality){console.error(JSON.stringify({executed,canon:!!canon,schema:!!schema,quality:!!quality},null,2));throw new Error('ONE audit globals were not produced before one-app.js');}

const COVER_BACKLOG='no canonical Doré/ONE Studio chapter cover assigned';
const sourceRows=Array.isArray(quality.chapters)?quality.chapters:[];
const rows=sourceRows.map(row=>{
  const issues=Array.isArray(row.issues)?row.issues:[];
  const backlog=issues.some(issue=>issue?.message===COVER_BACKLOG);
  const qualityIssues=issues.filter(issue=>issue?.message!==COVER_BACKLOG);
  const effectiveLevel=qualityIssues.some(issue=>issue?.level==='FAIL')?'FAIL':qualityIssues.length?'WARNING':backlog?'BACKLOG':'PASS';
  return {...row,backlog,qualityIssues,effectiveLevel};
});
const byStatus=rows.reduce((acc,row)=>{acc[row.effectiveLevel]=(acc[row.effectiveLevel]||0)+1;return acc;},{});
const reasonCounts={};
for(const row of rows){for(const issue of row.qualityIssues){const key=`${issue.level||row.effectiveLevel}: ${issue.message||'unspecified issue'}`;reasonCounts[key]=(reasonCounts[key]||0)+1;}}
const topReasons=Object.entries(reasonCounts).sort((a,b)=>b[1]-a[1]).slice(0,30);
const books={};
for(const row of rows){const key=`${String(row.bookNumber).padStart(2,'0')} ${row.book||''}`;books[key]||={PASS:0,BACKLOG:0,WARNING:0,FAIL:0,total:0};books[key][row.effectiveLevel]=(books[key][row.effectiveLevel]||0)+1;books[key].total++;}

const report={generatedAt:new Date().toISOString(),executedScripts:executed,canon,schema:{ok:schema.ok,errors:schema.errors,warnings:schema.warnings},quality:{structuralOk:quality.structuralOk,needsReview:(byStatus.WARNING||0)>0||(byStatus.FAIL||0)>0,coverBacklog:rows.filter(row=>row.backlog).length,byStatus,topReasons,books}};
fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-global-audit.json'),JSON.stringify(report,null,2));
let md=`# ONE Global Audit\n\n- Canon: **${canon.ok?'PASS':'FAIL'}** — ${canon.registeredBooks}/66 books, ${canon.registeredChapters}/1189 chapters\n- Schema: **${schema.ok?'PASS':'FAIL'}** — ${schema.errors.length} errors, ${schema.warnings.length} normalization warnings\n- Quality: **${quality.structuralOk?'STRUCTURALLY PASS':'FAIL'}** — PASS ${byStatus.PASS||0}, BACKLOG ${byStatus.BACKLOG||0}, WARNING ${byStatus.WARNING||0}, FAIL ${byStatus.FAIL||0}\n- Missing Plate backlog: **${report.quality.coverBacklog} chapters**\n\n## Top actionable issues\n\n`;
if(!topReasons.length)md+='- None\n';
for(const [reason,count] of topReasons)md+=`- ${count} × ${reason}\n`;
md+=`\n## Books\n\n| Book | PASS | BACKLOG | WARNING | FAIL | Total |\n|---|---:|---:|---:|---:|---:|\n`;
for(const [book,s] of Object.entries(books))md+=`| ${book} | ${s.PASS||0} | ${s.BACKLOG||0} | ${s.WARNING||0} | ${s.FAIL||0} | ${s.total} |\n`;
fs.writeFileSync(path.join(root,'audit-output','one-global-audit.md'),md);
console.log(md);
if(!canon.ok||!schema.ok||(byStatus.FAIL||0)>0)process.exitCode=1;
