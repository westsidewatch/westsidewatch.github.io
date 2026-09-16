import assert from 'node:assert/strict';
import {buildItalianSeedProjection} from './italian-evidence-intake.mjs';
const rows=buildItalianSeedProjection();
assert.equal(rows.length,3);
assert.deepEqual(rows.map(x=>x.evidenceId),['cg-1933-cover-12','cg-1933-cover-01-wrapper','cg-1933-p6-insert']);
for(const row of rows){
  assert.equal(row.researchState,'DECOMPOSED');
  assert.ok(row.supportedGrammarTokens.length>0);
  assert.ok(row.gamePotential.length>0);
  assert.equal(row.benchmarkTarget,'benchmark.sheep-enters-world.v0');
  assert.equal(row.authorityBoundary.historicalEvidence,true);
  assert.equal(row.authorityBoundary.gameGrammarAuthority,false);
  assert.equal(row.authorityBoundary.productionAuthority,false);
  assert.equal(row.authorityBoundary.canonicalArtDirection,false);
}
assert.ok(rows.find(x=>x.evidenceId==='cg-1933-cover-01-wrapper').gamePotential.includes('2d-to-3d'));
assert.ok(rows.find(x=>x.evidenceId==='cg-1933-p6-insert').gamePotential.includes('collision'));
console.log('DORE_GAME_ART_ITALIAN_EVIDENCE_INTAKE_V0=PASS');
