#!/usr/bin/env node
/**
 * Dawn Library Phase 2 / Cut 01
 * Lightweight multi-dimensional Visual Fuzzy Search.
 *
 * Guardrails:
 * - Doré Search modality, not a parallel search product.
 * - authority first, inference second.
 * - rights fail closed for branded/design/generation consumers.
 * - generated assets never enter authority/training retrieval.
 */

const DEFAULT_WEIGHTS = Object.freeze({
  semantic: 0.28,
  visual: 0.16,
  composition: 0.14,
  scripture: 0.18,
  authority: 0.16,
  surface: 0.08,
});

const AUTHORITY_SCORE = Object.freeze({ A: 1, B: 0.86, C: 0.72, D: 0.18 });
const SAFE_RIGHTS = new Set(['public-domain', 'pd', 'cc0', 'cc-by', 'cc-by-sa']);

function arr(value) {
  return Array.isArray(value) ? value : value == null ? [] : [value];
}
function norm(value) {
  return String(value ?? '').normalize('NFKC').trim().toLowerCase();
}
function tokens(value) {
  return new Set(norm(value).split(/[\s,.;:!?，。；：！？/|()[\]{}<>「」『』]+/u).filter(Boolean));
}
function jaccard(a, b) {
  if (!a.size || !b.size) return 0;
  let hit = 0;
  for (const x of a) if (b.has(x)) hit += 1;
  return hit / (a.size + b.size - hit);
}
function textOf(work) {
  return [work.canonicalTitle, work.title, work.creator, work.medium, work.series,
    ...arr(work.depicts), ...arr(work.persons), ...arr(work.places), ...arr(work.events),
    ...arr(work.iconography), ...arr(work.tags)].filter(Boolean).join(' ');
}
function scriptureScore(query, work) {
  const wanted = new Set(arr(query.scriptureRefs).map(norm));
  const refs = new Set(arr(work.scriptureRefs).map(norm));
  if (!wanted.size) return 0;
  return jaccard(wanted, refs);
}
function compositionScore(query, work) {
  const wanted = tokens(arr(query.composition).join(' '));
  const have = tokens([work.composition, work.visualLanguage, work.light, work.negativeSpace,
    ...arr(work.visualRoles)].filter(Boolean).join(' '));
  return jaccard(wanted, have);
}
function visualScore(query, work) {
  const wanted = tokens(arr(query.visual).join(' '));
  const have = tokens([work.medium, work.period, work.visualLanguage, ...arr(work.iconography),
    ...arr(work.depicts)].filter(Boolean).join(' '));
  return jaccard(wanted, have);
}
function surfaceScore(query, work) {
  if (!query.aspectRatio && !query.surfacePreset) return 0;
  const ratios = new Set(arr(work.aspectRatios).map(norm));
  const presets = new Set(arr(work.surfacePresets).map(norm));
  let score = 0;
  if (query.aspectRatio && ratios.has(norm(query.aspectRatio))) score += 0.5;
  if (query.surfacePreset && presets.has(norm(query.surfacePreset))) score += 0.5;
  return score;
}
function rightsAllowed(work, consumer) {
  if (!consumer || consumer === 'research' || consumer === 'search') return true;
  const rights = norm(work.rightsStatus || work.rights?.status);
  return SAFE_RIGHTS.has(rights);
}
function authorityAllowed(work) {
  if (work.generated === true || work.trainingCanon === false && norm(work.provenance) === 'generated') return false;
  return ['a', 'b', 'c'].includes(norm(work.authorityClass));
}

export function rankVisualWorks(query, works, options = {}) {
  const weights = { ...DEFAULT_WEIGHTS, ...(options.weights || {}) };
  const qTokens = tokens([query.text, ...arr(query.semantic)].filter(Boolean).join(' '));
  const consumer = options.consumer || query.consumer || 'search';
  const limit = Number(options.limit || query.limit || 12);

  return works
    .filter((work) => authorityAllowed(work))
    .filter((work) => rightsAllowed(work, consumer))
    .map((work) => {
      const dimensions = {
        semantic: jaccard(qTokens, tokens(textOf(work))),
        visual: visualScore(query, work),
        composition: compositionScore(query, work),
        scripture: scriptureScore(query, work),
        authority: AUTHORITY_SCORE[String(work.authorityClass || '').toUpperCase()] || 0,
        surface: surfaceScore(query, work),
      };
      const score = Object.entries(dimensions).reduce((sum, [key, value]) => sum + value * (weights[key] || 0), 0);
      return {
        id: work.id,
        visualWorkId: work.visualWorkId || work.id,
        score: Number(score.toFixed(6)),
        dimensions,
        authorityClass: work.authorityClass,
        rightsStatus: work.rightsStatus || work.rights?.status || 'unknown',
        provenance: work.provenance || 'authority',
        machineConfidence: work.machineConfidence ?? null,
      };
    })
    .filter((row) => row.score > 0)
    .sort((a, b) => b.score - a.score || String(a.id).localeCompare(String(b.id)))
    .slice(0, limit);
}

export const visualFuzzyContract = Object.freeze({
  schema: 'dore.visual-fuzzy-search.v1',
  modality: 'dore-search',
  dimensions: Object.keys(DEFAULT_WEIGHTS),
  authorityClasses: ['A', 'B', 'C'],
  generatedReentry: false,
  rightsGate: 'fail-closed-for-branded-design-generation',
});
