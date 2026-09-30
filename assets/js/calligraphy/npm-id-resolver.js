export function resolveNpmIiifIdentity(record, observed = {}) {
  if (!record?.collectionDetailId || !record?.workNumber || !record?.accessionNumber) {
    throw new Error('NPM identity requires collectionDetailId, workNumber and accessionNumber');
  }

  const candidate = {
    collectionDetailId: String(record.collectionDetailId),
    workNumber: record.workNumber,
    accessionNumber: record.accessionNumber,
    manifestCid: observed.manifestCid ? String(observed.manifestCid) : null,
    imageName: observed.imageName || null,
    canvasId: observed.canvasId || null,
    imageService: observed.imageService || null
  };

  const requiredObserved = ['manifestCid', 'canvasId', 'imageService'];
  const missing = requiredObserved.filter(key => !candidate[key]);

  return {
    ...candidate,
    status: missing.length ? 'blocked' : 'resolved',
    missing,
    manifestUrl: missing.includes('manifestCid')
      ? null
      : `https://digitalarchive.npm.gov.tw/Integrate/GetJson?cid=${encodeURIComponent(candidate.manifestCid)}&dept=P&imageName=${encodeURIComponent(candidate.imageName || '')}`
  };
}

export function assertNpmGlyphReady(identity) {
  if (!identity || identity.status !== 'resolved') {
    const missing = identity?.missing?.join(', ') || 'verified NPM IIIF identity';
    throw new Error(`NPM glyph promotion blocked: missing ${missing}`);
  }
  return identity;
}
