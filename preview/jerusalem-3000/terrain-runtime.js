import * as THREE from 'three';
export const TERRAIN_AUTHORITY_URL='./data/terrain-authority.json';
export const TERRAIN_MANIFEST_URL='./data/terrain-manifest.json';
const EARTH=6378137,DEG=Math.PI/180;
const MODULE_BASE=new URL('.',import.meta.url);
const MANIFEST_URL=new URL(TERRAIN_MANIFEST_URL,MODULE_BASE);
export function geographicToENU(lat,lon,origin){return{north:(lat-origin.lat)*DEG*EARTH,east:(lon-origin.lon)*DEG*EARTH*Math.cos(origin.lat*DEG)}}
export async function loadTerrainAuthority(){const authorityUrl=new URL(TERRAIN_AUTHORITY_URL,MODULE_BASE);const[authority,manifest]=await Promise.all([fetch(authorityUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`terrain authority unavailable (${r.status}) ${r.url}`);return r.json()}),fetch(MANIFEST_URL,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`terrain manifest unavailable (${r.status}) ${r.url}`);return r.json()})]);Object.defineProperty(manifest,'__manifestUrl',{value:MANIFEST_URL.href,enumerable:false});return{authority,manifest}}
function resolveTerrainAsset(manifest,path){return new URL(path,manifest.__manifestUrl||MANIFEST_URL.href)}
// Sample the rendered DEM triangles, avoiding bilinear heights that can hide
// narrow footpaths beneath the triangulated terrain surface.
export function sampleRenderedTerrainHeight(terrain,x,z) {
  const p=terrain.mesh?.geometry?.attributes?.position,g=terrain.grid;
  if(!p||!g?.width||!g?.height) return terrain.heightAtWorld?.(x,z)??NaN;
  const rawU=(x-terrain.mesh.position.x-p.getX(0))/(p.getX(g.width-1)-p.getX(0))*(g.width-1);
  const rawV=(z-terrain.mesh.position.z-p.getZ(0))/(p.getZ((g.height-1)*g.width)-p.getZ(0))*(g.height-1);
  // Float32 mesh extents can differ by sub-millimetres from source bounds.
  const epsilon=1e-5;
  if(rawU< -epsilon||rawV< -epsilon||rawU>g.width-1+epsilon||rawV>g.height-1+epsilon) return NaN;
  const u=Math.max(0,Math.min(g.width-1,rawU)),v=Math.max(0,Math.min(g.height-1,rawV));
  const col=Math.min(g.width-2,Math.floor(u)),row=Math.min(g.height-2,Math.floor(v)),a=u-col,b=v-row,i=row*g.width+col;
  const h00=p.getY(i),h10=p.getY(i+1),h01=p.getY(i+g.width),h11=p.getY(i+g.width+1);
  return (a+b<=1?h00+a*(h10-h00)+b*(h01-h00):h11+(1-a)*(h01-h11)+(1-b)*(h10-h11))+terrain.mesh.position.y;
}

export async function loadCanonicalTerrain(manifest,root){
  if(manifest.elevationGrid){const gridUrl=resolveTerrainAsset(manifest,manifest.elevationGrid);const g=await fetch(gridUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`canonical elevation grid unavailable (${r.status}) ${r.url}`);return r.json()});if(g.schema!=='j3k-elevation-grid-v1')throw new Error('unsupported elevation grid schema');const nw=geographicToENU(g.bounds.north,g.bounds.west,g.origin),se=geographicToENU(g.bounds.south,g.bounds.east,g.origin),geometry=new THREE.PlaneGeometry(se.east-nw.east,nw.north-se.north,g.width-1,g.height-1);geometry.rotateX(-Math.PI/2);const p=geometry.attributes.position;let min=Infinity,max=-Infinity;for(let i=0;i<p.count;i++){const x=i%g.width,y=Math.floor(i/g.width),e=g.values[y*g.width+x];min=Math.min(min,e);max=Math.max(max,e);p.setY(i,e-g.verticalDatumOffsetMetres)}geometry.computeVertexNormals();const material=new THREE.MeshStandardMaterial({color:0xc8b99e,roughness:.96,metalness:0}),mesh=new THREE.Mesh(geometry,material);mesh.name='canonical-jerusalem-dem';mesh.position.set((nw.east+se.east)/2,0,-(nw.north+se.north)/2);mesh.receiveShadow=true;root?.add(mesh);const sampler={mesh,grid:g},heightAtWorld=(east,z)=>sampleRenderedTerrainHeight(sampler,east,z);return{mesh,grid:g,min,max,sourceUrl:gridUrl.href,heightAtWorld,sampleElevation:(lat,lon)=>{const p=geographicToENU(lat,lon,g.origin);return heightAtWorld(p.east,-p.north)},dispose(){geometry.dispose();material.dispose();mesh.removeFromParent()}}}
  if(manifest.mesh?.url){const meshUrl=resolveTerrainAsset(manifest,manifest.mesh.url);const mesh=await fetch(meshUrl,{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error(`canonical terrain mesh unavailable (${r.status}) ${r.url}`);return r.json()});if(mesh.schema!=='j3k-terrain-mesh-v1')throw new Error('unsupported terrain mesh schema');return mesh}return null;
}
export function terrainRuntimeState(manifest){if(manifest.elevationGrid||manifest.mesh?.url)return{mode:'mesh',label:'REAL TERRAIN',ready:true};return{mode:'schematic',label:'TERRAIN DATA PENDING',ready:false}}
