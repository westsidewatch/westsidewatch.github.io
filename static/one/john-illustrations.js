/* 約翰福音 ONE：逐章插圖配置。direct / related 必須明確區分。 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const john=D?.john;
  if(!john?.chapterStudies)return;

  john.illustrationPolicy={artist:"Gustave Doré",source:"Wikimedia Commons",rule:"direct 優先；無直接約翰場景時才使用 related；卷內不得重複。"};
  const gallery="https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations";
  const file=(filename,title,alt,relation="direct",source=gallery)=>({src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(filename)}`,alt:`古斯塔夫・多雷版畫：${alt}`,title,source,catalog:gallery,relation});

  const illustrations={
    1:file("DoreJohntheBaptistPreachingintheWilderness.jpg","John the Baptist Preaching in the Wilderness","施洗約翰在曠野傳道","related"),
    2:file("Marriage at Cana engraving by Gustave Doré.jpg","The Marriage at Cana","迦拿婚宴"),
    3:file("The Brazen Serpent.jpg","The Brazen Serpent","銅蛇與仰望得生","related"),
    4:file("Jesus asks the Samaritan woman for a draft from the well.jpg","Jesus and the Woman of Samaria","耶穌與撒瑪利亞婦人"),
    5:file("Jesus healing the sick (89476181).jpg","Jesus Healing the Sick","耶穌醫治病人","related","https://commons.wikimedia.org/wiki/File:Jesus_healing_the_sick_(89476181).jpg"),
    6:file("Jesus walks on the sea.jpg","Jesus Walking on the Sea","耶穌在海面行走"),
    7:file("Dore Bible Sermon on the Mount.jpg","Jesus Preaching to the Multitude","耶穌向眾人教導","related"),
    8:file("Dore adultress.jpg","The Woman Taken in Adultery","行淫時被拿的婦人"),
    9:file("HealingGustaveDore.jpg","Healing in Gennesaret","耶穌醫治","related","https://commons.wikimedia.org/wiki/File:HealingGustaveDore.jpg"),
    10:file("DoreJesusSeaGalilee.jpg","Jesus Preaching at the Sea of Galilee","耶穌向羊群般的百姓教導","related"),
    11:file("The Bible panorama, or The Holy Scriptures in picture and story (1891) (14598514637).jpg","The Resurrection of Lazarus","拉撒路復活"),
    12:file("Gustave Dore - Jesus rides into Jerusalem on a donkey on Palm Sunday.jpg","Entry of Jesus Into Jerusalem","耶穌進入耶路撒冷","related"),
    13:file("Jesus and the disciples at the Last Supper.jpg","The Last Supper","耶穌與門徒最後的晚餐","related","https://commons.wikimedia.org/wiki/File:Jesus_and_the_disciples_at_the_Last_Supper.jpg"),
    14:file("DoreJesusPrayingintheGarden.jpg","Jesus Praying in the Garden","耶穌禱告","related","https://commons.wikimedia.org/wiki/File:DoreJesusPrayingintheGarden.jpg"),
    15:file("Dore Bible Sermon on the Mount 2.jpg","The Sermon on the Mount","耶穌教導門徒","related"),
    16:file("Jesus suffers agony in the garden of Gethseman.jpg","The Agony in the Garden","客西馬尼的禱告","related","https://commons.wikimedia.org/wiki/File:Jesus_suffers_agony_in_the_garden_of_Gethseman.jpg"),
    17:file("Gustave Dore - Jesus converses with the learned ones in the Temple.jpg","Jesus Converses with the Learned Ones in the Temple","耶穌談論父與子的事","related","https://commons.wikimedia.org/wiki/File:Gustave_Dore_-_Jesus_converses_with_the_learned_ones_in_the_Temple.jpg"),
    18:file("Peter denies that he is one of Jesus’ disciples.jpg","Peter Denying Christ","彼得不認主"),
    19:file("Christ Presented to the PeopleDore.jpg","Christ Presented to the People","彼拉多將耶穌帶到眾人面前"),
    20:file("The Bible panorama, or The Holy Scriptures in picture and story (1891) (14785046505).jpg","The Resurrection","復活的主","related","https://commons.wikimedia.org/wiki/File:The_Bible_panorama,_or_The_Holy_Scriptures_in_picture_and_story_(1891)_(14785046505).jpg"),
    21:file("La pêche miraculeuse de Gustave Doré.jpg","The Miraculous Draught of Fishes","提比哩亞海邊的一網魚")
  };

  const seen=new Set();
  let complete=true;
  for(let chapter=1;chapter<=21;chapter++){
    const illustration=illustrations[chapter];
    const study=john.chapterStudies[String(chapter)];
    if(!illustration||!study){complete=false;console.error(`ONE John illustration missing chapter ${chapter}`);continue;}
    if(seen.has(illustration.src)){complete=false;console.error(`ONE John duplicate illustration: chapter ${chapter}`,illustration.src);}
    seen.add(illustration.src);
    study.illustration=illustration;
  }
  john.illustrations=illustrations;
  document.documentElement.dataset.johnIllustrations=complete&&seen.size===21?"complete":"partial";
})();
