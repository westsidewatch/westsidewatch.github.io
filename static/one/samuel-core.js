/* ONE · 1 Samuel shared helpers */
(() => {
  "use strict";
  const art = (file, title) => ({
    src: `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file)}?width=1200`,
    alt: `古斯塔夫・多雷版畫：${title}`,
    title,
    source: `https://commons.wikimedia.org/wiki/File:${file.replaceAll(" ", "_")}`
  });

  const fallbackMap = (id) => {
    const maps = {
      46: ["Biblica Open Bible Map 05 The Twelve Tribes of Israel.png", "Biblica Open Bible · The Twelve Tribes of Israel"],
      47: ["Biblica Open Bible Map 05 The Twelve Tribes of Israel.png", "Biblica Open Bible · The Twelve Tribes of Israel"],
      48: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"],
      49: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"],
      50: ["Kingdom of Israel 1020 map mk.svg", "Kingdom of Israel c. 1020 BC"],
      51: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"],
      52: ["Biblica Open Bible Map 05 The Twelve Tribes of Israel.png", "Biblica Open Bible · The Twelve Tribes of Israel"],
      53: ["Kingdom of Israel 1020 map mk.svg", "Kingdom of Israel c. 1020 BC"],
      54: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"]
    };
    const [file, title] = maps[id] || maps[50];
    return {
      image: `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file)}?width=960`,
      source: `https://commons.wikimedia.org/wiki/File:${file.replaceAll(" ", "_")}`,
      title
    };
  };

  const bindMapFallback = () => {
    if (window.__ONE_MAP_FALLBACK_BOUND) return;
    window.__ONE_MAP_FALLBACK_BOUND = true;
    document.addEventListener("error", (event) => {
      const image = event.target;
      if (!(image instanceof HTMLImageElement) || !image.closest(".map-reading__plate") || image.dataset.oneFallbackApplied) return;
      const id = Number((image.currentSrc || image.src).match(/map_thumbs\/(\d+)/)?.[1]);
      const fallback = fallbackMap(id);
      image.dataset.oneFallbackApplied = "true";
      image.src = fallback.image;
      image.alt = fallback.title;
      const figure = image.closest(".map-reading__plate");
      const link = image.closest("a");
      if (link) link.href = fallback.source;
      const title = figure?.querySelector("figcaption strong");
      const credit = figure?.querySelector("figcaption span");
      if (title) title.textContent = fallback.title;
      if (credit) credit.textContent = "替代地圖：Wikimedia Commons；僅在聖光原圖載入失敗時使用";
    }, true);
  };
  bindMapFallback();

  const mapDef = (id, title, places, bbox, marker, reference, guide) => ({
    image: `https://biblegeography.holylight.org.tw/images/index/condensedbible/map_thumbs/${String(id).padStart(3, "0")}.jpg`,
    imageTitle: `撒上圖 · ${title}`,
    source: `https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${String(id).padStart(3, "0")}`,
    mapId: id,
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
