const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];
const clamp01 = value => Math.max(0, Math.min(1, Number(value) || 0));

export const visualSurfaceContextContract = Object.freeze({
  schema: 'dore.visual-surface-context.v1',
  upstream: ['dawn.visual-graph.v1', 'dore.visual-editorial-director.v1'],
  downstream: 'dore.visual-surface-orchestrator.v1',
  preservesEditorialRank: true,
});

export function normalizeSurfaceContext(input = {}) {
  const pageIndex = Math.max(1, Number(input.pageIndex) || 1);
  const pageCount = Math.max(pageIndex, Number(input.pageCount) || pageIndex);
  return {
    schema: visualSurfaceContextContract.schema,
    pageIndex,
    pageCount,
    pagePosition: pageIndex === 1 ? 'opening' : pageIndex === pageCount ? 'closing' : 'interior',
    contentRole: String(input.contentRole || '').trim() || 'unspecified',
    nextContentRole: String(input.nextContentRole || '').trim() || null,
    textDensity: clamp01(input.textDensity),
    previousVisualWorkIds: arr(input.previousVisualWorkIds).filter(Boolean),
    previousVisualTypes: arr(input.previousVisualTypes).filter(Boolean),
    preferredPreset: String(input.preferredPreset || 'card-8x5'),
    needsNegativeSpace: input.needsNegativeSpace === true,
  };
}

function includesAny(value, terms) {
  const text = String(value || '').toLowerCase();
  return terms.some(term => text.includes(term));
}

function roleTypeAffinity(contentRole, type) {
  if (includesAny(contentRole, ['opening','cover','proclamation']) && includesAny(type, ['engraving','painting','fresco','mosaic'])) return .08;
  if (includesAny(contentRole, ['study','exposition','scripture','teaching']) && includesAny(type, ['manuscript','map','engraving'])) return .07;
  if (includesAny(contentRole, ['testimony','witness','story']) && includesAny(type, ['photograph','painting','engraving'])) return .07;
  if (includesAny(contentRole, ['prayer','contemplation','closing']) && includesAny(type, ['painting','engraving','mosaic','fresco'])) return .05;
  return 0;
}

function cropSuitability(candidate, context) {
  const presets = arr(candidate.surfacePresets);
  const exact = presets.find(preset => preset.id === context.preferredPreset);
  if (exact && exact.focalRegionId) return .07;
  if (arr(candidate.surfacePresetIds).includes(context.preferredPreset)) return .035;
  return 0;
}

function sequenceDiversity(candidate, context) {
  if (context.previousVisualWorkIds.includes(candidate.visualWorkId)) return -.35;
  if (candidate.type && context.previousVisualTypes.includes(candidate.type)) return -.045;
  return context.pageIndex > 1 ? .025 : 0;
}

function textFit(candidate, context) {
  if (context.textDensity < .55 && !context.needsNegativeSpace) return 0;
  const focal = arr(candidate.surfacePresets).some(preset => preset.id === context.preferredPreset && preset.focalRegionId);
  return focal ? .035 : -.02;
}

export function scoreCandidateForContext(candidate = {}, inputContext = {}) {
  const context = normalizeSurfaceContext(inputContext);
  const editorialBase = Number(candidate.score) || 0;
  const adjustments = {
    sequenceDiversity: sequenceDiversity(candidate, context),
    contentRoleAffinity: roleTypeAffinity(context.contentRole, candidate.type),
    cropSuitability: cropSuitability(candidate, context),
    textFit: textFit(candidate, context),
  };
  const contextAdjustment = Object.values(adjustments).reduce((sum, value) => sum + value, 0);
  return {
    candidate,
    editorialBase,
    contextAdjustment,
    contextualScore: editorialBase + contextAdjustment,
    adjustments,
    context,
  };
}

export function rankCandidatesForSurface(candidates = [], inputContext = {}) {
  return arr(candidates)
    .map(candidate => scoreCandidateForContext(candidate, inputContext))
    .sort((a, b) => b.contextualScore - a.contextualScore || b.editorialBase - a.editorialBase)
    .map((entry, index) => ({ ...entry, contextualRank: index + 1 }));
}
