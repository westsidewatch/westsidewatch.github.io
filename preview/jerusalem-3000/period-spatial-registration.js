import { geographicToENU } from './terrain-runtime.js';

// Design envelopes and paths, geographically anchored without inheriting Herodian streets.
export function compilePeriodRegistration(data, phaseId, origin) {
  if (data?.schema !== 'j3k.period-spatial-layout.v1' || data.frame !== 'spring-relative-east-x-south-z-metres')
    throw new Error('Unsupported period spatial layout');
  const phase = data.phases?.[phaseId];
  if (!phase?.districts?.length || !phase.roads?.length) throw new Error(`Missing independent layout: ${phaseId}`);
  if (![origin?.lat, origin?.lon, data.anchor?.lat, data.anchor?.lon].every(Number.isFinite))
    throw new Error('Period layout requires a geographic anchor and terrain origin');
  const anchor = geographicToENU(data.anchor.lat, data.anchor.lon, origin);
  const point = p => {
    if (!Array.isArray(p) || p.length !== 2 || !p.every(Number.isFinite)) throw new Error('Invalid period spatial point');
    return { x: anchor.east + p[0], z: -anchor.north + p[1] };
  };
  const ids = new Set();
  const id = (kind, value) => {
    if (typeof value !== 'string' || !value || ids.has(`${kind}:${value}`)) throw new Error('Invalid or duplicate spatial ID');
    ids.add(`${kind}:${value}`);
    return `j3k:${phaseId}:${kind}:${value}`;
  };
  const geometry = (points, minimum, kind) => {
    if (!Array.isArray(points) || points.length < minimum) throw new Error(`Invalid ${kind} geometry`);
    const converted = points.map(point);
    if (kind === 'polygon') {
      const area = converted.reduce((sum,p,i) => {const q=converted[(i+1)%converted.length];return sum+p.x*q.z-q.x*p.z;},0);
      if (Math.abs(area) < 2) throw new Error('Degenerate period polygon');
    } else if (converted.every(p => p.x === converted[0].x && p.z === converted[0].z)) throw new Error('Degenerate period road');
    return { primitive: kind, frame: 'scene-local-metres', status: 'independent-inferred-not-surveyed', [kind === 'polygon' ? 'polygon' : 'points']: converted };
  };
  const districts = phase.districts.map(d => ({id:id('district',d.id), confidence:'inferred', geometry:geometry(d.polygon,3,'polygon'), sources:data.sources}));
  const roads = phase.roads.map(r => ({id:id('road',r.id), confidence:'inferred', geometry:geometry(r.points,2,'polyline')}));
  const reservations = (phase.reservations || []).map(r => ({id:id('reservation',r.id), metadata:{groundRole:'public-context'}, polygon:geometry(r.polygon,3,'polygon').polygon}));
  return {schema:'j3k.temporal-city.registration.v1',phase:phaseId,authority:data.authority,
    independentLayout:true,districts,roads,reservations,sources:data.sources,limitations:data.limitations,
    generation:{scope:'independent-period-districts',blockSize:58,roadClearance:6,infillMode:'district-constrained',maxBlockArea:12000,architectureProfile:phase.residentialArchitecture}};
}
