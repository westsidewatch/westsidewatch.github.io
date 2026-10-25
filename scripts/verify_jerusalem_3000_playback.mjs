import assert from 'node:assert/strict';
import {advancePlayback} from '../preview/jerusalem-3000/playback-clock.js';
assert.equal(advancePlayback(4,30,17,{ready:false}),4);
assert.equal(advancePlayback(3.999,20,17),4,'a slow frame must stop at the next phase boundary');
assert.equal(advancePlayback(4,20,17),4+.1/12,'generation/background time is never replayed as a jump');
assert.equal(advancePlayback(17,1,17),17);
for(const args of [[NaN,1,17],[1,-1,17],[18,1,17]])assert.throws(()=>advancePlayback(...args));
console.log('PASS: generation holds presentation time, long-frame budget, exact phase boundary and final endpoint');
