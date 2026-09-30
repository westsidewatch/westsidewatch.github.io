import { createComposition, compositionCoverage } from './jizi-core.js';

/** Fast path: scripture text -> usable calligraphy composition.
 * No research/workflow layer. The caller supplies the existing glyph corpus.
 */
export function scriptureJizi(text, corpus, options = {}) {
  const clean = Array.from(text || '')
    .filter(ch => !/[\s，。！？；：、,.!?;:'“”‘’（）()《》〈〉\[\]【】]/u.test(ch))
    .join('');

  const composition = createComposition(clean, corpus, {
    direction: options.direction || 'vertical',
    filters: {
      teacher: options.teacher,
      style: options.style,
      sourceId: options.sourceId
    }
  });

  const coverage = compositionCoverage(composition);
  return {
    text: clean,
    composition,
    coverage,
    writable: coverage.missing.length === 0,
    missing: [...new Set(coverage.missing)]
  };
}

/** Render-ready model: one cell per character, selected glyph first. */
export function scriptureJiziCells(result) {
  return (result?.composition?.cells || []).map(cell => ({
    literal: cell.literal,
    glyphId: cell.selectedGlyphId,
    glyph: cell.candidates.find(g => g.id === cell.selectedGlyphId) || null,
    alternatives: cell.candidates,
    transform: cell.transform,
    missing: !cell.selectedGlyphId
  }));
}
