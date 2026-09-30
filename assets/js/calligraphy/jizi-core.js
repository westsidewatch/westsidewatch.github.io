export function codepointId(character) {
  const cp = character.codePointAt(0);
  return cp == null ? null : `u${cp.toString(16).padStart(4, '0')}`;
}

export function buildCorpusIndex(corpus) {
  const characters = new Map();
  const literalToId = new Map();
  const glyphsByCharacter = new Map();

  for (const character of corpus.characters || []) {
    characters.set(character.id, character);
    literalToId.set(character.literal, character.id);
    for (const variant of character.variants || []) literalToId.set(variant, character.id);
  }

  for (const glyph of corpus.glyphs || []) {
    if (!glyphsByCharacter.has(glyph.characterId)) glyphsByCharacter.set(glyph.characterId, []);
    glyphsByCharacter.get(glyph.characterId).push(glyph);
  }

  return { characters, literalToId, glyphsByCharacter };
}

function glyphScore(glyph, filters = {}) {
  let score = 0;
  if (filters.teacher && glyph.teacher === filters.teacher) score += 100;
  if (filters.style && glyph.style === filters.style) score += 40;
  if (filters.sourceId && glyph.sourceId === filters.sourceId) score += 30;
  if (glyph.pixelProof === true || glyph.pixelProofStatus === 'verified') score += 20;
  if (glyph.provenance?.sourceUrl || glyph.sourceUrl) score += 10;
  if (glyph.context?.previous || glyph.context?.next) score += 5;
  return score;
}

export function collectText(text, corpus, filters = {}) {
  const index = buildCorpusIndex(corpus);
  return Array.from(text).filter(ch => !/\s/u.test(ch)).map((literal, position) => {
    const characterId = index.literalToId.get(literal) || codepointId(literal);
    const candidates = (index.glyphsByCharacter.get(characterId) || [])
      .filter(glyph => {
        if (filters.teacher && glyph.teacher !== filters.teacher) return false;
        if (filters.style && glyph.style !== filters.style) return false;
        if (filters.sourceId && glyph.sourceId !== filters.sourceId) return false;
        return true;
      })
      .map(glyph => ({ ...glyph, score: glyphScore(glyph, filters) }))
      .sort((a, b) => b.score - a.score);

    return {
      position,
      literal,
      characterId,
      status: candidates.length ? 'ready' : 'missing',
      candidates
    };
  });
}

export function createComposition(text, corpus, options = {}) {
  const filters = options.filters || {};
  return {
    version: 2,
    text,
    direction: options.direction || 'vertical',
    teacher: filters.teacher || null,
    style: filters.style || null,
    cells: collectText(text, corpus, filters).map(cell => ({
      ...cell,
      selectedGlyphId: cell.candidates[0]?.id || null,
      transform: { x: 0, y: 0, scale: 1, rotate: 0 }
    }))
  };
}

export function selectGlyph(composition, position, glyphId) {
  const cell = composition.cells?.find(item => item.position === position);
  if (!cell) return composition;
  if (!cell.candidates.some(glyph => glyph.id === glyphId)) return composition;
  cell.selectedGlyphId = glyphId;
  cell.status = 'ready';
  return composition;
}

export function updateCellTransform(composition, position, patch = {}) {
  const cell = composition.cells?.find(item => item.position === position);
  if (!cell) return composition;
  cell.transform = { ...cell.transform, ...patch };
  return composition;
}

export function compositionCoverage(composition) {
  const cells = composition.cells || [];
  const ready = cells.filter(cell => cell.selectedGlyphId).length;
  const missing = cells.filter(cell => !cell.selectedGlyphId).map(cell => cell.literal);
  return {
    total: cells.length,
    ready,
    missing,
    ratio: cells.length ? ready / cells.length : 0
  };
}
