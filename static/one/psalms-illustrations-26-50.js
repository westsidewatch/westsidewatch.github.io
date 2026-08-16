/* 詩篇 26–50：只使用已確認屬 Doré Old Testament 系列的作品。 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P)return;
const C="https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations";
const art=(file,title,alt)=>({src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,source:C,title,alt:`古斯塔夫・多雷版畫：${alt||title}`,artist:"Gustave Doré",testament:"OT"});
const A={
light:art("001.The Creation of Light.jpg","創造之光"),flood:art("007.The Great Flood.jpg","大洪水"),jacob:art("023.Jacob Prays for Protection.jpg","雅各祈求保護"),
goliath:art("071A.David Slays Goliath.jpg","大衛擊殺歌利亞"),saul:art("072.Saul Attempts to Kill David.jpg","掃羅企圖殺大衛"),escape:art("073.David Escapes through a Window.jpg","大衛從窗戶逃走"),spared:art("074.David Shows Saul How He Spared His Life.jpg","大衛饒掃羅性命"),absalom:art("081.David Mourns the Death of Absalom.jpg","大衛哀悼押沙龍"),
solomon:art("085.Solomon Receives the Queen of Sheba.jpg","所羅門接待示巴女王"),sennacherib:art("103.Sennacherib's Army Is Destroyed.jpg","西拿基立軍隊被毀"),ezra:art("114.Ezra Kneels in Prayer.jpg","以斯拉跪下禱告"),jeremiah:art("123.The Prophet Jeremiah.jpg","先知耶利米"),isaiah:art("120.The Prophet Isaiah.jpg","先知以賽亞")};
const plan={26:A.ezra,27:A.light,28:A.jacob,29:A.flood,30:A.absalom,31:A.escape,32:A.isaiah,33:A.light,34:A.spared,35:A.saul,36:A.light,37:A.jacob,38:A.jeremiah,39:A.isaiah,40:A.jacob,41:A.absalom,42:A.jacob,43:A.ezra,44:A.sennacherib,45:A.solomon,46:A.sennacherib,47:A.goliath,48:A.sennacherib,49:A.jeremiah,50:A.isaiah};
Object.entries(plan).forEach(([n,illustration])=>{const s=P.chapterStudies?.[n];if(s)s.illustration={...illustration};});
})();