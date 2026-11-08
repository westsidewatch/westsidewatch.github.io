'use strict';
// P2/04 V74 physical-card and continuous-terrain asset contract.
// Static source checks; visual inspection and Chromium scroll QA remain separate.
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const prefix='static/images/p2-realms/v15/';
const svgPaths=[];
for(const family of ['botanical','terrain']){
  const hashes=new Set();
  for(let edition=1;edition<=6;edition++){
    const rel=prefix+`04-olive-full-verso-v74-${family}-${edition}.svg`;
    const source=read(rel);
    assert.match(source,/<svg\b[^>]*viewBox="0 0 720 940"/,rel+' needs full 720×940 artwork');
    assert.match(source,new RegExp('<title>[^<]*'+edition+' \\/ 6<\\/title>'),rel+' needs its own edition');
    assert.match(source,/<path\b/,rel+' needs actual independent vector drawing');
    assert.doesNotMatch(source,/04-olive-terrain-fragment-v68|04-olive-botanical-impression-v60/,rel+' must not embed a crop');
    hashes.add(source);
    svgPaths.push(rel);
  }
  assert.equal(hashes.size,6,family+' folios must all be distinct');
}
const mother=read(prefix+'04-olive-terrain-continuous-mother-v74.svg');
assert.match(mother,/id="olivet-true-topography"/,'final terrain should have one actual terrain geometry source');
assert((mother.match(/<path\b/g)||[]).length>=24,'continuous master needs intact contour paths');
const js=read('static/js/p2-0104-olive-continuation.js');
const growth=read('static/js/p2-0104-olive-path-growth-v60.js');
const css=read('static/css/p2-0104-olive-continuation.css');
assert.match(js,/04-olive-full-verso-v74-/,'real reverse must use independent full folios');
assert.match(js,/isBotanical\?'botanical-':'terrain-'/,'left/right cards must alternate botanical and terrain');
assert.match(js,/turnFace\(carriers\[i\],turns\[i\]/,'full reverse must ride on actual physical flip');
assert.match(growth,/04-olive-terrain-continuous-mother-v74\.svg/,'stage must use continuous terrain');
assert.match(css,/\.olive-card__reverse::after\{content:none!important;display:none!important\}/,'retire duplicate cropped reverse detail');
console.log('PASS P2/04 V74: twelve distinct complete card folios, native flip wiring, and one measured contour mother.');
