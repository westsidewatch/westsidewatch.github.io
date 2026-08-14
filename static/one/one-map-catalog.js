/* ONE shared map catalog guard.
 * Rule: when a source map has numbered routes, the legend must expose the
 * same complete numbered set. Chapter story routes must never replace it.
 */
(() => {
  "use strict";

  const C = window.ONE_MAP_CATALOG = window.ONE_MAP_CATALOG || {};

  C[117] = {
    title: "徒圖五（117）保羅第二次行傳",
    source: "https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=117",
    expectedRouteCount: 10,
    routes: [
      ["①","徒 15:22–38","保羅和巴拿巴被差遣從耶路撒冷到安提阿工作。"],
      ["②","徒 15:39","巴拿巴和馬可往居比路。"],
      ["③","徒 15:40–41","保羅走遍敘利亞和基利家，堅固眾教會。"],
      ["④","徒 16:1–5","保羅到特庇、路司得和以哥念。"],
      ["⑤","徒 16:6–10","保羅經弗呂家、加拉太、每西亞，到特羅亞。"],
      ["⑥","徒 16:11–40","保羅渡海到腓立比。"],
      ["⑦","徒 17:1–14","保羅到帖撒羅尼迦、庇哩亞。"],
      ["⑧","徒 17:15–18:18","保羅到雅典、哥林多，並在哥林多住了一年半。"],
      ["⑨","徒 18:19–21","保羅到以弗所。"],
      ["⑩","徒 18:22","保羅經該撒利亞返耶路撒冷。"]
    ]
  };

  const mapId = (map) => {
    const text = `${map?.source || ""} ${map?.imageTitle || ""}`;
    const match = text.match(/(?:m_id=|[（(])(\d{3})(?:[）)]|\b)/);
    return match ? Number(match[1]) : null;
  };

  const applyCatalog = (study) => {
    if (!study?.map) return;
    const id = mapId(study.map);
    const entry = id && C[id];
    if (!entry) return;
    study.map.routes = entry.routes.map(row => [...row]);
    study.map.routeCount = entry.expectedRouteCount;
    study.map.routeLegendVerified = study.map.routes.length === entry.expectedRouteCount;
    if (!study.map.routeLegendVerified) {
      console.error(`[ONE map ${id}] route legend mismatch: expected ${entry.expectedRouteCount}, got ${study.map.routes.length}`);
    }
  };

  const walkStudies = () => {
    const D = window.ONE_DATA;
    if (!D) return;
    Object.values(D.studyBooks || {}).forEach(book => {
      Object.values(book?.chapterStudies || {}).forEach(applyCatalog);
    });
    Object.values(D.matthew?.chapterStudies || {}).forEach(applyCatalog);
    Object.values(D.thessalonians1?.chapterStudies || {}).forEach(applyCatalog);
    Object.values(D.thessalonians2?.chapterStudies || {}).forEach(applyCatalog);
  };

  window.ONE_applyMapCatalog = walkStudies;
})();
