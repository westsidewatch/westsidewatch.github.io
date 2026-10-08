// Provisional geometry adapter. It does not claim archaeological road or parcel locations.
// A source-specific registration must replace this scaffold before historical certification.
export function deriveEraRegistration(reference, phaseId, footprint) {
  if (!reference?.districts?.length || !reference?.roads?.length)
    throw new Error('Reference registration needs districts and roads');
  if (!phaseId || !footprint) throw new Error('Era registration needs a phase and footprint');
  const { cx = 0, cz = 0, sx = 1, sz = 1 } = footprint;
  const transform = ({ x, z }) => ({ x: x * sx + cx, z: z * sz + cz });
  const districts = reference.districts.map((district, index) => ({
    ...district,
    id: `j3k:${phaseId}:district:${index}`,
    confidence: 'inferred',
    geometry: {
      ...district.geometry,
      status: 'provisional-era-footprint-not-surveyed',
      polygon: district.geometry.polygon.map(transform),
    },
    sources: ['legacy-era-footprint', 'canonical-dem'],
    upgradeRequired: 'period-specific archaeological district registration',
  }));
  const roads = reference.roads.map((road, index) => ({
    ...road,
    id: `j3k:${phaseId}:road:${index}`,
    confidence: 'inferred',
    geometry: {
      ...road.geometry,
      status: 'provisional-era-road-not-surveyed',
      points: road.geometry.points.map(transform),
    },
  }));
  return {
    schema: 'j3k.temporal-city.registration.v1',
    phase: phaseId,
    authority: 'inferred geometry derived from legacy era footprint; not historical survey',
    districts,
    roads,
    generation: {
      ...reference.generation,
      scope: 'provisional-era-footprint',
      blockSize: Math.max(35, Math.round((reference.generation?.blockSize || 96) * Math.min(sx, sz))),
      roadClearance: Math.max(8, Math.round((reference.generation?.roadClearance || 18) * Math.min(sx, sz))),
    },
  };
}
