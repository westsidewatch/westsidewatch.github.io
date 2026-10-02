// Temporal facade-opening grammar for Jerusalem 3000.
// Adds a reusable urban layer above parcel massing without replacing evidence-driven geometry.

export const TEMPORAL_FACADE_PROFILES = Object.freeze({
  'herodian-jesus': Object.freeze({
    doorWidth: [0.82, 1.18], doorHeight: [1.78, 2.22],
    windowWidth: [0.42, 0.76], windowHeight: [0.48, 0.88],
    sillHeight: [1.18, 1.72], windowChance: 0.58,
    upperWindowChance: 0.72, shopfrontChance: 0.12,
    rhythm: [1.9, 3.6], recess: 0.055,
  }),
  default: Object.freeze({
    doorWidth: [0.78, 1.16], doorHeight: [1.75, 2.2],
    windowWidth: [0.4, 0.78], windowHeight: [0.46, 0.9],
    sillHeight: [1.15, 1.75], windowChance: 0.52,
    upperWindowChance: 0.66, shopfrontChance: 0.08,
    rhythm: [2.0, 3.8], recess: 0.05,
  }),
});

const rangeValue = (range, random) => range[0] + (range[1] - range[0]) * random();

function stableRandom(seed = 1) {
  let state = (seed >>> 0) || 1;
  return () => {
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

function facadeSeed(buildingId = '', face = 'south') {
  const source = `${buildingId}:${face}`;
  let hash = 2166136261;
  for (let i = 0; i < source.length; i += 1) {
    hash ^= source.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

export function buildFacadeOpenings({ buildingId, phaseId = 'default', face = 'south', width, height, floors = 1, streetFacing = true } = {}) {
  if (!streetFacing || !Number.isFinite(width) || width < 2.2 || !Number.isFinite(height) || height < 1.8) return [];

  const profile = TEMPORAL_FACADE_PROFILES[phaseId] || TEMPORAL_FACADE_PROFILES.default;
  const random = stableRandom(facadeSeed(buildingId, face));
  const openings = [];
  const doorWidth = Math.min(rangeValue(profile.doorWidth, random), width * 0.32);
  const doorHeight = Math.min(rangeValue(profile.doorHeight, random), height * 0.72);
  const doorX = (random() - 0.5) * Math.max(0, width - doorWidth - 0.5) * 0.7;

  openings.push({ kind: random() < profile.shopfrontChance ? 'shop-door' : 'door', x: doorX, y: doorHeight * 0.5, width: doorWidth, height: doorHeight, recess: profile.recess });

  const rhythm = rangeValue(profile.rhythm, random);
  const slots = Math.max(1, Math.floor(width / rhythm));
  const floorHeight = height / Math.max(1, floors);
  for (let floor = 0; floor < floors; floor += 1) {
    const chance = floor === 0 ? profile.windowChance : profile.upperWindowChance;
    for (let slot = 0; slot < slots; slot += 1) {
      if (random() > chance) continue;
      const x = -width * 0.5 + ((slot + 0.5) / slots) * width;
      if (floor === 0 && Math.abs(x - doorX) < doorWidth * 0.9) continue;
      const windowWidth = Math.min(rangeValue(profile.windowWidth, random), rhythm * 0.42);
      const windowHeight = Math.min(rangeValue(profile.windowHeight, random), floorHeight * 0.42);
      const sill = rangeValue(profile.sillHeight, random);
      const y = Math.min(floor * floorHeight + sill + windowHeight * 0.5, (floor + 1) * floorHeight - windowHeight * 0.62);
      openings.push({ kind: 'window', x, y, width: windowWidth, height: windowHeight, recess: profile.recess });
    }
  }
  return openings;
}

export function resolveStreetFacingFaces({ streetEdges = [] } = {}) {
  const faces = new Set();
  for (const edge of streetEdges) {
    if (edge === 'north' || edge === 'south' || edge === 'east' || edge === 'west') faces.add(edge);
  }
  return [...faces];
}
