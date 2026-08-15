/* Restore the chapter-level chronology that was lost when Matthew data was split. */
(() => {
  "use strict";
  const D = window.ONE_DATA;
  const studies = D?.matthew?.chapterStudies;
  if (!studies) return;

  const timelineUrl = "https://bibleeveryone.com/bible-timeline.php";

  if (studies["1"]) studies["1"].timeline = {
    title: "應許進入歷史",
    range: "馬太福音 1:1–25",
    note: "從亞伯拉罕的應許，經出埃及、大衛王朝與猶大被擄，抵達彌賽亞的降生。",
    url: timelineUrl,
    events: [
      ["族長時期", "亞伯拉罕蒙召", "創 12:1–3 · 太 1:1–2"],
      ["出埃及時期", "出埃及與西奈之約", "出 12–20"],
      ["約主前 1000 年", "大衛王朝", "撒下 7:12–16 · 太 1:6"],
      ["主前 586 年", "猶大被擄", "王下 25 · 太 1:11–12"],
      ["約主前 5–4 年", "耶穌降生", "太 1:18–25"]
    ]
  };

  if (studies["2"]) studies["2"].timeline = {
    title: "君王與出埃及的回聲",
    range: "馬太福音 2:1–23",
    note: "耶穌幼年的逃亡與歸回被馬太放在以色列出埃及的歷史回聲中。",
    url: "https://bibleeveryone.com/jesus-trip1.php",
    events: [
      ["出埃及時期", "以色列出埃及", "出 12–14 · 何 11:1"],
      ["約主前 5–4 年", "博士抵達耶路撒冷", "太 2:1–8"],
      ["約主前 5–4 年", "在伯利恆敬拜", "太 2:9–12"],
      ["約主前 4 年", "逃往埃及", "太 2:13–15"],
      ["希律死後", "回到拿撒勒", "太 2:19–23"]
    ]
  };

  if (studies["3"]) studies["3"].timeline = {
    title: "曠野中的起點",
    range: "馬太福音 3:1–17",
    note: "從出埃及後的曠野傳統到約旦河，約翰預備道路，耶穌受洗開始公開事奉。",
    url: "https://bibleeveryone.com/jesus-trip2.php",
    events: [
      ["出埃及之後", "以色列經過曠野", "出 16–申 8"],
      ["約主後 26 年", "約翰在曠野傳道", "太 3:1–6"],
      ["約主後 26 年", "悔改的呼召", "太 3:7–12"],
      ["約主後 26–27 年", "耶穌來到約旦河", "太 3:13–15"],
      ["約主後 26–27 年", "耶穌受洗", "太 3:16–17"]
    ]
  };
})();

/* Genesis bootstrap.
 * index.html loads one-chronology.js immediately after one-data.js and before one-app.js.
 * Keep Genesis in that parser-blocking window so the full 50 chapters are registered before
 * ONE decides which books are available. This prevents the previous "data exists but cannot open"
 * failure mode. The registry validates the full chapter set before exposing Book 01.
 */
(() => {
  "use strict";
  if(document.documentElement.dataset.genesisLoader)return;
  document.documentElement.dataset.genesisLoader="true";
  const version="20260815b";
  const files=[
    "genesis-core.js",
    "genesis-5-8.js",
    "genesis-9-12.js",
    "genesis-13-16.js",
    "genesis-17-20.js",
    "genesis-21-24.js",
    "genesis-25-28.js",
    "genesis-29-32.js",
    "genesis-33-36.js",
    "genesis-37-40.js",
    "genesis-41-44.js",
    "genesis-45-48.js",
    "genesis-49-50.js",
    "genesis-registry.js"
  ];
  document.write(files.map(file=>`<script src="./${file}?v=${version}"><\\/script>`).join(""));
})();
