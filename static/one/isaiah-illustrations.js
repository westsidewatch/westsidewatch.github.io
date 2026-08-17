/* Isaiah: only chapter-specific verified Doré works; no unrelated fallback.
 * Missing chapters intentionally remain without illustration until a canonical
 * chapter-specific generated engraving is added. Visual absence must never
 * affect navigation or chapter availability.
 */
(()=>{"use strict";const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
const historical=(file,title,alt)=>({
  src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
  source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
  title,
  alt:`古斯塔夫・多雷版畫：${alt}`,
  artist:"Gustave Doré",
  type:"historical",
  testament:"OT",
  morningStar:false
});
Object.values(I.chapterStudies).forEach(s=>{delete s.illustration});
const plan={
  1:historical("120.The Prophet Isaiah.jpg","The Prophet Isaiah","先知以賽亞"),
  13:historical("121.Isaiah's Vision of the Destruction of Babylon.jpg","Isaiah's Vision of the Destruction of Babylon","以賽亞看見巴比倫毀滅的異象"),
  27:historical("122.The Destruction of Leviathan.jpg","The Destruction of Leviathan","利維坦被毀滅"),
  36:historical("101.Sennacherib's Army Is Destroyed.jpg","Sennacherib's Army Is Destroyed","西拿基立軍隊被毀滅"),
  37:historical("101.Sennacherib's Army Is Destroyed.jpg","Sennacherib's Army Is Destroyed","西拿基立軍隊被毀滅")
};
Object.entries(plan).forEach(([n,a])=>{if(I.chapterStudies[n])I.chapterStudies[n].illustration=a});
})();