import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFileSync} from 'node:fs';
import {createInheritanceLayer,inheritanceTransitionIndex} from '../preview/jerusalem-3000/phase2-inheritance-runtime.js';
import {inheritanceFor} from '../preview/jerusalem-3000/phase2-inheritance.js';
const phases=JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/data/continuous-build-timeline.json',import.meta.url))).phases;
const index=inheritanceTransitionIndex(phases);assert.equal(index.length,17);
index.forEach((entry,i)=>{assert.equal(entry.from,phases[i].id);assert.equal(entry.to,phases[i+1].id);assert.equal(entry.survivalVerified,false);assert.equal(entry.historicalFate,'unresolved');assert.equal(entry.foundationAccepted,false);});
assert.equal(index.find(t=>t.to==='aelia').legacySourcePhase,'herodian-jesus');assert.equal(index.find(t=>t.to==='aelia').sourceSkipsAdjacentPhase,true);
assert.throws(()=>inheritanceTransitionIndex([...phases].reverse()));assert.throws(()=>inheritanceTransitionIndex(phases.slice(1)));
const rule=inheritanceFor('aelia');rule.retain=1;assert.equal(inheritanceFor('aelia').retain,.14,'audit callers cannot rewrite legacy selection');
const terrain={mesh:new THREE.Mesh(new THREE.PlaneGeometry(2,2)),grid:{},heightAtWorld:(x,z)=>30+x*.01+z*.02},parent=new THREE.Group(),runtime=createInheritanceLayer(parent,{terrain,phases});
const fingerprints=()=>runtime.runtime.meshes.map(m=>({id:m.userData.provisionalInheritance.id,position:m.position.toArray(),scale:m.scale.toArray(),visible:m.visible}));
for(const phase of ['aelia','ayyubid-mamluk','outside-walls']){
 runtime.setPhase(phase,.9);const diagnostics=runtime.diagnostics();assert.ok(diagnostics.visibleComponents>0);assert.equal(diagnostics.visibleComponents,diagnostics.tracedComponents);
 assert.equal(diagnostics.status,'provisional-overlay-visible');assert.equal(diagnostics.survivalVerified,false);
 const before=fingerprints();assert.equal(new Set(before.map(r=>r.id)).size,before.length);
 for(const mesh of runtime.runtime.meshes){assert.equal(mesh.userData.provisionalInheritance.sourceObjectId,null);assert.equal(mesh.userData.provisionalInheritance.targetPhase,phase);assert.equal(mesh.userData.provisionalInheritance.survivalVerified,false);}
 runtime.setProgress(phase,.2);runtime.setProgress(phase,.9);assert.deepEqual(fingerprints(),before,'reverse progress must retain display trace identity and transforms');
 runtime.setVisible(false);assert.equal(runtime.diagnostics().visibleComponents,0);runtime.setVisible(true);assert.equal(runtime.diagnostics().visibleComponents,diagnostics.visibleComponents);
 runtime.setPhase('byzantine',.9);assert.equal(runtime.runtime,null);assert.equal(runtime.diagnostics().status,'source-generator-unavailable');assert.equal(runtime.diagnostics().survivalVerified,false);
 runtime.setPhase(phase,.9);assert.deepEqual(fingerprints(),before,'return after teardown must reproduce trace IDs and transforms');
 const copy=runtime.transitionIndex();copy[0].survivalVerified=true;assert.equal(runtime.transitionIndex()[0].survivalVerified,false);
 diagnostics.transition.survivalVerified=true;assert.equal(runtime.diagnostics().transition.survivalVerified,false);
}
let disposed=0;for(const mesh of runtime.runtime.meshes)mesh.geometry.addEventListener('dispose',()=>disposed++);const count=runtime.runtime.meshes.length;
runtime.dispose();assert.equal(disposed,count);assert.equal(parent.children.length,0);terrain.mesh.geometry.dispose();terrain.mesh.material.dispose();
console.log('PASS: 17 adjacent transition audits, non-adjacent legacy source disclosure, no invented survivor IDs, traced overlays, missing-generator scope, immutable diagnostics, exact reverse/rebuild and cleanup');
