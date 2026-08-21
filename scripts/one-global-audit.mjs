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
const context = {
  console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,
  URL,URLSearchParams,AbortController,Headers,Request,Response,fetch,
  localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},
  location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-CI'}
};
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

const waitFor = async (predicate,{timeout=45000,interval=100,label='condition'}={}) => {
  const started=Date.now();
  while(Date.now()-started<timeout){
    if(predicate())return;
    await new Promise(resolve=>setTimeout(resolve,interval));
  }
  throw new Error(`Timed out waiting for ${label}`);
};

// Cross-reference Scripture loaders may fetch Public Domain CUV passages asynchronously.
// Wait for them and for the read-only global cross-reference audit before evaluating CI.
await waitFor(()=>{
  const major=context.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE?.status;
  const hebrews=context.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE?.status;
  const majorDone=major && !['loading','loading-long-references'].includes(major);
  const hebrewsDone=hebrews && hebrews!=='loading';
  return majorDone && hebrewsDone;
},{label:'major-prophet and Hebrews Scripture loaders'});
await waitFor(()=>Boolean(context.ONE_CROSS_REFERENCE_SCRIPTURE_GLOBAL_AUDIT),{label:'cross-reference Scripture global audit'});

const canon=context.ONE_CANON_66_AUDIT,schema=context.ONE_STUDY_SCHEMA_AUDIT,quality=context.ONE_GLOBAL_QUALITY_AUDIT;
const crossref=context.ONE_CROSS_REFERENCE_SCRIPTURE_GLOBAL_AUDIT;
if(!canon||!schema||!quality||!crossref){
  console.error(JSON.stringify({executed,canon:!!canon,schema:!!schema,quality:!!quality,crossref:!!crossref},null,2));
  throw new Error('ONE audit globals were not produced before one-app.js');
}

const sourceRows=Array.isArray(quality.chapters)?quality.chapters:[];
const rows=sourceRows.map(row=>{
  const issues=Array.isArray(row.issues)?row.issues:[];
  const effectiveLevel=issues.some(issue=>issue?.level==='FAIL')?'FAIL':issues.length?'WARNING':'PASS';
  return {...row,qualityIssues:issues,effectiveLevel};
});
const byStatus=rows.reduce((acc,row)=>{acc[row.effectiveLevel]=(acc[row.effectiveLevel]||0)+1;return acc;},{});
const reasonCounts={};
for(const row of rows){for(const issue of row.qualityIssues){const key=`${issue.level||row.effectiveLevel}: ${issue.message||'unspecified issue'}`;reasonCounts[key]=(reasonCounts[key]||0)+1;}}
const topReasons=Object.entries(reasonCounts).sort((a,b)=>b[1]-a[1]).slice(0,30);
const books={};
for(const row of rows){const key=`${String(row.bookNumber).padStart(2,'0')} ${row.book||''}`;books[key]||={PASS:0,WARNING:0,FAIL:0,total:0};books[key][row.effectiveLevel]=(books[key][row.effectiveLevel]||0)+1;books[key].total++;}

const structuralOk=Boolean(quality.summary?.structuralOk);
const actionableOk=structuralOk&&(byStatus.WARNING||0)===0&&(byStatus.FAIL||0)===0;
const crossrefOk=crossref.status==='PASS'&&crossref.missingRows===0&&crossref.incompleteChapters===0&&crossref.explanationCopied.length===0&&crossref.relationshipCopied.length===0&&crossref.conflicts.length===0;

// Submission UI guard: backend/debug status copy must never be present in the reader renderer.
const appSource=fs.readFileSync(path.join(oneDir,'one-app.js'),'utf8');
const forbiddenReaderCopy=['本條目前只保留串珠關係與說明','不以說明文字冒充經文引用','Scripture pending','經文待補'];
const readerLeaks=forbiddenReaderCopy.filter(text=>appSource.includes(text));
const readerUiOk=readerLeaks.length===0&&!appSource.includes('connection-scripture-missing');

