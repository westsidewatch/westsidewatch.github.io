#!/usr/bin/env node
/* Westside Design OS / Editorial Grammar: a composition JSON becomes a Hugo page.
   Example:
     node scripts/editorial-grammar-new.mjs --realm=journal \
       --slug=reading-room --source=fixtures/editorial-grammar/reading-room.json
   Draft by default. --publish requires the same full contract as CI.
   The command never edits P2 or another existing route. */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';

const args=Object.fromEntries(process.argv.slice(2).filter(x=>x.startsWith('--'))
 .map(x=>{const i=x.indexOf('=');return i>=0?[x.slice(2,i),x.slice(i+1)]:[x.slice(2),true]}));
const root=process.cwd();
const manifest=JSON.parse(fs.readFileSync(path.join(root,'data/editorial/sevenfold.json'),'utf8'));
const realms=new Set(manifest.sequence);
const blocksAllowed=new Set(['essay','scripture','index','plate','conversation','shelf']);
const modesAllowed=new Set(['identity','poster','atlas','portrait','ledger','cinematic','quiet']);
const slug=/^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$/;
const realm=args.realm, name=args.slug, source=args.source;
if(!realms.has(realm)||!name||!slug.test(name)||!source){
 throw new Error('Usage: --realm=church|journal|emmaus|olive|dawn-library|cinema|daylight-cafe --slug=lowercase-kebab --source=composition.json [--publish] [--dry-run]');
}
const data=JSON.parse(fs.readFileSync(path.resolve(root,source),'utf8'));
assert.equal(data.schema,'westside.editorial-grammar.v1');
assert.equal(data.realm,realm);
assert(modesAllowed.has(data.cover?.mode),'Cover mode is not in the shared vocabulary');
for(const k of ['titleZh','titleEn','deck','eyebrow','issue'])assert(data.cover[k]?.trim(), 'Missing cover field '+k);
const isSiteLink=x=>typeof x==='string'&&x.startsWith('/')&&!x.startsWith('//')&&!x.includes('..')&&!x.includes('<');
const verifyImage=(src,why)=>{
 assert(isSiteLink(src)&&src.startsWith('/images/'),why+' must reference verified first-party imagery');
 assert(fs.existsSync(path.join(root,'static',src.slice(1))),why+' artwork file does not exist: '+src);
};
if(data.cover.mode!=='identity')verifyImage(data.cover.art?.src,'Cover');
assert(Array.isArray(data.blocks)&&data.blocks.length>=2,'At least two real editorial blocks are required');
const ids=new Set();
for(const b of data.blocks){
 assert(blocksAllowed.has(b.type),'Unsupported command: '+b.type);
 assert(typeof b.id==='string'&&slug.test(b.id),'Every block needs safe unique ID');
 assert(!ids.has(b.id),'Duplicate block ID: '+b.id);
 ids.add(b.id);
 assert(typeof b.mode==='string'&&b.mode.length>0,'Missing block layout mode');
 if(b.type==='essay')assert(b.title?.trim()&&Array.isArray(b.paragraphs)&&b.paragraphs.every(x=>x.trim().length>=10));
 if(b.type==='plate')verifyImage(b.src,'Image plate '+b.id);
 if(b.type==='index'||b.type==='shelf'){
   assert(b.title?.trim()&&Array.isArray(b.entries)&&b.entries.length>=2);
   for(const e of b.entries){assert(e.title?.trim()&&isSiteLink(e.href),'All editorial entries need a real internal URL')}
 }
 if(b.type==='conversation')assert(b.title?.trim()&&Array.isArray(b.pairs)&&b.pairs.length>=1&&b.pairs.every(x=>x.question?.trim()&&x.answer?.trim()));
 if(b.type==='scripture')assert(b.heading?.trim()&&manifest.sections[realm].p2,'Shared V60 scripture source missing');
}
assert(data.cover.deck.length>=16,'A real editorial introduction is required');
const id=realm+'-'+name;
const entry=path.join(root,'data/editorial/grammar',id+'.json');
const page=path.join(root,'content',realm,name+'.md');
for(const file of [entry,page])assert(!fs.existsSync(file),'Refusing to overwrite existing approved content: '+file);
const yamlTitle=data.cover.titleZh.replaceAll('"','\\"');
const content=`---
title: "${yamlTitle}"
description: "${data.cover.deck.replaceAll('"','\\"')}"
layout: "ws-editorial-interior"
os_editorial: true
editorial_key: "${realm}"
grammar_id: "${id}"
build:
  render: always
  list: never
draft: ${args.publish?'false':'true'}
---
`;
if(args['dry-run']){console.log(JSON.stringify({source,composition:entry,page,route:`/${realm}/${name}/`,draft:!args.publish},null,2));process.exit(0)}
fs.mkdirSync(path.dirname(entry),{recursive:true});
fs.mkdirSync(path.dirname(page),{recursive:true});
fs.writeFileSync(entry,JSON.stringify(data,null,2)+'\n');
fs.writeFileSync(page,content);
console.log('EDITORIAL_GRAMMAR_PAGE_CREATED',JSON.stringify({realm,id,page,route:`/${realm}/${name}/`,draft:!args.publish}));
