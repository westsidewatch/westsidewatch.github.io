#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { boundaryDecisionForText } from './content-boundary.mjs';

const input = process.argv[2] || '../aic-api-data/json/artworks';
const candidateTarget = Number(process.env.DORE_CANDIDATE_TARGET || 10000);
const retainTarget = Number(process.env.DORE_RETAIN_TARGET || 1000);

const stable = value => parseInt(crypto.createHash('sha256').update(String(value)).digest('hex').slice(0, 8), 16);
const domainsFor = text => {
  const out = [];
  const rules = [
    ['editorial-typography', /poster|book|print|letter|type|graphic|publication|magazine|newspaper/],
    ['architecture-interior-furniture', /architect|building|church|house|interior|chair|table|cabinet|furniture|room|plan|elevation/],
    ['photography-illustration', /photo|photograph|drawing|engraving|etching|woodcut|lithograph|illustrat/],
    ['painting', /painting|watercolor|gouache|tempera|oil on/],
    ['industrial-design', /industrial|product|machine|appliance|object design/],
  ];
  for (const [name, re] of rules) if (re.test(text)) out.push(name);
  return out.length ? out : ['visual-design'];
};
const theologyFor = text => /church|christ|jesus|mary|madonna|saint|bible|biblical|gospel|temple|mosque|buddh|hindu|altar|crucifix|devotional|religio/.test(text) ? 'review-required' : 'not-applicable';

function listJsonFiles(root) {
  const stack=[root], files=[];
  while(stack.length){
    const current=stack.pop();
    for(const entry of fs.readdirSync(current,{withFileTypes:true})){
      const full=path.join(current,entry.name);
      if(entry.isDirectory()) stack.push(full);
      else if(entry.isFile() && entry.name.endsWith('.json')) files.push(full);
    }
  }
  return files.sort();
}

const candidates=[];
let scanned=0, parseErrors=0, boundaryExcluded=0, rightsFieldPresent=0;
const files=listJsonFiles(input);
for(const file of files){
  if(candidates.length>=candidateTarget) break;
  scanned++;
  let x;
  try { x=JSON.parse(fs.readFileSync(file,'utf8')); } catch { parseErrors++; continue; }
  const id=x.id ?? x.ID ?? x.object_id ?? file;
  const text=[x.title,x.artist_display,x.artist_title,x.classification_title,x.style_title,x.medium_display,x.description,x.short_description,...(x.subject_titles||[]),...(x.theme_titles||[])].filter(Boolean).join(' ').toLowerCase();
  const boundary=boundaryDecisionForText(text);
  if(boundary.decision==='exclude'){ boundaryExcluded++; continue; }
  const domains=domainsFor(text);
  const theology=theologyFor(text);
  if(Object.prototype.hasOwnProperty.call(x,'is_public_domain')) rightsFieldPresent++;
  const rights=x.is_public_domain===true ? 'public-domain' : 'metadata-reference-only';
  candidates.push({id:`aic-${id}`,source:'art-institute-chicago',domains,theology,rights,boundary:'pass',score:stable(id)});
}

const unique=[...new Map(candidates.map(x=>[x.id,x])).values()];
const buckets=new Map();
for(const item of unique) for(const domain of item.domains){
  if(!buckets.has(domain)) buckets.set(domain,[]);
  buckets.get(domain).push(item);
}
for(const arr of buckets.values()) arr.sort((a,b)=>a.score-b.score);

const selected=[]; const used=new Set(); const active=[...buckets.keys()].sort(); let cursor=0;
while(selected.length<Math.min(retainTarget,unique.length) && active.length){
  const idx=cursor%active.length, key=active[idx], arr=buckets.get(key); let item;
  while(arr.length && !item){ const x=arr.shift(); if(!used.has(x.id)) item=x; }
  if(item){ selected.push(item); used.add(item.id); cursor++; } else active.splice(idx,1);
}

const domainCounts={}; for(const x of unique) for(const d of x.domains) domainCounts[d]=(domainCounts[d]||0)+1;
const selectedDomainCounts={}; for(const x of selected) for(const d of x.domains) selectedDomainCounts[d]=(selectedDomainCounts[d]||0)+1;
const report={
  schema:'dore.global-design-nourishment-run.v2',
  round:2,
  source:'art-institute-chicago/api-data/full-artwork-json',
  mode:'full-authority-corpus-with-content-boundary',
  candidateTarget,retainTarget,filesDiscovered:files.length,scannedFiles:scanned,parseErrors,boundaryExcluded,rightsFieldPresent,
  candidateCount:candidates.length,uniqueCount:unique.length,retainedCount:selected.length,
  retentionRate:unique.length?selected.length/unique.length:0,
  domainCounts,selectedDomainCounts,
  theologyReviewRequired:selected.filter(x=>x.theology==='review-required').length,
  publicDomainRetained:selected.filter(x=>x.rights==='public-domain').length,
  metadataReferenceOnlyRetained:selected.filter(x=>x.rights==='metadata-reference-only').length,
  constraints:{externalBinariesOutOfRepo:true,contentBoundaryFailClosed:true,theologyFailClosed:true,rightsFailClosed:true,exploreMoreRetainLess:true},
  selected:selected.map(({score,...x})=>x)
};
fs.writeFileSync('dore-round2-corpus-report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,selected:undefined},null,2));
if(unique.length<candidateTarget) process.exitCode=2;
if(rightsFieldPresent===0) process.exitCode=3;
