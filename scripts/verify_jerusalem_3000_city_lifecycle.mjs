import assert from 'node:assert/strict';
import { HistoricalTimeEngine } from '../preview/jerusalem-3000/historical-time-engine.js';
import { RuinTransformationEngine } from '../preview/jerusalem-3000/ruin-transformation-engine.js';
import { createCityProjection } from '../preview/jerusalem-3000/city-lifecycle-projection.js';
import { auditProductionReadiness } from '../preview/jerusalem-3000/production-readiness.js';
import { readFileSync } from 'node:fs';
import { polygonsOverlap } from '../preview/jerusalem-3000/urban-exclusion.js';
const phases = JSON.parse(
  readFileSync(
    new URL(
      '../preview/jerusalem-3000/data/continuous-build-timeline.json',
      import.meta.url,
    ),
  ),
).phases;
const time = new HistoricalTimeEngine(phases),
  ruin = new RuinTransformationEngine(phases);
const mesh = {
  position: { x: 10, y: 130, z: 20 },
  scale: { y: 1 },
  userData: {
    cityObject: {
      parcelId: 'parcel-1',
      confidence: 'inferred',
      terrainGround: 100,
    },
    phase2: { groundY: 120 },
  },
};
const group = {},
  projection = createCityProjection(group, [mesh]);
const original = JSON.stringify({ position: mesh.position, scale: mesh.scale });
for (const position of [8, 8.9, 9, 9.25, 9.5, 9.9, 10, 9.5, 9, 8]) {
  const phase = time.sample(position).phase.id;
  assert.equal(phase, phases[Math.floor(position)].id);
  projection.apply({ phaseId: phase, ruin: ruin.sample(position).ruin });
  assert.equal(projection.diagnostics().visibleBuildings, position === 10 ? 0 : 1);
  assert.equal(mesh.userData.cityObject.buildingId, 'parcel-1:building');
  assert.equal(mesh.position.x, 10);
  assert.equal(mesh.position.z, 20);
  assert.ok(mesh.position.y >= 100);
  if (position === 9.5)
    assert.equal(mesh.userData.cityObject.lifecycleState, 'destruction');
  if (position === 10) assert.equal(group.visible, false, 'Aelia must not display a standing Herodian city');
}
assert.equal(
  JSON.stringify({ position: mesh.position, scale: mesh.scale }),
  original,
  'reverse scrub must restore exact transforms',
);
projection.apply({
  phaseId: 'herodian-jesus',
  evidenceAllowed: (c) => c === 'observed',
});
assert.equal(mesh.visible, false);
projection.apply({ phaseId: 'modern' });
assert.equal(group.visible, false);
const healthy = {
  status: 'ready',
  three: true,
  timeline: true,
  evidence: true,
  timeEngine: true,
  ruinEngine: true,
  evidenceObjects: {
    evidenceResolutionAudit: { ok: true },
    cityCoreAB: {
      ok: true,
      buildings: 1,
      semanticBoxes: 0,
      validation: { ok: true },
    },
  },
};
assert.equal(auditProductionReadiness(healthy).ok, true);
healthy.evidenceObjects.cityCoreAB.ok = false;
assert.ok(
  auditProductionReadiness(healthy).failures.includes('canonical-city-core'),
);
const rect = (x, z, w, d) => [
  { x, z },
  { x: x + w, z },
  { x: x + w, z: z + d },
  { x, z: z + d },
];
assert.ok(
  polygonsOverlap(rect(0, 0, 10, 10), rect(2, 2, 2, 2)),
  'contained monuments are reserved',
);
assert.ok(
  polygonsOverlap(rect(-20, -1, 40, 2), rect(-1, -20, 2, 40)),
  'crossing edges are reserved even without contained vertices',
);
assert.ok(
  polygonsOverlap(rect(0, 0, 10, 10), rect(10, 0, 10, 10)),
  'touching boundary is reserved',
);
assert.equal(polygonsOverlap(rect(0, 0, 10, 10), rect(11, 0, 10, 10)), false);
console.log(
  'PASS: stable identities, continuous ruin, exact reverse transforms, evidence filtering, failed-core rejection',
);
