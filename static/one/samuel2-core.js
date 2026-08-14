/* ONE · 2 Samuel shared helpers */
(() => {
  "use strict";
  const art = (file, title) => ({
    src: `https://commons.wikimedia.org/wiki/Special:FilePath/${encodeURIComponent(file)}?width=1200`,
    alt: `古斯塔夫・多雷版畫：${title}`,
    title,
    source: `https://commons.wikimedia.org/wiki/File:${file.replaceAll(" ", "_")}`
  });

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
      prepare: study.prepare || [
        `完整閱讀撒母耳記下第 ${number} 章，圈出王權、約、罪、審判與恩典的敘事線索`,
        "沿地圖找出本章城市、山地、河谷與戰線，說明地理如何推動故事",
        "把本章放進「大衛之約—王的失敗—神仍守約」的全卷主線中",
        "選一條串珠全文並讀上下文，寫下一個敬畏、悔改或忠誠上的具體回應"
      ]
    };
  };

  const studies = {};
  window.ONE_SAMUEL2 = { art, mapDef, timeline, compare, finish, studies };
})();
