/* ONE · 1 Samuel shared helpers */
(() => {
  "use strict";
  const art = (file, title) => ({
    src: `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file)}?width=1200`,
    alt: `古斯塔夫・多雷版畫：${title}`,
    title,
    source: `https://commons.wikimedia.org/wiki/File:${file.replaceAll(" ", "_")}`
  });

  const bindMapFallback = () => {
    if (window.__ONE_MAP_FALLBACK_BOUND) return;
    window.__ONE_MAP_FALLBACK_BOUND = true;
    const fallbackImage = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Biblica_Open_Bible_Map_06_The_Kingdoms_of_Saul_David_and_Solomon.png/960px-Biblica_Open_Bible_Map_06_The_Kingdoms_of_Saul_David_and_Solomon.png";
    const fallbackSource = "https://commons.wikimedia.org/wiki/File:Biblica_Open_Bible_Map_06_The_Kingdoms_of_Saul_David_and_Solomon.png";
    document.addEventListener("error", (event) => {
      const image = event.target;
      if (!(image instanceof HTMLImageElement) || !image.closest(".map-reading__plate") || image.dataset.oneFallbackApplied) return;
      image.dataset.oneFallbackApplied = "true";
      image.src = fallbackImage;
      image.alt = "Biblica Open Bible：掃羅、大衛與所羅門王國地圖";
      const figure = image.closest(".map-reading__plate");
      const link = image.closest("a");
      if (link) link.href = fallbackSource;
      const title = figure?.querySelector("figcaption strong");
      const credit = figure?.querySelector("figcaption span");
      if (title) title.textContent = "Biblica Open Bible · The Kingdoms of Saul, David and Solomon";
      if (credit) credit.textContent = "替代地圖：Biblica Open Bible · Wikimedia Commons · CC BY-SA 4.0";
    }, true);
  };
  bindMapFallback();

  const mapDef = (id, title, places, bbox, marker, reference, guide) => ({
    image: `https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${id}.GIF`,
    imageTitle: `撒上圖 · ${title}`,
    source: `https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${id}`,
    bbox, marker, places, reference, title, guide
  });

  const timeline = (title, range, note, events) => ({
    title, range, note, events, url: "https://bibleeveryone.com/bible-timeline.php"
  });

  const compare = (chapter, theme, related) => ({
    title: "書卷互照",
    headers: ["主題", "本章", "撒母耳記上", "舊約延伸", "新約回聲"],
    rows: [
      [theme, `撒上 ${chapter}`, related[0], related[1], related[2]],
      ["王權與聽命", `撒上 ${chapter}`, "撒上 8；12；15", "申 17:14–20", "可 10:42–45"],
      ["神的主權", `撒上 ${chapter}`, "撒上 2:1–10", "詩 75:6–7", "路 1:51–53"]
    ]
  });

  const finish = (number, study) => {
    if (study.map && Array.isArray(study.route)) {
      study.map.routes = study.route.map((item, index) => [
        `${index + 1}`,
        item[0],
        item[1]
      ]);
      study.map.preface = `第 ${number} 章先按經文路徑閱讀，再用聖光原圖確認城市、山地與戰線。`;
    }
    return {
      ...study,
      prepare: study.prepare || [
        `完整閱讀撒母耳記上第 ${number} 章，圈出「耶和華說／問耶和華／耶和華與他同在」等敘事線索`,
        "沿地圖找出本章城市、山地、曠野與戰線，說明地理如何推動故事",
        "把本章放進「神作王—先知說話—君王聽命」的全卷主線中",
        "選一條串珠全文並讀上下文，寫下一個順服上的具體回應"
      ]
    };
  };

  const studies = {};
  window.ONE_SAMUEL = { art, mapDef, timeline, compare, finish, studies };
})();
