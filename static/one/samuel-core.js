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

  // Complete numbered route legends from Holy Light maps 046–054.
  // Chapter-level study.route remains the story path for that chapter; it must not replace the map legend.
  const mapRoutes = {
    46: [
      ["1", "撒上 1:19–2:11；3:19–21", "撒母耳在拉瑪出生，斷奶後到示羅事奉；後來耶和華立他為先知。"],
      ["2", "撒上 4:1–4", "以色列在以便以謝附近敗給非利士人，從示羅把約櫃運到戰場。"],
      ["3", "撒上 4:10–11；5:1–12", "約櫃被擄，依次到亞實突、迦特、以革倫，非利士各城遭災。"],
      ["4", "撒上 6:1–16", "非利士人把約櫃送回，以牛車運到伯示麥。"],
      ["5", "撒上 6:19–7:2", "伯示麥人受擊打後，約櫃被迎到基列耶琳長期停留。"],
      ["6", "撒上 7:5–14", "以色列人在米斯巴聚集；非利士來攻卻敗退，以色列收復失地。"],
      ["7", "撒上 7:15–17", "撒母耳每年巡行伯特利、吉甲、米斯巴，再回拉瑪。"]
    ],
    47: [
      ["1", "撒上 9:3–10:8", "掃羅尋驢來到拉瑪，撒母耳膏他作王。"],
      ["2", "撒上 10:9–16", "掃羅回到基比亞，神的靈感動他在先知中受感說話。"],
      ["3", "撒上 10:17–24", "百姓在米斯巴聚集，抽籤選出掃羅為王。"]
    ],
    48: [
      ["1", "撒上 11:1–5", "基列雅比受亞捫威脅，向掃羅求援。"],
      ["2", "撒上 11:6–8", "掃羅召集以色列眾支派，在比色集結。"],
      ["3", "撒上 11:11；11:14", "掃羅分三隊擊潰亞捫人，之後在吉甲再次確認王位。"]
    ],
    49: [
      ["1", "撒上 13:3–4", "約拿單攻擊迦巴的非利士防營，掃羅召集以色列人。"],
      ["2", "撒上 13:4", "戰局逆轉後，掃羅從伯特利山與密抹一帶退到吉甲。"],
      ["3", "撒上 13:5–7", "非利士大軍到密抹，以色列人四散，部分逃往約但河東。"],
      ["4", "撒上 13:15–16", "掃羅離開吉甲回基比亞，與約拿單在迦巴一帶駐軍。"],
      ["5", "撒上 13:17–18", "非利士從密抹派出三隊掠兵。"],
      ["6", "撒上 14:1–14", "約拿單越過隘口突擊密抹的非利士防營，引發潰亂。"],
      ["7", "撒上 14:18", "掃羅與重新聚集的以色列人追擊非利士人直到伯亞文。"],
      ["8", "撒上 14:31", "以色列人繼續追擊至亞雅崙。"]
    ],
    50: [],
    51: [
      ["1", "撒上 15:1–9", "掃羅率軍南下攻擊亞瑪力人。"],
      ["2", "撒上 15:10–31", "掃羅帶戰利品經迦密回吉甲，在吉甲受撒母耳責備。"],
      ["3", "撒上 17:1–51", "非利士與以色列在以拉谷對陣，大衛擊殺歌利亞。"],
      ["4", "撒上 17:51–53", "以色列人乘勝追擊非利士人，直到以革倫與迦特方向。"]
    ],
    52: [
      ["1", "撒上 18:10–24；19:18–24", "掃羅屢次要害大衛；大衛最後逃到拉瑪見撒母耳。"],
      ["2", "撒上 21:1–9", "大衛到挪伯，從祭司亞希米勒得到聖餅與歌利亞的刀。"],
      ["3", "撒上 21:10–15", "大衛逃到迦特投靠亞吉。"],
      ["4", "撒上 22:1–3", "大衛離開迦特，藏身亞杜蘭洞，家人與追隨者前來投靠。"],
      ["5", "撒上 22:3–5", "大衛把父母送往摩押的米斯巴。"],
      ["6", "撒上 22:5", "大衛由摩押返回猶大，進入哈烈樹林。"],
      ["7", "撒上 23:1–5", "大衛前往基伊拉，解救受非利士攻擊的城。"],
      ["8", "撒上 23:7–14", "掃羅準備圍攻基伊拉，大衛轉入西弗曠野。"],
      ["9", "撒上 23:24–24:7；26:6–12", "大衛在西弗、瑪雲、隱基底等曠野山地躲避掃羅，兩次有機會卻不殺掃羅。"],
      ["10", "撒上 27:3–6", "大衛再次投靠迦特王亞吉，得到洗革拉。"],
      ["11", "撒上 27:7", "大衛以洗革拉為基地居住一年四個月。"]
    ],
    53: [
      ["1", "撒上 27:7–9", "大衛住洗革拉期間，攻擊南方基述人、基色人和亞瑪力人。"],
      ["2", "撒上 27:10–12", "大衛向亞吉報稱自己攻擊的是猶大與其南方盟族地區。"],
      ["3", "撒上 28:1–2；29:1–11", "大衛隨非利士軍到亞弗，但因不受信任被遣回洗革拉。"],
      ["4", "撒上 30:1–3、14", "亞瑪力人趁大衛不在時侵襲南地並焚毀洗革拉，擄走居民。"],
      ["5", "撒上 30:9–20", "大衛追上亞瑪力人，救回被擄者並奪回財物。"]
    ],
    54: [
      ["1", "撒上 31:1–6", "非利士人在基利波山擊敗以色列，掃羅與三子戰死。"],
      ["2", "撒上 28:5–25", "決戰前夜，掃羅繞過敵軍防區前往隱多珥求問交鬼婦人。"],
      ["3", "撒上 31:10–13", "掃羅等人的屍身被掛在伯珊；基列雅比勇士連夜取回安葬。"]
    ]
  };

  const mapDef = (id, title, places, bbox, marker, reference, guide) => ({
    image: `https://biblegeography.holylight.org.tw/images/index/condensedbible/map_thumbs/${String(id).padStart(3, "0")}.jpg`,
    imageTitle: `撒上圖 · ${title}`,
    source: `https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${String(id).padStart(3, "0")}`,
    mapId: id,
    routes: mapRoutes[id] || [],
    preface: mapRoutes[id]?.length ? `本段為聖光地圖 ${String(id).padStart(3, "0")} 的完整編號路線；本章故事路徑另依本章經文閱讀。` : "本圖為疆域總覽，聖光原圖沒有編號路線。",
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

  const finish = (number, study) => ({
    ...study,
    prepare: study.prepare || [
      `完整閱讀撒母耳記上第 ${number} 章，圈出「耶和華說／問耶和華／耶和華與他同在」等敘事線索`,
      "沿地圖找出本章城市、山地、曠野與戰線，說明地理如何推動故事",
      "把本章放進「神作王—先知說話—君王聽命」的全卷主線中",
      "選一條串珠全文並讀上下文，寫下一個順服上的具體回應"
    ]
  });

  const studies = {};
  window.ONE_SAMUEL = { art, mapDef, timeline, compare, finish, studies, mapRoutes };
})();
