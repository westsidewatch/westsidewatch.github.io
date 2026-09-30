function assertFinitePositive(value, name) {
  if (!Number.isFinite(value) || value <= 0) throw new Error(`${name} must be a positive finite number`);
}

export function validateCrop(crop) {
  if (!crop || crop.verified !== true) throw new Error('crop must be visually verified');
  for (const key of ['x', 'y', 'width', 'height']) assertFinitePositive(crop[key], key);
  if (!crop.canvasId && !crop.imageService) throw new Error('crop requires IIIF canvasId or imageService');
  if (!crop.evidenceUrl) throw new Error('crop requires evidenceUrl');
  return true;
}

export function iiifRegionUrl(imageService, crop, outputWidth = 800) {
  validateCrop({ ...crop, imageService });
  const region = [crop.x, crop.y, crop.width, crop.height].map(Math.round).join(',');
  return `${imageService.replace(/\/$/, '')}/${region}/${outputWidth},/0/default.jpg`;
}

export function promoteVerifiedCrop({ source, characterId, literal, crop, sequence = 1 }) {
  validateCrop(crop);
  if (!source?.id) throw new Error('source id required');
  if (!characterId || !literal) throw new Error('character identity required');
  return {
    id: `${source.id}-${characterId}-${String(sequence).padStart(2, '0')}`,
    characterId,
    sourceId: source.id,
    style: source.style || 'other',
    asset: crop.asset || iiifRegionUrl(crop.imageService, crop),
    derivativeOf: crop.evidenceUrl,
    crop: {
      page: crop.page ?? null,
      x: crop.x,
      y: crop.y,
      width: crop.width,
      height: crop.height,
      rotation: crop.rotation || 0
    },
    evidence: {
      literal,
      evidenceUrl: crop.evidenceUrl,
      canvasId: crop.canvasId || null,
      verified: true
    }
  };
}
