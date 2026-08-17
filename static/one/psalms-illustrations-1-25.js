/* Psalms ONE · 1–25.
 * Historical engravings are attached only when the scene is defensibly related
 * to the Psalm's superscription/context. Generic OT and NT image recycling is
 * forbidden. Chapters without a reliable historical match remain intentionally
 * unillustrated until their canonical chapter-specific engraving is generated.
 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P?.chapterStudies)return;
const historical=(file,title,alt)=>({
  src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
  source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
  title,
  alt:`古斯塔夫・多雷版畫：${alt||title}`,
  artist:"Gustave Doré",
  type:"historical",
  testament:"OT",
  morningStar:false
});
Object.values(P.chapterStudies).slice(0,25).forEach(s=>{if(s)delete s.illustration});
const A={
  s:historical("072.Saul Attempts to Kill David.jpg","Saul Attempts to Kill David","掃羅企圖殺大衛"),
  e:historical("073.David Escapes through a Window.jpg","David Escapes through a Window","大衛從窗戶逃走"),
  j:historical("073A.David and Jonathan.jpg","David and Jonathan","大衛與約拿單"),
  p:historical("074.David Shows Saul How He Spared His Life.jpg","David Shows Saul How He Spared His Life","大衛饒掃羅性命"),
  a:historical("081.David Mourns the Death of Absalom.jpg","David Mourns the Death of Absalom","大衛哀悼押沙龍")
};
/* Only Psalms whose historical setting can be responsibly associated with the
 * selected David scenes receive them here. Others deliberately use the shared
 * canonical no-image cover until a chapter-specific generated engraving exists.
 */
const plan={3:A.a,7:A.p,11:A.e,13:A.e};
Object.entries(plan).forEach(([n,a])=>{if(P.chapterStudies[n])P.chapterStudies[n].illustration={...a}});
})();