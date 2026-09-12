const BOOK_MODEL_SCHEMA = 'dore.book-model.v1';
const BOOK_BUILD_SCHEMA = 'dore.book-build.v1';

function text(value = '') {
  return typeof value === 'string' ? value.trim() : '';
}

function list(value) {
  return Array.isArray(value) ? value.filter(Boolean) : [];
}

function publicMetadata(source = {}) {
  return {
    title: text(source.title),
    subtitle: text(source.subtitle),
    authors: list(source.authors || source.author),
    language: list(source.language || source.languages || ['zh-Hant']),
    publisher: text(source.publisher),
    description: text(source.description),
    rights: text(source.rights),
    identifiers: list(source.identifiers)
  };
}

export function buildBookIntent(source = {}, overrides = {}) {
  const declared = source.bookIntent || source.intent || {};
  return {
    category: text(overrides.category || declared.category || source.category || 'longform'),
    thesis: text(overrides.thesis || declared.thesis || source.thesis),
    audience: text(overrides.audience || declared.audience),
    readingMode: text(overrides.readingMode || declared.readingMode || 'continuous'),
    visualTone: text(overrides.visualTone || declared.visualTone),
    illustrationDensity: text(overrides.illustrationDensity || declared.illustrationDensity || 'low'),
    scriptureDensity: text(overrides.scriptureDensity || declared.scriptureDensity)
  };
}

export function buildBookModel({ source = {}, sections = [], intent = null, internalProvenance = {} } = {}) {
  const normalizedSections = list(sections).map((section, index) => ({
    id: text(section.id) || `section-${index + 1}`,
    index,
    role: text(section.role) || 'chapter',
    title: text(section.title),
    text: typeof section.text === 'string' ? section.text : '',
    draft: Boolean(section.draft)
  }));

  return {
    schema: BOOK_MODEL_SCHEMA,
    id: text(source.id),
    workId: text(source.workId || source.work_id || source.id),
    editionId: text(source.editionId || source.edition_id),
    intent: intent || buildBookIntent(source),
    publicationMetadata: publicMetadata(source),
    structure: {
      frontMatter: normalizedSections.filter(section => section.role === 'front_matter'),
      body: normalizedSections.filter(section => !['front_matter', 'back_matter'].includes(section.role)),
      backMatter: normalizedSections.filter(section => section.role === 'back_matter')
    },
    sections: normalizedSections,
    assets: list(source.assets),
    notes: list(source.notes),
    citations: list(source.citations),
    relations: list(source.relations),
    design: {
      grammar: text(source.design?.grammar),
      artDirection: source.design?.artDirection || null,
      cover: source.design?.cover || source.cover || null
    },
    artifacts: { web: null, epub: null, pdf: null },
    validation: { status: 'pending', gates: [] },
    internalProvenance: { ...internalProvenance }
  };
}

export function buildBookBuild({ bookModel, sourceFolioId = '', sourceRevision = '', buildId = '' } = {}) {
  if (!bookModel || bookModel.schema !== BOOK_MODEL_SCHEMA) {
    throw new Error('A valid Doré BookModel is required.');
  }

  return {
    schema: BOOK_BUILD_SCHEMA,
    buildId: text(buildId) || `book-build-${Date.now()}`,
    sourceFolioId: text(sourceFolioId || bookModel.id),
    sourceRevision: text(sourceRevision),
    workId: text(bookModel.workId),
    editionId: text(bookModel.editionId),
    bookModelVersion: BOOK_MODEL_SCHEMA,
    grammarVersion: text(bookModel.design?.grammar),
    artDirectionId: '',
    coverArtifactId: '',
    epubArtifactId: '',
    webArtifactId: '',
    pdfArtifactId: '',
    epubCheckResult: null,
    qaResult: { status: 'pending', attempts: 0, maxAutoRepairAttempts: 3 },
    theologyGateResult: null,
    createdAt: new Date().toISOString(),
    publishedAt: null
  };
}

export function publicationProjection(bookModel) {
  if (!bookModel || bookModel.schema !== BOOK_MODEL_SCHEMA) {
    throw new Error('A valid Doré BookModel is required.');
  }

  // Deliberately excludes internalProvenance. Public publishing artifacts must
  // never inherit private runtime/provider/debug provenance by object spread.
  return {
    schema: bookModel.schema,
    id: bookModel.id,
    workId: bookModel.workId,
    editionId: bookModel.editionId,
    intent: bookModel.intent,
    publicationMetadata: bookModel.publicationMetadata,
    structure: bookModel.structure,
    sections: bookModel.sections,
    assets: bookModel.assets,
    notes: bookModel.notes,
    citations: bookModel.citations,
    relations: bookModel.relations,
    design: bookModel.design
  };
}

export { BOOK_MODEL_SCHEMA, BOOK_BUILD_SCHEMA };
