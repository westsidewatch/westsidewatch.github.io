/* ONE runtime book supplements: Acts full-book first pass + Revelation 1–3 geography.
 * Kept here temporarily so the supplements execute before one-app.js without changing the canonical cover resolver order.
 */
(() => {
  "use strict";
  const D = window.ONE_DATA;
  if (!D) return;
  const HL = "https://biblegeography.holylight.org.tw";
  const mapBase = (id,title,places) => ({image:`${HL}/images/index/condensedbible/map/${id}.GIF`,imageTitle:title,source:`${HL}/index/condensedbible_map_detail?m_id=${id}`,places});
  const actMaps = {
    J:{...mapBase(112,"新圖二（112）新約時代的羅馬帝國",["耶路撒冷","猶太","撒瑪利亞","羅馬"]),bbox:"29.5,31,38,34.8",marker:"31.778,35.235"},
    P:{...mapBase(113,"徒圖一（113）五旬節時猶太人分佈各處情形",["耶路撒冷","帕提亞","瑪代","以攔","米所波大米","加帕多家","本都","亞西亞","埃及","羅馬","亞拉伯"]),bbox:"-12,24,65,48",marker:"31.778,35.235"},
    S:{...mapBase(114,"徒圖二（114）腓利和彼得傳道",["耶路撒冷","撒瑪利亞","迦薩","亞鎖都","呂大","約帕","該撒利亞"]),bbox:"31,31,36.5,33.4",marker:"32.0853,34.7818"},
    E:{...mapBase(115,"徒圖三（115）使徒到猶太省外傳道、保羅信主和早期工作",["耶路撒冷","大馬士革","該撒利亞","大數","安提阿","腓尼基","居比路"]),bbox:"30,32,38.5,37.5",marker:"33.5138,36.2765"},
    F:{...mapBase(116,"徒圖四（116）保羅第一次旅行傳道",["安提阿","西流基","撒拉米","帕弗","別加","彼西底安提阿","以哥念","路司得","特庇","亞大利"]),bbox:"29,34,37,37.5",marker:"36.2021,36.1607"},
    T:{...mapBase(117,"徒圖五（117）保羅第二次旅行傳道",["安提阿","路司得","特羅亞","腓立比","帖撒羅尼迦","庇哩亞","雅典","哥林多","以弗所"]),bbox:"20.5,36.2,39,42.8",marker:"40.6401,22.9444"},
    H:{...mapBase(118,"徒圖六（118）保羅第三次旅行傳道",["安提阿","以弗所","特羅亞","馬其頓","哥林多","米利都","推羅","該撒利亞","耶路撒冷"]),bbox:"20.5,31,38.5,42.8",marker:"37.9497,27.3639"},
    R:{...mapBase(119,"徒圖七（119）保羅被解押去羅馬",["耶路撒冷","該撒利亞","西頓","每拉","佳澳","米利大","敘拉古","部丟利","亞比烏市","三館","羅馬"]),bbox:"10,30,37,42.5",marker:"41.9028,12.4964"}
  };
  const mapRoutes={
    J:[["①","徒 1:1–8","复活的主以耶路撒冷、犹太、撒玛利亚直到地极建立整卷路线。"],["②","徒 1–7","福音首先在耶路撒冷公开见证，并在逼迫中增长。"]],
    P:[["①","徒 2:5–11","天下各国来的犹太人在耶路撒冷听见各地乡谈。"],["②","徒 2:14–41","彼得宣讲复活基督，约三千人受洗。"]],
    S:[["①","徒 8","腓利到撒玛利亚，并在往迦萨路上向埃提阿伯太监传福音。"],["②","徒 9:32–10:48","彼得经吕大、约帕到该撒利亚哥尼流家。"]],
    E:[["①","徒 9","扫罗往大马士革途中遇见主，再回耶路撒冷并经该撒利亚往大数。"],["②","徒 11","四散门徒到腓尼基、居比路、安提阿；巴拿巴到大数找扫罗。"]],
    F:[["①","徒 13","安提阿差派，经居比路进入小亚细亚。"],["②","徒 14","以哥念、路司得、特庇后原路坚固教会。"],["③","徒 15","为外邦信徒问题上耶路撒冷。"]],
    T:[["①","徒 16","经特罗亚进入马其顿，到腓立比。"],["②","徒 17","帖撒罗尼迦、庇哩亚、雅典。"],["③","徒 18","哥林多、以弗所并回程。"]],
    H:[["①","徒 19","以弗所长期教导。"],["②","徒 20","马其顿、希腊、特罗亚、米利都。"],["③","徒 21","沿海经推罗、该撒利亚回耶路撒冷。"]],
    R:[["①","徒 21–23","耶路撒冷被捕后送到该撒利亚。"],["②","徒 24–26","该撒利亚两年受审并上告凯撒。"],["③","徒 27","经革哩底遭风暴船难至米利大。"],["④","徒 28","经西西里、意大利南部抵达罗马。"]]
  };
  const rows = [
    [1,"升天、等候与见证使命","使徒行傳 1:1–26","耶路撒冷：复活主差遣门徒","复活的耶稣四十天向门徒显现，吩咐他们在耶路撒冷等候圣灵，并宣告要从耶路撒冷直到地极作见证。主升天后，众人同心祷告并补选马提亚。","J"],
    [2,"五旬节：圣灵降临与新群体","使徒行傳 2:1–47","耶路撒冷：万国乡谈听见福音","五旬节圣灵降临，门徒说起各地乡谈；彼得宣告耶稣已被神立为主、为基督。约三千人受洗，教会恒心遵守使徒教训、团契、擘饼和祈祷。","P"],
    [3,"美门医治与所罗门廊讲道","使徒行傳 3:1–26","耶路撒冷圣殿：耶稣的名使人站立","彼得和约翰奉耶稣基督的名使生来瘸腿的人站起。彼得把神迹指向被杀而复活的生命之主，并呼召群众悔改归正。","J"],
    [4,"不能不说：第一次公会冲突","使徒行傳 4:1–37","耶路撒冷：威吓中的放胆见证","彼得、约翰因传复活被捕，在公会前宣告除耶稣以外别无拯救；获释后教会同心祷告求放胆传道。","J"],
    [5,"圣洁、能力与使徒受逼迫","使徒行傳 5:1–42","耶路撒冷：教会内外都受主治理","亚拿尼亚、撒非喇事件显明群体圣洁；使徒被囚又蒙释放，在公会受打后仍欢喜不断传耶稣是基督。","J"],
    [6,"七人被立与司提反受控告","使徒行傳 6:1–15","耶路撒冷：道增长带来新的服事结构","寡妇供给争议促使教会设立七位有好名声、被圣灵和智慧充满的人；司提反大有恩惠能力，却被抓到公会。","J"],
    [7,"司提反的申诉与殉道","使徒行傳 7:1–60","耶路撒冷：殉道成为扩展转折","司提反从亚伯拉罕到圣殿重述以色列历史，指出百姓屡次抗拒神所差来的人；他看见人子站在神右边，并在被石打时为仇敌祈求。","J"],
    [8,"撒玛利亚与旷野路上的福音","使徒行傳 8:1–40","撒玛利亚与迦萨路：跨越族群边界","司提反殉道后门徒分散传道；腓利到撒玛利亚宣讲基督，又在往迦萨的路上向埃提阿伯太监解明以赛亚书并施洗。","S"],
    [9,"扫罗遇见主；彼得周流服事","使徒行傳 9:1–43","大马士革与沿海：逼迫者成为见证人","扫罗往大马士革途中遇见耶稣，从逼迫者转为传道人；彼得则在吕大和约帕服事，以尼雅得医治，多加从死里起来。","E"],
    [10,"哥尼流：外邦人的门被打开","使徒行傳 10:1–48","约帕到该撒利亚：神不偏待人","哥尼流蒙指示邀请彼得；彼得见大布异象后进入外邦人家，圣灵降在听道者身上，他们受洗归入基督。","S"],
    [11,"安提阿：门徒首次称为基督徒","使徒行傳 11:1–30","耶路撒冷到安提阿：外邦使命得到辨认","彼得向耶路撒冷解释哥尼流事件；福音传到安提阿，巴拿巴从大数找扫罗一同教导，门徒首次被称为基督徒。","E"],
    [12,"希律的手不能拦阻神的道","使徒行傳 12:1–25","耶路撒冷与该撒利亚：王权与神主权对照","希律杀雅各、囚彼得；教会切切祷告，彼得奇妙出监。希律后来受审判而死，神的道却日见兴旺。","E"],
    [13,"第一次旅行：圣灵差遣","使徒行傳 13:1–52","安提阿到居比路与彼西底","安提阿教会敬拜禁食时，圣灵差遣巴拿巴和扫罗；他们经居比路到彼西底安提阿，保罗从以色列历史宣讲复活的耶稣与赦罪称义。","F"],
    [14,"以哥念、路司得、特庇","使徒行傳 14:1–28","小亚细亚内陆：患难中建立教会","保罗、巴拿巴在以哥念、路司得、特庇传道，经历误拜、逼迫与石打；回程坚固门徒、设立长老，最后回安提阿报告使命。","F"],
    [15,"耶路撒冷会议与第二次差遣","使徒行傳 15:1–41","安提阿与耶路撒冷：恩典与共同体","割礼争议使使徒长老聚集，确认外邦人靠主耶稣的恩得救，不把不必要的律法重担加给他们；之后宣教队重新组合。","F"],
    [16,"马其顿异象、吕底亚与禁卒","使徒行傳 16:1–40","小亚细亚到马其顿：福音进入欧洲","圣灵引导保罗一行到特罗亚，看见马其顿异象后渡海到腓立比；吕底亚信主，保罗西拉下监后禁卒一家也信主受洗。","T"],
    [17,"帖撒罗尼迦、庇哩亚与雅典","使徒行傳 17:1–34","马其顿到雅典：福音面对城市思想世界","保罗在帖撒罗尼迦从圣经证明基督受害复活，庇哩亚人天天考查圣经；在雅典亚略巴古，他从创造主讲到悔改和复活。","T"],
    [18,"哥林多一年半与以弗所入口","使徒行傳 18:1–28","哥林多到以弗所：城市教会与同工网络","保罗在哥林多与亚居拉、百基拉同住作工并服事一年半；后来到以弗所，亚波罗也在那里受更准确的教导。","T"],
    [19,"以弗所：道大大兴旺而且得胜","使徒行傳 19:1–41","以弗所：福音触动宗教、经济与公共秩序","保罗在推喇奴学房长期教导，神的道广传；行邪术者焚书，银匠底米丢因亚底米相关生意受威胁而煽动全城骚乱。","H"],
    [20,"特罗亚到米利都：长老的眼泪与托付","使徒行傳 20:1–38","马其顿到特罗亚、米利都：回程中的牧养告别","保罗经过马其顿和希腊，在特罗亚聚会后沿岸到米利都，召以弗所长老告别，回顾流泪服事并把他们交托给神和祂恩惠的道。","H"],
    [21,"向耶路撒冷前行并被捕","使徒行傳 21:1–40","米利都到推罗、该撒利亚、耶路撒冷","保罗沿海回耶路撒冷，虽不断听见捆绑患难的预警仍前行；在圣殿被群众抓住，罗马千夫长介入救他脱离暴民。","H"],
    [22,"在暴民面前述说自己的蒙召","使徒行傳 22:1–30","耶路撒冷：用自己的故事作见证","保罗向群众述说自己从逼迫者到大马士革遇见耶稣、蒙召往外邦人去的经历；群众激怒时，他以罗马公民身份避免非法鞭打。","R"],
    [23,"公会冲突与夜送该撒利亚","使徒行傳 23:1–35","耶路撒冷到该撒利亚：主保守见证人前往罗马","保罗在公会因复活盼望引发争论；夜间主应许他也要在罗马作见证。杀害阴谋被揭露后，罗马军夜送他到该撒利亚。","R"],
    [24,"在腓力斯面前：公义、节制与审判","使徒行傳 24:1–27","该撒利亚：被囚中的福音辩护","保罗在腓力斯面前为自己辩护，强调复活盼望与无亏良心；腓力斯多次听道，却在公义、节制和将来审判面前恐惧。","R"],
    [25,"非斯都审案与上告凯撒","使徒行傳 25:1–27","该撒利亚：罗马法律成为去罗马的道路","非斯都上任后案件继续；保罗不愿被交回耶路撒冷，作为罗马公民正式上告凯撒，案件随后提交亚基帕王听审。","R"],
    [26,"在亚基帕面前：没有违背天上异象","使徒行傳 26:1–32","该撒利亚：王与官长听见复活见证","保罗述说自己的复活盼望、大马士革蒙召与外邦使命，宣告没有违背天上异象，只传摩西和先知所指向的受苦、复活之基督。","R"],
    [27,"风暴、船难与全船得保全","使徒行傳 27:1–44","该撒利亚到革哩底、米利大：海上危难中的见证","保罗作为囚犯被押往罗马，船遭友拉革罗狂风；在众人绝望时，他以神的应许鼓励全船，最终船毁而二百七十六人全部登岸得救。","R"],
    [28,"米利大到罗马：神的道不被禁止","使徒行傳 28:1–31","米利大到罗马：地理终点，使命仍未结束","保罗在米利大蒙保守并医治病人，之后经西西里与意大利南部抵达罗马；全书以他放胆传讲神国和主耶稣基督、并没有人禁止结束。","R"]
  ];
  const study=(n,title,passage,movement,story,key)=>({title,passage,movement,story,position:`第 ${n} 章位于徒 1:8 的扩展路线中。把本章的人物行动、城市移动与圣灵推动放在同一张地图上阅读。`,route:[[passage,title]],map:{...actMaps[key],title:`${title}｜地理路线`,reference:passage,guide:"按经文顺序定位人物移动，并观察福音如何跨越新的城市、族群或政治边界。",preface:"使徒行传的地图不是装饰，而是徒 1:8『耶路撒冷、犹太和撒玛利亚、直到地极』的叙事骨架。",routes:mapRoutes[key]},timeline:{title:`${title}｜使徒时代`,range:"约主后 30–62 年",note:"精确年代在部分事件上有讨论；ONE 以相对次序和公认的大致时段为主。",events:[["徒 1:8","从耶路撒冷直到地极","整卷使命骨架"],[passage,title,movement]],url:"https://bibleeveryone.com/bible-timeline.php"},background:[["圣灵与见证","教会扩展首先归因于圣灵的主动引导，而不是人的帝国式扩张。","地图上每一次边界突破都要与祷告、逼迫、异象、差遣或圣灵介入一起观察。"],["第一世纪地中海世界","路加大量保留真实城市、省份、道路、港口和罗马行政细节。","地理使神学见证落在可追踪的历史空间中。"],["复活核心","彼得到保罗都反复见证耶稣被杀、神使祂复活、如今掌权。","比较不同城市与听众，看同一福音如何被表达。"]],scout:["圣灵如何推动本章","见证中心句","跨越了哪一道地理或族群边界","反对为何出现","如何承接徒 1:8"],connections:[["使徒行传 1:8","整卷使命骨架","但圣灵降临在你们身上，你们就必得着能力；并要在耶路撒冷、犹太全地和撒玛利亚，直到地极，作我的见证。"],["路加福音 24:46–49","从耶路撒冷起直传万邦","基督必受害，第三日从死里复活，并且人要奉他的名传悔改、赦罪的道，从耶路撒冷起直传到万邦。"],["使徒行传 28:30–31","开放式结尾","保罗放胆传讲神国的道，将主耶稣基督的事教导人，并没有人禁止。"]],questions:["本章在徒 1:8 地图上跨越了什么边界？","人物如何分辨圣灵带领与人的计划？","复活见证受到什么抵抗？","本章对今天教会见证提出什么挑战？"],prepare:[`完整阅读使徒行传第 ${n} 章并在地图上标出地点`,`圈出圣灵、见证、道、复活或主名相关语句`,`与徒 1:8 并读，定位本章在整卷路线的位置`,`写下本章最关键的叙事转折`]});
  if(!D.acts){
    const chapterStudies=Object.fromEntries(rows.map(r=>[String(r[0]),study(...r)]));
    D.acts={number:44,code:"ACT",zhCode:"徒",enCode:"ACT",name:"使徒行傳",nameEn:"Acts",summary:"复活的主借着圣灵继续工作：见证从耶路撒冷出发，越过犹太、撒玛利亚、外邦人与帝国城市，直到罗马；全书以『并没有人禁止』留下继续向地极前行的开放结尾。",meta:[["位置","新约第 5 卷 · 第44卷"],["文体","历史叙事 · 宣教见证"],["章数","28章"],["核心线索","圣灵 · 见证 · 复活 · 道增长 · 从耶路撒冷到罗马"]],movements:[["01","1–7","耶路撒冷：圣灵建立见证群体"],["02","8–12","犹太、撒玛利亚与外邦人的门"],["03","13–15","第一次旅行与耶路撒冷会议"],["04","16–18","第二次旅行：进入马其顿与亚该亚"],["05","19–21","第三次旅行与返回耶路撒冷"],["06","22–26","被捕、受审与上告凯撒"],["07","27–28","风暴、米利大与抵达罗马"]],chapters:rows.map(r=>r[1]),chapterStudies,nowCards:[["使命","耶路撒冷 · 犹太 · 撒玛利亚 · 直到地极"],["动力","圣灵降临 · 复活见证 · 神的道兴旺"]]};
    D.studyBooks={...(D.studyBooks||{}),44:D.acts};
  }
  const R=D.revelation;
  if(R?.chapterStudies){
    const revBase={image:`${HL}/images/index/condensedbible/map/120.GIF`,imageTitle:"启图一（120）启示录：亚西亚七个教会",source:`${HL}/index/condensedbible_map_detail?m_id=120`,bbox:"26,36.5,29.5,40.5",places:["拔摩岛","以弗所","士每拿","别迦摩","推雅推喇","撒狄","非拉铁非","老底嘉"]};
    R.chapterStudies["1"].map={...revBase,title:"拔摩岛与亚西亚七教会",reference:"启示录 1:9–11",guide:"先定位约翰所在的拔摩岛，再看爱琴海东岸亚西亚七教会的真实位置。",preface:"第 1 章的异象是在真实地理与真实地方教会中领受的。",marker:"37.309,26.547",routes:[["①","启 1:9–11","约翰在拔摩岛领受命令，把所看见的写给七教会。"],["②","启 1:12–20","视野由地理背景转向行走在七个金灯台中间的基督。"]]};
    R.chapterStudies["2"].map={...revBase,title:"七教会北段：以弗所至推雅推喇",reference:"启示录 2:1–29",guide:"依次阅读以弗所、士每拿、别迦摩、推雅推喇，保留七教会全貌并突出前四城。",preface:"四封信针对真实城市处境，却都向众教会开放。",marker:"38.4192,27.1287",routes:[["①","启 2:1–7","以弗所"],["②","启 2:8–11","士每拿"],["③","启 2:12–17","别迦摩"],["④","启 2:18–29","推雅推喇"]]};
    R.chapterStudies["3"].map={...revBase,title:"七教会南东段：撒狄、非拉铁非、老底嘉",reference:"启示录 3:1–22",guide:"继续沿亚西亚内陆路线辨认撒狄、非拉铁非与老底嘉，使第 2–3 章构成连续地理回路。",preface:"第 4 章起进入天上与象征性异象空间，因此不再强制配置普通地理地图。",marker:"37.835,29.107",routes:[["①","启 3:1–6","撒狄"],["②","启 3:7–13","非拉铁非"],["③","启 3:14–22","老底嘉"]]};
  }
  document.documentElement.dataset.oneActs="complete-28-with-map-core";
  document.documentElement.dataset.revelationMaps="chapters-1-3";
})();

