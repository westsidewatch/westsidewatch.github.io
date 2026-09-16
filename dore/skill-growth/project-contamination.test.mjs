import assert from 'node:assert/strict';
import { contaminationBlock, assertCrossProjectTransfer } from './project-contamination.js';

// Shared lifecycle rule now protects both Design and Writing: transfer operation, never project identity.
const writing = contaminationBlock([
  { id:'technique:slow-scene', kind:'writing-operation', projectId:'tian-guo-yu-yan', transferable:true },
  { id:'motif:babel', kind:'project-motif', projectId:'tian-guo-yu-yan', transferable:false },
  { id:'voice:tgyy', kind:'character-voice', projectId:'tian-guo-yu-yan', transferable:false }
], { currentProject:'cross-shadow' });
assert.deepEqual(writing.admitted.map(x=>x.id), ['technique:slow-scene']);
assert.deepEqual(writing.blocked.map(x=>x.id), ['motif:babel','voice:tgyy']);

const design = contaminationBlock([
  { id:'capability:hierarchy', kind:'design-operation', projectId:'living-water', transferable:true },
  { id:'style:quiet-sacred', kind:'surface-specific-style', projectId:'living-water', transferable:false }
], { currentProject:'yangzoumi' });
assert.deepEqual(design.admitted.map(x=>x.id), ['capability:hierarchy']);
assert.deepEqual(design.blocked.map(x=>x.id), ['style:quiet-sacred']);

const clean = contaminationBlock([{ id:'capability:hierarchy', kind:'design-operation', projectId:'living-water', transferable:true }], { currentProject:'yangzoumi' });
const transfer = assertCrossProjectTransfer({ capability:'design.hierarchy', sourceProject:'living-water', targetProject:'yangzoumi', contamination:clean, evidence:['render:living-water','render:yangzoumi'] });
assert.equal(transfer.promotionEligible, true);
assert.equal(transfer.authority.maySelfPromote, false);
assert.throws(() => assertCrossProjectTransfer({ capability:'design.style', sourceProject:'living-water', targetProject:'yangzoumi', contamination:design, evidence:['render:x'] }), /contamination/);
console.log('DORE_PROJECT_CONTAMINATION=PASS');
