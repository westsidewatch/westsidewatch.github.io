'use strict';
// V77 isolated Olive chapter: six preserved Crane folios, six real-DEM terrain views.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const base='static/images/p2-realms/v15/';
for(const family of ['botanical','terrain']){
 const signatures=new Set();
 for(let edition=1;edition<=6;edition++){
  const rel=family==='botanical'
   ?base+`04-olive-full-verso-v74-botanical-${edition}.svg`
   :base+`v77-exhibition/04-olive-terrain-v77-${edition}.svg`;
  const svg=read(rel);
  assert.match(svg,/<svg\b[^>]*viewBox="0 0 720 940"/,rel+' maintains folio dimensions');
  assert.match(svg,/<title>/,rel+' needs independent title');
  assert.match(svg,/<path\b/,rel+' must contain real vector drawing');
  assert.doesNotMatch(svg,/04-olive-terrain-fragment-v68|04-olive-botanical-impression-v60/,rel+' contains no V68 fragments');
  if(family==='terrain'){
   assert.match(svg,/Olivet.*(?:DEM|geographic)|geographic.*DEM/i,rel+' must cite real geographical source');
   assert.equal((svg.match(/<path\b/g)||[]).length,64,rel+' preserves one full DEM geographic field');
   assert.match(svg,/mask="url\(#mx\)"/,rel+' feathers outer plate edges');
   assert.match(svg,/id="endfade"/,rel+' must soften original DEM line ends');
   assert.doesNotMatch(svg,/M85 102H635|M85 823H635/,rel+' rejects cut-edge frame rules');
  }else assert.match(svg,/crane-public-domain-olive/,rel+' preserves public domain botanical artwork');
  signatures.add(svg);
 }
 assert.equal(signatures.size,6,family+' needs six independent compositions');
}
const mother=read(base+'04-olive-terrain-continuous-mother-v76.svg');
assert.match(mother,/id="olivet-true-topography"/);
assert.equal((mother.match(/<path\b/g)||[]).length,64,'a single continuous 64-path landscape');
assert.match(mother,/terrain-horizontal-feather/);
assert.match(mother,/terrain-vertical-feather/);
const js=read('static/js/p2-0104-olive-continuation.js');
const growth=read('static/js/p2-0104-olive-path-growth-v60.js');
const css=read('static/css/p2-0104-olive-continuation.css');
const gallery=read('static/experiments/olive-v77-exhibition.html');
assert.match(js,/04-olive-full-verso-v74-botanical-/,'original botanical source must remain');
assert.match(js,/v76-exhibition\/04-olive-terrain-v76-/,'six new geographic backs must be mounted');
assert.match(js,/turnFace\(carriers\[i\],turns\[i\]/,'retain physical card flip');
assert.match(growth,/04-olive-terrain-continuous-mother-v76\.svg/,'one V76 final stage geography');
assert.match(css,/\.olive-card__reverse::after\{content:none!important;display:none!important\}/,'no cropped duplicate backside');
assert.equal((gallery.match(/v76-exhibition\/04-olive-terrain-v76-[1-6]\.svg/g)||[]).length,6,'gallery shows every new terrain folio');
assert.match(gallery,/04-olive-terrain-continuous-mother-v76\.svg/,'gallery shows unified final backdrop');
console.log('PASS P2/04 V77: twelve complete folios, six real geographic cards, one continuous geographic field.');
