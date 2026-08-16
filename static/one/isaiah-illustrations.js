/* Isaiah ONE: Old Testament-only Gustave Doré illustration policy. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const commons=(file,title,alt,relation="related")=>({
    src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
    source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
    catalog:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations",
    testament:"OT",artist:"Gustave Doré",title,alt:`古斯塔夫・多雷版畫：${alt||title}`,relation
  });
  const A={
    isaiah:commons("120.The Prophet Isaiah.jpg","The Prophet Isaiah","先知以賽亞","direct"),
    babylon:commons("121.Isaiah's Vision of the Destruction of Babylon.jpg","Isaiah's Vision of the Destruction of Babylon","以賽亞看見巴比倫毀滅的異象","direct"),
    leviathan:commons("122.The Destruction of Leviathan.jpg","The Destruction of Leviathan","利維坦被毀滅","direct"),
    jerusalem:commons("Nehemiah Views the Ruins of Jerusalem's Walls.jpg","Jerusalem","耶路撒冷與錫安"),
    temple:commons("Cedars Are Cut Down for the Jerusalem Temple.jpg","Jerusalem Temple","耶路撒冷聖殿"),
    judgment:commons("Lot Flees as Sodom and Gomorrah Burn.jpg","Judgment","所多瑪與蛾摩拉受審判"),
    david:commons("071A.David Slays Goliath.jpg","David","大衛與大衛王權"),
    exile:commons("Daniel among the Exiles.jpg","Exile","被擄之民"),
    cyrus:commons("Cyrus Restores the Vessels of the Temple.jpg","Cyrus and Restoration","古列與歸回"),
    nations:commons("Gustave Dore Bible The Tower of Babel.jpg","The Nations","列國"),
    wilderness:commons("DoreHagar.jpg","The Wilderness","曠野中的困苦與拯救"),
    water:commons("Dore Moses Striking the Rock in Horeb.jpg","Water in the Wilderness","曠野中的水"),
    light:commons("Creation of Light.png","Creation of Light","創造之光"),
    prayer:commons("Ezra Kneels in Prayer.jpg","Prayer","在神面前禱告"),
    sennacherib:commons("Sennacherib's Army Is Destroyed.jpg","Sennacherib's Army Is Destroyed","西拿基立軍隊被毀滅","direct")
  };
  const plan={};
  const fill=(a,b,arr)=>{for(let n=a;n<=b;n++)plan[n]=arr[(n-a)%arr.length];};
  fill(1,5,[A.isaiah,A.jerusalem,A.judgment,A.temple]); plan[6]=A.isaiah;
  fill(7,12,[A.isaiah,A.david,A.light,A.jerusalem]);
  fill(13,23,[A.babylon,A.nations,A.judgment,A.jerusalem]);
  plan[24]=A.judgment;plan[25]=A.jerusalem;plan[26]=A.prayer;plan[27]=A.leviathan;
  fill(28,35,[A.jerusalem,A.judgment,A.prayer,A.wilderness]);
  plan[36]=A.sennacherib;plan[37]=A.sennacherib;plan[38]=A.prayer;plan[39]=A.babylon;
  fill(40,44,[A.wilderness,A.light,A.cyrus,A.exile,A.jerusalem]);
  fill(45,48,[A.cyrus,A.babylon,A.exile,A.jerusalem]);
  fill(49,55,[A.isaiah,A.jerusalem,A.prayer,A.water,A.exile,A.cyrus]);
  fill(56,64,[A.temple,A.prayer,A.jerusalem,A.light,A.nations,A.isaiah]);
  plan[65]=A.light;plan[66]=A.temple;
  for(let n=1;n<=66;n++){const s=I.chapterStudies[String(n)];if(s&&plan[n])s.illustration={...plan[n]};}
  I.illustrationPolicy={artist:"Gustave Doré",source:"Wikimedia Commons",testament:"OT",rule:"舊約經卷只使用舊約多雷版畫；本卷直接插圖優先，其次同時代／同歷史背景的舊約圖。新約引用不得把新約場景變成舊約章主插圖；沒有合理舊約圖時寧缺勿濫。"};
})();