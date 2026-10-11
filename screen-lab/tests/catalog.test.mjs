// Run with: node --test screen-lab/tests/catalog.test.mjs
import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
const root = new URL('../', import.meta.url);
const file = name => readFileSync(new URL(name,root),'utf8');
const films=JSON.parse(file('curated.json'));
const html=file('index.html'),catalog=file('catalog.js'),player=file('player.js');
test('curated catalog uses real metadata and no pretend playable links',()=>{
 assert.ok(films.length>=6);
 const seen=new Set();
 for(const film of films){
   assert.ok(film.title && film.year && film.type);
   assert.ok(!seen.has(film.title));seen.add(film.title);
   assert.match(film.source,/^https:\/\//);
   assert.ok(!film.stream,'No unverified stream should be shipped');
   if(film.poster){assert.match(film.poster,/^https:\/\//);assert.ok(film.posterCredit && film.posterLicense && film.posterSource,'Posters require attribution, license and provenance');}
 }
});
test('standalone page does not link back into Paradise Cinema UI',()=>{
 assert.match(html,/id="grid"/);
 assert.match(html,/src="catalog.js"/);
 assert.match(html,/src="player.js"/);
 assert.ok(!html.includes('href="/cinema/"'));
 assert.ok(!html.includes('cinema/cinema.js'));
});
test('catalog and player keep unverified playback distinct from confirmed playing',()=>{
 assert.match(catalog,/待驗證片源/);
 assert.match(player,/addEventListener\('playing'/);
 assert.match(player,/addEventListener\('error'/);
 assert.match(player,/new URL\(input.value.trim\(\)\)/);
});
test('filters are module-bound, not missing globals',()=>{
 assert.ok(!html.includes('onclick="setFilter('));
 assert.match(catalog,/data-screen-filter/);
});
