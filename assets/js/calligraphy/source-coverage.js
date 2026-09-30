export function uniqueCharacters(text) {
  return [...new Set(Array.from(text).filter(ch => /\p{Script=Han}/u.test(ch)))];
}

export function sourceCoverage(phrase, transcription) {
  const sourceSet = new Set(uniqueCharacters(transcription.text || ''));
  const requested = uniqueCharacters(phrase);
  const present = requested.filter(ch => sourceSet.has(ch));
  const missing = requested.filter(ch => !sourceSet.has(ch));
  return {
    sourceId: transcription.sourceId,
    phrase,
    requested,
    present,
    missing,
    coverage: requested.length ? present.length / requested.length : 1
  };
}

export function requireVerifiedCrop(glyph) {
  if (!glyph?.crop) throw new Error('glyph crop missing');
  if (glyph.crop.verified !== true) throw new Error('glyph crop is not verified');
  if (!glyph.crop.evidenceRegion) throw new Error('glyph evidence region missing');
  return glyph;
}
