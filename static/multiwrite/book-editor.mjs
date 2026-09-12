const EDITORIAL_REPORT_SCHEMA = 'dore.editorial-report.v1';

function issue({ code, severity = 'info', actionClass, message, sectionId = '', details = {} }) {
  return { code, severity, actionClass, message, sectionId, details };
}

function normalizedTitle(value = '') {
  return String(value).trim().replace(/\s+/g, ' ');
}

function nonEmptySections(bookModel) {
  return (bookModel.sections || []).filter(section => String(section.text || '').trim());
}

function headingDepthProblems(text = '') {
  const levels = String(text).split(/\r?\n/).map(line => line.match(/^(#{1,6})\s+/)?.[1]?.length || 0).filter(Boolean);
  const problems = [];
  for (let i = 1; i < levels.length; i += 1) {
    if (levels[i] - levels[i - 1] > 1) problems.push({ from: levels[i - 1], to: levels[i], index: i });
  }
  return problems;
}

function obviousDuplicateTitles(sections = []) {
  const seen = new Map();
  const duplicates = [];
  for (const section of sections) {
    const key = normalizedTitle(section.title).toLocaleLowerCase();
    if (!key) continue;
    if (seen.has(key)) duplicates.push([seen.get(key), section.id]);
    else seen.set(key, section.id);
  }
  return duplicates;
}

function hasLikelyConclusion(sections = []) {
  return sections.some(section => /^(結語|結論|後記|conclusion|epilogue)$/i.test(normalizedTitle(section.title)) || section.role === 'conclusion');
}

function hasLikelyIntroduction(sections = []) {
  return sections.some(section => /^(序|序言|前言|引言|introduction|preface)$/i.test(normalizedTitle(section.title)) || ['introduction', 'preface'].includes(section.role));
}

export function analyzeBookForPublication(bookModel) {
  if (!bookModel || bookModel.schema !== 'dore.book-model.v1') throw new Error('A valid Doré BookModel is required.');

  const issues = [];
  const sections = bookModel.sections || [];
  const contentSections = nonEmptySections(bookModel);

  if (!normalizedTitle(bookModel.publicationMetadata?.title)) {
    issues.push(issue({ code: 'metadata.title.missing', severity: 'error', actionClass: 'AUTHORIAL_DECISION_REQUIRED', message: '書名缺失，成書前需要作者確認。' }));
  }

  if (!sections.length) {
    issues.push(issue({ code: 'structure.empty', severity: 'error', actionClass: 'AUTHORIAL_DECISION_REQUIRED', message: '書稿沒有章節結構。' }));
  }

  sections.forEach(section => {
    if (!normalizedTitle(section.title)) {
      issues.push(issue({ code: 'section.title.missing', severity: 'warning', actionClass: 'SUGGESTED_COMPLETION', message: '章節缺少標題。', sectionId: section.id }));
    }
    if (!String(section.text || '').trim()) {
      issues.push(issue({ code: 'section.content.empty', severity: 'warning', actionClass: 'SUGGESTED_COMPLETION', message: '章節沒有正文。', sectionId: section.id }));
    }
    const depthProblems = headingDepthProblems(section.text);
    if (depthProblems.length) {
      issues.push(issue({ code: 'section.heading.depth', severity: 'warning', actionClass: 'AUTO_FIX', message: '標題層級存在跳級，可在不改變內容的情況下機械修復。', sectionId: section.id, details: { depthProblems } }));
    }
  });

  for (const [firstId, secondId] of obviousDuplicateTitles(sections)) {
    issues.push(issue({ code: 'section.title.duplicate', severity: 'warning', actionClass: 'AUTHORIAL_DECISION_REQUIRED', message: '存在重複章節標題，需要作者判斷是否為重複內容或有意安排。', sectionId: secondId, details: { firstId, secondId } }));
  }

  if (contentSections.length >= 3 && !hasLikelyIntroduction(sections)) {
    issues.push(issue({ code: 'structure.introduction.missing', severity: 'info', actionClass: 'SUGGESTED_COMPLETION', message: '長篇書稿尚未識別到序言／引言，可考慮補充，但不自動生成進正文。' }));
  }

  if (contentSections.length >= 3 && !hasLikelyConclusion(sections)) {
    issues.push(issue({ code: 'structure.conclusion.missing', severity: 'info', actionClass: 'SUGGESTED_COMPLETION', message: '長篇書稿尚未識別到結語／結論，可考慮補充，但不自動生成進正文。' }));
  }

  if (!normalizedTitle(bookModel.intent?.thesis)) {
    issues.push(issue({ code: 'intent.thesis.undeclared', severity: 'info', actionClass: 'SUGGESTED_COMPLETION', message: '尚未有明確的中心論旨。Book Intelligence 可以提出摘要候選，但不得覆寫作者立場。' }));
  }

  const blockers = issues.filter(item => item.severity === 'error' || item.actionClass === 'AUTHORIAL_DECISION_REQUIRED');
  const autoFixes = issues.filter(item => item.actionClass === 'AUTO_FIX');
  const suggestions = issues.filter(item => item.actionClass === 'SUGGESTED_COMPLETION');
  const readiness = blockers.some(item => item.severity === 'error') ? 'blocked' : blockers.length ? 'review-required' : 'ready';

  return {
    schema: EDITORIAL_REPORT_SCHEMA,
    bookId: bookModel.id,
    readiness,
    counts: {
      sections: sections.length,
      nonEmptySections: contentSections.length,
      issues: issues.length,
      autoFixes: autoFixes.length,
      suggestions: suggestions.length,
      authorialDecisions: blockers.filter(item => item.actionClass === 'AUTHORIAL_DECISION_REQUIRED').length
    },
    issues,
    policy: {
      silentActionsAllowed: ['AUTO_FIX'],
      generatedCompletionMustRemainProposed: true,
      doctrinalOrSubstantiveRewriteAllowed: false,
      humanAuthorityDecisive: true
    },
    createdAt: new Date().toISOString()
  };
}

export function applyMechanicalEditorialFixes(bookModel, editorialReport) {
  if (!editorialReport || editorialReport.schema !== EDITORIAL_REPORT_SCHEMA) throw new Error('A valid EditorialReport is required.');
  // Phase 2 deliberately does not mutate prose. The function establishes the only
  // legal silent-mutation boundary; concrete mechanical fixers attach here later.
  return { bookModel, applied: [], remaining: editorialReport.issues };
}

export { EDITORIAL_REPORT_SCHEMA };
