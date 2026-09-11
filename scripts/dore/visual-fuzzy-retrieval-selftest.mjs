#!/usr/bin/env node
import assert from 'node:assert/strict';
import { rankVisualWorks, visualFuzzyContract } from './visual-fuzzy-retrieval.mjs';

const works = [
  { id:'dore-storm', canonicalTitle:'Christ in the Storm', creator:'Gustave Doré', depicts:['Jesus','disciples','storm'], scriptureRefs:['Mark 4:35-41'], medium:'engraving', composition:'dramatic light negative space', authorityClass:'A', rightsStatus:'public-domain', provenance:'authority', aspectRatios:['8:5'], surfacePresets:['card-8x5'] },
  { id:'map-galilee', canonicalTitle:'Historical Map of Galilee', places:['Galilee'], scriptureRefs:['Mark 4:35-41'], medium:'map', authorityClass:'B', rightsStatus:'cc-by', provenance:'authority', aspectRatios:['8:5'] },
  { id:'generated-storm', canonicalTitle:'AI storm study', depicts:['Jesus','storm'], scriptureRefs:['Mark 4:35-41'], medium:'generated image', authorityClass:'D', rightsStatus:'public-domain', provenance:'generated', generated:true, trainingCanon:false },
  { id:'unknown-rights', canonicalTitle:'Storm painting', depicts:['storm'], authorityClass:'A', rightsStatus:'unknown', provenance:'authority' },
];

const search = rankVisualWorks({ text:'Jesus storm', scriptureRefs:['Mark 4:35-41'], visual:['engraving'], composition:['dramatic light'], aspectRatio:'8:5' }, works, { consumer:'search' });
assert.equal(search[0].id, 'dore-storm');
assert.equal(search.some(x => x.id === 'generated-storm'), false, 'generated assets must never re-enter authority retrieval');

const design = rankVisualWorks({ text:'storm' }, works, { consumer:'design' });
assert.equal(design.some(x => x.id === 'unknown-rights'), false, 'unknown rights must fail closed for design');
assert.equal(visualFuzzyContract.modality, 'dore-search');
assert.equal(visualFuzzyContract.generatedReentry, false);

console.log(JSON.stringify({ status:'PASS', schema:visualFuzzyContract.schema, top:search[0].id, searchResults:search.length, designResults:design.length }));
