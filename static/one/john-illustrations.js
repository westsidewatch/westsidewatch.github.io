/* 約翰福音 ONE：canonical chapter-cover illustration policy.
 * Historical art is retained only when it directly depicts the chapter scene.
 * Loose thematic / parallel-Gospel substitutions are forbidden. Missing direct
 * art intentionally falls through to ONE's canonical no-image cover until a
 * chapter-specific ONE Studio engraving is generated.
 */
(() => {
  "use strict";
  const D=window.ONE_DATA;
  const john=D?.john;
  if(!john?.chapterStudies)return;

  john.illustrationPolicy={
    artist:"Gustave Doré / verified historical engraving",
    source:"Wikimedia Commons",
    rule:"direct historical art first; otherwise canonical no-image cover until chapter-specific ONE Studio art exists; never use related thematic substitutes; never duplicate within the book."
  };
  const gallery="https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations";
  const file=(filename,title,alt,source=gallery)=>({
    src:`https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(filename)}`,
    alt:`古典聖經版畫：${alt}`,
    title,source,catalog:gallery,relation:"direct",kind:"historical",morningStar:false
  });

  /* Only defensible direct chapter scenes survive this pass. */
  const illustrations={
    2:file("Marriage at Cana engraving by Gustave Doré.jpg","The Marriage at Cana","迦拿婚宴"),
    4:file("Jesus asks the Samaritan woman for a draft from the well.jpg","Jesus and the Woman of Samaria","耶穌與撒瑪利亞婦人"),
    6:file("Jesus walks on the sea.jpg","Jesus Walking on the Sea","耶穌在海面行走"),
    8:file("Dore adultress.jpg","The Woman Taken in Adultery","行淫時被拿的婦人"),
    11:file("The Bible panorama, or The Holy Scriptures in picture and story (1891) (14598514637).jpg","The Resurrection of Lazarus","拉撒路復活"),
    18:file("Peter denies that he is one of Jesus’ disciples.jpg","Peter Denying Christ","彼得不認主"),
    19:file("Christ Presented to the PeopleDore.jpg","Christ Presented to the People","彼拉多將耶穌帶到眾人面前"),
    21:file("La pêche miraculeuse de Gustave Doré.jpg","The Miraculous Draught of Fishes","提比哩亞海邊的一網魚")
  };

  const seen=new Set();
  let valid=true;
  for(let chapter=1;chapter<=21;chapter++){
    const study=john.chapterStudies[String(chapter)];
    if(!study)continue;
    /* Critical: remove any illustration inherited from core/legacy data first. */
    delete study.illustration;
    const illustration=illustrations[chapter];
    if(!illustration)continue;
    if(seen.has(illustration.src)){
      valid=false;
      console.error(`ONE John duplicate direct illustration: chapter ${chapter}`,illustration.src);
      continue;
    }
    seen.add(illustration.src);
    study.illustration=illustration;
  }
  john.illustrations=illustrations;
  john.pendingGeneratedIllustrations=[];
  for(let chapter=1;chapter<=21;chapter++)if(!illustrations[chapter])john.pendingGeneratedIllustrations.push(chapter);
  document.documentElement.dataset.johnIllustrations=valid?"canonical":"invalid";
})();