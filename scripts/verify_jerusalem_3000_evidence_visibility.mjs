import assert from 'node:assert/strict';
import * as THREE from 'three';
import {readFileSync} from 'node:fs';
import {allowsEvidence} from '../preview/jerusalem-3000/evidence-visibility.js';
import {createLandscapeSettlement} from '../preview/jerusalem-3000/earliest-settlement.js';
import {createInheritanceLayer} from '../preview/jerusalem-3000/phase2-inheritance-runtime.js';
import {TemporalCityCore} from '../preview/jerusalem-3000/temporal-city-core.js';
const json=p=>JSON.parse(readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url))),phases=json('data/continuous-build-timeline.json').phases;
const terrain={mesh:new THREE.Mesh(new THREE.PlaneGeometry(2,2)),grid:{origin:{lat:31.773235,lon:35.2368303}},heightAtWorld:(x,z)=>40+x*.01-z*.02};
const core=new TemporalCityCore({phases,terrain}),parent=new THREE.Group();
const modes={all:['observed','reconstructed','inferred','disputed'],observed:['observed'],reconstructed:['observed','reconstructed'],inferred:['observed','reconstructed','inferred'],disputed:['disputed']};
for(const [mode,allowed]of Object.entries(modes))for(const confidence of modes.all)assert.equal(allowsEvidence(mode,confidence),allowed.includes(confidence));
assert.throws(()=>allowsEvidence('invalid','inferred'));
for(const [index,name]of ['earliest','middle-bronze','late-bronze-iron1','david-solomon'].entries()){
 const data=json(`data/settlement/${name}.v1.json`),runtime=createLandscapeSettlement(parent,{data,terrain,ledgerCore:core});
 const ids=runtime.annotations().map(a=>a.id);assert.equal(ids.length,[1,1,9,10][index]);
 const positions=parent.children.at(-1).children.map(m=>m.position.toArray());
 for(const mode of Object.keys(modes)){
  runtime.apply({phaseId:data.phase,evidenceAllowed:confidence=>allowsEvidence(mode,confidence)});
  const annotations=runtime.annotations();assert.equal(runtime.diagnostics().displayAnnotations.visibleComponents,annotations.filter(a=>a.visible).length);
  for(const a of annotations){assert.equal(a.visible,allowsEvidence(mode,a.confidence));assert.equal(a.sourceObjectId,null);assert.equal(a.semanticCityObject,false);assert.equal(core.get(a.id),null);assert.equal(a.geometryVerified,false);}
 }
 const changed=runtime.annotations();changed[0].role='wrong';assert.notEqual(runtime.annotations()[0].role,'wrong');
 runtime.apply({phaseId:'modern',evidenceAllowed:()=>true});assert.ok(runtime.annotations().every(a=>!a.visible));
 runtime.apply({phaseId:data.phase,evidenceAllowed:()=>true});assert.deepEqual(runtime.annotations().map(a=>a.id),ids);assert.deepEqual(parent.children.at(-1).children.map(m=>m.position.toArray()),positions);runtime.dispose();
}
const inheritance=createInheritanceLayer(parent,{terrain,phases});
for(const phase of ['aelia','ayyubid-mamluk','outside-walls']){
 inheritance.setEvidenceMode('observed');inheritance.setPhase(phase,.9);assert.equal(inheritance.diagnostics().visibleComponents,0,'filter before generating must be respected');
 inheritance.setEvidenceMode('all');const count=inheritance.diagnostics().visibleComponents;assert.ok(count>0);
 const before=inheritance.runtime.meshes.map(m=>[m.userData.provisionalInheritance.id,m.position.toArray(),m.scale.toArray()]);
 for(const mode of Object.keys(modes)){inheritance.setEvidenceMode(mode);inheritance.setProgress(phase,.9);assert.equal(inheritance.diagnostics().visibleComponents,allowsEvidence(mode,'inferred')?count:0);}
 inheritance.setEvidenceMode('all');assert.deepEqual(inheritance.runtime.meshes.map(m=>[m.userData.provisionalInheritance.id,m.position.toArray(),m.scale.toArray()]),before);
 inheritance.setVisible(false);inheritance.setEvidenceMode('all');assert.equal(inheritance.diagnostics().visibleComponents,0,'evidence change must not re-enable a phase-hidden layer');inheritance.setVisible(true);assert.equal(inheritance.diagnostics().visibleComponents,count);
}
inheritance.dispose();assert.equal(parent.children.length,0);assert.equal(core.objects.size,0);terrain.mesh.geometry.dispose();terrain.mesh.material.dispose();
console.log('PASS: common five-mode policy, 21 non-semantic annotations, no invented core objects, phase isolation, filter-before-generation, inferred-only overlays, exact restoration and phase-hidden precedence');
