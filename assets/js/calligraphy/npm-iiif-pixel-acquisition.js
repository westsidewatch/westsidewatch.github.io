function assertUrl(value, label) {
  if (!value || !/^https:\/\//u.test(value)) throw new Error(`${label} must be an https URL`);
  return value;
}

export function npmManifestEndpoint(cid, dept = 'P') {
  if (!Number.isInteger(cid) || cid <= 0) throw new Error('NPM IIIF cid must be a positive integer');
  return `https://digitalarchive.npm.gov.tw/opendata/Integrate/GetJson?cid=${cid}&dept=${encodeURIComponent(dept)}&imageName=`;
}

export function extractIiifImages(manifest) {
  const canvases = manifest?.sequences?.flatMap(sequence => sequence.canvases || []) || [];
  return canvases.flatMap((canvas, canvasIndex) =>
    (canvas.images || []).map((annotation, imageIndex) => {
      const resource = annotation?.resource || {};
      const service = Array.isArray(resource.service) ? resource.service[0] : resource.service;
      const serviceId = service?.['@id'] || service?.id || null;
      const resourceId = resource?.['@id'] || resource?.id || null;
      return {
        canvasIndex,
        imageIndex,
        canvasId: canvas?.['@id'] || canvas?.id || null,
        width: resource.width || canvas.width || null,
        height: resource.height || canvas.height || null,
        imageService: serviceId,
        resourceId,
        fullImageUrl: serviceId ? `${serviceId.replace(/\/$/u, '')}/full/full/0/default.jpg` : resourceId
      };
    })
  );
}

export function requirePixelCandidate(candidate) {
  if (!candidate) throw new Error('IIIF image candidate is required');
  const url = assertUrl(candidate.fullImageUrl, 'IIIF full image');
  if (!(candidate.width > 0) || !(candidate.height > 0)) {
    throw new Error('IIIF image dimensions must be resolved before crop verification');
  }
  return { ...candidate, fullImageUrl: url, pixelVerified: false };
}

export function bindImageId(candidate, imageId) {
  if (!Number.isInteger(imageId) || imageId <= 0) throw new Error('NPM imageId must be a positive integer');
  return { ...requirePixelCandidate(candidate), npmImageId: imageId };
}
