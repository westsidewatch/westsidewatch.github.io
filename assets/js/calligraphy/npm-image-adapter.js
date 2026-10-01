export function npmImageEndpoint(imageId, randomCode = null) {
  if (!Number.isInteger(Number(imageId)) || Number(imageId) <= 0) {
    throw new Error('A verified positive NPM imageId is required');
  }
  const url = new URL('https://digitalarchive.npm.gov.tw/Image/GetImage');
  url.searchParams.set('imageId', String(imageId));
  if (randomCode != null) url.searchParams.set('randomCode', String(randomCode));
  return url.toString();
}

export function assertPixelEvidence(image) {
  if (!image?.imageId) throw new Error('Missing verified NPM imageId');
  if (!image?.width || !image?.height) throw new Error('Missing actual image pixel dimensions');
  if (!image?.sha256) throw new Error('Missing immutable image checksum');
  return image;
}

export function createManualCropEvidence(image, literal, crop) {
  assertPixelEvidence(image);
  for (const key of ['x', 'y', 'width', 'height']) {
    if (!Number.isFinite(crop?.[key]) || crop[key] < 0) throw new Error(`Invalid crop ${key}`);
  }
  if (crop.x + crop.width > image.width || crop.y + crop.height > image.height) {
    throw new Error('Crop exceeds source image bounds');
  }
  if (crop.visualVerified !== true) throw new Error('Crop requires visual verification');
  return {
    provider: 'npm-open-image',
    imageId: Number(image.imageId),
    sourceSha256: image.sha256,
    literal,
    crop: { x: crop.x, y: crop.y, width: crop.width, height: crop.height },
    visualVerified: true
  };
}
