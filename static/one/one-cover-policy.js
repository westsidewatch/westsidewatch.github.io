/* ONE cover policy — the central Doré registry is the only cover authority.
 * Book/chapter files may contain legacy illustration fields, but they are ignored and cleared here.
 * Future books must register Book+Chapter -> Doré ID in ONE_DORE_COVER_REGISTRY.maps.
 */
(() => {
  "use strict";
  const D = window.ONE_DATA;
  const R = window.ONE_DORE_COVER_REGISTRY;
  if (!D || !R) return;

  const parseMap = raw => {
    if (!raw) return {};
    if (typeof raw === "object") return raw;
    return Object.fromEntries(String(raw).split(",").filter(Boolean).map(pair => {
      const [chapter, id] = pair.split(":");
      return [String(Number(chapter)), Number(id)];
    }));
  };

  const makeArt = id => {
    const file = R.files?.[id];
    if (!file) return null;
    const title = R.titles?.[id] || `Doré plate ${String(id).padStart(3, "0")}`;
    return {
      src: `https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=1280`,
      alt: `古斯塔夫・多雷版畫：${title}`,
      title,
      source: "https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations",
      artist: "Gustave Doré",
      doreId: String(id).padStart(3, "0"),
      master: "ONE-DORE-241-MASTER-MAPPING"
    };
  };

  const clearLegacyCovers = () => {
    Object.values(D.studyBooks || {}).forEach(book => {
      Object.values(book?.chapterStudies || {}).forEach(study => {
        if (!study || typeof study !== "object") return;
        delete study.illustration;
        delete study.illustrations;
        delete study.coverIllustration;
        delete study.coverImage;
      });
    });
  };

  const applyBook = bookNumber => {
    const book = D.studyBooks?.[Number(bookNumber)];
    if (!book) return { applied: 0, unresolved: [] };
    const mapping = parseMap(R.maps?.[Number(bookNumber)] ?? R.maps?.[String(bookNumber)]);
    let applied = 0;
    const unresolved = [];

    Object.values(book.chapterStudies || {}).forEach(study => {
      if (!study || typeof study !== "object") return;
      delete study.illustration;
      delete study.illustrations;
      delete study.coverIllustration;
      delete study.coverImage;
    });

    Object.entries(mapping).forEach(([chapter, id]) => {
      const study = book.chapterStudies?.[chapter];
      if (!study) return;
      const art = makeArt(Number(id));
      study.doreCover = {
        id: String(id).padStart(3, "0"),
        title: R.titles?.[id],
        stage: "CENTRAL_DORE_ONLY",
        assetVerified: Boolean(art)
      };
      if (art) {
        study.illustration = art;
        applied += 1;
      } else {
        unresolved.push(`${bookNumber}:${chapter}:${String(id).padStart(3, "0")}`);
      }
    });
    return { applied, unresolved };
  };

  const applyAll = () => {
    clearLegacyCovers();
    let applied = 0;
    const unresolved = [];
    Object.keys(D.studyBooks || {}).forEach(bookNumber => {
      const result = applyBook(bookNumber);
      applied += result.applied;
      unresolved.push(...result.unresolved);
    });
    document.documentElement.dataset.oneCoverPolicy = "central-dore-only";
    document.documentElement.dataset.oneCoverApplied = String(applied);
    document.documentElement.dataset.oneCoverUnresolved = unresolved.join(",");
    return { applied, unresolved };
  };

  const registerBookMapping = (bookNumber, mapping) => {
    if (!R.maps) R.maps = {};
    R.maps[Number(bookNumber)] = mapping;
    return applyBook(Number(bookNumber));
  };

  window.ONE_COVER_POLICY = {
    mode: "CENTRAL_DORE_ONLY",
    legacyCoverRulesEnabled: false,
    clearLegacyCovers,
    applyBook,
    applyAll,
    registerBookMapping,
    getCover(bookNumber, chapter) {
      const mapping = parseMap(R.maps?.[Number(bookNumber)] ?? R.maps?.[String(bookNumber)]);
      const id = Number(mapping[String(Number(chapter))]);
      return id ? makeArt(id) : null;
    }
  };

  applyAll();
})();