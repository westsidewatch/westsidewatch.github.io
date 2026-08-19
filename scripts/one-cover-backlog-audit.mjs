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
const context={console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,URL,URLSearchParams,localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-COVER-AUDIT'}};
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

const ranges=[
  [1,5,'TORAH','NARRATIVE_LAW'],[6,17,'HISTORY','NARRATIVE_HISTORY'],[18,18,'WISDOM','POETIC_WISDOM'],[19,19,'PSALMS','POETIC_LITURGICAL'],[20,22,'WISDOM','POETIC_WISDOM'],
  [23,27,'MAJOR_PROPHETS','PROPHETIC_VISION'],[28,39,'MINOR_PROPHETS','PROPHETIC_ORACLE'],[40,43,'GOSPELS','GOSPEL_NARRATIVE'],[44,44,'ACTS','APOSTOLIC_NARRATIVE'],[45,65,'EPISTLES','EPISTOLARY_CONCEPTUAL'],[66,66,'REVELATION','APOCALYPTIC_VISION']
];
const classifyBook=n=>{const r=ranges.find(([a,b])=>n>=a&&n<=b);return{section:r?.[2]||'OTHER',genreClass:r?.[3]||'OTHER'};};
const routeFor=genre=>({
  NARRATIVE_LAW:'STUDIO_SCRIPTURE_SCENE',NARRATIVE_HISTORY:'STUDIO_SCRIPTURE_SCENE',GOSPEL_NARRATIVE:'STUDIO_SCRIPTURE_SCENE',APOSTOLIC_NARRATIVE:'STUDIO_SCRIPTURE_SCENE',
  POETIC_WISDOM:'STUDIO_POETIC_SYMBOLIC',POETIC_LITURGICAL:'STUDIO_PSALM_GRAMMAR',PROPHETIC_VISION:'STUDIO_PROPHETIC_VISION',PROPHETIC_ORACLE:'STUDIO_PROPHETIC_ORACLE',
  EPISTOLARY_CONCEPTUAL:'STUDIO_EPISTLE_GRAMMAR',APOCALYPTIC_VISION:'STUDIO_APOCALYPTIC_VISION'
}[genre]||'EDITORIAL_REVIEW_REQUIRED');
const layerFor=(book,chapter,cover)=>{
  if(!cover)return'MISSING_PLATE';
  const p=policy.officialParallelMapping?.[book]?.[chapter];if(p)return'DORE_OFFICIAL_PARALLEL';
  const h=policy.historicalMatchMapping?.[book]?.[chapter];if(h)return'DORE_HISTORICAL_MATCH';
  const t=policy.typologyMapping?.[book]?.[chapter];if(t)return'DORE_EXPLICIT_TYPOLOGY';
  if(cover.origin==='DORE_ORIGINAL_LIBRARY')return'DORE_CANONICAL_ORIGINAL';
  if(String(cover.origin||'').startsWith('ONE_STUDIO'))return'ONE_STUDIO_FIXED';
  return'APPROVED_NON_DORE_FIXED';
};
const gradeFor=(layer,cover)=>{
  if(layer==='DORE_CANONICAL_ORIGINAL')return'A1_SOURCE_LOCKED';
  if(layer==='DORE_OFFICIAL_PARALLEL')return'A2_CANONICAL_PARALLEL';
  if(layer==='DORE_HISTORICAL_MATCH')return'A3_HISTORICAL_MATCH';
  if(layer==='DORE_EXPLICIT_TYPOLOGY')return'A4_EXPLICIT_TYPOLOGY';
  if(layer==='ONE_STUDIO_FIXED')return'B1_STUDIO_EDITORIAL_FIXED';
  if(layer==='APPROVED_NON_DORE_FIXED')return'B2_NON_DORE_EDITORIAL_FIXED';
  return'BACKLOG_UNASSIGNED';
};
const metadataStatus=cover=>!cover?'NOT_APPLICABLE':(['src','alt','title','source','artist','origin','master'].every(k=>typeof cover[k]==='string'&&cover[k].trim())?'COMPLETE':'REVIEW_METADATA');

const bookRows=[];const chapters=[];
for(const [bookKey,book] of Object.entries(D.studyBooks).sort((a,b)=>Number(a[0])-Number(b[0]))){
  const bookNumber=Number(bookKey);const {section,genreClass}=classifyBook(bookNumber);const total=book.chapters?.length||Object.keys(book.chapterStudies||{}).length;
  let covered=0,backlog=0;
  for(let chapter=1;chapter<=total;chapter++)if(policy.getCover(bookNumber,chapter))covered++;else backlog++;
  const completionLeverage=backlog===0?'COMPLETE':backlog<=3?'VERY_HIGH':backlog<=10?'HIGH':backlog<=20?'MEDIUM':'LOW';
  for(let chapter=1;chapter<=total;chapter++){
    const study=book.chapterStudies?.[String(chapter)]||{};const cover=policy.getCover(bookNumber,chapter);const layer=layerFor(bookNumber,chapter,cover);const isBacklog=!cover;
    let wave='W5_LONG_TAIL';
    if(isBacklog&&backlog<=3)wave='W1_FINISH_BOOK';
    else if(isBacklog&&['GOSPEL_NARRATIVE','APOCALYPTIC_VISION'].includes(genreClass))wave='W2_HIGH_VISIBILITY';
    else if(isBacklog&&['POETIC_LITURGICAL','POETIC_WISDOM','EPISTOLARY_CONCEPTUAL'].includes(genreClass))wave='W3_BUILD_REUSABLE_GRAMMAR';
    else if(isBacklog&&['NARRATIVE_LAW','NARRATIVE_HISTORY','APOSTOLIC_NARRATIVE'].includes(genreClass))wave='W4_NARRATIVE_COVERAGE';
    else if(isBacklog&&['PROPHETIC_VISION','PROPHETIC_ORACLE'].includes(genreClass))wave='W4_PROPHETIC_COVERAGE';
    chapters.push({bookNumber,book:book.name,nameEn:book.nameEn||'',code:book.enCode||book.code||'',chapter,title:study.title||'',passage:study.passage||`${book.name} ${chapter}`,section,genreClass,status:isBacklog?'BACKLOG':'COVERED',coverLayer:layer,qualityGrade:gradeFor(layer,cover),metadataStatus:metadataStatus(cover),productionRoute:isBacklog?routeFor(genreClass):'NONE',completionLeverage,wave,cover:cover?{origin:cover.origin||'',doreId:cover.doreId||null,studioAssetId:cover.studioAssetId||null,title:cover.title||'',source:cover.source||''}:null});
  }
  bookRows.push({bookNumber,book:book.name,nameEn:book.nameEn||'',section,genreClass,total,covered,backlog,coveragePercent:Number((covered/total*100).toFixed(1)),completionLeverage});
}

const backlogRows=chapters.filter(r=>r.status==='BACKLOG');const coveredRows=chapters.filter(r=>r.status==='COVERED');
const countBy=(rows,key)=>rows.reduce((a,r)=>{const v=r[key]||'UNKNOWN';a[v]=(a[v]||0)+1;return a;},{});
const priorityBooks=bookRows.filter(b=>b.backlog>0).sort((a,b)=>{
  const leverage={VERY_HIGH:4,HIGH:3,MEDIUM:2,LOW:1}[b.completionLeverage]-({VERY_HIGH:4,HIGH:3,MEDIUM:2,LOW:1}[a.completionLeverage]);
  return leverage||a.backlog-b.backlog||a.bookNumber-b.bookNumber;
});
const report={generatedAt:new Date().toISOString(),executedScripts:executed,canon:{books:canon.registeredBooks,chapters:canon.registeredChapters,ok:canon.ok},policy:{mode:policy.mode,semanticExpansionEnabled:policy.semanticExpansionEnabled,originalDoréPlacementLocked:policy.originalDoréPlacementLocked,studioLibrarySeparate:policy.studioLibrarySeparate},summary:{totalChapters:chapters.length,covered:coveredRows.length,backlog:backlogRows.length,coveragePercent:Number((coveredRows.length/chapters.length*100).toFixed(1)),byCoverLayer:countBy(coveredRows,'coverLayer'),byQualityGrade:countBy(coveredRows,'qualityGrade'),backlogByGenre:countBy(backlogRows,'genreClass'),backlogByRoute:countBy(backlogRows,'productionRoute'),backlogByWave:countBy(backlogRows,'wave'),metadataReview:coveredRows.filter(r=>r.metadataStatus==='REVIEW_METADATA').length},priorityBooks,books:bookRows,chapters};
if(report.summary.totalChapters!==1189)throw new Error(`Expected 1189 chapters, got ${report.summary.totalChapters}`);
if(report.summary.covered+report.summary.backlog!==1189)throw new Error('Cover coverage invariant failed');
if(report.summary.backlog!==983)throw new Error(`Expected current Missing Plate baseline 983, got ${report.summary.backlog}; rerun classification review before accepting baseline change`);

fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-cover-backlog.json'),JSON.stringify(report,null,2));
const fmt=o=>Object.entries(o).sort((a,b)=>b[1]-a[1]).map(([k,v])=>`- ${v} × ${k}`).join('\n')||'- None';
let md=`# ONE Cover Backlog Classification\n\n- Canon: **${report.canon.ok?'PASS':'FAIL'}** — ${report.canon.books}/66 books, ${report.canon.chapters}/1189 chapters\n- Covered: **${report.summary.covered}** (${report.summary.coveragePercent}%)\n- Missing Plate BACKLOG: **${report.summary.backlog}**\n- Metadata review among covered assets: **${report.summary.metadataReview}**\n- Fuzzy semantic expansion: **${report.policy.semanticExpansionEnabled?'ENABLED — INVALID FOR THIS BASELINE':'DISABLED'}**\n\n## Existing cover quality/provenance\n\n${fmt(report.summary.byQualityGrade)}\n\n## Backlog by production route\n\n${fmt(report.summary.backlogByRoute)}\n\n## Backlog by production wave\n\n${fmt(report.summary.backlogByWave)}\n\n## Priority books — completion leverage first\n\n| Book | Covered | Backlog | Coverage | Leverage | Genre |\n|---|---:|---:|---:|---|---|\n`;
for(const b of priorityBooks)md+=`| ${String(b.bookNumber).padStart(2,'0')} ${b.book} | ${b.covered} | ${b.backlog} | ${b.coveragePercent}% | ${b.completionLeverage} | ${b.genreClass} |\n`;
md+=`\n## Production rules\n\n1. Never create a Doré mapping by fuzzy thematic similarity.\n2. Existing canonical Doré originals remain source-locked and outrank all generated assets.\n3. Official parallel / historical / explicit typology reuse remains explicit policy data only; this audit never invents those relationships.\n4. Missing chapters route to ONE Studio grammars by biblical genre.\n5. W1 finishes nearly complete books; W2 prioritizes reader-facing Gospel/Revelation gaps; W3 builds reusable poetic/wisdom/epistle grammars to unlock high-volume coverage; W4 expands narrative and prophetic coverage.\n6. A Studio plate becomes COVERED only after editorial approval, stable asset registration and explicit chapter assignment.\n`;
fs.writeFileSync(path.join(root,'audit-output','one-cover-backlog.md'),md);console.log(md);
