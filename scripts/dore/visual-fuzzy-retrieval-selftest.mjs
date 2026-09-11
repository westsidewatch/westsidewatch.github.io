#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {normalizeVisualGraph,rankVisualWorks,visualFuzzyContract} from './visual-fuzzy-retrieval.mjs';
import {selectEditorialVisuals} from './visual-editorial-director-adapter.mjs';
const graph=JSON.parse(await readFile(new URL('../../data/visual_graph.json',import.meta.url),'utf8'));
const works=normalizeVisualGraph(graph);
assert.ok(works.length>=4);
const storm=rankVisualWorks({text:'Sea of Galilee storm boat',scriptureRefs:['Mark 4:35–41'],aspectRatio:'8:5',operation:'display'},works);
assert.equal(storm[0].id,'visual-princeton-galilee-storm-1591');
assert.ok(storm[0].surfacePresetIds.includes('card-8x5'));
const design=rankVisualWorks({text:'Moses Leviticus',operation:'design'},works);
assert.equal(design.some(x=>x.id==='visual-initiale-lev1-god-speaking-moses'),false);
const ved=selectEditorialVisuals({content:'Sea of Galilee storm',w:'WATCH',scriptureRefs:['Mark 4:35–41'],aspectRatio:'8:5',operation:'display'},graph);
assert.equal(ved.schema,'dore.visual-editorial-director.v1');
assert.equal(ved.candidates[0].id,'visual-princeton-galilee-storm-1591');
assert.equal(visualFuzzyContract.generatedReentry,false);
console.log(JSON.stringify({status:'PASS',fixtures:works.length,top:storm[0].id,vedTop:ved.candidates[0].id}));
