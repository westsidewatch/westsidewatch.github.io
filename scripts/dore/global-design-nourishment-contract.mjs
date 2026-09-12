#!/usr/bin/env node

export const globalDesignNourishmentContract = Object.freeze({
  schema: 'dore.global-design-nourishment.v1',
  purpose: 'cross-domain-design-capability-acquisition',
  principle: 'more-capability-less-burden',
  preservesUpstream: [
    'dawn.visual-graph.v1',
    'dore.visual-fuzzy-search.v1',
    'dore.visual-editorial-director.v1',
    'dore.visual-surface-context.v1',
    'dore.storybook-art-direction-loop.v1',
  ],
  domains: [
    'editorial', 'typography', 'painting', 'illustration', 'photography',
    'architecture', 'interior', 'furniture', 'industrial-design',
    'web', 'interaction', 'motion', 'christian-screen',
  ],
  outputs: ['design-exemplar', 'dawn-resource', 'boundary-evidence'],
  admission: {
    provenanceRequired: true,
    rightsRequired: true,
    theologyFailClosed: true,
    uncertainTheology: 'theology-review-required',
    nonDawnReligiousMaterial: 'design-only-semantic-isolation',
    generatedAuthorityPromotion: false,
    generatedTrainingCanonPromotion: false,
  },
  evaluation: {
    baselineRequired: true,
    dimensions: [
      'design-literacy', 'design-judgment', 'design-action',
      'cross-domain-transfer', 'theology-boundary', 'efficiency',
    ],
    stopIfCorpusGrowsWithoutCapabilityDelta: true,
    nextRoundFromCapabilityGap: true,
  },
});

export const roundOneManifest = Object.freeze({
  schema: 'dore.global-design-nourishment-round1.v1',
  mode: 'broad-authority-diversity-sampling',
  domains: globalDesignNourishmentContract.domains,
  sourceClasses: {
    authority: ['museum-open-access', 'library-archive', 'structured-design-collection'],
    curated: ['editorial-archive', 'design-history-archive', 'architecture-case-library', 'web-history-archive'],
    contemporaryReference: ['curated-contemporary-design'],
  },
  christianScreen: {
    separateResourceLayer: true,
    scope: ['film', 'series', 'miniseries', 'short-form', 'documentary'],
    dawnAdmissionRequiresTheologyAuthority: true,
    cinematicDesignLearningMayProceedWhenTheologySemanticsAreIsolated: true,
    generalFilmExplorationLocked: true,
  },
  churchArchitecture: {
    researchLine: '光之教會',
    role: ['dawn-research', 'architecture-curriculum', 'future-dore-architecture-foundation'],
    progression: [
      'biblical-space', 'early-church', 'historic-church-architecture',
      'reformation-protestant-space', 'evangelical-space', 'modern-church',
      'global-contemporary-church', 'architecture-anatomy', 'cross-media-transfer',
      'future-church-design',
    ],
    designSequence: ['theology', 'ecclesiology', 'ministry', 'human-activity', 'spatial-relationships', 'architecture'],
  },
});

export function classifyNourishmentItem(item = {}) {
  if (!item.provenance || !item.rights) return { decision: 'reject', reason: 'missing-provenance-or-rights' };
  const theology = item.theologyStatus || 'not-applicable';
  if (theology === 'uncertain') return { decision: 'theology-review-required', dawn: false, design: true, religiousSemantics: false };
  if (theology === 'outside-boundary' || theology === 'mixed') return { decision: 'design-only', dawn: false, design: true, religiousSemantics: false };
  if (theology === 'approved') return { decision: 'dawn+design', dawn: true, design: true, religiousSemantics: true };
  return { decision: 'design-only', dawn: false, design: true, religiousSemantics: false };
}
