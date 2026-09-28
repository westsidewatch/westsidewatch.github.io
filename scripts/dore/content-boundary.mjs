export const contentBoundary = Object.freeze({
  schema: 'dore.content-boundary.v2',
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

const disputePatterns = [
  ['armed-conflict', /\b(war|battle|military|army|navy|soldier|weapon|rifle|bomb|missile|invasion|occupation)\b/i],
  ['partisan-public-affairs', /\b(election|campaign|partisan|political party|presidential|parliamentary)\b/i],
  ['national-or-ethnic-conflict', /\b(ethnic conflict|racial conflict|nationalist movement|territorial dispute)\b/i],
  ['ideological-propaganda', /\b(propaganda|extremist|extremism|terrorist|terrorism)\b/i]
];

export function classifyBoundaryText(text = '') {
  const value = String(text);
  const contexts = [];
  for (const [context, pattern] of disputePatterns) if (pattern.test(value)) contexts.push(context);
  return contexts;
}

export function boundaryDecision({ contexts = [], uncertain = false } = {}) {
  if (uncertain) return 'exclude';
  if (contexts.some(x => contentBoundary.excludedContexts.includes(x))) return 'exclude';
  return 'continue-rights-and-theology-gates';
}

export function boundaryDecisionForText(text = '') {
  const contexts = classifyBoundaryText(text);
  return { contexts, decision: boundaryDecision({ contexts }) };
}
