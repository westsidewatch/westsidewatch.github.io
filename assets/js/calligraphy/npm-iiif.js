export function npmManifestUrl(cid, { openData = false } = {}) {
  if (!Number.isInteger(cid) || cid <= 0) throw new Error('NPM cid must be a positive integer');
  const root = openData
    ? 'https://digitalarchive.npm.gov.tw/opendata/Integrate/GetJson'
    : 'https://digitalarchive.npm.gov.tw/Integrate/GetJson';
  return `${root}?cid=${cid}&dept=P&imageName=`;
}

export function extractNpmCanvases(manifest) {
  const sequences = manifest?.sequences || [];
  const canvases = sequences.flatMap(sequence => sequence?.canvases || []);
  return canvases.map((canvas, index) => {
    const image = canvas?.images?.[0]?.resource;
    const service = image?.service;
    const serviceId = typeof service === 'string' ? service : service?.['@id'];
    const imageId = serviceId?.match(/\/([^/%]+)(?:\/info\.json)?$/)?.[1] || null;
    return {
      index,
      canvasId: canvas?.['@id'] || null,
      label: canvas?.label || null,
      width: canvas?.width || image?.width || null,
      height: canvas?.height || image?.height || null,
      imageService: serviceId || null,
      imageId
    };
  });
}

export function assertResolvableCanvas(canvas) {
  if (!canvas?.canvasId) throw new Error('missing IIIF canvas id');
  if (!canvas?.imageService) throw new Error('missing IIIF image service');
  if (!canvas?.width || !canvas?.height) throw new Error('missing source dimensions');
  return canvas;
}

export function buildRegionUrl(canvas, crop, { size = 'max', format = 'jpg' } = {}) {
  assertResolvableCanvas(canvas);
  for (const key of ['x', 'y', 'width', 'height']) {
    if (!Number.isFinite(crop?.[key]) || crop[key] < 0) throw new Error(`invalid crop ${key}`);
  }
  if (!crop.visuallyVerified) throw new Error('crop must be visually verified before IIIF region export');
  const region = [crop.x, crop.y, crop.width, crop.height].join(',');
  return `${canvas.imageService.replace(/\/$/, '')}/${region}/${size}/0/default.${format}`;
}