const report={
  generatedAt:new Date().toISOString(),executedScripts:executed,canon,
  schema:{ok:schema.ok,errors:schema.errors,warnings:schema.warnings},
  quality:{structuralOk,actionableOk,needsReview:!actionableOk,coverModes:{valid:quality.summary?.counts?.validCovers||0,illustration:quality.summary?.counts?.illustrationCovers||0},byStatus,topReasons,books},
  crossReferences:{
    ok:crossrefOk,status:crossref.status,chaptersWithConnections:crossref.chaptersWithConnections,
    completeChapters:crossref.completeChapters,incompleteChapters:crossref.incompleteChapters,
    totalRows:crossref.totalRows,filledRows:crossref.filledRows,missingRows:crossref.missingRows,
    explanationCopied:crossref.explanationCopied,relationshipCopied:crossref.relationshipCopied,
    conflicts:crossref.conflicts,missing:crossref.missing,
    majorProphets:context.ONE_MAJOR_PROPHETS_CROSS_REFERENCE_SCRIPTURE,
    hebrews:context.ONE_HEBREWS_CROSS_REFERENCE_SCRIPTURE
  },
  readerUi:{ok:readerUiOk,backendCopyLeaks:readerLeaks}
};
fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-global-audit.json'),JSON.stringify(report,null,2));
let md=`# ONE Global Audit\n\n- Canon: **${canon.ok?'PASS':'FAIL'}** — ${canon.registeredBooks}/66 books, ${canon.registeredChapters}/1189 chapters\n- Schema: **${schema.ok?'PASS':'FAIL'}** — ${schema.errors.length} errors, ${schema.warnings.length} normalization warnings\n- Quality: **${actionableOk?'PASS':structuralOk?'REVIEW':'FAIL'}** — PASS ${byStatus.PASS||0}, WARNING ${byStatus.WARNING||0}, FAIL ${byStatus.FAIL||0}\n- Cover system: **PASS** — ${report.quality.coverModes.valid}/1189 valid chapter covers; ${report.quality.coverModes.illustration} use an approved illustration; all others use the canonical book-cover mode\n- Cross-reference Scripture: **${crossrefOk?'PASS':'FAIL'}** — ${crossref.filledRows}/${crossref.totalRows} filled, ${crossref.incompleteChapters} incomplete chapters, ${crossref.explanationCopied.length+crossref.relationshipCopied.length} copied-commentary errors, ${crossref.conflicts.length} conflicts\n- Reader UI backend-copy guard: **${readerUiOk?'PASS':'FAIL'}**${readerLeaks.length?` — ${readerLeaks.join(' | ')}`:''}\n\n## Top actionable issues\n\n`;
if(!topReasons.length)md+='- None\n';
for(const [reason,count] of topReasons)md+=`- ${count} × ${reason}\n`;
md+=`\n## Books\n\n| Book | PASS | WARNING | FAIL | Total |\n|---|---:|---:|---:|---:|\n`;
for(const [book,s] of Object.entries(books))md+=`| ${book} | ${s.PASS||0} | ${s.WARNING||0} | ${s.FAIL||0} | ${s.total} |\n`;
if(!crossrefOk){
  md+='\n## Cross-reference Scripture failures\n\n';
  if(crossref.missingRows)md+=`- Missing Scripture rows: ${crossref.missingRows}\n`;
  if(crossref.incompleteChapters)md+=`- Incomplete chapters: ${crossref.incompleteChapters}\n`;
  if(crossref.explanationCopied.length)md+=`- Explanation copied into Scripture: ${crossref.explanationCopied.length}\n`;
  if(crossref.relationshipCopied.length)md+=`- Relationship copied into Scripture: ${crossref.relationshipCopied.length}\n`;
  if(crossref.conflicts.length)md+=`- Conflicting texts for same reference: ${crossref.conflicts.length}\n`;
}
fs.writeFileSync(path.join(root,'audit-output','one-global-audit.md'),md);
console.log(md);
if(!canon.ok||!schema.ok||(byStatus.FAIL||0)>0||!crossrefOk||!readerUiOk)process.exitCode=1;
