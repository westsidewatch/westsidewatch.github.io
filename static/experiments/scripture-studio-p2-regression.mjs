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
assert.match(html,/\.piece\.en\{letter-spacing:-\.018em\}/,'Both orientations must use one optical English tracking rule');
assert.match(html,/const opticalTarget=\.84/,'Optical ranking must leave breathing room, not only maximize fill');
assert.match(html,/const editorialFloor=Math\.min\(\.75,minimum\)/,'Editorial variants must retain the two-way fill safety floor');
assert.match(html,/\.plate\.inverse \.cornerCitation\{right:3\.8%;top:8\.5%/,'English-first citation must be fixed to the upper-right corner');
assert.match(html,/\.plate:not\(\.inverse\) \.cornerCitation\{left:8\.5%;bottom:3\.8%/,'Chinese-first citation must occupy one fixed horizontal bottom register');
assert.doesNotMatch(html,/\.cornerCitation::before/,'Citation must not gain ornamental divider lines');
assert.match(html,/ScriptureStudioPassageModel\.runSignatures\(z,e,24\)/,'Non-Isaiah passages must use the existing V50 shared grammar');
assert.match(html,/const toolThemes=\[/,'Site and product verses must have a separate, source-labelled selector');
assert.match(html,/themeFromUrl/,'Tool theme preview must be addressable without changing the P2 scene');
assert.match(html,/measured<\.75/,'Actual two-orientation optical-fill gate must reject narrow arrangements');
assert.match(html,/for\(const fold of \(scripturePassage\.id===/,'Every non-baseline passage must search both one-lane and two-lane arrangements');
assert.match(html,/node\.style\.top=part\.laneTop/,'Two-dimensional layout must place measured semantic runs in the shared mother forme');

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
 ...Object.entries(passages).filter(([id])=>/^0[134567]$/.test(id)).map(([id,data])=>({id,...data}))];
assert.equal(seven.length,7);
assert.equal(passages.HOME.reference.chapterVerse,'13:12');
assert.equal(passages.ONE.reference.chapterVerse,'36:9');
assert.equal(passages.DORE_SEARCH.reference.chapterVerse,'33:3');
assert.equal(passages.HABAKKUK.reference.chapterVerse,'2:2');
assert.equal(passages.MULTIWRITE.reference.chapterVerse,'45:1');
assert.match(passages.ONE.zh,/在你的光中，\|我們必得見光/);
assert.match(passages.ONE.en,/in thy light \|shall we see light/);
const modelContext={};
runInNewContext(readFileSync(join(here,'scripture-studio-passage-model.js'),'utf8'),modelContext);
const grammar=modelContext.ScriptureStudioPassageModel;
const all=[...seven,...Object.entries(passages).filter(([id])=>!/^(02|0[134567])$/.test(id)).map(([id,data])=>({id,...data}))];
for(const p of all){
 const chunks=p.zh.split('|');
 assert(chunks.every(c=>c.length>=2),`${p.id} orphaned Chinese strip`);
 assert(chunks.every(c=>!/^[的了啊呢嗎吧，。！？]/.test(c)),`${p.id} invalid initial Chinese particle blocks candidate generation`);
 const missing=[...new Set([...chunks.join(''),...p.reference.zh].filter(c=>!coverage.has(c.codePointAt(0))))];
 assert.deepEqual(missing,[],`${p.id} Chiron glyphs missing`);
 if(p.en){
  const english=p.en.split('|');
  assert(english.every(c=>c.trim().split(/\s+/).length>=2),`${p.id} orphaned English word`);
  assert.equal(english.join(''),p.en.replaceAll('|',''),`${p.id} KJV text changed`);
  const alternatives=grammar.runSignatures(chunks,english,24);
  assert(alternatives.length>0,`${p.id} shared grammar produced no variants`);
  assert(alternatives.every(c=>grammar.verifyMixedRuns(chunks,english,c.signatures).ok),`${p.id} shared grammar lost text or H4 alternation`);
 }
}
assert(passages['04'].en.split('|').some(x=>x.includes('by the word of God')),'Romans 10:17 protected phrase split');
for(const match of html.matchAll(/<script(?: [^>]*)?>([\s\S]*?)<\/script>/g)){
 if(match[1].trim())new Script(match[1]);
}
console.log(`PASS: ${seven.length} P2 passages and ${all.length-seven.length} verified site/tool impressions; 200/900 Chiron glyph coverage, bilingual grammar and source integrity`);
console.log('NOT VERIFIED: browser optical fill, rotation, responsive and print proof');
