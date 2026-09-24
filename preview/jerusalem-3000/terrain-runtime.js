export const TERRAIN_AUTHORITY_URL='./data/terrain-authority.json';
export const TERRAIN_MANIFEST_URL='./data/terrain-manifest.json';

export async function loadTerrainAuthority(){
  const [authority,manifest]=await Promise.all([
    fetch(TERRAIN_AUTHORITY_URL).then(r=>{if(!r.ok)throw new Error('terrain authority unavailable');return r.json()}),
    fetch(TERRAIN_MANIFEST_URL).then(r=>{if(!r.ok)throw new Error('terrain manifest unavailable');return r.json()})
  ]);
  return {authority,manifest};
}

export function terrainRuntimeState(manifest){
  if(manifest.mesh?.url) return {mode:'mesh',label:'REAL TERRAIN',ready:true};
  return {mode:'schematic',label:'TERRAIN DATA PENDING',ready:false};
}
