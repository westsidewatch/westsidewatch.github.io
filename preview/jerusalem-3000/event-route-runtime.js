import {buildTerrainSampler} from './object-terrain-runtime.js';

export function drapeEventRoute(route,mesh){
  const sample=buildTerrainSampler(mesh);
  return {...route,segments:route.segments.map(segment=>{
    if(!segment.coordinatesENU) return {...segment,drapedCoordinates:null};
    return {...segment,drapedCoordinates:segment.coordinatesENU.map(([east,north])=>{
      const hit=sample(east,north);
      return {enu:[east,hit.up,north],sampleDistanceMetres:hit.distanceMetres};
    })};
  })};
}

export function routeEvidenceClass(status){
  if(status==='textual-anchor') return 'known';
  if(status==='topographic-reconstruction'||status==='topographic-inference') return 'inferred';
  if(status==='disputed-exact-gate') return 'disputed';
  return 'withheld';
}

export function validateEventRoute(route){
  const nodeIds=new Set(route.nodes.map(n=>n.id));
  const errors=[];
  for(const s of route.segments){
    if(!nodeIds.has(s.from)||!nodeIds.has(s.to)) errors.push(`${s.id}: orphan endpoint`);
    if(s.geometry==='withheld'&&s.coordinatesENU) errors.push(`${s.id}: withheld segment has coordinates`);
  }
  return errors;
}
