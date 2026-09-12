#!/usr/bin/env node
import { rankCandidatesForSurfaceContext, visualSurfaceContextContract } from './visual-surface-context.mjs';

const arr = value => Array.isArray(value) ? value : value == null ? [] : [value];

export const storybookArtDirectionContract = Object.freeze({
  schema: 'dore.storybook-art-direction-loop.v1',
  source: visualSurfaceContextContract.schema,
  upstream: ['dawn.visual-graph.v1', 'dore.visual-editorial-director.v1', 'dore.visual-surface-context.v1'],
  purpose: 'editorial-art-direction-learning',
  preservesAuthority: true,
  preservesEditorialRank: true,
  learnsFrom: ['page-sequence', 'content-role', 'visual-sequence', 'text-density', 'surface-role', 'crop-suitability'],
});

const normalizePage = (page = {}, index = 0, pages = []) => ({
  pageIndex: Number(page.pageIndex || index + 1),
  pageCount: Number(page.pageCount || pages.length || 1),
  contentRole: page.contentRole || 'editorial',
  nextContentRole: page.nextContentRole || pages[index + 1]?.contentRole || null,
  textDensity: page.textDensity || 'medium',
  preferredPreset: page.preferredPreset || 'card-8x5',
  needsNegativeSpace: page.needsNegativeSpace === true,
});

export function directStorybookSequence({ pages = [], candidates = [] } = {}) {
  const usedIds = [];
  const usedTypes = [];
  const decisions = [];

  arr(pages).forEach((page, index, allPages) => {
    const context = {
      ...normalizePage(page, index, allPages),
      previousVisualWorkIds: [...usedIds],
      previousVisualTypes: [...usedTypes],
    };
    const ranked = rankCandidatesForSurfaceContext(candidates, context);
    const selected = ranked[0] || null;
    if (selected) {
      usedIds.push(selected.visualWorkId);
      if (selected.type) usedTypes.push(selected.type);
    }
    decisions.push({
      pageIndex: context.pageIndex,
      context,
      selectedVisualWorkId: selected?.visualWorkId || null,
      selectedType: selected?.type || null,
      editorialScore: selected?.score ?? null,
      contextualScore: selected?.contextualScore ?? selected?.score ?? null,
      adjustment: selected?.surfaceContextAdjustment ?? 0,
      rationale: selected?.surfaceContextReasons || [],
    });
  });

  return {
    schema: storybookArtDirectionContract.schema,
    source: storybookArtDirectionContract.source,
    mode: 'critique-ready-sequence',
    decisions,
  };
}

export function critiqueStorybookSequence(sequence = {}) {
  const decisions = arr(sequence.decisions);
  const findings = [];
  decisions.forEach((decision, index) => {
    const previous = decisions[index - 1];
    if (previous?.selectedVisualWorkId && previous.selectedVisualWorkId === decision.selectedVisualWorkId) {
      findings.push({ pageIndex: decision.pageIndex, severity: 'high', code: 'visual-repeat', message: 'Adjacent pages repeat the same visual work.' });
    }
    if (previous?.selectedType && previous.selectedType === decision.selectedType) {
      findings.push({ pageIndex: decision.pageIndex, severity: 'medium', code: 'type-repeat', message: 'Adjacent pages repeat the same visual language.' });
    }
    if (decision.context?.textDensity === 'high' && decision.context?.needsNegativeSpace && !decision.rationale?.includes('crop-focal-ready')) {
      findings.push({ pageIndex: decision.pageIndex, severity: 'medium', code: 'text-fit-risk', message: 'Dense text requests negative space without strong crop/focal evidence.' });
    }
  });
  return {
    schema: 'dore.storybook-art-direction-critique.v1',
    source: storybookArtDirectionContract.schema,
    pass: findings.every(item => item.severity !== 'high'),
    findings,
  };
}

export function runStorybookArtDirectionLoop(input = {}) {
  const sequence = directStorybookSequence(input);
  return {
    ...sequence,
    critique: critiqueStorybookSequence(sequence),
  };
}
