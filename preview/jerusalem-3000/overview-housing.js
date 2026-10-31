import {overviewPlanForArchitecture} from './residential-era-profiles.js';
import * as THREE from 'three';
import {partitionOverviewBlock,overviewModuleMetrics} from './overview-block-layout.js';
export const OVERVIEW_HOUSING_GRAMMAR='terrain-courtyard-mass-v1';
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const inset=(p,f)=>{const c={x:p.reduce((s,v)=>s+v.x,0)/p.length,z:p.reduce((s,v)=>s+v.z,0)/p.length};return p.map(v=>({x:c.x+(v.x-c.x)*f,z:c.z+(v.z-c.z)*f}));};
export function overviewHousingGeometry(polygon,terrain,height,{block=false,singleRoom=false,admitPolygon=null,metricPolicy=null,planForm=singleRoom?'single-room':'courtyard'}={}){
 if(!polygon||polygon.length<3||area(polygon)<1||polygon.some(p=>![p.x,p.z].every(Number.isFinite))||!Number.isFinite(height)||height<=0)throw new Error('Invalid overview housing');
 if(!['single-room','courtyard','four-room-analogy','open-court'].includes(planForm))throw new Error('Unknown residential plan form');
 const cells=block?partitionOverviewBlock(polygon):[polygon];
 const vertices=[];let projectedRoofAreaSquareMetres=0,roofRanges=0,withheldVisualModules=0,slenderSolidModules=0,maxVisualModuleSpanMetres=0,omittedSliverAreaSquareMetres=0;
 const solid=raw=>{let p=raw;const signed=p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0);if(signed<0)p=[...p].reverse();const y=p.map(v=>terrain.heightAtWorld(v.x,v.z));if(y.some(v=>!Number.isFinite(v)))throw new Error('Overview outside canonical DEM');const push=(i,top)=>vertices.push(p[i].x,y[i]+(top?height:.2),p[i].z);for(const t of THREE.ShapeUtils.triangulateShape(p.map(v=>new THREE.Vector2(v.x,v.z)),[]))for(const i of [...t].reverse())push(i,true);for(let i=0;i<p.length;i++){const j=(i+1)%p.length;for(const [k,top]of [[i,false],[j,true],[j,false],[i,false],[i,true],[j,true]])push(k,top);}projectedRoofAreaSquareMetres+=area(p);roofRanges++;};
 for(const cell of cells){const outer=metricPolicy&&!block?cell:inset(cell,.92);if(outer.length<3||area(outer)<1){withheldVisualModules++;continue;}if(admitPolygon&&!admitPolygon(outer)){withheldVisualModules++;continue;}const shape=overviewModuleMetrics(outer);if(block&&shape.width<1.5){withheldVisualModules++;omittedSliverAreaSquareMetres+=area(outer);continue;}maxVisualModuleSpanMetres=Math.max(maxVisualModuleSpanMetres,shape.span);if(planForm==='single-room'||area(outer)<30||shape.width<6){if(shape.width<6)slenderSolidModules++;solid(outer);continue;}if(['four-room-analogy','open-court'].includes(planForm)&&outer.length===4){
  // Bilinear ranges stay inside a convex registered quadrilateral. Match the
  // detailed low-rise grammar: two longitudinal wings and a broad rear room.
  const point=(u,v)=>({x:outer[0].x*(1-u)*(1-v)+outer[1].x*u*(1-v)+outer[2].x*u*v+outer[3].x*(1-u)*v,z:outer[0].z*(1-u)*(1-v)+outer[1].z*u*(1-v)+outer[2].z*u*v+outer[3].z*(1-u)*v});
  const rect=(u0,v0,u1,v1)=>solid([point(u0,v0),point(u1,v0),point(u1,v1),point(u0,v1)]);
  const side=planForm==='four-room-analogy'?.3:.27,rear=planForm==='four-room-analogy'?.72:.74;
  rect(0,0,side,rear);rect(1-side,0,1,rear);rect(0,rear,1,1);
 }else{
  const inner=inset(outer,planForm==='open-court'?.56:.48);
  for(let i=0;i<outer.length;i++){const j=(i+1)%outer.length;if(!['four-room-analogy','open-court'].includes(planForm)||i!==0)solid([outer[i],outer[j],inner[j],inner[i]]);}
 }}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();g.userData={overviewGrammar:OVERVIEW_HOUSING_GRAMMAR,planForm,roofReconstructionVerified:false,visualModules:cells.length-withheldVisualModules,withheldVisualModules,roofRanges,projectedRoofAreaSquareMetres,slenderSolidModules,maxVisualModuleSpanMetres,omittedSliverAreaSquareMetres,semanticBuildings:!block,archaeologicalSubdivision:false,subdivision:block?'boundary-aligned-adaptive-mass-v1':'existing-parcel',worldGrid:false,metricPolicy:metricPolicy?{metresPerSceneUnit:1,maxParcelSpanMetres:block?null:metricPolicy.maxParcelSpanMetres,moduleScope:block?'existing-coarse-block-not-a-house':'new-metre-parcel',dimensionsHistoricallyVerified:false}:null};return g;
}
export function buildOverviewHouse(group,meshes,materials,terrain,parcel,index,profile){
 if(profile&&(!Number.isFinite(profile.wallHeightMetres)||profile.wallHeightMetres<2.2||profile.wallHeightMetres>4.6))throw new Error('Invalid overview profile height');
 const height=profile?profile.wallHeightMetres:4.5,geometry=overviewHousingGeometry(parcel.geometry.polygon,terrain,height,{metricPolicy:parcel.metadata?.metricPolicy,planForm:overviewPlanForArchitecture(profile)}),mesh=new THREE.Mesh(geometry,materials.lowRise||materials.inferred||materials.reconstructed);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage:'overview-courtyard',start:.25,baseHeight:height,groundY:0};mesh.userData.cityObject={parcelId:parcel.id,terrainGround:0,kind:'overview-courtyard',confidence:'inferred',semantic:true};mesh.userData.overview={grammar:OVERVIEW_HOUSING_GRAMMAR};
 // Store vertex-ground authority for the same exact reversible ruin projection.
 mesh.userData.restPositions=new Float32Array(geometry.attributes.position.array);mesh.userData.groundHeights=Array.from({length:geometry.attributes.position.count},(_,i)=>terrain.heightAtWorld(geometry.attributes.position.getX(i),geometry.attributes.position.getZ(i))+.2);
 group.add(mesh);meshes.push(mesh);return {typology:profile?.id||'courtyard-house',components:1,terrainFit:'canonical-dem-overview'};
}
