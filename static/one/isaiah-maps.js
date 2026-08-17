/* Isaiah maps: geography where it materially aids reading; no forced map per chapter. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const holy=(id,title,note)=>({mapId:id,title,note,source:`https://biblegeography.holylight.org.tw/index/condensedbible_map_detail?m_id=${id}`,image:`https://biblegeography.holylight.org.tw/images/index/condensedbible/map/${id}.GIF`,imageTitle:title,routes:[]});
  const maps={
    crisis:holy(75,"亞蘭、以色列與猶大：主前八世紀的危機","閱讀賽 7–12 時，先定位耶路撒冷、北國以色列／撒馬利亞、大馬士革與亞述；重點是猶大夾在區域聯盟與亞述帝國之間。"),
    nations:holy(76,"以賽亞時代的列國與亞述勢力","賽 13–23 的默示跨越巴比倫、摩押、大馬士革、古實、埃及、以東、亞拉伯、推羅與西頓；地圖用來建立列國彼此位置，不把默示誤讀成單一路線。"),
    assyria:holy(77,"亞述進攻猶大與耶路撒冷","閱讀賽 28–37，特別注意亞述由北方與沿海平原南下、拉吉與耶路撒冷的位置，以及猶大向埃及求援的地理背景。"),
    exile:holy(84,"猶大、巴比倫與被擄方向","賽 39–48 從希西家時代轉向巴比倫被擄與歸回的先知視野；地圖幫助理解耶路撒冷、巴比倫與帝國道路的距離。"),
    return:holy(91,"巴比倫歸回耶路撒冷","閱讀賽 40–55 的『預備道路』『出巴比倫』與古列背景時使用；這是歸回的大尺度地理框架，不把詩性語言縮成一條精確行軍線。"),
    edom:holy(93,"以東、波斯拉與錫安","賽 63 的守望視野從以東／波斯拉轉向錫安；地圖只用於定位，不把象徵性的審判圖像當作歷史旅行記錄。")
  };
  const assign=(chapters,map)=>chapters.forEach(n=>{const s=I.chapterStudies[String(n)];if(s)s.map={...map};});
  assign([7,8,9,10,11,12],maps.crisis);
  assign([13,14,15,16,17,18,19,20,21,22,23],maps.nations);
  assign([28,29,30,31,32,33,34,35,36,37],maps.assyria);
  assign([39,40,41,42,43,44,45,46,47,48],maps.exile);
  assign([49,50,51,52,53,54,55],maps.return);
  assign([63],maps.edom);
  I.mapPolicy={rule:"只在地理、帝國關係、戰爭或遷徙能實質幫助理解時配置地圖；同一歷史單元共享地圖。詩性／神學章節不為形式完整而硬加地圖。",mappedChapters:[7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,28,29,30,31,32,33,34,35,36,37,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,63]};
})();