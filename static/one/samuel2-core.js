/* ONE · 2 Samuel shared helpers */
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

  const illustrationFor = (chapter) => {
    const c = Number(chapter);
    if (c === 1) return art("077.Jabesh-Gileadites Recover the Bodies of Saul and His Sons.jpg", "Jabesh-Gileadites Recover the Bodies of Saul and His Sons");
    if (c >= 2 && c <= 9) return art("078.Combat between Soldiers of Ish-bosheth and David.jpg", "Combat between Soldiers of Ish-bosheth and David");
    if (c >= 10 && c <= 14) return art("079.David Attacks the Ammonites.jpg", "David Attacks the Ammonites");
    if (c >= 15 && c <= 18) return art("080.The Death of Absalom.jpg", "The Death of Absalom");
    if (c >= 19 && c <= 20) return art("081.David Mourns the Death of Absalom.jpg", "David Mourns the Death of Absalom");
    if (c === 21) return art("082.Rizpah’s Kindness toward the Dead.jpg", "Rizpah’s Kindness toward the Dead");
    if (c >= 22 && c <= 23) return art("083.Abishai Saves David's Life.jpg", "Abishai Saves David's Life");
    return art("102A.The Plague of Jerusalem.jpg", "The Plague of Jerusalem");
  };

  const mapDef = (id, title, places, bbox, marker, reference, guide) => ({
    image: `https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${id}.GIF`,
    imageTitle: `撒下圖 · ${title}`,
    source: `https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${id}`,
    bbox, marker, places, reference, title, guide
  });

  const timeline = (title, range, note, events) => ({
    title, range, note, events, url: "https://bibleeveryone.com/bible-timeline.php"
  });

  const compare = (chapter, theme, related) => ({
    title: "書卷互照",
    headers: ["主題", "本章", "撒母耳記下", "舊約延伸", "新約回聲"],
    rows: [
      [theme, `撒下 ${chapter}`, related[0], related[1], related[2]],
      ["大衛之約與王權", `撒下 ${chapter}`, "撒下 7", "詩 89；132", "路 1:32–33"],
      ["罪、審判與恩典", `撒下 ${chapter}`, "撒下 11–12；24", "詩 51", "羅 5:20–21"]
    ]
  });

  const finish = (number, study) => {
    if (study.map && Array.isArray(study.route)) {
      study.map.routes = study.route.map((item, index) => [`${index + 1}`, item[0], item[1]]);
      study.map.preface = `第 ${number} 章先按經文路徑閱讀，再用聖光原圖確認城市、山地、河谷與戰線。`;
    }
    return {
      ...study,
      illustration: study.illustration || illustrationFor(number),
      prepare: study.prepare || [
        `完整閱讀撒母耳記下第 ${number} 章，圈出王權、約、罪、審判與恩典的敘事線索`,
        "沿地圖找出本章城市、山地、河谷與戰線，說明地理如何推動故事",
        "把本章放進「大衛之約—王的失敗—神仍守約」的全卷主線中",
        "選一條串珠全文並讀上下文，寫下一個敬畏、悔改或忠誠上的具體回應"
      ]
    };
  };

  const studies = {};
  window.ONE_SAMUEL2 = { art, illustrationFor, mapDef, timeline, compare, finish, studies };
})();
