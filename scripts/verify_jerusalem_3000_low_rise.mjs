import assert from 'node:assert/strict';import * as THREE from 'three';import{buildEraParcelArchitecture,buildEraParcelArchitectureAsync}from'../preview/jerusalem-3000/herodian-typology-grammar.js';import{TemporalCityCore}from'../preview/jerusalem-3000/temporal-city-core.js';import{createCityProjection}from'../preview/jerusalem-3000/city-lifecycle-projection.js';
const material=new THREE.MeshStandardMaterial(),opaque=new THREE.MeshStandardMaterial({transparent:false,opacity:1}),materials={inferred:material,facadeOpening:material,lowRise:opaque},terrain={heightAtWorld:(x,z)=>40+x*.12+z*.08};
function coreFor(profile){const core=new TemporalCityCore({phases:[{id:'late-first-temple'},{id:'babylonian-destruction'}]});core.register({id:'parcel',type:'parcel',phaseIds:['late-first-temple'],source:{blockId:'block'},geometry:{primitive:'polygon',polygon:[{x:0,z:0},{x:12,z:0},{x:12,z:16},{x:0,z:16}]},metadata:{architectureProfile:profile}});return core;}
for(const id of ['iron-age-four-room-analogy','persian-courtyard-analogy']){
 const profile={id,wallHeightMetres:3.2,sources:[],authority:'test analogy',limitations:['not surveyed']},core=coreFor(profile),group=new THREE.Group(),result=buildEraParcelArchitecture(group,core,materials,terrain,{phaseId:'late-first-temple',destroyedPhase:'babylonian-destruction'});
 assert.equal(result.buildings,1);assert.equal(core.get('parcel:building').typology,id);assert.ok(!result.meshes.some(m=>['upper-room','roof-room','roof-parapet'].includes(m.userData.cityObject.kind)));
 assert.ok(result.meshes.some(m=>m.userData.cityObject.kind==='low-rise-entry-lintel'));
 assert.ok(result.meshes.every(m=>m.material===opaque),'all low-rise components use the shared opaque surface');
 group.updateMatrixWorld(true);
 const ray=new THREE.Raycaster();
 // Check real triangles, not just the existence of a component named entry.
 // The house is inset .89 around the parcel centre; the entry spans z=.88..1.38.
 const floor=terrain.heightAtWorld(11.34,15.12);
 ray.set(new THREE.Vector3(6,floor+1,0),new THREE.Vector3(0,0,1));
 assert.ok(!ray.intersectObjects(result.meshes).some(hit=>hit.distance<1.5),'entry must have usable open headroom');
 ray.set(new THREE.Vector3(6,100,7),new THREE.Vector3(0,-1,0));
 assert.equal(ray.intersectObjects(result.meshes).length,0,'central court must remain open to the sky');
 ray.set(new THREE.Vector3(1.5,100,7),new THREE.Vector3(0,-1,0));
 assert.ok(ray.intersectObjects(result.meshes).some(hit=>hit.object.userData.cityObject.kind==='low-rise-flat-roof'),'side range must have a solid roof');
 const bounds=new THREE.Box3().setFromObject(group);assert.ok(bounds.max.y<48,'early houses must not inherit 12-22m walls');
 const snapshots=result.meshes.map(m=>Array.from(m.geometry.attributes.position.array));const projection=createCityProjection(group,result.meshes,{phaseIds:['late-first-temple','babylonian-destruction'],standingPhase:'late-first-temple'});
 const grounded=()=>{for(const m of result.meshes){m.updateMatrix();const p=m.geometry.attributes.position;for(let i=0;i<p.count;i++){const v=new THREE.Vector3(p.getX(i),p.getY(i),p.getZ(i)).applyMatrix4(m.matrix);assert.ok(v.y>=terrain.heightAtWorld(v.x,v.z)-1e-4,'low-rise/ruin vertices must stay above rendered terrain');assert.ok(v.x>=0&&v.x<=12&&v.z>=0&&v.z<=16,'actual geometry must stay in parcel');}}};
 projection.apply({phaseId:'late-first-temple'});grounded();const fingerprint=projection.diagnostics().transformFingerprint;
 projection.apply({phaseId:'babylonian-destruction',ruin:.8});grounded();assert.notEqual(projection.diagnostics().transformFingerprint,fingerprint);
 projection.apply({phaseId:'late-first-temple'});result.meshes.forEach((m,i)=>assert.deepEqual(Array.from(m.geometry.attributes.position.array),snapshots[i]));
 const asyncGroup=new THREE.Group(),asyncResult=await buildEraParcelArchitectureAsync(asyncGroup,coreFor(profile),materials,terrain,{phaseId:'late-first-temple',maxBatch:1});assert.deepEqual(asyncResult.buildingIds,result.buildingIds);asyncResult.meshes.forEach((m,i)=>assert.deepEqual(Array.from(m.geometry.attributes.position.array),snapshots[i]));
 [...result.meshes,...asyncResult.meshes].forEach(m=>m.geometry.dispose());
}
const legacy=buildEraParcelArchitecture(new THREE.Group(),coreFor(null),materials,terrain,{phaseId:'late-first-temple'});assert.ok(legacy.meshes.some(m=>m.userData.cityObject.kind==='roof-parapet'),'unprofiled canonical grammar remains available');legacy.meshes.forEach(m=>m.geometry.dispose());material.dispose();opaque.dispose();console.log('PASS: period-specific low-rise forms, open entry/court, ground contact through ruin, parcel containment, exact reversal and async identity');
