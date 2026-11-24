import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {join} from 'node:path';
const read=p=>readFileSync(p,'utf8');
const registry=JSON.parse(read('data/editorial/sevenfold.json'));
const realms=['church','journal','emmaus','olive','dawn-library','cinema','daylight-cafe'];
const coverModes=new Set(['identity','poster','atlas','portrait','ledger','cinematic','quiet']);
const blockTypes=new Set(['essay','scripture','index','plate','conversation','shelf']);
const groups={};
const ids=new Set();
const coverSet=new Set(),typesSeen=new Set(),sequences=new Set();
assert.deepEqual(registry.sequence,realms,'All seven realms must be present in original OS');
const sources=read('layouts/partials/editorial/grammar/page.html')+
  read('layouts/partials/editorial/grammar/cover.html')+
  read('layouts/partials/editorial/grammar/block.html');
const styles=read('static/css/westside-editorial-grammar.css');
const shell=read('layouts/_default/baseof.html');
const mount=read('layouts/_default/ws-editorial-interior.html');
assert(mount.includes('editorial/grammar/page.html'),'Hugo must execute grammar, not discarded fixed layout');
assert(shell.includes('if .Params.os_editorial')&&shell.includes('westside-editorial-grammar.css'),'Grammar must be scoped to original OS');
assert(sources.includes('site.Data.editorial.grammar')&&sources.includes('range $i, $block := $composition.blocks'),'Content JSON must drive page HTML');
assert(sources.includes('p2 }}&amp;layout=sevenfold-vertical'),'Scripture blocks must reuse original V60');
assert(styles.includes('var(--ws-paper)')&&styles.includes('var(--ws-type-display-zh)')&&styles.includes('var(--ws-type-display-en-sc)'));
assert(!/#[0-9a-f]{3,8}\\b/i.test(styles),'No independent hardcoded chromatic system');
assert(!styles.includes('body.home')&&!styles.includes('sites-section-'),'Never globally override legacy P2');
function asset(src,label){
 assert(typeof src==='string'&&src.startsWith('/images/')&&!src.includes('..'),label+' needs an existing site asset path');
 assert(existsSync(join('static',src.slice(1))),label+' references missing image: '+src);
}
for(const key of realms){
 const path='data/editorial/grammar/'+key+'.json',page='content/'+key+'/folio.md';
 assert(existsSync(path)&&existsSync(page),'No actual renderable editorial source for '+key);
 const d=JSON.parse(read(path));assert.equal(d.schema,'westside.editorial-grammar.v1');assert.equal(d.realm,key);
 assert(coverModes.has(d.cover.mode)&&d.cover.titleZh?.length>0&&d.cover.titleEn?.length>0&&d.cover.deck?.length>=16);
 coverSet.add(d.cover.mode);
 if(key==='church')assert.equal(d.cover.mode,'identity','Preserve official church original name artwork');
 else asset(d.cover.art.src,key+' cover');
 assert(Array.isArray(d.blocks)&&d.blocks.length>=3,'At least three authored modules for each live composition');
 const blockIds=new Set();
 for(const b of d.blocks){
  assert(blockTypes.has(b.type),'Unknown grammar command '+b.type);
  assert(b.id&&!blockIds.has(b.id),'Missing or duplicate block id '+key+':'+b.id);
  blockIds.add(b.id);typesSeen.add(b.type);
  assert(b.mode,'Every command must select a layout mode');
  if(b.type==='plate')asset(b.src,key+' plate '+b.id);
  if(b.type==='index'||b.type==='shelf'){
   assert(b.entries.length>=2);
   for(const link of b.entries)assert(link.title?.length>0&&link.href.startsWith('/')&&!link.href.startsWith('//'),
     key+' index includes invalid href');
  }
  if(b.type==='essay')assert(b.paragraphs.length>0&&b.paragraphs.every(x=>x.length>=10));
  if(b.type==='conversation')assert(b.pairs.length>0);
  if(b.type==='scripture')assert(registry.sections[key].p2,'Missing canonical scripture in original realm');
 }
 sequences.add(d.blocks.map(x=>x.type).join('>'));
 const md=read(page);
 assert(md.includes('layout: "ws-editorial-interior"')&&md.includes('editorial_key: "'+key+'"'));
 assert(md.includes('list: never')&&!md.includes('draft: true'),'Live candidate folios must build and never auto-alter original navigation');
 groups[key]={mode:d.cover.mode,blocks:d.blocks.map(x=>x.type),page};
}
assert.equal(coverSet.size,7,'Seven individual covers should not be recolored duplicates');
assert.equal(typesSeen.size,6,'Every available grammar command must actually be used across the seven pages');
assert(sequences.size>=6,'Seven pages must have deliberately different editorial order');
assert(sources.includes('ws-gram-cover__official-identity'),'Original church artwork must remain protected');
assert(existsSync('scripts/editorial-grammar-new.mjs'),'Template must have working creation command');
console.log('EDITORIAL_GRAMMAR_CONTRACT_PASS',JSON.stringify({realms:7,coverModes:coverSet.size,blockTypes:typesSeen.size,compositionPatterns:sequences.size,groups}));
