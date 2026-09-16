import fs from 'node:fs';
import assert from 'node:assert/strict';

const path='dore/game-art-direction/candidates/sheep-enters-world.g01.json';
const c=JSON.parse(fs.readFileSync(path,'utf8'));

assert.equal(c.project,'羊走迷');
assert.equal(c.benchmark,'benchmark.sheep-enters-world.v0');
assert.equal(c.generation,'G01');
assert.equal(c.status,'EXPERIMENTAL');
assert.equal(c.canonicalArtDirection,false);
assert.equal(c.productionPromoted,false);
assert.equal(c.family,'italian-lineage');

for(const id of ['cg-1933-cover-12','cg-1933-cover-01-wrapper','cg-1933-p6-insert']) {
  assert(c.visualGenome.historicalLineage.includes(id));
}
for(const key of ['composition','geometry','line','palette','typography','material','motion','collision','spatial','scriptureCompatibility','distinctiveness']) {
  assert(Array.isArray(c.visualGenome[key]) && c.visualGenome[key].length>0, `missing genome ${key}`);
}
assert.deepEqual(Object.keys(c.temporalBeauty),['t0','drag','collision','recomposed','rotationOrFold','3dState']);
assert.equal(c.benchmarkScene.worldState,'Sheep + Maze only');
assert.equal(c.benchmarkScene.sheepfoldVisible,false);
assert.equal(c.benchmarkScene.exitMarkerVisible,false);
assert.equal(c.benchmarkScene.revelationTriggered,false);
assert.equal(c.evidencePolicy.historicalEvidenceRemainsEvidence,true);
assert.equal(c.evidencePolicy.generatedOutputIsEvaluationEvidenceOnly,true);
assert.equal(c.evidencePolicy.mayCopyHistoricalCover,false);
assert.equal(c.evidencePolicy.mayCopyMastheadOrLogo,false);
assert.equal(c.evidencePolicy.maySelfPromote,false);
assert.equal(c.evaluation.beautyAdmissionFloor,true);
assert.equal(c.evaluation.everyLegalStateMustRemainComposed,true);
assert.equal(c.evaluation.champion,false);
assert.equal(c.evaluation.humanJudgmentRequiredForPromotion,true);

console.log('DORE_GAME_ART_DIRECTION_G01=PASS');
