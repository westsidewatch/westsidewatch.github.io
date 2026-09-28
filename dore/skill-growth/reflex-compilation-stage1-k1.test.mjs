import assert from 'node:assert/strict';
import { assessReflexCandidate } from './reflex-candidate-contract.js';
import { compileExperienceTraces } from './experience-trace-compiler.js';

const safe = assessReflexCandidate({id:'x',bounded:true,verifiedSuccesses:2,independentlyVerifiable:true,recoverable:true,authoritySafe:true,boundedChoice:true,evidence:['e1','e2']});
assert.equal(safe.eligible,true);
assert.equal(safe.reflexClass,'R1-bounded-choice');
assert.equal(safe.requiredNextStage,'shadow');
assert.equal(safe.authority.mayExecute,false);

const unsafe = assessReflexCandidate({bounded:true,verifiedSuccesses:2,independentlyVerifiable:true,recoverable:true,authoritySafe:false,boundedChoice:true});
assert.equal(unsafe.eligible,false);
assert.equal(unsafe.reflexClass,'R3-deliberative');

const events=[1,2].map(n=>({id:`e${n}`,recurrenceKey:'source:static-http',decision:'extract',verification:'PASS',bounded:true,independentVerifier:true,recoverable:true,authoritySafe:true,mode:'bounded-choice'}));
const [compiled]=compileExperienceTraces(events);
assert.equal(compiled.eligible,true);
assert.deepEqual(compiled.evidence,['e1','e2']);

const unknown=[...events.slice(0,1),{...events[1],verification:'UNKNOWN'}];
assert.equal(compileExperienceTraces(unknown)[0].eligible,false);

console.log('DORE_REFLEX_COMPILATION_STAGE1_K1=PASS');
