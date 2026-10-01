// Resolve real calligraphy glyph images. Never silently render a font glyph as if it were a crop.
export function glyphImage(glyph) {
  return glyph?.cropUrl || glyph?.regionUrl || glyph?.imageUrl || glyph?.src || null;
}

export function realGlyphCoverage(composition) {
  const cells = composition?.cells || [];
  const real = cells.filter(cell => glyphImage(cell.candidates?.find(g => g.id === cell.selectedGlyphId))).length;
  return { total: cells.length, real, pending: cells.length - real, ratio: cells.length ? real / cells.length : 0 };
}

export function assertRealGlyphs(composition) {
  const missing = (composition?.cells || []).filter(cell => {
    const glyph = cell.candidates?.find(g => g.id === cell.selectedGlyphId);
    return !glyphImage(glyph);
  }).map(cell => cell.literal);
  return { ready: missing.length === 0, missing };
}
