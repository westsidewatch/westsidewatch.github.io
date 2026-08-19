import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const root=process.cwd(),oneDir=path.join(root,'static','one'),indexPath=path.join(oneDir,'index.html');
const html=fs.readFileSync(indexPath,'utf8'),noop=()=>{};
const fakeNode=()=>({hidden:false,dataset:{},style:{},classList:{add:noop,remove:noop,toggle:noop},setAttribute:noop,removeAttribute:noop,append:noop,appendChild:noop,querySelector:()=>null,querySelectorAll:()=>[],closest:()=>null,addEventListener:noop,removeEventListener:noop,textContent:'',innerHTML:''});
const documentElement=fakeNode();
const document={documentElement,body:fakeNode(),head:fakeNode(),getElementById:()=>null,querySelector:()=>null,querySelectorAll:()=>[],createElement:()=>fakeNode(),addEventListener:noop,removeEventListener:noop};
const context={console,document,MutationObserver:class{observe(){} disconnect(){}},queueMicrotask,setTimeout,clearTimeout,URL,URLSearchParams,localStorage:{getItem:()=>null,setItem:noop,removeItem:noop},location:{href:'http://localhost/one/',pathname:'/one/',search:'',hash:''},navigator:{userAgent:'ONE-INDEX-CI'}};
context.window=context;context.globalThis=context;vm.createContext(context);
const tagRe=/<script(?:\s+[^>]*)?>([\s\S]*?)<\/script>/gi,srcRe=/\bsrc=["']\.\/([^"'?]+)(?:\?[^"']*)?["']/i;
let match,executed=0;
while((match=tagRe.exec(html))){
  const full=match[0],inline=match[1].trim(),srcMatch=full.match(srcRe);
  if(srcMatch){
    const file=srcMatch[1];if(file==='one-app.js'||file==='one-opening-simple.js')break;
    const filePath=path.join(oneDir,file);if(!fs.existsSync(filePath))throw new Error(`Missing script: ${file}`);
    vm.runInContext(fs.readFileSync(filePath,'utf8'),context,{filename:filePath});executed++;
  }else if(inline){vm.runInContext(inline,context,{filename:`${indexPath}:inline`});executed++;}
}
const canonIndexPath=path.join(oneDir,'one-canon-index.js');
vm.runInContext(fs.readFileSync(canonIndexPath,'utf8'),context,{filename:canonIndexPath});
const I=context.ONE_CANON_INDEX;if(!I)throw new Error('ONE_CANON_INDEX was not created');
const stats=I.stats;
if(stats.books!==66||stats.chapters!==1189||stats.searchable!==1189)throw new Error(`Canon index invariant failed: ${JSON.stringify(stats)}`);
const identityErrors=[];
for(const r of I.records){if(I.get(r.bookNumber,r.chapter)?.id!==r.id)identityErrors.push(r.id);if(!/^\/one\/\?book=\d+&chapter=\d+$/.test(r.url))identityErrors.push(`${r.id}:url`);}
if(identityErrors.length)throw new Error(`Canon index identity errors: ${identityErrors.slice(0,20).join(', ')}`);
const brokenEdges=I.graphEdges.filter(e=>!I.byId[e.source]||!I.byId[e.target]);if(brokenEdges.length)throw new Error(`Broken graph edges: ${brokenEdges.length}`);
const atlasChapters=I.records.filter(r=>r.places.length>0).length,graphChapters=I.records.filter(r=>r.connections.length>0).length;
const report={generatedAt:new Date().toISOString(),executedScripts:executed,mode:I.mode,version:I.version,stats,atlas:{places:stats.places,maps:stats.maps,chaptersWithPlaces:atlasChapters},graph:{edges:stats.graphEdges,chaptersWithConnectionText:graphChapters,brokenEdges:brokenEdges.length},search:{searchable:stats.searchable,sampleLight:I.search('光',{limit:5}).map(r=>r.id),sampleJerusalem:I.search('耶路撒冷',{limit:5}).map(r=>r.id)},identityErrors};
fs.mkdirSync(path.join(root,'audit-output'),{recursive:true});
fs.writeFileSync(path.join(root,'audit-output','one-canon-index.json'),JSON.stringify(report,null,2));
const md=`# ONE Canon Index Audit\n\n- Identity: **PASS** — ${stats.books}/66 books, ${stats.chapters}/1189 chapters\n- Search corpus: **${stats.searchable}/1189** chapters\n- Atlas: **${stats.places} places**, **${stats.maps} map IDs**, ${atlasChapters} chapters with explicit places\n- Scripture Graph: **${stats.graphEdges} normalized chapter edges**, ${graphChapters} chapters with connection/harmony text\n- Broken graph edges: **${brokenEdges.length}**\n\nThis is the shared read-only identity/data layer. Atlas, Scripture Graph and Search must consume this index rather than maintain separate chapter identities.\n`;
fs.writeFileSync(path.join(root,'audit-output','one-canon-index.md'),md);console.log(md);