/* ONE Studio Fixed Asset Registry — NON-DORÉ, EDITORIALLY REPLACEABLE LIBRARY.
 * Doré originals are immutable; Studio assets are stable at runtime and versioned editorially.
 */
(() => {
  "use strict";
  const existing=window.ONE_STUDIO_ASSET_REGISTRY;if(existing?.mode==="ONE_STUDIO_VERSIONED_ASSETS")return;
  const assets=Object.create(null),chapterMap=Object.create(null),history=Object.create(null);
  const chapterKey=(book,chapter)=>`${String(Number(book))}:${String(Number(chapter))}`,now=()=>new Date().toISOString();
  const validateAsset=(id,asset)=>{if(!id||typeof id!=="string")throw new Error("ONE Studio asset id is required");if(!asset||typeof asset!=="object"||!asset.src)throw new Error(`Invalid ONE Studio asset: ${id}`);if(asset.doreId||asset.master==="ONE-DORE-241-MASTER-MAPPING")throw new Error(`ONE Studio asset ${id} must not contain Doré registry identity`);return true};
  const makeVersion=(id,asset,revision,previousId=null)=>Object.freeze({id,revision,previousId,src:asset.src,alt:asset.alt||"ONE Studio biblical illustration",title:asset.title||id,source:asset.source||"ONE Studio Fixed Asset",artist:asset.artist||"ONE Studio",origin:asset.origin||"ONE_STUDIO",status:"ACTIVE_FIXED",generatedOnce:true,replaceableByEditorialReview:true,palette:asset.palette||"MONOCHROME_ENGRAVING",scripture:asset.scripture||"",note:asset.note||"",approvedAt:asset.approvedAt||now(),master:"ONE-STUDIO-VERSIONED-ASSET-LIBRARY"});
  const registerAsset=(id,asset)=>{validateAsset(id,asset);if(assets[id])throw new Error(`ONE Studio asset id already exists: ${id}; use replaceAsset()`);const version=makeVersion(id,asset,1);assets[id]=version;history[id]=[version];return version};
  const replaceAsset=(id,asset,meta={})=>{validateAsset(id,asset);const current=assets[id];if(!current)throw new Error(`Unknown ONE Studio asset: ${id}; use registerAsset()`);const replacement=makeVersion(id,{...asset,note:meta.reason?`${asset.note||""}${asset.note?" · ":""}Replacement reason: ${meta.reason}`:asset.note},Number(current.revision||1)+1,id);assets[id]=replacement;history[id]=[...(history[id]||[]),replacement];return replacement};
  const registerChapter=(book,chapter,assetId,meta={})=>{const key=chapterKey(book,chapter);if(!assets[assetId])throw new Error(`Unknown ONE Studio fixed asset: ${assetId}`);if(chapterMap[key])throw new Error(`Chapter assignment already exists: ${key}; use reassignChapter()`);chapterMap[key]=Object.freeze({book:Number(book),chapter:Number(chapter),assetId,revision:1,priority:meta.priority||"P7_ONE_STUDIO_FIXED",basis:meta.basis||"SCRIPTURE_DERIVED_EDITORIALLY_APPROVED",assignedAt:now()});return chapterMap[key]};
  const reassignChapter=(book,chapter,assetId,meta={})=>{const key=chapterKey(book,chapter);if(!assets[assetId])throw new Error(`Unknown ONE Studio fixed asset: ${assetId}`);const current=chapterMap[key];chapterMap[key]=Object.freeze({book:Number(book),chapter:Number(chapter),assetId,revision:Number(current?.revision||0)+1,priority:meta.priority||current?.priority||"P7_ONE_STUDIO_FIXED",basis:meta.basis||"EDITORIAL_REPLACEMENT",reason:meta.reason||"",assignedAt:now()});return chapterMap[key]};
  const getAssignment=(book,chapter)=>chapterMap[chapterKey(book,chapter)]||null,getAsset=id=>assets[id]||null,getHistory=id=>Object.freeze([...(history[id]||[])]),resolve=(book,chapter)=>{const assignment=getAssignment(book,chapter);if(!assignment)return null;const asset=getAsset(assignment.assetId);return asset?{assignment,asset}:null};
  window.ONE_STUDIO_ASSET_REGISTRY=Object.freeze({mode:"ONE_STUDIO_VERSIONED_ASSETS",version:"2026-08-18-v11",doreAssetsAllowed:false,generatedAssetsAllowed:true,nonDoréHistoricalAssetsAllowed:true,runtimeReplacementAllowed:false,editorialReplacementAllowed:true,assets,chapterMap,registerAsset,replaceAsset,registerChapter,reassignChapter,getAsset,getAssignment,getHistory,resolve});
  registerAsset("REV-02-DORE-STUDIO-001",{src:"/one/studio/revelation-02-dore-final-full.png?v=20260818k",alt:"启示录第二章：基督在七灯台中间向教会说话，约翰俯伏在前",title:"Among the Lampstands",source:"/one/studio/revelation-02-dore-final-full.png?v=20260818k",artist:"Westside Watch Engraving Studio · Doré continuation",origin:"ONE_STUDIO_DORE_CONTINUATION",palette:"MONOCHROME_ENGRAVING",scripture:"Revelation 2:1–29",approvedAt:"2026-08-18",note:"Editorial FINAL FULL PNG. Canonical Revelation 2 artwork."});
  registerChapter(66,2,"REV-02-DORE-STUDIO-001",{priority:"P7_ONE_STUDIO_FIXED",basis:"EDITORIAL_FINAL_FULL_PNG"});
  registerAsset("OBA-01-DORE-STUDIO-002",{src:"/one/studio/obadiah-01-dore-studio-r2.png?v=31c0e72f3e17",alt:"Obadiah 1:1–21 · ONE Studio engraving",title:"From the Clefts of the Rock",source:"/one/studio/obadiah-01-dore-studio-r2.png?v=31c0e72f3e17",artist:"Westside Watch Engraving Studio · Doré continuation",origin:"ONE_STUDIO_DORE_CONTINUATION",palette:"MONOCHROME_ENGRAVING",scripture:"Obadiah 1:1–21",approvedAt:"2026-08-21",note:"Editorially approved Doré-continuation Studio plate. SHA-256 31c0e72f3e1728fbb9be55df5241f5e69e6ea9d7ccdb2f2572809a357fd44da4; 3521988 bytes."});
  registerChapter(31,1,"OBA-01-DORE-STUDIO-002",{priority:"P7_ONE_STUDIO_FIXED",basis:"EDITORIAL_FINAL_NATIVE_BINARY"});
  document.documentElement.dataset.oneStudioAssets="separate-versioned-library";
})();
