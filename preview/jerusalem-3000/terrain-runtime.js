export const TERRAIN_AUTHORITY_URL='./data/terrain-authority.json';
export const TERRAIN_MANIFEST_URL='./data/terrain-manifest.json';

export async function loadTerrainAuthority(){
  const [authority,manifest]=await Promise.all([
    fetch(TERRAIN_AUTHORITY_URL).then(r=>{if(!r.ok)throw new Error('terrain authority unavailable');return r.json()}),
    fetch(TERRAIN_MANIFEST_URL).then(r=>{if(!r.ok)throw new Error('terrain manifest unavailable');return r.json()})
  ]);
  return {authority,manifest};
}

export async function loadCanonicalTerrain(manifest){
  if(!manifest.mesh?.url) return null;
  const mesh=await fetch(manifest.mesh.url).then(r=>{if(!r.ok)throw new Error('canonical terrain mesh unavailable');return r.json()});
  if(mesh.schema!=='j3k-terrain-mesh-v1') throw new Error('unsupported terrain mesh schema');
  return mesh;
}

export function terrainRuntimeState(manifest){
  if(manifest.mesh?.url) return {mode:'mesh',label:'REAL TERRAIN',ready:true};
  return {mode:'schematic',label:'TERRAIN DATA PENDING',ready:false};
}
