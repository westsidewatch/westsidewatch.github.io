/* 約翰福音 ONE：逐章插圖配置。direct / related 必須明確區分。 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const john=D?.john;
  if(!john)return;

  john.illustrations=john.illustrations||{};
  john.illustrationPolicy={
    artist:"Gustave Doré",
    source:"Wikimedia Commons",
    rule:"direct 優先；無直接約翰場景時才使用 related；卷內不得重複。"
  };

  /* 先建立已核實的 direct 錨點；其餘章位分批加入，避免未核實 URL 進入正式資料。 */
  Object.assign(john.illustrations,{
    "2":{title:"The Marriage in Cana",ref:"John 2:5–7",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "4":{title:"Jesus and the Woman of Samaria",ref:"John 4:13–14",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "18":{title:"Peter Denying Christ",ref:"John 18:26–27",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "19":{title:"Christ Presented to the People",ref:"John 19:15",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "21":{title:"The Miraculous Draught of Fishes",ref:"John 21:10–11",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/File:The_Bible_panorama,_or_The_Holy_Scriptures_in_picture_and_story_(1891)_(14804865203).jpg"}
  });

  document.documentElement.dataset.johnIllustrations="partial";
})();
