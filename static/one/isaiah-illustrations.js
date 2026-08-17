/* Isaiah ONE illustrations: verified Doré works only; no rotating fallback. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const commons=(file,title,alt,relation)=>({
    src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
    source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
    catalog:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations",
    testament:"OT",artist:"Gustave Doré",title,alt:`古斯塔夫・多雷版畫：${alt}`,relation
  });
  const prophet=commons("120.The Prophet Isaiah.jpg","The Prophet Isaiah","先知以賽亞","book");
  const babylon=commons("121.Isaiah's Vision of the Destruction of Babylon.jpg","Isaiah's Vision of the Destruction of Babylon","以賽亞看見巴比倫毀滅的異象","direct");
  const leviathan=commons("122.The Destruction of Leviathan.jpg","The Destruction of Leviathan","利維坦被毀滅","direct");
  const sennacherib=commons("101.Sennacherib's Army Is Destroyed.jpg","Sennacherib's Army Is Destroyed","西拿基立軍隊被毀滅","historical");
  for(let n=1;n<=66;n++){
    const s=I.chapterStudies[String(n)];
    if(!s)continue;
    s.illustration={...prophet};
  }
  I.chapterStudies["13"].illustration={...babylon};
  I.chapterStudies["27"].illustration={...leviathan};
  I.chapterStudies["36"].illustration={...sennacherib};
  I.chapterStudies["37"].illustration={...sennacherib};
  I.illustrationPolicy={artist:"Gustave Doré",source:"Wikimedia Commons",testament:"OT",rule:"以賽亞書只使用已核實的多雷作品。賽13與賽27使用本章直接作品；賽36–37使用西拿基立歷史作品；其他章使用全卷肖像《The Prophet Isaiah》，不再以不相干舊約場景循環替代。"};
})();