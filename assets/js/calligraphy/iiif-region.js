export function assertRegion(region) {
  if (!region || !Number.isFinite(region.x) || !Number.isFinite(region.y) ||
      !Number.isFinite(region.width) || !Number.isFinite(region.height)) {
    throw new Error('verified xywh region required');
  }
  if (region.x < 0 || region.y < 0 || region.width <= 0 || region.height <= 0) {
    throw new Error('invalid IIIF region');
  }
  if (region.verified !== true || !region.verifiedBy || !region.verifiedAt) {
    throw new Error('human visual verification required');
  }
  return region;
}

export function buildIiifCropUrl(imageService, region, options = {}) {
  assertRegion(region);
  if (!/^https:\/\//.test(imageService || '')) throw new Error('HTTPS IIIF image service required');
  const xywh = [region.x, region.y, region.width, region.height].map(Math.round).join(',');
  const size = options.size || 'max';
  const rotation = options.rotation || 0;
  const quality = options.quality || 'default';
  const format = options.format || 'jpg';
  return `${imageService.replace(/\/$/, '')}/${xywh}/${size}/${rotation}/${quality}.${format}`;
}

export function promoteVerifiedRegion({ sourceId, characterId, glyphId, imageService, canvas, region, style = 'running' }) {
  assertRegion(region);
  if (!sourceId || !characterId || !glyphId || !canvas) throw new Error('complete provenance required');
  return {
    id: glyphId,
    characterId,
    sourceId,
    style,
    asset: buildIiifCropUrl(imageService, region),
    derivativeOf: canvas,
    crop: {
      x: region.x,
      y: region.y,
      width: region.width,
      height: region.height,
      rotation: 0
    },
    evidence: {
      canvas,
      imageService,
      verifiedBy: region.verifiedBy,
      verifiedAt: region.verifiedAt
    }
  };
}
