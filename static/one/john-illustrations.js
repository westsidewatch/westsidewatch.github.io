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

  const dore="https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations";
  Object.assign(john.illustrations,{
    "1":{title:"John the Baptist Preaching in the Wilderness",ref:"Mark 1:6–7; related to John 1:19–34",match:"related",sourcePage:dore},
    "2":{title:"The Marriage in Cana",ref:"John 2:5–7",match:"direct",sourcePage:dore},
    "3":{title:"The Bronze Serpent",ref:"Numbers 21; related to John 3:14–15",match:"related",sourcePage:dore},
    "4":{title:"Jesus and the Woman of Samaria",ref:"John 4:13–14",match:"direct",sourcePage:dore},
    "5":{title:"Jesus Healing the Sick",ref:"Matthew 15:31; related to John 5:1–18",match:"related",sourcePage:dore},
    "6":{title:"Jesus Walking on the Sea",ref:"John 6:19–20",match:"direct",sourcePage:dore},
    "7":{title:"Jesus Preaching to the Multitude",ref:"Luke 12:29–31; related to John 7",match:"related",sourcePage:dore},
    "8":{title:"Jesus and the Woman Taken in Adultery",ref:"John 8:3–5",match:"direct",sourcePage:dore},
    "9":{title:"Healing in Gennesaret",ref:"Gospel healing scene; related to John 9 healing of the man born blind",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/File:HealingGustaveDore.jpg"},
    "10":{title:"Jesus Preaching at the Sea of Galilee",ref:"Luke 5:3; related teaching image for John 10",match:"related",sourcePage:dore},
    "11":{title:"Resurrection of Lazarus",ref:"John 11:41–43",match:"direct",sourcePage:dore},
    "12":{title:"Entry of Jesus Into Jerusalem",ref:"Matthew 21:7–8; same event as John 12:12–19",match:"related",sourcePage:dore},
    "13":{title:"The Last Supper",ref:"Mark 14:22–24; related to John 13",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/File:Jesus_and_the_disciples_at_the_Last_Supper.jpg"},
    "14":{title:"Jesus Praying in the Garden",ref:"Matthew 26:40–41; related to the farewell setting",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/File:DoreJesusPrayingintheGarden.jpg"},
    "15":{title:"The Sermon on the Mount",ref:"Matthew 5:7–10; related teaching image for John 15",match:"related",sourcePage:dore},
    "16":{title:"The Agony in the Garden",ref:"Luke 22:43–44; related to the approaching passion in John 16",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/File:Jesus_suffers_agony_in_the_garden_of_Gethseman.jpg"},
    "17":{title:"Jesus Converses with the Learned Ones in the Temple",ref:"Temple teaching scene; related to John 17's revelation of the Father and the Son",match:"related",sourcePage:"https://commons.wikimedia.org/wiki/File:Gustave_Dore_-_Jesus_converses_with_the_learned_ones_in_the_Temple.jpg"},
    "18":{title:"Peter Denying Christ",ref:"John 18:26–27",match:"direct",sourcePage:dore},
    "19":{title:"Christ Presented to the People",ref:"John 19:15",match:"direct",sourcePage:dore},
    "20":{title:"The Resurrection",ref:"Matthew 28:5–6; related to John 20",match:"related",sourcePage:dore},
    "21":{title:"The Miraculous Draught of Fishes",ref:"John 21:10–11",match:"direct",sourcePage:dore}
  });

  const entries=Object.values(john.illustrations);
  const placeholders=entries.filter(item=>item.match.includes("placeholder")).length;
  const titles=entries.map(item=>item.title);
  const uniqueTitles=new Set(titles).size===titles.length;
  document.documentElement.dataset.johnIllustrations=entries.length===21&&placeholders===0&&uniqueTitles?"ready":"review";
})();
