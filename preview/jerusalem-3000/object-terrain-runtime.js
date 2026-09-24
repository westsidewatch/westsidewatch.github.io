export function buildTerrainSampler(mesh){
  const vertices=(mesh.vertices||[]).filter(Boolean);
  if(!vertices.length) throw new Error('terrain mesh has no valid vertices');
  return function sampleUp(east,north){
    let best=null;
    for(const v of vertices){
      const de=v[0]-east,dn=v[2]-north,d2=de*de+dn*dn;
      if(!best||d2<best.d2) best={d2,up:v[1]};
    }
    return {up:best.up,distanceMetres:Math.sqrt(best.d2),method:'nearest-canonical-terrain-vertex'};
  };
}

export function registerObjectsToTerrain(objects,mesh){
  const sample=buildTerrainSampler(mesh);
  return objects.map(object=>{
    const enu=object.spatial?.enuMetres;
    if(!enu) return object;
    const hit=sample(enu.east,enu.north);
    return {...object,spatial:{...object.spatial,enuMetres:{...enu,up:hit.up},elevationRegistration:{...hit,authority:'canonical-terrain-mesh'}}};
  });
}

export function threePosition(spatial){
  const p=spatial?.enuMetres;
  if(!p||p.up==null) return null;
  return [p.east,p.up,p.north];
}
