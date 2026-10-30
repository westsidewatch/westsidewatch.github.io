import * as THREE from 'three';
import {pointInPolygon} from './urban-exclusion.js';
// Colour the existing DEM only. No replacement surface, displaced terrain,
// terrace height, paving reconstruction or archaeological land-use claim.
export function createUrbanGroundPresentation(mesh){
 const attribute=mesh.geometry.getAttribute('color'),base=new Float32Array(attribute.array),p=mesh.geometry.attributes.position,n=mesh.geometry.attributes.normal,cache=new Map();let active=null,stats={phase:null,changedVertices:0};
 const sun=new THREE.Vector3(-.8,.55,.35).normalize();
 const prepare=zone=>{const xs=zone.polygon.map(p=>p.x),zs=zone.polygon.map(p=>p.z);return {...zone,minX:Math.min(...xs),maxX:Math.max(...xs),minZ:Math.min(...zs),maxZ:Math.max(...zs)};};
 const inside=(q,z)=>q.x>=z.minX&&q.x<=z.maxX&&q.z>=z.minZ&&q.z<=z.maxZ&&pointInPolygon(q,z.polygon);
 return {
  apply({key,phase,zones=[],rings=[],allowed=true}){
   key=key+'|'+allowed;if(key===active)return;let entry=cache.get(key);
   if(!entry){const indices=[],values=[],prepared=zones.map(prepare),counts={quarter:0,reserved:0,public:0};
    if(allowed)for(let i=0;i<p.count;i++){
     const q={x:p.getX(i)+mesh.position.x,z:p.getZ(i)+mesh.position.z},candidates=prepared.filter(z=>inside(q,z));if(!candidates.length)continue;
     const zone=candidates.find(z=>z.kind==='reserved')||candidates.find(z=>z.kind==='public')||candidates[0];if(rings.length&&!zone.explicitExpansion&&!rings.some(r=>pointInPolygon(q,r)))continue;
     const light=.64+.36*Math.max(0,n.getX(i)*sun.x+n.getY(i)*sun.y+n.getZ(i)*sun.z),colour=new THREE.Color(zone.kind==='reserved'?0xa9a49b:zone.kind==='public'?0xc5b99e:0xc6b69c).multiplyScalar(light);
     indices.push(i);values.push(colour.r,colour.g,colour.b);counts[zone.kind==='reserved'?'reserved':zone.kind==='public'?'public':'quarter']++;
    }
    entry={indices:new Uint32Array(indices),values:new Float32Array(values),counts};cache.set(key,entry);
   }
   attribute.array.set(base);entry.indices.forEach((index,i)=>attribute.array.set(entry.values.subarray(i*3,i*3+3),index*3));attribute.needsUpdate=true;active=key;
   stats={phase,changedVertices:entry.indices.length,...entry.counts,cachedPresentations:cache.size,terrainPositionsChanged:false,historicalLandUseVerified:false,legend:'褐色：街區示意；淺石色：公共院落／遺址語境，未定位項目不再清空街區；不代表已核定古地面'};
  },
  diagnostics:()=>({...stats}),
  dispose(){attribute.array.set(base);attribute.needsUpdate=true;cache.clear();}
 };
}
