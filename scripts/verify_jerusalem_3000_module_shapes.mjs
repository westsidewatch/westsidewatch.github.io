import assert from 'node:assert/strict';import fs from 'node:fs';import * as THREE from 'three';
import {partitionOverviewBlock,overviewModuleMetrics,MAX_OVERVIEW_MODULE_SPAN_METRES as limit} from '../preview/jerusalem-3000/overview-block-layout.js';
import {overviewHousingGeometry} from '../preview/jerusalem-3000/overview-housing.js';
import {compileIndependentLaterSkeleton,buildIndependentLaterSkeleton} from '../preview/jerusalem-3000/independent-later-skeleton.js';
import {applyMetricResidentialRegistration} from '../preview/jerusalem-3000/metric-residential-layout.js';
import {compileWallReference} from '../preview/jerusalem-3000/old-city-wall-reference.js';
import {housingBoundaryAt} from '../preview/jerusalem-3000/housing-boundary.js';
import {completeUrbanCoverage} from '../preview/jerusalem-3000/urban-coverage.js';
const read=p=>JSON.parse(fs.readFileSync(new URL('../preview/jerusalem-3000/'+p,import.meta.url))),terrain={grid:{origin:{lat:31.778,lon:35.235}},heightAtWorld:()=>100},material=new THREE.MeshStandardMaterial(),rows=[];
const strip=[{x:0,z:0},{x:124,z:0},{x:124,z:3},{x:0,z:3}],cells=partitionOverviewBlock(strip);assert.ok(cells.length>1,'a low-area124m strip must not survive as one long wall');assert.ok(cells.every(p=>overviewModuleMetrics(p).span<=limit+1e-5));
const g=overviewHousingGeometry(strip,terrain,6,{block:true});assert.ok(g.userData.slenderSolidModules>0,'narrow strips use solid caps rather than implausible needle courtyards');assert.equal(g.userData.withheldVisualModules,0,'buildable narrow strip is subdivided, not erased');assert.equal(g.userData.omittedSliverAreaSquareMetres,0);g.dispose();
const wedge=[{x:0,z:0},{x:120,z:0},{x:120,z:12}],w=overviewHousingGeometry(wedge,terrain,6,{block:true});assert.ok(w.userData.visualModules>0);assert.ok(w.userData.omittedSliverAreaSquareMetres<15,'only the physically too narrow tip may remain as ground');w.dispose();
const defenseData=read('data/urban/defense-timeline.v1.json'),wall=compileWallReference(read('data/urban/old-city-walls.reference.v1.json'),terrain);
for(const pack of ['roman-byzantine-islamic','medieval-ottoman','expansion-modern']){const data=read(`data/urban/${pack}.skeleton.v1.json`);for(const phase of Object.keys(data.phases)){
 const r=applyMetricResidentialRegistration(compileIndependentLaterSkeleton(data,phase,data.origin,{wallReference:wall})),rings=housingBoundaryAt({phaseId:phase,offset:.9,defenseData,wallReference:wall,origin:data.origin}).rings;r.housingBoundaryRings=rings;completeUrbanCoverage(r,{rings});
 const runtime=buildIndependentLaterSkeleton(new THREE.Group(),r,{inferred:material},terrain),blocks=runtime.meshes.filter(m=>m.userData.overview);let maximum=0,omitted=0,roofArea=0;
 for(const m of blocks){const d=m.geometry.userData;assert.ok(d.maxVisualModuleSpanMetres<=limit+1e-5,phase);maximum=Math.max(maximum,d.maxVisualModuleSpanMetres);omitted+=d.omittedSliverAreaSquareMetres;const p=m.geometry.attributes.position;for(let i=0;i<p.count;i+=3){for(let k=0;k<3;k++){const j=(k+1)%3;assert.ok(Math.hypot(p.getX(i+k)-p.getX(i+j),p.getZ(i+k)-p.getZ(i+j))<=limit+1e-4,'actual rendered triangle edge must not span a knife wall');}if([0,1,2].every(k=>p.getY(i+k)>105)){const a=[0,1,2].map(k=>({x:p.getX(i+k),z:p.getZ(i+k)}));roofArea+=Math.abs((a[1].x-a[0].x)*(a[2].z-a[0].z)-(a[1].z-a[0].z)*(a[2].x-a[0].x))/2;}}}
 assert.ok(roofArea>0);assert.ok(omitted/roofArea<.01,'thin-tip rejection cannot clear large neighbourhoods');rows.push({phase,maximum,omitted,roofArea,blocks:blocks.length});runtime.meshes.forEach(m=>m.geometry.dispose());runtime.disposeMaterials();
}}
material.dispose();console.log(JSON.stringify(rows,null,2));console.log('PASS:124m needle reproduced, bounded actual roof modules in8later phases, narrow lots retained as solids, only tiny unbuildable tips omitted');
