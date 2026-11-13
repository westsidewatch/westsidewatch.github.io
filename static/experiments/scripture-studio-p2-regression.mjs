// Run: node static/experiments/scripture-studio-p2-regression.mjs
// This is source/font coverage QA; optical/browser QA remains separate.
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {dirname,join} from 'node:path';
import {runInNewContext,Script} from 'node:vm';
import assert from 'node:assert/strict';

const here=dirname(fileURLToPath(import.meta.url));
const html=readFileSync(join(here,'scripture-studio-motherform-live.html'),'utf8');
const manifest=JSON.parse(readFileSync(join(here,'../fonts/scripture-studio/ChironHeiHK-P2-coverage.json'),'utf8'));
assert.deepEqual(manifest.weights,[200,900]);
const coverage=new Set(manifest.codepoints);
for(const weight of [200,900])assert.match(html,new RegExp(`ChironHeiHK-P2-${weight}\\.woff2`));
assert.match(html,/font-synthesis:none/);
assert.match(html,/\.piece\.en\{letter-spacing:-\.045em\}/,'Both orientations must use one tighter English tracking rule');

const marker='const realmVerseData=';
const at=html.indexOf(marker);
assert(at>=0);
const end=html.indexOf('\n};',at);
assert(end>at);
const passages=runInNewContext('('+html.slice(at+marker.length,end+2)+')');
const baselineMatch=html.match(/let z=(\[[^;]+\]);/);
assert(baselineMatch);
const baseline=runInNewContext(baselineMatch[1]);
const seven=[{id:'02',reference:{zh:'以賽亞書'},zh:baseline.join('|')},
 ...Object.entries(passages).map(([id,data])=>({id,...data}))];
assert.equal(seven.length,7);
for(const p of seven){
 const chunks=p.zh.split('|');
 assert(chunks.every(c=>c.length>=2),`${p.id} orphaned Chinese strip`);
 assert(chunks.every(c=>!/^[的了啊呢嗎吧，。！？]/.test(c)),`${p.id} invalid initial Chinese particle blocks candidate generation`);
 const missing=[...new Set([...chunks.join(''),...p.reference.zh].filter(c=>!coverage.has(c.codePointAt(0))))];
 assert.deepEqual(missing,[],`${p.id} Chiron glyphs missing`);
 if(p.en){
  const english=p.en.split('|');
  assert(english.every(c=>c.trim().split(/\s+/).length>=2),`${p.id} orphaned English word`);
  assert.equal(english.join(''),p.en.replaceAll('|',''),`${p.id} KJV text changed`);
 }
}
assert(passages['04'].en.split('|').some(x=>x.includes('by the word of God')),'Romans 10:17 protected phrase split');
for(const match of html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)){
 if(match[1].trim())new Script(match[1]);
}
console.log(`PASS: ${seven.length} P2 passages, uniform Chiron glyph coverage, both faces, inline scripts, protected phrases`);
console.log('NOT VERIFIED: browser optical fill, rotation, responsive and print proof');
