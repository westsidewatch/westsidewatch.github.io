/* ONE Studio Fixed Asset Registry — NON-DORÉ, EDITORIALLY REPLACEABLE LIBRARY.
 *
 * Doré originals are immutable. ONE Studio/generated assets are different:
 * they are fixed for runtime use, but may be explicitly replaced after later editorial review.
 * Runtime never guesses, regenerates, or swaps them automatically.
 * ONE_COVER_POLICY remains the sole runtime illustration writer/resolver.
 */
(() => {
  "use strict";

  const existing = window.ONE_STUDIO_ASSET_REGISTRY;
  if (existing?.mode === "ONE_STUDIO_VERSIONED_ASSETS") return;

  const assets = Object.create(null);
  const chapterMap = Object.create(null);
  const history = Object.create(null);

  const normalizeBook = value => String(Number(value));
  const normalizeChapter = value => String(Number(value));
  const chapterKey = (book, chapter) => `${normalizeBook(book)}:${normalizeChapter(chapter)}`;
  const now = () => new Date().toISOString();

  const validateAsset = (id, asset) => {
    if (!id || typeof id !== "string") throw new Error("ONE Studio asset id is required");
    if (!asset || typeof asset !== "object") throw new Error(`Invalid ONE Studio asset: ${id}`);
    if (!asset.src || typeof asset.src !== "string") throw new Error(`ONE Studio asset ${id} requires a stable src`);
    if (asset.doreId || asset.master === "ONE-DORE-241-MASTER-MAPPING") {
      throw new Error(`ONE Studio asset ${id} must not contain Doré registry identity`);
    }
    return true;
  };

  const makeVersion = (id, asset, revision, previousId = null) => Object.freeze({
    id,
    revision,
    previousId,
    src: asset.src,
    alt: asset.alt || "ONE Studio biblical illustration",
    title: asset.title || id,
    source: asset.source || "ONE Studio Fixed Asset",
    artist: asset.artist || "ONE Studio",
    origin: asset.origin || "ONE_STUDIO",
    status: "ACTIVE_FIXED",
    generatedOnce: true,
    replaceableByEditorialReview: true,
    palette: asset.palette || "MONOCHROME_ENGRAVING",
    scripture: asset.scripture || "",
    note: asset.note || "",
    approvedAt: asset.approvedAt || now(),
    master: "ONE-STUDIO-VERSIONED-ASSET-LIBRARY"
  });

  const registerAsset = (id, asset) => {
    validateAsset(id, asset);
    if (assets[id]) throw new Error(`ONE Studio asset id already exists: ${id}; use replaceAsset()`);
    const version = makeVersion(id, asset, 1);
    assets[id] = version;
    history[id] = [version];
    return version;
  };

  const replaceAsset = (id, asset, meta = {}) => {
    validateAsset(id, asset);
    const current = assets[id];
    if (!current) throw new Error(`Unknown ONE Studio asset: ${id}; use registerAsset()`);
    const revision = Number(current.revision || 1) + 1;
    const replacement = makeVersion(id, {
      ...asset,
      note: meta.reason ? `${asset.note || ""}${asset.note ? " · " : ""}Replacement reason: ${meta.reason}` : asset.note
    }, revision, id);
    assets[id] = replacement;
    history[id] = [...(history[id] || []), replacement];
    return replacement;
  };

  const registerChapter = (book, chapter, assetId, meta = {}) => {
    const key = chapterKey(book, chapter);
    if (!assets[assetId]) throw new Error(`Unknown ONE Studio fixed asset: ${assetId}`);
    if (chapterMap[key]) throw new Error(`Chapter assignment already exists: ${key}; use reassignChapter()`);
    chapterMap[key] = Object.freeze({
      book: Number(book),
      chapter: Number(chapter),
      assetId,
      revision: 1,
      priority: meta.priority || "P7_ONE_STUDIO_FIXED",
      basis: meta.basis || "SCRIPTURE_DERIVED_EDITORIALLY_APPROVED",
      assignedAt: now()
    });
    return chapterMap[key];
  };

  const reassignChapter = (book, chapter, assetId, meta = {}) => {
    const key = chapterKey(book, chapter);
    if (!assets[assetId]) throw new Error(`Unknown ONE Studio fixed asset: ${assetId}`);
    const current = chapterMap[key];
    chapterMap[key] = Object.freeze({
      book: Number(book),
      chapter: Number(chapter),
      assetId,
      revision: Number(current?.revision || 0) + 1,
      priority: meta.priority || current?.priority || "P7_ONE_STUDIO_FIXED",
      basis: meta.basis || "EDITORIAL_REPLACEMENT",
      reason: meta.reason || "",
      assignedAt: now()
    });
    return chapterMap[key];
  };

  const getAssignment = (book, chapter) => chapterMap[chapterKey(book, chapter)] || null;
  const getAsset = id => assets[id] || null;
  const getHistory = id => Object.freeze([...(history[id] || [])]);
  const resolve = (book, chapter) => {
    const assignment = getAssignment(book, chapter);
    if (!assignment) return null;
    const asset = getAsset(assignment.assetId);
    return asset ? { assignment, asset } : null;
  };

  window.ONE_STUDIO_ASSET_REGISTRY = Object.freeze({
    mode: "ONE_STUDIO_VERSIONED_ASSETS",
    version: "2026-08-17-v2",
    doreAssetsAllowed: false,
    generatedAssetsAllowed: true,
    nonDoréHistoricalAssetsAllowed: true,
    runtimeReplacementAllowed: false,
    editorialReplacementAllowed: true,
    assets,
    chapterMap,
    registerAsset,
    replaceAsset,
    registerChapter,
    reassignChapter,
    getAsset,
    getAssignment,
    getHistory,
    resolve
  });

  document.documentElement.dataset.oneStudioAssets = "separate-versioned-library";
})();