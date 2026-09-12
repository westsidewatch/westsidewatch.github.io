#!/usr/bin/env node
import assert from 'node:assert/strict';
import { mkdir, writeFile } from 'node:fs/promises';

const TARGET = Number(process.env.DORE_CANDIDATES || 10000);
const PAGE_SIZE = 100;
const MAX_PAGES = Math.ceil(TARGET / PAGE_SIZE);
const SELECT_LIMIT = Number(process.env.DORE_SELECTION_LIMIT || 500);
const FIELDS = [
  'id','title','artist_display','date_display','classification_title','artwork_type_title',
  'medium_display','is_public_domain','image_id','thumbnail'
].join(',');

function normalizeText(...parts) {
  return parts.filter(Boolean).join(' ').toLowerCase();
}

function inferDomains(item) {
  const text = normalizeText(item.classification_title, item.artwork_type_title, item.medium_display, item.title);
  const out = new Set();
  if (/photo|photograph/.test(text)) out.add('photography');
  if (/chair|furniture|table|cabinet|desk|stool|bench/.test(text)) out.add('furniture');
  if (/textile|fabric|weav|carpet|rug|tapestry/.test(text)) out.add('textile');
  if (/poster|print|book|page|letter|type|typograph|graphic/.test(text)) { out.add('editorial'); out.add('typography'); }
  if (/architect|building|interior|room|temple|church|chapel/.test(text)) { out.add('architecture'); out.add('interior'); }
  if (/painting|painted|oil|watercolor|gouache/.test(text)) out.add('painting');
  if (/drawing|illustrat|engraving|etching|woodcut|lithograph/.test(text)) out.add('illustration');
  if (/design|industrial|object|vessel|machine/.test(text)) out.add('industrial-design');
  if (out.size === 0) out.add('visual-design');
  return [...out];
}

function designSignals(item) {
  const text = normalizeText(item.classification_title, item.artwork_type_title, item.medium_display, item.title);
  const signals = new Set(['composition']);
  if (/poster|print|book|page|letter|type|typograph|graphic/.test(text)) signals.add('hierarchy');
  if (/photo|photograph|painting|drawing|illustrat/.test(text)) { signals.add('crop'); signals.add('visual-weight'); }
  if (/architect|building|interior|room|chair|furniture/.test(text)) { signals.add('proportion'); signals.add('spatial-hierarchy'); }
  if (/textile|fabric|weav|pattern|ornament/.test(text)) { signals.add('rhythm'); signals.add('repeat'); }
  if (/light|shadow/.test(text)) signals.add('light');
  return [...signals];
}

function theologyRoute(item) {
  const text = normalizeText(item.title, item.classification_title, item.artwork_type_title, item.medium_display);
  const religious = /christ|jesus|mary|madonna|saint|church|chapel|temple|buddh|hindu|islam|mosque|religio|biblical|bible/.test(text);
  if (!religious) return { theologyStatus: 'not-applicable', decision: 'design-only' };
  return { theologyStatus: 'uncertain', decision: 'theology-review-required' };
}

async function fetchPage(page) {
  const url = new URL('https://api.artic.edu/api/v1/artworks');
  url.searchParams.set('page', String(page));
  url.searchParams.set('limit', String(PAGE_SIZE));
  url.searchParams.set('fields', FIELDS);
  const res = await fetch(url, { headers: { 'AIC-User-Agent': 'DoreGlobalDesignNourishment/1.0' } });
  if (!res.ok) throw new Error(`AIC ${res.status} page ${page}`);
  return res.json();
}

const candidates = [];
for (let page = 1; page <= MAX_PAGES && candidates.length < TARGET; page++) {
  const payload = await fetchPage(page);
  for (const raw of payload.data || []) {
    const route = theologyRoute(raw);
    candidates.push({
      id: `aic-${raw.id}`,
      source: 'art-institute-chicago',
      sourceId: raw.id,
      title: raw.title,
      creator: raw.artist_display || null,
      date: raw.date_display || null,
      provenance: 'museum-authority-api',
      rights: raw.is_public_domain ? 'public-domain-item' : 'metadata-only',
      imageAvailable: Boolean(raw.image_id),
      domains: inferDomains(raw),
      designSignals: designSignals(raw),
      ...route,
    });
    if (candidates.length >= TARGET) break;
  }
}

assert.ok(candidates.length >= Math.min(TARGET, 10000), `expected >= ${Math.min(TARGET,10000)} candidates, got ${candidates.length}`);

const seen = new Set();
const selected = [];
const bucketCounts = new Map();
for (const item of candidates) {
  const key = `${item.title}|${item.creator}|${item.date}`;
  if (seen.has(key)) continue;
  seen.add(key);
  const bucket = item.domains.slice().sort().join('+');
  const count = bucketCounts.get(bucket) || 0;
  if (count >= 40) continue;
  bucketCounts.set(bucket, count + 1);
  selected.push(item);
  if (selected.length >= SELECT_LIMIT) break;
}

const domainSet = new Set(selected.flatMap(x => x.domains));
const signalSet = new Set(selected.flatMap(x => x.designSignals));
const reviewRequired = selected.filter(x => x.decision === 'theology-review-required').length;
const publicDomain = selected.filter(x => x.rights === 'public-domain-item').length;

const report = {
  schema: 'dore.global-design-mass-run.v1',
  round: 2,
  source: 'art-institute-chicago',
  candidateTarget: TARGET,
  candidateCount: candidates.length,
  uniqueAfterMetadataDedup: seen.size,
  selectedCount: selected.length,
  selectionLimit: SELECT_LIMIT,
  domainCoverage: [...domainSet].sort(),
  designSignalCoverage: [...signalSet].sort(),
  theologyBoundary: { reviewRequired, failClosed: true },
  rights: { publicDomainSelected: publicDomain, metadataOnlySelected: selected.length - publicDomain },
  learningYield: {
    selectedPer1000Candidates: Number((selected.length / candidates.length * 1000).toFixed(2)),
    domainsPer100Selected: Number((domainSet.size / selected.length * 100).toFixed(2)),
    signalsPer100Selected: Number((signalSet.size / selected.length * 100).toFixed(2)),
  },
  corePolicy: {
    externalBinariesRetained: 0,
    retainedFields: ['authority-metadata','rights-decision','theology-decision','design-signals','domain-relations'],
    principle: 'explore-more-retain-less',
  },
  exemplarSample: selected.slice(0, 50),
};

assert.ok(report.selectedCount > 0);
assert.ok(report.domainCoverage.length >= 3);
assert.equal(report.corePolicy.externalBinariesRetained, 0);

await mkdir('tmp', { recursive: true });
await writeFile('tmp/dore_round2_mass_run.json', JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
