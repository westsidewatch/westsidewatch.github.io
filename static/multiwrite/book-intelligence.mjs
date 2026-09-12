const BOOK_INTELLIGENCE_SCHEMA = 'dore.book-intelligence-report.v1';

function text(value = '') {
  return typeof value === 'string' ? value.trim() : '';
}

function normalizedTitle(value = '') {
  return text(value).replace(/^第[^\s]+[章篇部]\s*/u, '').trim();
}

function countScriptureSignals(value = '') {
  const input = String(value || '');
  const chineseRefs = input.match(/[\u4e00-\u9fff]{1,4}\s*\d{1,3}\s*[:：]\s*\d{1,3}/gu) || [];
  const englishRefs = input.match(/[A-Za-z]{2,20}\s+\d{1,3}:\d{1,3}/g) || [];
  return chineseRefs.length + englishRefs.length;
}

function inferDensity(count, sections) {
  const ratio = count / Math.max(1, sections);
  if (ratio >= 6) return 'high';
  if (ratio >= 2) return 'moderate';
  return 'low';
}

function sectionSummary(section, index) {
  const body = String(section?.text || '');
  return {
    id: text(section?.id) || `section-${index + 1}`,
    role: text(section?.role) || 'chapter',
    title: text(section?.title),
    normalizedTitle: normalizedTitle(section?.title),
    characters: body.length,
    scriptureSignals: countScriptureSignals(body),
    empty: !body.trim()
  };
}

export function analyzeBookIntelligence({ source = {}, sections = [] } = {}) {
  const summaries = (Array.isArray(sections) ? sections : []).map(sectionSummary);
  const body = summaries.filter(item => !['front_matter', 'back_matter', 'appendix'].includes(item.role));
  const scriptureSignals = summaries.reduce((sum, item) => sum + item.scriptureSignals, 0);
  const declared = source.bookIntent || source.intent || {};
  const thesis = text(declared.thesis || source.thesis);

  return {
    schema: BOOK_INTELLIGENCE_SCHEMA,
    source: { id: text(source.id), title: text(source.title), subtitle: text(source.subtitle) },
    intent: {
      category: text(declared.category || source.category) || (scriptureSignals ? 'biblical-reflection' : 'longform'),
      thesis,
      audience: text(declared.audience),
      readingMode: text(declared.readingMode) || 'continuous',
      visualTone: text(declared.visualTone),
      illustrationDensity: text(declared.illustrationDensity) || 'low',
      scriptureDensity: text(declared.scriptureDensity) || inferDensity(scriptureSignals, body.length)
    },
    structure: {
      chapterCount: body.length,
      frontMatterCount: summaries.filter(item => item.role === 'front_matter').length,
      backMatterCount: summaries.filter(item => item.role === 'back_matter').length,
      appendixCount: summaries.filter(item => item.role === 'appendix').length,
      chapterTitles: body.map(item => item.title).filter(Boolean),
      sequence: summaries.map(item => ({ id: item.id, role: item.role, title: item.title }))
    },
    signals: {
      scriptureSignals,
      emptySections: summaries.filter(item => item.empty).map(item => item.id),
      totalCharacters: summaries.reduce((sum, item) => sum + item.characters, 0)
    },
    authority: {
      thesisSource: thesis ? 'author-declared' : 'not-established',
      mayRewriteThesis: false,
      substantiveInferenceRequiresReview: true
    }
  };
}

export function bookIntentFromIntelligence(report = {}) {
  const intent = report.intent || {};
  return {
    category: text(intent.category) || 'longform',
    thesis: text(intent.thesis),
    audience: text(intent.audience),
    readingMode: text(intent.readingMode) || 'continuous',
    visualTone: text(intent.visualTone),
    illustrationDensity: text(intent.illustrationDensity) || 'low',
    scriptureDensity: text(intent.scriptureDensity)
  };
}

export { BOOK_INTELLIGENCE_SCHEMA };
