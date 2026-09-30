export function requirePixelProof(record) {
  if (!record) throw new Error('pixel proof record required');
  const required = ['imageId', 'width', 'height', 'sha256', 'crop'];
  for (const key of required) {
    if (record[key] == null) throw new Error(`pixel proof missing ${key}`);
  }
  if (!Number.isInteger(record.width) || record.width <= 0) throw new Error('invalid image width');
  if (!Number.isInteger(record.height) || record.height <= 0) throw new Error('invalid image height');
  if (!/^[a-f0-9]{64}$/i.test(record.sha256)) throw new Error('invalid sha256');
  if (record.humanVisualVerified !== true) throw new Error('human visual verification required');

  const { x, y, width, height } = record.crop;
  for (const [name, value] of Object.entries({ x, y, width, height })) {
    if (!Number.isFinite(value)) throw new Error(`invalid crop ${name}`);
  }
  if (x < 0 || y < 0 || width <= 0 || height <= 0) throw new Error('crop outside valid range');
  if (x + width > record.width || y + height > record.height) throw new Error('crop exceeds source pixels');
  if (!record.character || Array.from(record.character).length !== 1) throw new Error('single target character required');
  if (!record.sourcePage || !record.workNumber) throw new Error('source provenance required');
  return true;
}

export function promotePixelProofToGlyph(record) {
  requirePixelProof(record);
  return {
    id: `${record.workNumber}-${record.imageId}-${record.character.codePointAt(0).toString(16)}`,
    character: record.character,
    characterId: `u${record.character.codePointAt(0).toString(16).padStart(4, '0')}`,
    sourceId: record.sourceId,
    style: record.style || 'running',
    asset: record.asset,
    derivativeOf: record.originalAsset,
    crop: { ...record.crop, page: null, rotation: record.crop.rotation || 0 },
    evidence: {
      sourcePage: record.sourcePage,
      workNumber: record.workNumber,
      imageId: record.imageId,
      sourceSha256: record.sha256,
      humanVisualVerified: true
    }
  };
}
