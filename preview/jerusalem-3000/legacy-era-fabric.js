import * as THREE from 'three';
// Existing illustrative footprints, not surveyed city boundaries.
export const ERA_FOOTPRINTS = {
  'chalcolithic-early-bronze': {
    cx: -430,
    cz: 360,
    sx: 0.38,
    sz: 0.52,
    density: 7,
  },
  'middle-bronze': { cx: -360, cz: 300, sx: 0.5, sz: 0.65, density: 10 },
  'late-bronze-iron1': { cx: -330, cz: 270, sx: 0.58, sz: 0.72, density: 12 },
  'david-solomon': { cx: -260, cz: 210, sx: 0.7, sz: 0.82, density: 18 },
  'late-first-temple': { cx: -100, cz: 120, sx: 1.05, sz: 1.05, density: 28 },
  'babylonian-destruction': {
    cx: -100,
    cz: 120,
    sx: 1.05,
    sz: 1.05,
    density: 18,
  },
  'persian-nehemiah': { cx: -220, cz: 170, sx: 0.72, sz: 0.82, density: 18 },
  'hellenistic-hasmonean': { cx: -40, cz: 80, sx: 1.05, sz: 1.02, density: 30 },
  'herodian-jesus': { cx: 80, cz: 0, sx: 1.25, sz: 1.15, density: 40 },
  'roman-destruction': { cx: 80, cz: 0, sx: 1.25, sz: 1.15, density: 24 },
  aelia: { cx: 40, cz: -40, sx: 1.02, sz: 1.02, density: 28 },
  byzantine: { cx: 20, cz: -30, sx: 1.14, sz: 1.1, density: 34 },
  'early-islamic': { cx: 10, cz: -20, sx: 1.08, sz: 1.06, density: 32 },
  crusader: { cx: 0, cz: -20, sx: 0.96, sz: 0.94, density: 30 },
  'ayyubid-mamluk': { cx: 0, cz: -10, sx: 1, sz: 0.98, density: 32 },
  ottoman: { cx: 0, cz: 0, sx: 1.02, sz: 1, density: 38 },
  'outside-walls': { cx: 55, cz: -35, sx: 1.28, sz: 1.18, density: 48 },
  modern: { cx: 120, cz: -80, sx: 1.65, sz: 1.5, density: 58 },
};
function terrainY(terrain, x, z) {
  const y = terrain?.heightAtWorld?.(x, z);
  return Number.isFinite(y) ? y : 0;
}
export function addEraFabric(
  group,
  phaseId,
  material,
  ruined = false,
  terrain = null,
) {
  const era = ERA_FOOTPRINTS[phaseId];
  if (!era) return [];
  const meshes = [];
  for (let i = 0; i < era.density; i++) {
    const col = i % 8,
      row = Math.floor(i / 8),
      jx = ((i * 47) % 71) - 35,
      jz = ((i * 29) % 59) - 29,
      x = era.cx + (col - 3.5) * 125 * era.sx + jx,
      z = era.cz + (row - 2.2) * 125 * era.sz + jz,
      w = (62 + ((i * 17) % 70)) * era.sx,
      d = (54 + ((i * 23) % 62)) * era.sz,
      h = ruined ? 12 + (i % 3) * 4 : 34 + ((i * 19) % 72);
    const mesh = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), material);
    mesh.userData.foundation={owner:'legacy-footprint',phaseId,role:'provisional-mass',historicalGeometryVerified:false};
    mesh.userData.phase2={stage:'mass',start:0,baseHeight:h};
    mesh.position.set(x, terrainY(terrain, x, z) + h / 2 + 4, z);
    mesh.rotation.y = (((i * 13) % 17) - 8) * 0.018;
    mesh.receiveShadow = true;
    group.add(mesh);
    meshes.push(mesh);
  }
  return meshes;
}
