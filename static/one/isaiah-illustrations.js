/* Isaiah ONE: chapter illustrations using the existing Gustave Doré illustration path. */
(() => {
  "use strict";
  const I=window.ONE_DATA?.isaiah;if(!I?.chapterStudies)return;
  const commons=(file,title,alt,relation="related")=>({
    src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(file)}?width=960`,
    source:`https://commons.wikimedia.org/wiki/File:${file.replaceAll(' ','_')}`,
    catalog:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations",
    title,alt:`古斯塔夫・多雷版畫：${alt||title}`,relation
  });
  const A={
    prophet:commons("DoreIsaiah.jpg","The Prophet Isaiah","先知以賽亞","direct"),
    temple:commons("Gustave Dore - Jesus converses with the learned ones in the Temple.jpg","The Temple","聖殿與敬拜"),
    prayer:commons("DoreJesusPrayingintheGarden.jpg","Prayer","在患難中禱告"),
    city:commons("Jerusalem from the Mount of Olives by Gustave Dore.jpg","Jerusalem","耶路撒冷與錫安"),
    judgment:commons("The destruction of Sodom and Gomorrah.jpg","Judgment","神的審判"),
    king:commons("071A.David Slays Goliath.jpg","The Davidic King","大衛王權與得勝"),
    exile:commons("The Flight of the Prisoners.jpg","Exile","被擄與離散"),
    return:commons("The Return of the Prodigal Son (Doré).jpg","Return","歸回與憐憫"),
    nations:commons("The Tower of Babel.jpg","The Nations","列國"),
    wilderness:commons("DoreJohntheBaptistPreachingintheWilderness.jpg","The Wilderness","曠野中的呼聲"),
    shepherd:commons("The Good Shepherd by Gustave Dore.jpg","The Shepherd","牧者與羊群"),
    servant:commons("Crucifixion-dore.jpg","The Suffering Servant","受苦僕人"),
    water:commons("Jesus asks the Samaritan woman for a draft from the well.jpg","Living Water","乾渴與活水"),
    light:commons("Creation of Light.png","Light","光照黑暗"),
    resurrection:commons("The Bible panorama, or The Holy Scriptures in picture and story (1891) (14785046505).jpg","Resurrection Hope","復活與新創造")
  };
  const pick=n=>{
    if(n<=5)return [A.city,A.judgment,A.temple][(n-1)%3];
    if(n===6)return A.prophet;
    if(n<=12)return [A.king,A.wilderness,A.light,A.shepherd][(n-7)%4];
    if(n<=23)return [A.nations,A.judgment,A.city][(n-13)%3];
    if(n<=27)return [A.resurrection,A.city,A.prayer,A.shepherd][(n-24)%4];
    if(n<=35)return [A.judgment,A.city,A.prayer,A.wilderness][(n-28)%4];
    if(n<=39)return [A.city,A.prayer,A.king,A.exile][n-36];
    if(n<=48)return [A.wilderness,A.light,A.shepherd,A.return,A.exile][(n-40)%5];
    if(n<=55)return [A.shepherd,A.servant,A.water,A.return][(n-49)%4];
    return [A.temple,A.prayer,A.light,A.city,A.resurrection][(n-56)%5];
  };
  for(let n=1;n<=66;n+=1){const s=I.chapterStudies[String(n)];if(s)s.illustration={...pick(n)};}
  I.illustrationPolicy={artist:"Gustave Doré",source:"Wikimedia Commons",rule:"優先採用與本章主題直接或最接近的多雷版畫；先知書沒有對應直接場景時使用 related 圖像，不改變經文含義。"};
})();