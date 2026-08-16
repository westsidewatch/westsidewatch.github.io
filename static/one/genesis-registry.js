/* 創世記 ONE：開卷註冊、完整性保護與聖光地圖綁定
 * 必須在 genesis-core 與所有分章資料載入完成後、one-map-catalog / one-app 之前執行。
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const genesis=D?.genesis;
  if(!D||!genesis)return;

  const expected=D.books?.find(book=>book[0]===1)?.[3]||50;
  const studies=genesis.chapterStudies||{};
  const chapters=Array.from({length:expected},(_,index)=>{
    const number=index+1;
    return studies[String(number)]?.title||`第 ${number} 章`;
  });

  genesis.number=1;
  genesis.code="GEN";
  genesis.zhCode="GEN";
  genesis.enCode="GEN";
  genesis.name="創世記";
  genesis.nameEn="Genesis";
  genesis.chapters=chapters;
  genesis.summary=genesis.summary||"創世記從創造、墮落與洪水，進入亞伯拉罕、以撒、雅各與約瑟的故事；神以後裔、土地、祝福與約展開救贖歷史的起點。";
  genesis.meta=genesis.meta||[["位置","舊約第一卷 · 第01卷"],["文體","律法書 · 起源與族長敘事"],["章數","50章"],["核心線索","創造 · 後裔 · 土地 · 祝福 · 約 · 神的護理"]];
  genesis.nowCards=genesis.nowCards||[["主線","創造 · 墮落 · 應許 · 族長 · 約瑟"],["辨別","後裔 · 土地 · 祝福 · 約 · 神同在"]];

  const map=(id,title,routes=[])=>({
    id,title,
    source:`https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${String(id).padStart(3,"0")}`,
    image:`https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${String(id).padStart(3,"0")}.GIF`,
    routes
  });
  const maps={
    6:map(6,"創圖一（006）伊甸和洪水之前之地"),
    7:map(7,"創圖二（007）挪亞後代的國族圖"),
    8:map(8,"創圖三（008）族長們在迦南地以外之活動",[
      ["①","創 11:27–12:9","亞伯蘭離開吾珥，經哈蘭進入迦南。"],
      ["②","創 12:10–13:3","亞伯拉罕因饑荒下埃及，之後返回迦南。"],
      ["③","創 14:1–5","北方四王南下攻打南方五王。"],
      ["④","創 24","亞伯拉罕差僕人往米所波大米為以撒娶妻。"],
      ["⑤","創 25:6","亞伯拉罕打發庶子往東方居住。"],
      ["⑥","創 25:17–18","以實瑪利後裔分布於東方地區。"],
      ["⑦","創 27:43–31:21","雅各往哈蘭，後攜眷返回迦南。"],
      ["⑧","創 37:12–28","約瑟在多坍被賣，隨商隊下埃及。"],
      ["⑨","創 46:1–47:12","雅各全家遷往埃及並定居歌珊。"],
      ["⑩","創 50","雅各遺體由埃及運回希伯崙安葬。"]
    ]),
    9:map(9,"創圖四（009）亞伯拉罕的生平",[
      ["①","創 12:5","亞伯蘭從吾珥經哈蘭到迦南。"],
      ["②","創 12:6–9","亞伯蘭到示劍，再到伯特利與艾之間，漸往南地。"],
      ["③","創 12:10–13:1","亞伯蘭因饑荒往埃及，之後回南地。"],
      ["④","創 13:3–13","亞伯蘭回伯特利，羅得在此與他分開。"],
      ["⑤","創 13:18","亞伯蘭遷往希伯崙居住。"],
      ["⑥","創 20","亞伯拉罕遷往基拉耳，後來再回希伯崙。"]
    ]),
    10:map(10,"創圖五（010）羅得和他的後代——摩押和亞捫",[
      ["①","創 13:4–13","羅得離開亞伯蘭往東遷移，直到所多瑪。"],
      ["②","創 19:1–14","天使從希伯崙方向到所多瑪，羅得接待天使。"],
      ["③","創 19:15–22","羅得一家逃出所多瑪，前往瑣珥。"],
      ["④","創 18:30–19:38；申 2:10–21","羅得後裔摩押、亞捫後來形成兩個民族。"]
    ]),
    11:map(11,"創圖六（011）北方四王攻打南方五王",[
      ["①","創 14:1–4","北方四王南征，沿途攻擊利乏音人和蘇西人。"],
      ["②","創 14:6","聯軍擊敗以米人和何利人。"],
      ["③","創 14:7","聯軍擊敗亞瑪力人和亞摩利人。"],
      ["④","創 14:8","聯軍在西訂谷擊敗南方五王。"],
      ["⑤","創 14:11–12","聯軍掠走五城財物並擄去羅得一家。"],
      ["⑥","創 14:13–16","亞伯蘭北追四王，救回羅得與財物。"]
    ]),
    12:map(12,"創圖七（012）夏甲和以實瑪利",[
      ["①","創 16","夏甲逃到書珥路曠野，蒙神使者指示後返回亞伯蘭家。"],
      ["②","創 21:14–21","夏甲與以實瑪利離家，在別是巴曠野蒙眷顧，後到巴蘭曠野。"]
    ]),
    13:map(13,"創圖八（013）以撒的生平",[
      ["①","創 22:1–20","亞伯拉罕帶以撒前往摩利亞獻祭，後返回別是巴。"],
      ["②","創 24","亞伯拉罕僕人往拿鶴城為以撒娶回利百加。"],
      ["③","創 25:11","以撒遷往庇耳拉海萊附近居住。"],
      ["④","創 26","以撒往基拉耳，經井爭後在別是巴立約。"]
    ]),
    14:map(14,"創圖九（014）雅各的生平",[
      ["①","創 27:43–29:1","雅各逃往哈蘭，在哈蘭成家。"],
      ["②","創 31:3–32:1","雅各攜眷離開哈蘭返回迦南。"],
      ["③","創 33:1–16","以掃從西珥前來與雅各相會。"],
      ["④","創 33:17–35:27","雅各經疏割、示劍、伯特利，最後到希伯崙。"],
      ["⑤","創 46:1–7；47:11–12","雅各全家遷往埃及並住在歌珊。"]
    ]),
    15:map(15,"創圖十（015）以掃的生平、以東、亞瑪力和米甸"),
    16:map(16,"創圖十一（016）約瑟和猶大的生平",[
      ["①","創 37:13","約瑟從父家經示劍到多坍尋找兄長。"],
      ["②","創 37:25–36","約瑟被商人從多坍帶往埃及，賣給波提乏。"],
      ["③","創 38","猶大離開弟兄，在亞杜蘭、亭拿一帶活動。"],
      ["④","創 46:1–47:12","約瑟接雅各全家進埃及並定居歌珊。"],
      ["⑤","創 50:7–14","約瑟將雅各遺體從埃及運回希伯崙安葬。"]
    ])
  };

  const mapPlan={
    2:6,3:6,4:6,6:6,7:6,8:6,9:7,10:7,11:7,
    12:9,13:10,14:11,15:9,16:12,17:9,18:9,19:10,20:9,21:12,22:13,23:9,24:13,25:8,26:13,
    27:14,28:14,29:14,30:14,31:14,32:14,33:14,34:14,35:14,36:15,
    37:16,38:16,39:16,40:16,41:16,42:16,43:16,44:16,45:16,46:16,47:16,48:14,49:16,50:16
  };
  Object.entries(mapPlan).forEach(([chapter,id])=>{
    const study=studies[chapter],catalog=maps[id];
    if(!study?.map||!catalog)return;
    study.map.mapId=id;
    study.map.source=catalog.source;
    study.map.image=catalog.image;
    study.map.imageTitle=catalog.title;
    study.map.routes=catalog.routes.map(route=>[...route]);
    study.map.routeCount=catalog.routes.length;
    study.map.routeLegendVerified=true;
  });

  /* Book availability is determined by the actual study object, not by optional audits. */
  D.studyBooks={...(D.studyBooks||{}),1:genesis};

  const missing=[];
  for(let number=1;number<=expected;number+=1){
    if(!studies[String(number)])missing.push(number);
  }
  const mapErrors=[];
  Object.entries(mapPlan).forEach(([chapter,id])=>{
    const study=studies[chapter],catalog=maps[id];
    if(!study?.map)return mapErrors.push(`${chapter}:no-map`);
    const routes=Array.isArray(study.map.routes)?study.map.routes:[];
    if(routes.length!==catalog.routes.length)mapErrors.push(`${chapter}:${routes.length}/${catalog.routes.length}`);
    if(!study.map.image||!study.map.source)mapErrors.push(`${chapter}:missing-source`);
  });

  const allReady=missing.length===0;
  document.documentElement.dataset.genesisReady=allReady?"true":"partial";
  document.documentElement.dataset.genesisChapterCount=String(Object.keys(studies).filter(key=>/^\d+$/.test(key)).length);
  document.documentElement.dataset.genesisMapAudit=mapErrors.length?mapErrors.join("|"):"ok";
  if(missing.length)console.error(`[ONE Genesis] missing chapter studies: ${missing.join(", ")}`);
  if(mapErrors.length)console.warn(`[ONE Genesis] map audit warning: ${mapErrors.join(", ")}`);

  document.addEventListener("DOMContentLoaded",()=>{
    const item=document.querySelector('.cover-book[data-book="1"]');
    if(!item)return;
    const available=Boolean(D.studyBooks?.[1]);
    item.classList.toggle("has-study",available);
    item.classList.toggle("forthcoming",!available);
    item.setAttribute("aria-label",available?"第 1 卷，創世記，可開始查考":"第 1 卷，創世記，資料尚未載入");
  });
})();
