function assertHttpUrl(value, field) {
  if (!/^https:\/\//i.test(value || '')) throw new Error(`${field} must be an explicit https URL`);
}

export function admitOpenImage(input) {
  const {
    sourceId,
    objectNumber,
    imageUrl,
    officialRecordUrl,
    rights,
    attribution = null,
    width,
    height
  } = input || {};

  if (!sourceId || !objectNumber) throw new Error('source identity required');
  assertHttpUrl(imageUrl, 'imageUrl');
  assertHttpUrl(officialRecordUrl, 'officialRecordUrl');
  if (!['CC0', 'CC BY 4.0'].includes(rights)) throw new Error('unsupported or unverified rights');
  if (rights === 'CC BY 4.0' && !attribution) throw new Error('attribution required');
  if (!Number.isInteger(width) || width <= 0 || !Number.isInteger(height) || height <= 0) {
    throw new Error('verified pixel dimensions required');
  }

  return {
    sourceId,
    objectNumber,
    original: {
      url: imageUrl,
      width,
      height,
      rights,
      attribution,
      evidenceUrl: officialRecordUrl,
      immutable: true
    },
    status: 'image-admitted'
  };
}

export function promoteManualCrop(image, crop) {
  if (!image?.original?.immutable) throw new Error('admitted immutable original required');
  const { character, characterId, x, y, width, height, verifiedByHuman } = crop || {};
  if (!character || !characterId) throw new Error('character identity required');
  if (![x, y, width, height].every(Number.isInteger)) throw new Error('integer pixel crop required');
  if (x < 0 || y < 0 || width <= 0 || height <= 0) throw new Error('invalid crop bounds');
  if (x + width > image.original.width || y + height > image.original.height) throw new Error('crop exceeds original');
  if (verifiedByHuman !== true) throw new Error('visual verification required');

  return {
    character,
    characterId,
    sourceId: image.sourceId,
    objectNumber: image.objectNumber,
    crop: { x, y, width, height },
    evidenceUrl: image.original.evidenceUrl,
    rights: image.original.rights,
    attribution: image.original.attribution,
    status: 'crop-verified'
  };
}
