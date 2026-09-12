#!/usr/bin/env node
import { normalizeSurfaceContext, rankCandidatesForSurface } from './visual-surface-context.mjs';

const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];

export const dawnSurfaceContract = Object.freeze({
  schema: 'dore.visual-surface-orchestrator.v1',
  source: 'dore.visual-editorial-director.v1',
  context: 'dore.visual-surface-context.v1',
  graphOwns: 'identity+relationships',
  surfaceOwns: 'presentation+motion',
});

const surfacePlan = [
  { id: 'hero', role: 'primary', preset: 'card-8x5', weight: 2, motion: 'near-still', limit: 1 },
  { id: 'river', role: 'secondary', preset: 'card-8x5', weight: 1, motion: 'slow-flow', limit: 2 },
  { id: 'focus', role: 'reading-focus', preset: 'card-8x5', weight: 1, motion: 'focus', limit: 1 },
];

export function orchestrateDawnSurfaces(selection = {}, surfaceContext = null) {
  const candidates = arr(selection.candidates);
  const used = new Set();
  const context = surfaceContext ? normalizeSurfaceContext(surfaceContext) : null;
  const surfaces = surfacePlan.map(spec => {
    const eligible = candidates.filter(candidate =>
      !used.has(candidate.visualWorkId) && arr(candidate.surfacePresetIds).includes(spec.preset));
    const ranked = context
      ? rankCandidatesForSurface(eligible, { ...context, preferredPreset: spec.preset, contentRole: context.contentRole === 'unspecified' ? spec.role : context.contentRole })
      : eligible.map((candidate, index) => ({ candidate, editorialBase: Number(candidate.score) || 0, contextAdjustment: 0, contextualScore: Number(candidate.score) || 0, contextualRank: index + 1 }));
    const picked = ranked.slice(0, spec.limit);
    picked.forEach(entry => used.add(entry.candidate.visualWorkId));
    return {
      id: `dawn-${spec.id}`,
      role: spec.role,
      surfacePreset: spec.preset,
      editorialWeight: spec.weight,
      motion: spec.motion,
      visualWorkIds: picked.map(entry => entry.candidate.visualWorkId),
      ...(context ? {
        contextDecision: {
          schema: context.schema,
          pageIndex: context.pageIndex,
          pagePosition: context.pagePosition,
          contentRole: context.contentRole,
          picks: picked.map(entry => ({
            visualWorkId: entry.candidate.visualWorkId,
            editorialBase: entry.editorialBase,
            contextAdjustment: entry.contextAdjustment,
            contextualScore: entry.contextualScore,
            contextualRank: entry.contextualRank,
            adjustments: entry.adjustments,
          })),
        },
      } : {}),
    };
  });
  return {
    schema: dawnSurfaceContract.schema,
    source: dawnSurfaceContract.source,
    selectionId: selection.id || 'dawn-library-featured',
    ...(context ? { context } : {}),
    surfaces,
  };
}
