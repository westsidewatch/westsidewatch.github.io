const MODES = new Set(['original','zh-Hant','bilingual']);

export function createDawnTranslationSurface({ workId, sourceLanguage = 'und', mode = 'original', segmentId = null, position = {}, provenance = {}, rights = {} } = {}) {
  if (!workId) throw new Error('workId required');
  if (!MODES.has(mode)) throw new Error(`unsupported reading mode: ${mode}`);
  return {
    schema: 'dawn.translation-reading-surface.v1',
    surfaceId: 'dawn-library-translation-reader',
    workId,
    profile: 'reading',
    modes: ['original','zh-Hant','bilingual'],
    activeMode: mode,
    sourceLanguage,
    targetLanguage: 'zh-Hant',
    authority: 'source-text',
    translationLabel: '黎明書局即時中文閱讀',
    segmentId,
    position: structuredClone(position),
    provenance: structuredClone(provenance),
    rights: structuredClone(rights),
    capability: { faculty: 'translation', profile: 'reading' },
    bibleTextExcluded: true
  };
}

export function setDawnTranslationMode(surface, mode) {
  if (!surface || surface.schema !== 'dawn.translation-reading-surface.v1') throw new Error('invalid Dawn translation surface');
  if (!MODES.has(mode)) throw new Error(`unsupported reading mode: ${mode}`);
  return { ...surface, activeMode: mode };
}

export function translationRequest(surface, segments = []) {
  if (!surface || surface.bibleTextExcluded !== true) throw new Error('Bible exclusion gate missing');
  if (surface.activeMode === 'original') return null;
  return {
    faculty: 'translation',
    profile: 'reading',
    surface: 'dawn-library',
    workId: surface.workId,
    sourceLanguage: surface.sourceLanguage,
    targetLanguage: surface.targetLanguage,
    mode: surface.activeMode,
    segments,
    provenance: surface.provenance,
    rights: surface.rights,
    bibleTextExcluded: true
  };
}
