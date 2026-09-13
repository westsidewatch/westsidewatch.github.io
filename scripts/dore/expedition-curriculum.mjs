#!/usr/bin/env node
import fs from 'node:fs';
const x=JSON.parse(fs.readFileSync(process.argv[2]||'dore-expedition-ingested.json','utf8'));
const words=[['typography',/type|poster|book|print|graphic/i],['architecture',/architect|building|church|interior|plan/i],['furniture',/chair|table|furniture|cabinet/i],['photography',/photo|photograph/i],['illustration',/drawing|engraving|etching|woodcut|illustrat/i],['painting',/painting|watercolor|oil/i],['industrial-design',/industrial|product|machine|appliance/i]];
const buckets={};
for(const item of x.items){const names=words.filter(([,r])=>r.test(item.raw)).map(([n])=>n); for(const n of names.length?names:['visual-design'])(buckets[n]??=[]).push(item);}
const selected=[]; const seen=new Set();
for(const key of Object.keys(buckets).sort()) for(const item of buckets[key].slice(0,100)){if(!seen.has(item.id)){seen.add(item.id);selected.push({...item,domain:key});}}
const report={schema:'dore.expedition.curriculum.v1',source:x.source,ingested:x.retained,domains:Object.fromEntries(Object.entries(buckets).map(([k,v])=>[k,v.length])),selectedCount:selected.length,selected};
fs.writeFileSync('dore-expedition-curriculum.json',JSON.stringify(report,null,2)); console.log(JSON.stringify({...report,selected:undefined}));