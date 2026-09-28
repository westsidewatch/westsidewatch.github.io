import assert from 'node:assert/strict';
import { runShadowReflex, summarizeShadowRuns } from './shadow-reflex.js';

const candidate={id:'r1',eligible:true,requiredNextStage:'shadow',proposedDecision:'extract'};
const agree=runShadowReflex(candidate,{decision:'extract'},{verification:'PASS'});
assert.equal(agree.executed,false);
assert.equal(agree.agreement,'AGREE');
assert.equal(agree.classification,'agreement-pass');
assert.equal(agree.authority.mayMutateLiveDecision,false);

const disagree=runShadowReflex(candidate,{decision:'defer'},{verification:'PASS'});
assert.equal(disagree.agreement,'DISAGREE');
assert.equal(disagree.classification,'disagreement-pass');

const unknown=runShadowReflex(candidate,{decision:'extract'},{verification:'UNKNOWN'});
assert.equal(unknown.classification,'unknown');
assert.equal(summarizeShadowRuns([agree,disagree,unknown]).promotableEvidence,2);
assert.equal(summarizeShadowRuns([agree,disagree,unknown]).unknownIsPass,false);

const blocked=runShadowReflex({...candidate,eligible:false},'extract','PASS');
assert.equal(blocked.status,'NOT_ELIGIBLE');

console.log('DORE_REFLEX_COMPILATION_STAGE1_K2_SHADOW=PASS');
