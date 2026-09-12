#!/usr/bin/env node
import fs from 'node:fs';
const p='data/dore_global_design_expedition_01.json';
const x=JSON.parse(fs.readFileSync(p,'utf8'));
if(x.schema!=='dore.global-design-expedition.v1') throw new Error('schema');
if(x.items.length!==x.curriculum.selected_count) throw new Error('selected_count');
const ids=new Set();
const allowedRights=new Set(['public-domain','metadata-reference-only']);
const banned=/\b(election|partisan|political party|presidential|parliamentary|ethnic conflict|racial conflict|nationalist movement|territorial dispute|propaganda|extremist|terrorist|terrorism|war|battle|military|army|navy|soldier|weapon|rifle|bomb|missile|invasion|occupation)\b/i;
for(const item of x.items){
  if(ids.has(item.id)) throw new Error(`duplicate ${item.id}`); ids.add(item.id);
  if(!allowedRights.has(item.rights)) throw new Error(`rights ${item.id}`);
  if(banned.test(item.title)) throw new Error(`boundary ${item.id}`);
  if(item.theology==='review-required' && item.boundary!=='pass-design-only') throw new Error(`theology ${item.id}`);
  if(!item.source_url) throw new Error(`source ${item.id}`);
}
const counts={}; for(const item of x.items) counts[item.source]=(counts[item.source]||0)+1;
for(const [k,v] of Object.entries(x.curriculum.source_counts)) if(counts[k]!==v) throw new Error(`source count ${k}`);
const rights={}; for(const item of x.items) rights[item.rights]=(rights[item.rights]||0)+1;
for(const [k,v] of Object.entries(x.curriculum.rights_counts)) if(rights[k]!==v) throw new Error(`rights count ${k}`);
const review=x.items.filter(i=>i.theology==='review-required').length;
if(review!==x.curriculum.theology_review_required) throw new Error('theology review count');
console.log(JSON.stringify({status:'PASS',items:x.items.length,sources:Object.keys(counts).length,domains:new Set(x.items.map(i=>i.domain)).size,rights,theologyReviewRequired:review,excluded:x.excluded.length}));