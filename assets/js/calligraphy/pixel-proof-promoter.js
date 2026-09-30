function assertSha256(value) {
  if (!/^[a-f0-9]{64}$/i.test(value || '')) throw new Error('pixel-proof: invalid sha256');
}

function assertPositiveInt(value, label) {
  if (!Number.isInteger(value) || value <= 0) throw new Error(`pixel-proof: invalid ${label}`);
}

export function promotePixelProof({ source, image, target, proof }) {
  if (!source?.id || !source?.workNumber) throw new Error('pixel-proof: source identity required');
  if (!image?.imageId) throw new Error('pixel-proof: imageId required');
  if (!target?.characterId || !target?.literal) throw new Error('pixel-proof: target required');
  if (!proof?.humanVisualVerified) throw new Error('pixel-proof: human visual verification required');

  assertPositiveInt(proof.width, 'width');
  assertPositiveInt(proof.height, 'height');
  assertSha256(proof.sha256);

  const { x, y, width, height } = proof.crop || {};
  for (const [label, value] of Object.entries({ x, y, width, height })) {
    if (!Number.isInteger(value) || value < 0 || ((label === 'width' || label === 'height') && value === 0)) {
      throw new Error(`pixel-proof: invalid crop ${label}`);
    }
  }
  if (x + width > proof.width || y + height > proof.height) throw new Error('pixel-proof: crop outside image bounds');

  return {
    id: `${source.id}-${image.imageId}-${target.characterId}`,
    characterId: target.characterId,
    sourceId: source.id,
    sourceWorkNumber: source.workNumber,
    sourceImageId: image.imageId,
    style: source.style || 'other',
    asset: proof.asset,
    derivativeOf: proof.originalAsset,
    crop: { x, y, width, height, rotation: proof.rotation || 0 },
    evidence: {
      officialRecord: source.officialRecord,
      sha256: proof.sha256,
      humanVisualVerified: true,
      verifiedLiteral: target.literal
    }
  };
}
