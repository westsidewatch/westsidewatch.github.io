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

  /* 只加入已由 Commons 檔案頁或 Doré 完整目錄核實的場景。 */
  Object.assign(john.illustrations,{
    "2":{title:"The Marriage in Cana",ref:"John 2:5–7",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "4":{title:"Jesus and the Woman of Samaria",ref:"John 4:13–14",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "6":{title:"Jesus Walking on the Sea",ref:"John 6:19–20",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/File:Jesus_of_Nazareth-_His_life_and_teachings%3B_founded_on_the_four_Gospels%2C_and_illustrated_by_reference_to_the_manners%2C_customs%2C_religious_beliefs%2C_and_political_institutions_of_His_times_(1869)_(14783321292).jpg"},
    "11":{title:"The Resurrection of Lazarus",ref:"John 11:41–43",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/File:The_Bible_panorama,_or_The_Holy_Scriptures_in_picture_and_story_(1891)_(14598514637).jpg"},
    "18":{title:"Peter Denying Christ",ref:"John 18:26–27",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "19":{title:"Christ Presented to the People",ref:"John 19:15",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "20":{title:"The Resurrection",ref:"Matthew 28:5–6; related to John 20",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"},
    "21":{title:"The Miraculous Draught of Fishes",ref:"John 21:10–11",match:"direct",sourcePage:"https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations"}
  });

  const assigned=Object.keys(john.illustrations).length;
  document.documentElement.dataset.johnIllustrations=assigned===21?"ready":"partial";
})();
