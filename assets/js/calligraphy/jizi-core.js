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

export function collectText(text, corpus, filters = {}) {
  const index = buildCorpusIndex(corpus);
  return Array.from(text).filter(ch => !/\s/u.test(ch)).map((literal, position) => {
    const characterId = index.literalToId.get(literal) || codepointId(literal);
    const candidates = (index.glyphsByCharacter.get(characterId) || []).filter(glyph => {
      if (filters.style && glyph.style !== filters.style) return false;
      if (filters.sourceId && glyph.sourceId !== filters.sourceId) return false;
      return true;
    });
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
  return {
    version: 1,
    text,
    direction: options.direction || 'vertical',
    cells: collectText(text, corpus, options.filters || {}).map(cell => ({
      ...cell,
      selectedGlyphId: cell.candidates[0]?.id || null,
      transform: { x: 0, y: 0, scale: 1, rotate: 0 }
    }))
  };
}
