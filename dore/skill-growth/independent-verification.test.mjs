import assert from 'node:assert/strict';
import { verifyOutcome, verifyDesignOutcome } from './independent-verification.js';

const pass=verifyOutcome({action:'extract',expectedState:'artifact',observableDelta:'created',consumerVerification:{status:'PASS',independent:true,evidence:['consumer:test']}});
assert.equal(pass.status,'PASS');
assert.equal(pass.authority.reflexMayOverrideConsumer,false);

const selfClaim=verifyOutcome({action:'extract',expectedState:'artifact',consumerVerification:{status:'PASS',independent:false}});
assert.equal(selfClaim.status,'UNKNOWN');

const weird=verifyOutcome({action:'x',expectedState:'y',consumerVerification:{status:'SUCCESS',independent:true}});
assert.equal(weird.status,'UNKNOWN');

const design=verifyDesignOutcome({
 functional:{action:'render',expectedState:'no-overflow',consumerVerification:{status:'PASS',independent:true}},
 beautiful:{action:'render',expectedState:'beautiful-gate',consumerVerification:{status:'UNKNOWN',independent:true}}
});
assert.equal(design.status,'UNKNOWN');
assert.equal(design.gates.functionalPassIsBeautifulPass,false);
assert.equal(design.gates.beautifulRequired,true);

const ugly=verifyDesignOutcome({
 functional:{action:'render',expectedState:'works',consumerVerification:{status:'PASS',independent:true}},
 beautiful:{action:'render',expectedState:'beautiful',consumerVerification:{status:'FAIL',independent:true}}
});
assert.equal(ugly.status,'FAIL');

console.log('DORE_REFLEX_COMPILATION_STAGE1_K3_VERIFICATION=PASS');
