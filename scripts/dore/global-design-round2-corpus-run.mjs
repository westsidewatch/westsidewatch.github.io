#!/usr/bin/env node
import fs from 'node:fs';
import readline from 'node:readline';
import crypto from 'node:crypto';

const input = process.argv[2] || '../aic-api-data/getting-started/allArtworks.jsonl';
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

const candidates = [];
const stream = fs.createReadStream(input, { encoding: 'utf8' });
const rl = readline.createInterface({ input: stream, crlfDelay: Infinity });
let lines = 0;
let parseErrors = 0;
for await (const line of rl) {
  if (!line.trim()) continue;
  lines++;
  let x;
  try { x = JSON.parse(line); } catch { parseErrors++; continue; }
  const id = x.id ?? x.ID ?? x.object_id ?? lines;
  const text = [x.title,x.artist_display,x.classification_title,x.style_title,x.medium_display,x.description,...(x.subject_titles||[])].filter(Boolean).join(' ').toLowerCase();
  const domains = domainsFor(text);
  const theology = theologyFor(text);
  const rights = x.is_public_domain === true ? 'public-domain' : 'metadata-reference-only';
  candidates.push({ id:`aic-${id}`, source:'art-institute-chicago', domains, theology, rights, score:stable(id) });
  if (candidates.length >= candidateTarget) break;
}

const unique = [...new Map(candidates.map(x => [x.id, x])).values()];
const buckets = new Map();
for (const item of unique) for (const domain of item.domains) {
  if (!buckets.has(domain)) buckets.set(domain, []);
  buckets.get(domain).push(item);
}
for (const arr of buckets.values()) arr.sort((a,b) => a.score-b.score);

const selected=[]; const used=new Set(); const active=[...buckets.keys()].sort(); let cursor=0;
while (selected.length < Math.min(retainTarget, unique.length) && active.length) {
  const idx=cursor%active.length, key=active[idx], arr=buckets.get(key); let item;
  while(arr.length && !item){ const x=arr.shift(); if(!used.has(x.id)) item=x; }
  if(item){ selected.push(item); used.add(item.id); cursor++; } else active.splice(idx,1);
}

const domainCounts={};
for(const x of unique) for(const d of x.domains) domainCounts[d]=(domainCounts[d]||0)+1;
const selectedDomainCounts={};
for(const x of selected) for(const d of x.domains) selectedDomainCounts[d]=(selectedDomainCounts[d]||0)+1;
const report={
  schema:'dore.global-design-nourishment-run.v1',
  round:2,
  source:'art-institute-chicago/api-data',
  mode:'streaming-authority-corpus',
  candidateTarget,
  retainTarget,
  scannedLines:lines,
  parseErrors,
  candidateCount:candidates.length,
  uniqueCount:unique.length,
  retainedCount:selected.length,
  retentionRate:unique.length ? selected.length/unique.length : 0,
  domainCounts,
  selectedDomainCounts,
  theologyReviewRequired:selected.filter(x=>x.theology==='review-required').length,
  publicDomainRetained:selected.filter(x=>x.rights==='public-domain').length,
  constraints:{externalBinariesOutOfRepo:true,theologyFailClosed:true,exploreMoreRetainLess:true},
  selected:selected.map(({score,...x})=>x)
};
fs.writeFileSync('dore-round2-corpus-report.json', JSON.stringify(report,null,2));
console.log(JSON.stringify({...report,selected:undefined},null,2));
if(unique.length < candidateTarget) process.exitCode=2;
