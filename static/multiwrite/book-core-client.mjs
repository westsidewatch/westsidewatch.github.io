const SEMANTIC_TIMEOUT_MS = 20000;
const BOOK_INTELLIGENCE_CAPABILITY = 'publishing.book-intelligence';

function clean(value = '') {
  return typeof value === 'string' ? value.trim() : '';
}

function degradedSemantic(reason = 'core-unavailable') {
  return {
    schema: 'dore.book-intelligence-report.v2',
    category: '',
    declaredThesis: '',
    inferredThesis: '',
    thesisRelationship: 'unknown',
    confidence: 0,
    audience: '',
    readingMode: '',
    chapterRoles: [],
    argumentRelations: [],
    structuralGaps: [],
    visualToneHints: [],
    evidence: [],
    authority: { declaredThesis: 'author', mayRewriteThesis: false },
    runtime: { semantic: false, degraded: true, reason }
  };
}

export function requestCoreBookIntelligence({ source = {}, sections = [] } = {}) {
  return new Promise(resolve => {
    const requestId = `book-intelligence-${Date.now()}-${Math.random().toString(36).slice(2)}`;
    let settled = false;
    const finish = value => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      window.removeEventListener('dore:book-intelligence-result', handleResult);
      resolve(value);
    };
    const handleResult = event => {
      const detail = event.detail || {};
      if (detail.request_id !== requestId) return;
      const payload = detail.payload || {};
      finish(payload.ok && payload.report ? payload.report : degradedSemantic('core-invalid-response'));
    };
    const timer = setTimeout(() => finish(degradedSemantic('core-timeout')), SEMANTIC_TIMEOUT_MS);
    window.addEventListener('dore:book-intelligence-result', handleResult);
    window.dispatchEvent(new CustomEvent('dore:book-intelligence', {
      detail: {
        capability: BOOK_INTELLIGENCE_CAPABILITY,
        request_id: requestId,
        args: { source, sections }
      }
    }));
  });
}

export function mergeBookIntelligence(deterministic = {}, semantic = {}) {
  const localIntent = deterministic.intent || {};
  const semanticRuntime = semantic.runtime || {};
  const visualTone = clean(localIntent.visualTone)
    || (Array.isArray(semantic.visualToneHints) ? semantic.visualToneHints.map(clean).filter(Boolean).join(' / ') : '');

  return {
    ...deterministic,
    schema: 'dore.book-intelligence-report.composite.v1',
    intent: {
      ...localIntent,
      category: clean(localIntent.category) || clean(semantic.category) || 'longform',
      thesis: clean(localIntent.thesis),
      audience: clean(localIntent.audience) || clean(semantic.audience),
      readingMode: clean(localIntent.readingMode) || clean(semantic.readingMode) || 'continuous',
      visualTone
    },
    authority: {
      ...(deterministic.authority || {}),
      mayRewriteThesis: false,
      substantiveInferenceRequiresReview: true
    },
    semantic: {
      schema: semantic.schema || 'dore.book-intelligence-report.v2',
      inferredThesis: clean(semantic.inferredThesis),
      thesisRelationship: clean(semantic.thesisRelationship) || 'unknown',
      confidence: Number.isFinite(Number(semantic.confidence)) ? Number(semantic.confidence) : 0,
      chapterRoles: Array.isArray(semantic.chapterRoles) ? semantic.chapterRoles : [],
      argumentRelations: Array.isArray(semantic.argumentRelations) ? semantic.argumentRelations : [],
      structuralGaps: Array.isArray(semantic.structuralGaps) ? semantic.structuralGaps : [],
      visualToneHints: Array.isArray(semantic.visualToneHints) ? semantic.visualToneHints : [],
      evidence: Array.isArray(semantic.evidence) ? semantic.evidence : [],
      runtime: {
        semantic: semanticRuntime.semantic === true,
        degraded: semanticRuntime.degraded !== false,
        reason: clean(semanticRuntime.reason)
      }
    }
  };
}

export { SEMANTIC_TIMEOUT_MS };
