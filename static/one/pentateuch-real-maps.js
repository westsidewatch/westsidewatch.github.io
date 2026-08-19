/* ONE Pentateuch real-map correction.
 * Replaces placeholder geography objects with actual Holy Light Bible Geography map assets.
 * Maps appear only where geography materially helps the chapter.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  if(!D?.studyBooks)return;
  const HL="https://biblegeography.holylight.org.tw";
  const asset=(id,imageTitle,routes=[])=>({
    mapId:id,
    image:`${HL}/images/index/condensedbible/map/${String(id).padStart(3,"0")}.GIF`,
    imageTitle,
    source:`${HL}/index/condensedbible_map_detail?m_id=${String(id).padStart(3,"0")}`,
    routes:routes.map(r=>[...r]),
    routeCount:routes.length,
    routeLegendVerified:true
  });
  const A={
    18:asset(18,"出圖一（018）摩西早年",[
      ["①","出 2:11–22","摩西逃往米甸並成家。"],
      ["②","出 3:1–4:17","摩西在何烈山蒙召。"],
      ["③","出 4:18–26","摩西一家啟程回埃及，到了何烈山。"],
      ["④","出 4:27–31","亞倫到何烈山迎接摩西，一同回埃及。"]
    ]),
    19:asset(19,"出圖二（019）以色列人出埃及到西乃山",[
      ["①","出 12:37","蘭塞 → 疏割。"],["②","出 13:20","疏割 → 以倘。"],["③","出 14:2","轉回到比哈希錄、密奪與海之間。"],["④","出 14:21–22；15:20","過海後在曠野行三天到瑪拉。"],["⑤","出 15:27","瑪拉 → 以琳。"],["⑥","出 16:1","以琳 → 汛的曠野。"],["⑦","出 17:1","汛 → 利非訂。"],["⑧","出 17:8–16","亞瑪力人在利非訂攻擊以色列。"],["⑨","出 18:1–5","葉忒羅由米甸來到摩西處。"],["⑩","出 19:1","利非訂 → 西乃曠野。"]
    ]),
    20:asset(20,"民圖一（020）從西乃山到加低斯",[["①","民 10:11–12:16","自西乃山到巴蘭曠野。"]]),
    21:asset(21,"民圖二（021）探看應許地和應許地之範圍",[
      ["①","民 13:17–29","十二探子從南地直到哈馬口窺探迦南。"],
      ["②","民 14:43–44","百姓擅自攻打迦南人而失敗。"]
    ]),
    22:asset(22,"民圖三（022）從何珥山到摩押平原",[
      ["①","民 20:22","加低斯 → 何珥山，亞倫去世。"],["②","民 21:1–3","南地迦南人攻擊以色列而被擊敗。"],["③","民 21:10","經阿伯、以耶亞巴琳到撒烈谷；路線有不同重建方案。"],["④","民 21:13–20","過亞嫩河，經摩押地到毘斯迦山頂。"],["⑤","民 21:21–32","擊敗亞摩利王西宏。"],["⑥","民 21:33–22:1","擊敗巴珊王噩後到摩押平原。"]
    ]),
    23:asset(23,"民圖四（023）分地給兩個半支派",[]),
    24:asset(24,"民圖五（024）出埃及和進迦南的旅程",[
      ["①","民 33:5–15","出埃及到西乃山。"],["②","民 33:16–36","西乃山到加低斯。"],["③","民 33:41–44","何珥山到以耶亞巴琳。"],["④","民 33:45–49","以耶亞巴琳到亞伯什亭。"]
    ]),
    25:asset(25,"申圖一（025）應許之地全圖",[]),
    26:asset(26,"申圖二（026）進迦南和分地給兩個半支派",[
      ["①","申 1:19","何烈山 → 加低斯巴尼亞。"],["②","申 2:8–13","由西珥、亞拉巴、以旬迦別繞向摩押曠野到撒烈溪。"],["③","申 2:16–19","撒烈溪 → 摩押 → 亞嫩谷。"],["④","申 2:24–36","擊敗希實本王西宏。"],["⑤","申 3:1–11","擊敗巴珊王噩。"]
    ]),
    27:asset(27,"申圖三（027）摩西觀看迦南地後去世和埋葬",[])
  };
  const set=(bookNumber,chapter,id,title,guide,places=[])=>{
    const study=D.studyBooks?.[bookNumber]?.chapterStudies?.[String(chapter)];
    if(!study)return;
    study.map={...A[id],reference:`${D.studyBooks[bookNumber].name} ${chapter}`,title,guide,places,preface:"採用聖光聖經地理原圖；地圖只在能直接幫助理解本章地理時出現，並保留原圖完整路線圖例。"};
  };
  const clear=(bookNumber,chapters)=>chapters.forEach(ch=>{const s=D.studyBooks?.[bookNumber]?.chapterStudies?.[String(ch)];if(s)delete s.map;});

  // Exodus: 018 is the real early-Moses map; 019 is the real Exodus-to-Sinai map.
  for(let ch=1;ch<=12;ch++)set(2,ch,18,"摩西早年與埃及背景","從埃及、米甸、何烈山到回埃及，辨認出埃及事件發生前的地理骨架。",["埃及","米甸","何烈山"]);
  for(let ch=13;ch<=40;ch++)set(2,ch,19,"從埃及到西乃山","沿蘭塞、疏割、以倘、過海、瑪拉、以琳、汛、利非訂直到西乃山，理解出埃及與立約的空間進程。",["蘭塞","疏割","以倘","比哈希錄","瑪拉","以琳","汛的曠野","利非訂","西乃山"]);

  // Leviticus is stationary legislation at Sinai; a repeated travel map is misleading, so omit it.
  clear(3,Array.from({length:27},(_,i)=>i+1));

  // Numbers: use the five canonical Numbers maps by narrative movement, not a generic placeholder.
  for(let ch=1;ch<=12;ch++)set(4,ch,20,"從西乃山到加低斯","西乃營地完成編組後開始起行，地圖顯示從西乃到巴蘭曠野的實際路程。",["西乃山","巴蘭曠野","哈洗錄","加低斯"]);
  [13,14].forEach(ch=>set(4,ch,21,"探看應許地","十二探子由南地向北窺探迦南，再返回加低斯。",["加低斯","南地","希伯崙","哈馬口"]));
  clear(4,[15,16,17,18,19]);
  [20,21].forEach(ch=>set(4,ch,22,"從何珥山到摩押平原","結束曠野漂流後，以色列繞過以東、越過亞嫩河並進至摩押平原。",["加低斯","何珥山","以東","亞嫩河","希實本","摩押平原"]));
  for(let ch=22;ch<=32;ch++)set(4,ch,23,"摩押平原與河東分地","巴蘭事件、第二次數點、米甸戰事與兩個半支派分地都以摩押平原和河東為主要背景。",["摩押平原","亞嫩河","基列","巴珊"]);
  set(4,33,24,"出埃及到迦南的四十二站","民數記 33 章以全程站口回顧從埃及到摩押平原的道路。",["埃及","西乃山","加低斯","何珥山","摩押平原"]);
  set(4,34,21,"應許地的範圍","配合民 34 的疆界規定，使用同時標示應許地範圍的民圖二。",["迦南","南地","地中海","約但河"]);
  clear(4,[35,36]);

  // Deuteronomy: maps only for geographical retrospection, the land itself, and Moses' final ascent.
  for(let ch=1;ch<=4;ch++)set(5,ch,26,"重述從何烈山到摩押平原","申命記開篇回顧何烈山、加低斯、曠野與河東征戰。",["何烈山","加低斯","以東","摩押","亞嫩谷","巴珊"]);
  clear(5,[5,6,7,8,9,10]);
  set(5,11,25,"應許之地全圖","摩西描述即將進入之地及其疆域，以全圖建立地理背景。",["迦南","利巴嫩","南地","地中海","約但河"]);
  clear(5,Array.from({length:15},(_,i)=>i+12));
  set(5,27,26,"以巴路山與基利心山的立約儀式","申圖二的說明直接連結申 27 的以巴路山、基利心山祝福與咒詛。",["以巴路山","基利心山","約但河"]);
  set(5,28,25,"應許之地與盟約祝福","本章祝福與咒詛以居住在應許地為背景，因此只保留應許地全圖。",["應許之地"]);
  [29,30,31].forEach(ch=>set(5,ch,25,"摩押平原面向應許之地","摩西在約但河東重申盟約，百姓面向將要進入的應許地。",["摩押平原","約但河","迦南"]));
  [32,33,34].forEach(ch=>set(5,ch,27,"尼波山與摩西最後的觀看","摩西最後登尼波山觀看迦南，去世並被葬在摩押地。",["摩押平原","尼波山","耶利哥","迦南"]));

  window.ONE_PENTATEUCH_REAL_MAPS_READY=true;
  document.documentElement.dataset.pentateuchMaps="holylight-018-027-canonical";
})();
