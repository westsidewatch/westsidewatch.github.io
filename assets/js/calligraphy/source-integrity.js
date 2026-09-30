export function assertSourceIntegrity(glyphDraft, sourceSelection) {
  if (!glyphDraft || !sourceSelection?.selected) throw new Error('source-integrity:missing-input');
  const source = sourceSelection.selected;
  if (glyphDraft.collectionDetailId !== source.collectionDetailId) throw new Error('source-integrity:collection-mismatch');
  if (glyphDraft.workNumber !== source.workNumber) throw new Error('source-integrity:work-mismatch');
  if (!source.officialImageIds.includes(glyphDraft.imageId)) throw new Error('source-integrity:image-mismatch');
  if (!source.targets.includes(glyphDraft.literal)) throw new Error('source-integrity:unexpected-character');
  if (!glyphDraft.crop || !Number.isFinite(glyphDraft.crop.x) || !Number.isFinite(glyphDraft.crop.y) || !Number.isFinite(glyphDraft.crop.width) || !Number.isFinite(glyphDraft.crop.height)) {
    throw new Error('source-integrity:missing-crop');
  }
  if (glyphDraft.crop.width <= 0 || glyphDraft.crop.height <= 0) throw new Error('source-integrity:invalid-crop');
  if (glyphDraft.visualVerification !== true) throw new Error('source-integrity:unverified');
  return true;
}

export function glyphEvidenceKey(glyphDraft) {
  return [glyphDraft.workNumber, glyphDraft.imageId, glyphDraft.literal, glyphDraft.crop.x, glyphDraft.crop.y, glyphDraft.crop.width, glyphDraft.crop.height].join(':');
}
