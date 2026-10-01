import { createComposition, compositionCoverage } from './jizi-core.js';

const cleanText = text => Array.from(text || '')
  .filter(ch => !/[\s，。！？；：、,.!?;:'“”‘’（）()《》〈〉\[\]【】]/u.test(ch))
  .join('');

function firstCandidate(text, corpus, filters) {
  return createComposition(text, corpus, { direction: 'vertical', filters }).cells[0]?.candidates?.[0] || null;
}

function fillMissingFast(composition, corpus, options) {
  for (const cell of composition.cells || []) {
    if (cell.selectedGlyphId) continue;

    // 1. Same teacher, relax source/style restrictions.
    let glyph = options.teacher ? firstCandidate(cell.literal, corpus, { teacher: options.teacher }) : null;
    // 2. Project Hand: production fallback trained from the core teachers.
    if (!glyph) glyph = firstCandidate(cell.literal, corpus, { teacher: options.projectHand || 'project-hand' });
    // 3. Any verified corpus glyph: keep scripture writable rather than blocking the whole work.
    if (!glyph && options.allowCrossTeacherFallback !== false) glyph = firstCandidate(cell.literal, corpus, {});

    if (glyph) {
      cell.candidates = [glyph, ...cell.candidates.filter(g => g.id !== glyph.id)];
      cell.selectedGlyphId = glyph.id;
      cell.status = 'fallback';
      cell.fallback = glyph.teacher === options.teacher ? 'same-teacher' : (glyph.teacher === (options.projectHand || 'project-hand') ? 'project-hand' : 'cross-teacher');
    } else {
      cell.status = 'needs-generation';
      cell.fallback = 'project-hand-generation';
    }
  }
  return composition;
}

/** Fast production path: scripture -> glyphs -> fallback -> renderable composition. */
export function scriptureJizi(text, corpus, options = {}) {
  const clean = cleanText(text);
  const composition = createComposition(clean, corpus, {
    direction: options.direction || 'vertical',
    filters: { teacher: options.teacher, style: options.style, sourceId: options.sourceId }
  });

  fillMissingFast(composition, corpus, options);
  const coverage = compositionCoverage(composition);
  const needsGeneration = (composition.cells || []).filter(c => !c.selectedGlyphId).map(c => c.literal);

  return {
    text: clean,
    composition,
    coverage,
    writable: needsGeneration.length === 0,
    missing: [...new Set(needsGeneration)],
    generationQueue: [...new Set(needsGeneration)]
  };
}

export function scriptureJiziCells(result) {
  return (result?.composition?.cells || []).map(cell => ({
    literal: cell.literal,
    glyphId: cell.selectedGlyphId,
    glyph: cell.candidates.find(g => g.id === cell.selectedGlyphId) || null,
    alternatives: cell.candidates,
    transform: cell.transform,
    fallback: cell.fallback || null,
    missing: !cell.selectedGlyphId
  }));
}
