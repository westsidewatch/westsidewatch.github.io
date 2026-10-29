import fs from 'node:fs';
import {RESIDENTIAL_ERA_PROFILES,residentialEraProfile} from '../preview/jerusalem-3000/residential-era-profiles.js';
import {partitionOverviewBlock} from '../preview/jerusalem-3000/overview-block-layout.js';
import {pointInPolygon} from '../preview/jerusalem-3000/urban-exclusion.js';
import assert from 'node:assert/strict';import * as THREE from 'three';
import {overviewHousingGeometry,buildOverviewHouse,OVERVIEW_HOUSING_GRAMMAR} from '../preview/jerusalem-3000/overview-housing.js';
const terrain={heightAtWorld:(x,z)=>100+x*.02-z*.03},p=[{x:0,z:0},{x:100,z:0},{x:100,z:80},{x:0,z:80}];
const g=overviewHousingGeometry(p,terrain,6,{block:true});assert.ok(g.userData.visualModules>1);assert.ok(g.userData.roofRanges>g.userData.visualModules);assert.equal(g.userData.archaeologicalSubdivision,false);
const pos=g.attributes.position;for(let i=0;i<pos.count;i++){const x=pos.getX(i),z=pos.getZ(i),h=pos.getY(i)-terrain.heightAtWorld(x,z);assert.ok(x>=0&&x<=100&&z>=0&&z<=80);assert.ok(Math.abs(h-.2)<1e-4||Math.abs(h-6)<1e-4);}
assert.deepEqual(Array.from(overviewHousingGeometry(p,terrain,6,{block:true}).attributes.position.array),Array.from(pos.array));
const cells=partitionOverviewBlock(p),theta=.37,move=q=>({x:123+q.x*Math.cos(theta)-q.z*Math.sin(theta),z:-81+q.x*Math.sin(theta)+q.z*Math.cos(theta)}),moved=partitionOverviewBlock(p.map(move));
assert.equal(g.userData.subdivision,'boundary-aligned-adaptive-mass-v1');assert.equal(g.userData.worldGrid,false);assert.equal(g.userData.semanticBuildings,false);
assert.equal(cells.length,moved.length);for(let n=0;n<cells.length;n++){assert.equal(cells[n].length,moved[n].length);for(let i=0;i<cells[n].length;i++){const expected=move(cells[n][i]);assert.ok(Math.hypot(expected.x-moved[n][i].x,expected.z-moved[n][i].z)<1e-5,'block subdivision must move/rotate with its boundary, not snap to world grid');}}
const concave=[{x:0,z:0},{x:120,z:0},{x:120,z:40},{x:40,z:40},{x:40,z:120},{x:0,z:120}],irregular=overviewHousingGeometry(concave,terrain,6,{block:true});
const cp=irregular.attributes.position;for(let i=0;i<cp.count;i++){assert.ok(pointInPolygon({x:cp.getX(i),z:cp.getZ(i)},concave),'no mass may bridge a concave boundary notch');}
assert.ok(partitionOverviewBlock([{x:0,z:0},{x:1000,z:0},{x:1000,z:1000},{x:0,z:1000}]).length<=1024,'recursive visual subdivision is bounded');irregular.dispose();
const small=[{x:0,z:0},{x:12,z:0},{x:12,z:14},{x:0,z:14}],courtyard=overviewHousingGeometry(small,terrain,3.2);assert.equal(courtyard.userData.roofRanges,4);
for(let i=0;i<courtyard.attributes.position.count;i+=3){const a=courtyard.attributes.position,x=(a.getX(i)+a.getX(i+1)+a.getX(i+2))/3,z=(a.getZ(i)+a.getZ(i+1)+a.getZ(i+2))/3;assert.ok(!(x>4&&x<8&&z>5&&z<9),'central courtyard stays open');}
const group=new THREE.Group(),meshes=[],material=new THREE.MeshStandardMaterial(),parcel={id:'same-parcel',geometry:{polygon:small}};const result=buildOverviewHouse(group,meshes,{inferred:material},terrain,parcel,0,{id:'iron-age-four-room-analogy',wallHeightMetres:3.2});assert.equal(result.components,1);assert.equal(meshes[0].geometry.userData.planForm,'four-room-analogy');assert.equal(meshes[0].geometry.userData.roofRanges,3);assert.notDeepEqual(Array.from(meshes[0].geometry.attributes.position.array),Array.from(courtyard.attributes.position.array),'Iron Age overview must change actual roof geometry, not just typology metadata');assert.throws(()=>overviewHousingGeometry(small,terrain,3,{planForm:'invented-era'}));assert.equal(meshes[0].userData.cityObject.parcelId,'same-parcel');assert.equal(meshes[0].userData.overview.grammar,OVERVIEW_HOUSING_GRAMMAR);assert.equal(meshes[0].userData.groundHeights.length,meshes[0].geometry.attributes.position.count);assert.throws(()=>overviewHousingGeometry(p,{heightAtWorld:()=>NaN},4));assert.throws(()=>overviewHousingGeometry([{x:0,z:0}],terrain,4));assert.throws(()=>buildOverviewHouse(group,meshes,{inferred:material},terrain,parcel,0,{wallHeightMetres:NaN}));
for(const geometry of [g,courtyard,...meshes.map(m=>m.geometry)])geometry.dispose();material.dispose();console.log('PASS: common courtyard/roof mass grammar, block modules within parent footprint, open courts, exact DEM fitting, stable subdivision and existing parcel identity');

const phases=JSON.parse(fs.readFileSync(new URL('../preview/jerusalem-3000/data/continuous-build-timeline.json',import.meta.url))).phases;
assert.deepEqual(Object.keys(RESIDENTIAL_ERA_PROFILES),phases.map(p=>p.id),'no missing era or silently borrowed phase');
for(const phase of phases){const profile=residentialEraProfile(phase.id);assert.equal(profile.historicalGeometryAccepted,false);assert.equal(profile.wholeCityTypologyVerified,false);const copy=residentialEraProfile(phase.id);copy.planForms.push('invalid');assert.equal(residentialEraProfile(phase.id).planForms.length,1,'diagnostics cannot mutate active profiles');}
for(const [ruin,prior] of [['babylonian-destruction','late-first-temple'],['roman-destruction','herodian-jesus']]){assert.equal(residentialEraProfile(ruin).modelPredecessor,prior);assert.deepEqual(residentialEraProfile(ruin).planForms,residentialEraProfile(prior).planForms);}
assert.throws(()=>residentialEraProfile('unregistered-era'));
const rect=[{x:0,z:0},{x:12,z:0},{x:12,z:14},{x:0,z:14}],forms=['single-room','four-room-analogy','open-court','courtyard'],buffers=[];
for(const planForm of forms){const geometry=overviewHousingGeometry(rect,terrain,3.2,{planForm});const a=geometry.attributes.position;assert.ok(Array.from(a.array).every(Number.isFinite));for(let i=0;i<a.count;i++)assert.ok(a.getX(i)>=0&&a.getX(i)<=12&&a.getZ(i)>=0&&a.getZ(i)<=14,'typology changes cannot enlarge a parcel');buffers.push(Array.from(a.array).join(','));geometry.dispose();}
assert.equal(new Set(buffers).size,4,'declared forms must affect actual geometry');
console.log('PASS:18 residential profiles, inherited ruin forms, immutable diagnostics and distinct contained plan geometry');
