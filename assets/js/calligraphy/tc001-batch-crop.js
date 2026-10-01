import { glyphImage, assertRealGlyphs } from './crop-resolver.js';

export const TC001 = '敬畏耶和華是智慧的開端';

/**
 * Execute the existing acquisition/crop adapters as one batch.
 * adapters.resolve(glyph) must return a real cropped/region image URL or null.
 * This deliberately does not download whole works.
 */
export async function cropTC001(corpus, adapters) {
  const wanted = new Set(Array.from(TC001));
  const glyphs = (corpus.glyphs || []).filter(g => wanted.has(
    corpus.characters?.find(c => c.id === g.characterId)?.literal
  ));

  const results = await Promise.all(glyphs.map(async glyph => {
    if (glyphImage(glyph)) return { id: glyph.id, status: 'ready', url: glyphImage(glyph) };
    try {
      const url = await adapters.resolve(glyph);
      if (!url) return { id: glyph.id, status: 'pending' };
      glyph.cropUrl = url;
      glyph.cropStatus = 'ready';
      return { id: glyph.id, status: 'ready', url };
    } catch (error) {
      return { id: glyph.id, status: 'error', error: String(error?.message || error) };
    }
  }));

  return {
    text: TC001,
    results,
    ready: results.filter(x => x.status === 'ready').length,
    pending: results.filter(x => x.status !== 'ready').map(x => x.id),
    corpus
  };
}

export function tc001RealRenderGate(composition) {
  return assertRealGlyphs(composition);
}
