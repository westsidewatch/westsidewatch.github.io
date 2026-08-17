/* 詩篇 ONE：第 1–25 篇插圖。只使用可確認的舊約 Gustave Doré 作品；不使用新約圖，不設 fallback。 */
(() => {
  "use strict";
  const P=window.ONE_DATA?.psalms;if(!P)return;
  const commons=(file,title,alt)=>({
    src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
    source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
    title,alt:`古斯塔夫・多雷版畫：${alt||title}`,artist:"Gustave Doré",testament:"OT"
  });
  const art={
    goliath:commons("071A.David Slays Goliath.jpg","大衛擊殺歌利亞","大衛與歌利亞"),
    saul:commons("072.Saul Attempts to Kill David.jpg","掃羅企圖殺大衛","大衛在掃羅逼迫之下"),
    escape:commons("073.David Escapes through a Window.jpg","大衛從窗戶逃走","大衛逃避追殺"),
    jonathan:commons("073A.David and Jonathan.jpg","大衛與約拿單","大衛與約拿單"),
    spared:commons("074.David Shows Saul How He Spared His Life.jpg","大衛向掃羅表明自己曾饒他性命","大衛把伸冤交給神"),
    absalom:commons("081.David Mourns the Death of Absalom.jpg","大衛哀悼押沙龍","大衛在哀傷中"),
    jacobPrayer:commons("025.Jacob Prays for Protection.jpg","雅各祈求保護","在危難中向神呼求"),
    isaiah:commons("120.The Prophet Isaiah.jpg","先知以賽亞","受膏者與耶和華救恩的先知盼望")
  };
  const plan={
    1:art.goliath,2:art.goliath,3:art.absalom,4:art.absalom,5:art.jacobPrayer,
    6:art.absalom,7:art.spared,8:art.goliath,9:art.goliath,10:art.saul,
    11:art.escape,12:art.saul,13:art.escape,14:art.saul,15:art.jonathan,
    16:art.jonathan,17:art.spared,18:art.goliath,19:art.goliath,20:art.goliath,
    21:art.goliath,22:art.isaiah,23:art.jonathan,24:art.goliath,25:art.jacobPrayer
  };
  Object.entries(plan).forEach(([number,illustration])=>{
    const study=P.chapterStudies?.[number];
    if(study)study.illustration={...illustration};
  });
})();
