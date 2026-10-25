import * as THREE from 'three';
export const OVERVIEW_HOUSING_GRAMMAR='terrain-courtyard-mass-v1';
const area=p=>Math.abs(p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0))/2;
const inset=(p,f)=>{const c={x:p.reduce((s,v)=>s+v.x,0)/p.length,z:p.reduce((s,v)=>s+v.z,0)/p.length};return p.map(v=>({x:c.x+(v.x-c.x)*f,z:c.z+(v.z-c.z)*f}));};
function clip(p,axis,limit,sign){const out=[];for(let i=0;i<p.length;i++){const a=p[i],b=p[(i+1)%p.length],da=(a[axis]-limit)*sign,db=(b[axis]-limit)*sign;if(da<=0)out.push(a);if((da<0&&db>0)||(da>0&&db<0)){const t=da/(da-db);out.push({x:a.x+(b.x-a.x)*t,z:a.z+(b.z-a.z)*t});}}return out;}
export function overviewHousingGeometry(polygon,terrain,height,{block=false,singleRoom=false}={}){
 if(!polygon?.length||polygon.some(p=>![p.x,p.z].every(Number.isFinite))||!Number.isFinite(height)||height<=0)throw new Error('Invalid overview housing');
 let cells=[polygon];if(block){cells=[];const xs=polygon.map(p=>p.x),zs=polygon.map(p=>p.z);for(let x=Math.floor(Math.min(...xs)/18)*18;x<Math.max(...xs);x+=18)for(let z=Math.floor(Math.min(...zs)/18)*18;z<Math.max(...zs);z+=18){let p=polygon;for(const [axis,limit,sign]of [['x',x+1,-1],['x',x+17,1],['z',z+1,-1],['z',z+17,1]])p=clip(p,axis,limit,sign);if(p.length>=3&&area(p)>16)cells.push(p);}}
 if(!cells.length)cells=[polygon];
 const vertices=[];let roofRanges=0;
 const solid=raw=>{let p=raw;const signed=p.reduce((s,a,i)=>{const b=p[(i+1)%p.length];return s+a.x*b.z-b.x*a.z;},0);if(signed<0)p=[...p].reverse();const y=p.map(v=>terrain.heightAtWorld(v.x,v.z));if(y.some(v=>!Number.isFinite(v)))throw new Error('Overview outside canonical DEM');const push=(i,top)=>vertices.push(p[i].x,y[i]+(top?height:.2),p[i].z);for(const t of THREE.ShapeUtils.triangulateShape(p.map(v=>new THREE.Vector2(v.x,v.z)),[]))for(const i of [...t].reverse())push(i,true);for(let i=0;i<p.length;i++){const j=(i+1)%p.length;for(const [k,top]of [[i,false],[j,true],[j,false],[i,false],[i,true],[j,true]])push(k,top);}roofRanges++;};
 for(const cell of cells){const outer=inset(cell,.92);if(singleRoom||area(outer)<30){solid(outer);continue;}const inner=inset(outer,.48);for(let i=0;i<outer.length;i++){const j=(i+1)%outer.length;solid([outer[i],outer[j],inner[j],inner[i]]);}}
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.computeVertexNormals();g.userData={overviewGrammar:OVERVIEW_HOUSING_GRAMMAR,visualModules:cells.length,roofRanges,semanticBuildings:!block,archaeologicalSubdivision:false};return g;
}
export function buildOverviewHouse(group,meshes,materials,terrain,parcel,index,profile){
 const height=profile?.wallHeightMetres||4.5,geometry=overviewHousingGeometry(parcel.geometry.polygon,terrain,height),mesh=new THREE.Mesh(geometry,materials.lowRise||materials.inferred||materials.reconstructed);mesh.castShadow=true;mesh.receiveShadow=true;mesh.userData.phase2={stage:'overview-courtyard',start:.25,baseHeight:height,groundY:0};mesh.userData.cityObject={parcelId:parcel.id,terrainGround:0,kind:'overview-courtyard',confidence:'inferred',semantic:true};mesh.userData.overview={grammar:OVERVIEW_HOUSING_GRAMMAR};
 // Store vertex-ground authority for the same exact reversible ruin projection.
 mesh.userData.restPositions=new Float32Array(geometry.attributes.position.array);mesh.userData.groundHeights=Array.from({length:geometry.attributes.position.count},(_,i)=>terrain.heightAtWorld(geometry.attributes.position.getX(i),geometry.attributes.position.getZ(i))+.2);
 group.add(mesh);meshes.push(mesh);return {typology:profile?.id||'courtyard-house',components:1,terrainFit:'canonical-dem-overview'};
}
