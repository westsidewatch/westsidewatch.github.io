/* ONE Studio Fixed Asset Registry — NON-DORÉ LIBRARY.
 *
 * Purpose:
 * - Stores reviewed, frozen ONE Studio/generated illustrations and other approved non-Doré fixed images.
 * - NEVER stores or aliases any of the canonical 241 Gustave Doré originals.
 * - Does not write chapter study.illustration directly.
 * - ONE_COVER_POLICY remains the sole runtime illustration writer/resolver.
 *
 * Fixed asset lifecycle:
 * CREATE -> REVIEW SCRIPTURE FIDELITY -> FREEZE FILE -> REGISTER ASSET -> REGISTER CHAPTER -> RENDER
 */
(() => {
  "use strict";

  const existing = window.ONE_STUDIO_ASSET_REGISTRY;
  if (existing?.mode === "ONE_STUDIO_FIXED_ASSETS") return;

  const assets = Object.create(null);
  const chapterMap = Object.create(null);

  const normalizeBook = value => String(Number(value));
  const normalizeChapter = value => String(Number(value));
  const chapterKey = (book, chapter) => `${normalizeBook(book)}:${normalizeChapter(chapter)}`;

  const validateAsset = (id, asset) => {
    if (!id || typeof id !== "string") throw new Error("ONE Studio asset id is required");
    if (!asset || typeof asset !== "object") throw new Error(`Invalid ONE Studio asset: ${id}`);
    if (!asset.src || typeof asset.src !== "string") throw new Error(`ONE Studio asset ${id} requires a stable src`);
    if (asset.doreId || asset.master === "ONE-DORE-241-MASTER-MAPPING") {
      throw new Error(`ONE Studio asset ${id} must not contain Doré registry identity`);
    }
    return true;
  };

  const registerAsset = (id, asset) => {
    validateAsset(id, asset);
    if (assets[id]) throw new Error(`ONE Studio asset is immutable once registered: ${id}`);
    assets[id] = Object.freeze({
      id,
      src: asset.src,
      alt: asset.alt || "ONE Studio biblical illustration",
      title: asset.title || id,
      source: asset.source || "ONE Studio Fixed Asset",
      artist: asset.artist || "ONE Studio",
      origin: asset.origin || "ONE_STUDIO",
      status: "FIXED_GENERATED",
      generatedOnce: true,
      palette: asset.palette || "MONOCHROME_ENGRAVING",
      scripture: asset.scripture || "",
      note: asset.note || ""
    });
    return assets[id];
  };

  const registerChapter = (book, chapter, assetId, meta = {}) => {
    const key = chapterKey(book, chapter);
    if (!assets[assetId]) throw new Error(`Unknown ONE Studio fixed asset: ${assetId}`);
    if (chapterMap[key]) throw new Error(`ONE Studio chapter assignment is immutable once registered: ${key}`);
    chapterMap[key] = Object.freeze({
      book: Number(book),
      chapter: Number(chapter),
      assetId,
      priority: meta.priority || "P3_ONE_STUDIO_FIXED",
      basis: meta.basis || "SCRIPTURE_DERIVED_GENERATE_ONCE"
    });
    return chapterMap[key];
  };

  const getAssignment = (book, chapter) => chapterMap[chapterKey(book, chapter)] || null;
  const getAsset = id => assets[id] || null;
  const resolve = (book, chapter) => {
    const assignment = getAssignment(book, chapter);
    if (!assignment) return null;
    const asset = getAsset(assignment.assetId);
    return asset ? { assignment, asset } : null;
  };

  window.ONE_STUDIO_ASSET_REGISTRY = Object.freeze({
    mode: "ONE_STUDIO_FIXED_ASSETS",
    version: "2026-08-17-v1",
    doréAssetsAllowed: false,
    generatedAssetsAllowed: true,
    nonDoréHistoricalAssetsAllowed: true,
    assets,
    chapterMap,
    registerAsset,
    registerChapter,
    getAsset,
    getAssignment,
    resolve
  });

  document.documentElement.dataset.oneStudioAssets = "separate-fixed-library";
})();
