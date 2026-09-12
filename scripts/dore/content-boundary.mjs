export const contentBoundary = Object.freeze({
  schema: 'dore.content-boundary.v1',
  purpose: 'keep brand and nourishment focused on theology, Scripture, inner-life formation, and neutral design learning',
  defaultDecision: 'exclude-when-uncertain',
  excludedContexts: [
    'partisan-public-affairs',
    'national-or-ethnic-conflict',
    'armed-conflict',
    'ideological-propaganda',
    'content-likely-to-create-public-dispute'
  ],
  allowedContexts: [
    'scripture',
    'theology-within-authority-boundary',
    'inner-life-formation',
    'church-ministry',
    'neutral-design-language'
  ]
});

export function boundaryDecision({ contexts = [], uncertain = false } = {}) {
  if (uncertain) return 'exclude';
  if (contexts.some(x => contentBoundary.excludedContexts.includes(x))) return 'exclude';
  return 'continue-rights-and-theology-gates';
}
