const DORE_LOCAL_CAPABILITY_URL = 'http://127.0.0.1:8788/capability';
const SEMANTIC_TIMEOUT_MS = 20000;

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

export async function requestCoreBookIntelligence({ source = {}, sections = [] } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), SEMANTIC_TIMEOUT_MS);
  try {
    const response = await fetch(DORE_LOCAL_CAPABILITY_URL, {
      method: 'POST',
      cache: 'no-store',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({
        capability: 'publishing.book-intelligence',
        args: { source, sections }
      }),
      signal: controller.signal
    });
    if (!response.ok) return degradedSemantic(`core-http-${response.status}`);
    const payload = await response.json();
    if (!payload?.ok || !payload?.report) return degradedSemantic(payload?.error || 'core-invalid-response');
    return payload.report;
  } catch (error) {
    const reason = error?.name === 'AbortError' ? 'core-timeout' : 'core-unavailable';
    return degradedSemantic(reason);
  } finally {
    clearTimeout(timer);
  }
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
      // Author thesis is canonical. Core inference is diagnostic only and never replaces it.
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

export { DORE_LOCAL_CAPABILITY_URL, SEMANTIC_TIMEOUT_MS };
