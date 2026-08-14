/* ONE · 2 Samuel shared helpers */
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
      55: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"],
      56: ["Kingdom of Israel 1020 map mk.svg", "Kingdom of Israel c. 1020 BC"],
      57: ["Biblica Open Bible Map 06 The Kingdoms of Saul David and Solomon.png", "Biblica Open Bible · The Kingdoms of Saul, David and Solomon"],
      58: ["Biblica Open Bible Map 05 The Twelve Tribes of Israel.png", "Biblica Open Bible · The Twelve Tribes of Israel"],
      59: ["1759 map Holy Land and 12 Tribes.jpg", "Holy Land and the Twelve Tribes · 1759"]
    };
    const [file, title] = maps[id] || maps[55];
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

  // Complete numbered route legends from Holy Light maps 055–059.
  // Chapter-level study.route remains the story path for that chapter; it must not replace the map legend.
  const mapRoutes = {
    55: [
      ["1", "撒下 2:1–4", "大衛上希伯崙，猶大人在那裡膏他作猶大家的王。"],
      ["2", "撒下 2:12–31", "押尼珥從瑪哈念領兵到基遍，與大衛一方交戰後敗退。"],
      ["3", "撒下 4:5–12；5:1–5", "伊施波設被殺，其首級被帶到希伯崙；其後眾支派在希伯崙膏大衛作全以色列王。"]
    ],
    56: [
      ["1", "撒下 5:6–10；代上 11:4", "大衛攻取耶路撒冷，立為首都。"],
      ["2", "撒下 5:17–18；代上 14:8–9", "非利士軍進入利乏音谷，威脅耶路撒冷。"],
      ["3", "撒下 5:19–20；代上 14:10–11", "大衛在巴力毘拉心擊敗非利士人。"],
      ["4", "撒下 5:21；代上 14:12", "非利士人棄下偶像逃走。"],
      ["5", "撒下 5:22；代上 14:13", "非利士人再次進入利乏音谷。"],
      ["6", "撒下 5:23–25；代上 14:14–16", "大衛按神指示從後方包抄非利士軍。"],
      ["7", "撒下 5:25；代上 14:16", "大衛追擊非利士人，戰線延伸到基色方向。"],
      ["8", "撒下 6:1–19；代上 13:1–14", "大衛把約櫃從巴拉猶大一帶迎往耶路撒冷。"]
    ],
    57: [
      ["1", "撒下 8:1；代上 18:1", "大衛制服非利士。"],
      ["2", "撒下 8:2；代上 18:2", "大衛制服摩押。"],
      ["3", "撒下 8:3–8；代上 18:3–4", "大衛北上擊敗瑣巴勢力。"],
      ["4", "撒下 8:5–6；代上 18:5–8", "大衛擊敗大馬色的亞蘭援軍並設防。"],
      ["5", "撒下 8:9–12；代上 18:9–11", "哈馬等國向大衛致意進貢，戰利品歸耶和華。"],
      ["6", "撒下 8:13–14；代上 18:12–13", "大衛在南方擊敗以東勢力並設置駐軍。"],
      ["7", "撒下 9", "大衛把約拿單之子米非波設從羅底巴接到耶路撒冷。"],
      ["8", "撒下 10:1–8；代上 19:1–7", "亞捫招募亞蘭軍隊，準備與大衛交戰。"],
      ["9", "撒下 10:9–14；代上 19:8–15", "約押分兵兩路，擊退亞捫與亞蘭聯軍。"],
      ["10", "撒下 10:15–16；代上 19:16", "亞蘭從幼發拉底河以北再調軍到希蘭集結。"],
      ["11", "撒下 10:17–19；代上 19:17–19", "大衛渡河到希蘭決戰，擊敗亞蘭軍，諸王轉而臣服。"]
    ],
    58: [
      ["1", "撒下 13:23–29", "押沙龍在巴力夏瑣設宴，殺死暗嫩。"],
      ["2", "撒下 13:37–39", "押沙龍逃往基述，在外祖父的國中住了三年。"],
      ["3", "撒下 14:1–25", "約押藉提哥亞婦人說情，押沙龍獲准回耶路撒冷。"],
      ["4", "撒下 15:7–12", "押沙龍到希伯崙公開發動叛變。"],
      ["5", "撒下 15:13–17:24", "大衛離開耶路撒冷，經約但河東逃到瑪哈念。"],
      ["6", "撒下 17:24", "押沙龍的軍隊也渡過約但河，進入河東戰區。"],
      ["7", "撒下 18:1–16", "大衛軍分三隊與押沙龍交戰；押沙龍在以法蓮樹林一帶兵敗被殺。"]
    ],
    59: [
      ["1", "撒下 20:4–10", "示巴叛變後，大衛命亞瑪撒召兵；亞瑪撒遲延，後在基遍被約押殺死。"],
      ["2", "撒下 20:14–23", "約押追擊示巴到亞比拉；城中婦人促成示巴被殺，叛亂結束。"],
      ["3", "撒下 21:12", "大衛從基列雅比取回掃羅和約拿單的骸骨，帶回便雅憫地安葬。"],
      ["4", "撒下 24:2–9", "約押奉命走遍以色列全地數點百姓，最後回到耶路撒冷。"]
    ]
  };

  const mapDef = (id, title, places, bbox, marker, reference, guide) => ({
    image: `https://biblegeography.holylight.org.tw/images/index/condensedbible/map_thumbs/${String(id).padStart(3, "0")}.jpg`,
    imageTitle: `撒下圖 · ${title}`,
    source: `https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${String(id).padStart(3, "0")}`,
    mapId: id,
    routes: mapRoutes[id] || [],
    preface: `本段為聖光地圖 ${String(id).padStart(3, "0")} 的完整編號路線；本章故事路徑另依本章經文閱讀。`,
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

  const finish = (number, study) => ({
    ...study,
    illustration: study.illustration || illustrationFor(number),
    prepare: study.prepare || [
      `完整閱讀撒母耳記下第 ${number} 章，圈出王權、約、罪、審判與恩典的敘事線索`,
      "沿地圖找出本章城市、山地、河谷與戰線，說明地理如何推動故事",
      "把本章放進「大衛之約—王的失敗—神仍守約」的全卷主線中",
      "選一條串珠全文並讀上下文，寫下一個敬畏、悔改或忠誠上的具體回應"
    ]
  });

  const studies = {};
  window.ONE_SAMUEL2 = { art, illustrationFor, mapDef, timeline, compare, finish, studies, mapRoutes };
})();
