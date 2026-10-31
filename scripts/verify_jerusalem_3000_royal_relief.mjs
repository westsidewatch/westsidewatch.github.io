import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from 'three';
import {loadCanonicalTerrain} from '../preview/jerusalem-3000/terrain-runtime.js';
import {sampleRoyalRelief} from '../preview/jerusalem-3000/royal-relief.js';
import {settlementSurfaceHeight} from '../preview/jerusalem-3000/earliest-settlement.js';
const read=p=>JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url)));
const grid=read('data/terrain/copernicus-glo30-jerusalem.json'),data=read('data/settlement/david-solomon.v1.json');
const originalFetch=globalThis.fetch;let terrain;
try{globalThis.fetch=async()=>({ok:true,json:async()=>structuredClone(grid)});terrain=await loadCanonicalTerrain({elevationGrid:'x'},new THREE.Group());}finally{globalThis.fetch=originalFetch;}
const positions=Array.from(terrain.mesh.geometry.attributes.position.array),profile=sampleRoyalRelief(data,terrain);
assert.equal(profile.verticalScale,1);assert.equal(profile.threshingFloorLocationVerified,false);
assert.ok(profile.deltaSouth>65&&profile.deltaSouth<85,'existing southern/northern reference points must sample the uphill DEM, not swapped latitude');
assert.ok(profile.deltaMiddle>40&&profile.deltaMiddle<65);assert.ok(profile.distance>600&&profile.distance<650);
for(const [i,p] of profile.samples.entries()){
 assert.ok(Math.abs(p.y-settlementSurfaceHeight(terrain,p.x,p.z))<1e-8);
 assert.equal(p.elevation,p.y+grid.verticalDatumOffsetMetres);
 if(i)assert.ok(p.distance>profile.samples[i-1].distance&&p.distance-profile.samples[i-1].distance<=10.0001);
}
assert.deepEqual(Array.from(terrain.mesh.geometry.attributes.position.array),positions,'profile must never move ground or monuments');
assert.deepEqual(sampleRoyalRelief(data,terrain),profile,'stable forward/backward reference');
const bad=structuredClone(data);bad.royalCity.temple.offset=[NaN,0];assert.throws(()=>sampleRoyalRelief(bad,terrain));
console.log(JSON.stringify({distance:profile.distance,deltaSouth:profile.deltaSouth,deltaMiddle:profile.deltaMiddle,authority:profile.authority}));
terrain.dispose();console.log('PASS: measured modern-DEM royal transect, independent lower-city references, unchanged geometry and unverified ancient placement');
