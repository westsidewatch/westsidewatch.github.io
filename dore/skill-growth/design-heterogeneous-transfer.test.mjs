import assert from 'node:assert/strict';
import { transferLivingWaterPreference, heterogeneousTransferToExperience } from './design-heterogeneous-transfer.js';

const realTaste={delta:{kind:'design.preference-delta',change:'hierarchy-through-light',before:'sacred-threshold',after:'quiet-light',conditions:['church-identity-preserved'],evidence:['raster:sha-sacred','raster:sha-quiet','pairwise:sacred-threshold->quiet-light'],authority:{canonical:false,maySelfPromote:false}}};
const clean=transferLivingWaterPreference(realTaste,{targetProject:'yangzoumi',targetContext:'playful-game-world',transferableItems:[
 {id:'operation:hierarchy-through-light',kind:'design-operation',projectId:'living-water',transferable:true}
],targetEvidence:['render:yangzoumi:real-browser','identity:yangzoumi:playful-game'],styleLeakage:false});
assert.equal(clean.projectTransfer.promotionEligible,true);
assert.equal(clean.preferenceTransfer.promotionEligible,true);
assert.equal(clean.contamination.blocked.length,0);
assert.equal(clean.authority.maySelfPromote,false);
const experience=heterogeneousTransferToExperience(clean,'observation:lw-to-yangzoumi:01');
assert.equal(experience.state,'experience');
assert.deepEqual(experience.relatedCapabilities,['design.taste']);
assert.equal(experience.authority.maySelfPromote,false);

assert.throws(()=>transferLivingWaterPreference(realTaste,{targetProject:'yangzoumi',targetContext:'playful-game-world',transferableItems:[
 {id:'style:quiet-sacred',kind:'surface-specific-style',projectId:'living-water',transferable:false}
],targetEvidence:['render:yangzoumi'],styleLeakage:false}),/project contamination blocked/);

assert.throws(()=>transferLivingWaterPreference(realTaste,{targetProject:'yangzoumi',targetContext:'playful-game-world',transferableItems:[
 {id:'operation:hierarchy-through-light',kind:'design-operation',projectId:'living-water',transferable:true}
],targetEvidence:['render:yangzoumi'],styleLeakage:true}),/no-style-leakage/);

assert.throws(()=>transferLivingWaterPreference(realTaste,{targetProject:'living-water',targetContext:'other',transferableItems:[],targetEvidence:['x'],styleLeakage:false}),/materially different consumer/);
console.log('DORE_DESIGN_HETEROGENEOUS_TRANSFER=PASS');
