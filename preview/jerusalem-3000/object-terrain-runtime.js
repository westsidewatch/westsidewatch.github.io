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

function drapePoint(point,sample){
  if(!Array.isArray(point)||point.length<2) throw new Error('invalid ENU geometry point');
  const east=point[0],north=point[1],hit=sample(east,north);
  return {enu:[east,hit.up,north],sampleDistanceMetres:hit.distanceMetres};
}

function drapeLine(line,sample){return line.map(p=>drapePoint(p,sample));}

export function drapeGeometryEntry(entry,mesh){
  if(entry.status==='withheld'||entry.coordinatesENU==null) return {...entry,drapedGeometry:null};
  const sample=buildTerrainSampler(mesh),g=entry.coordinatesENU;
  let coordinates;
  if(entry.geometryType==='LineString') coordinates=drapeLine(g,sample);
  else if(entry.geometryType==='MultiLineString') coordinates=g.map(line=>drapeLine(line,sample));
  else if(entry.geometryType==='Polygon') coordinates=g.map(ring=>drapeLine(ring,sample));
  else throw new Error(`unsupported geometry type: ${entry.geometryType}`);
  return {...entry,drapedGeometry:{frame:'local-enu',verticalAuthority:'canonical-terrain-mesh',coordinates}};
}

export function drapeGeometryRegistry(registry,mesh){
  return {...registry,entries:registry.entries.map(entry=>drapeGeometryEntry(entry,mesh))};
}

export function threePosition(spatial){
  const p=spatial?.enuMetres;
  if(!p||p.up==null) return null;
  return [p.east,p.up,p.north];
}
