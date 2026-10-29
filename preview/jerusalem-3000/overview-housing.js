import * as THREE from 'three';
import {partitionOverviewBlock} from './overview-block-layout.js';
export const OVERVIEW_HOUSING_GRAMMAR='terrain-courtyard-mass-v1';
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const inset=(p,f)=>{const c={x:p.reduce((s,v)=>s+v.x,0)/p.length,z:p.reduce((s,v)=>s+v.z,0)/p.length};return p.map(v=>({x:c.x+(v.x-c.x)*f,z:c.z+(v.z-c.z)*f}));};
export function overviewHousingGeometry(polygon,terrain,height,{block=false,singleRoom=false,admitPolygon=null}={}){
 if(!polygon||polygon.length<3||area(polygon)<1||polygon.some(p=>![p.x,p.z].every(Number.isFinite))||!Number.isFinite(height)||height<=0)throw new Error('Invalid overview housing');
 const cells=block?partitionOverviewBlock(polygon):[polygon];
 const vertices=[];let roofRanges=0,withheldVisualModules=0;
 const solid=raw=>{let p=raw;const signed=p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0);if(signed<0)p=[...p].reverse();const y=p.map(v=>terrain.heightAtWorld(v.x,v.z));if(y.some(v=>!Number.isFinite(v)))throw new Error('Overview outside canonical DEM');const push=(i,top)=>vertices.push(p[i].x,y[i]+(top?height:.2),p[i].z);for(const t of THREE.ShapeUtils.triangulateShape(p.map(v=>new THREE.Vector2(v.x,v.z)),[]))for(const i of [...t].reverse())push(i,true);for(let i=0;i<p.length;i++){const j=(i+1)%p.length;for(const [k,top]of [[i,false],[j,true],[j,false],[i,false],[i,true],[j,true]])push(k,top);}roofRanges++;};
 for(const cell of cells){const outer=inset(cell,.92);if(admitPolygon&&!admitPolygon(outer)){withheldVisualModules++;continue;}if(singleRoom||area(outer)<30){solid(outer);continue;}const inner=inset(outer,.48);for(let i=0;i<outer.length;i++){const j=(i+1)%outer.length;solid([outer[i],outer[j],inner[j],inner[i]]);}}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();g.userData={overviewGrammar:OVERVIEW_HOUSING_GRAMMAR,visualModules:cells.length-withheldVisualModules,withheldVisualModules,roofRanges,semanticBuildings:!block,archaeologicalSubdivision:false,subdivision:block?'boundary-aligned-adaptive-mass-v1':'existing-parcel',worldGrid:false};return g;
}
export function buildOverviewHouse(group,meshes,materials,terrain,parcel,index,profile){
 if(profile&&(!Number.isFinite(profile.wallHeightMetres)||profile.wallHeightMetres<2.2||profile.wallHeightMetres>4.6))throw new Error('Invalid overview profile height');
 const height=profile?profile.wallHeightMetres:4.5,geometry=overviewHousingGeometry(parcel.geometry.polygon,terrain,height),mesh=new THREE.Mesh(geometry,materials.lowRise||materials.inferred||materials.reconstructed);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage:'overview-courtyard',start:.25,baseHeight:height,groundY:0};mesh.userData.cityObject={parcelId:parcel.id,terrainGround:0,kind:'overview-courtyard',confidence:'inferred',semantic:true};mesh.userData.overview={grammar:OVERVIEW_HOUSING_GRAMMAR};
 // Store vertex-ground authority for the same exact reversible ruin projection.
 mesh.userData.restPositions=new Float32Array(geometry.attributes.position.array);mesh.userData.groundHeights=Array.from({length:geometry.attributes.position.count},(_,i)=>terrain.heightAtWorld(geometry.attributes.position.getX(i),geometry.attributes.position.getZ(i))+.2);
 group.add(mesh);meshes.push(mesh);return {typology:profile?.id||'courtyard-house',components:1,terrainFit:'canonical-dem-overview'};
}
