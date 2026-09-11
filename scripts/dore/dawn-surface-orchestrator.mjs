#!/usr/bin/env node

const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];

export const dawnSurfaceContract = Object.freeze({
  schema: 'dore.visual-surface-orchestrator.v1',
  source: 'dore.visual-editorial-director.v1',
  graphOwns: 'identity+relationships',
  surfaceOwns: 'presentation+motion',
});

const surfacePlan = [
  { id: 'hero', role: 'primary', preset: 'card-8x5', weight: 2, motion: 'near-still', limit: 1 },
  { id: 'river', role: 'secondary', preset: 'card-8x5', weight: 1, motion: 'slow-flow', limit: 2 },
  { id: 'focus', role: 'reading-focus', preset: 'card-8x5', weight: 1, motion: 'focus', limit: 1 },
];

export function orchestrateDawnSurfaces(selection = {}) {
  const candidates = arr(selection.candidates);
  const used = new Set();
  const surfaces = surfacePlan.map(spec => {
    const eligible = candidates.filter(candidate =>
      !used.has(candidate.visualWorkId) && arr(candidate.surfacePresetIds).includes(spec.preset));
    const picked = eligible.slice(0, spec.limit);
    picked.forEach(candidate => used.add(candidate.visualWorkId));
    return {
      id: `dawn-${spec.id}`,
      role: spec.role,
      surfacePreset: spec.preset,
      editorialWeight: spec.weight,
      motion: spec.motion,
      visualWorkIds: picked.map(candidate => candidate.visualWorkId),
    };
  });
  return {
    schema: dawnSurfaceContract.schema,
    source: dawnSurfaceContract.source,
    selectionId: selection.id || 'dawn-library-featured',
    surfaces,
  };
}
