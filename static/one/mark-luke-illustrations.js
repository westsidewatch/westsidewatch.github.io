/* ONE · 馬可福音／路加福音逐章多雷插圖配置
 * 作品選擇依 Wikimedia Commons 的 Doré's Bible Illustrations 完整目錄逐項核對。
 * 不使用 Gutenberg 編號猜測；已核實檔名優先，source 永遠指向 Commons 可核對搜尋。
 */
(() => {
  'use strict';
  const D = window.ONE_DATA;
  if (!D) return;

  const commonsGallery = 'https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations';
  const mediaSearch = title => `https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=${encodeURIComponent(`Gustave Doré ${title}`)}`;
  const file = (filename, title, alt, relation='direct') => ({
    src: `https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(filename)}`,
    alt: `古斯塔夫・多雷版畫：${alt}`,
    title,
    source: mediaSearch(title),
    catalog: commonsGallery,
    relation
  });

  const known = {
    annunciation: 'Gustave Dore - The Annunciation.jpg',
    johnWilderness: 'DoreJohntheBaptistPreachingintheWilderness.jpg',
    tempest: 'JesusCalmingtheTempestDore.jpg',
    seaGalilee: 'DoreJesusSeaGalilee.jpg',
    marthaMary: 'Jesus talks with Mary and Martha in their house.jpg',
    entry: 'Gustave Dore - Jesus rides into Jerusalem on a donkey on Palm Sunday.jpg',
    tribute: 'Gustave Dore - Jesus talks of the tribute money.jpg',
    baptism: 'Gustave Dore - John the Baptist baptizes Jesus.jpg',
    betrayal: 'Gustave Dore - Judas betrays Jesus with a kiss.jpg',
    transfiguration: 'Gustave Dore - The Transfiguration.jpg',
    jairus: 'Gustave Dore - Jesus raises the daughter of Jairus from the dead.jpg',
    lastSupper: 'Jesus and the disciples at the Last Supper.jpg',
    gethsemane: 'Jesus suffers agony in the garden of Gethseman.jpg',
    prayerGarden: 'DoreJesusPrayingintheGarden.jpg',
    ascension: 'Gusta Dore - The Ascension.jpg',
    pharisee: 'The Pharisee and the publican.jpg',
    prodigal: "Le retour de l'enfant prodigue, par Gustave Doré.jpg",
    lazarus: 'Gustave Dore Lazarus and the Rich Man.jpg',
    emmaus: 'The Bible panorama, or The Holy Scriptures in picture and story (1891) (14598534357).jpg'
  };

  /* direct = Commons 目錄有直接經文對應；related = 本章沒有專屬多雷版畫時採同章／相鄰主題。 */
  const mark = {
    1: file(known.johnWilderness, 'John the Baptist Preaching in the Wilderness', '施洗約翰在曠野傳道'),
    2: file('Gustave Dore - The Disciples Plucking Corn on the Sabbath.jpg', 'The Disciples Plucking Corn on the Sabbath', '門徒在安息日掐麥穗'),
    3: file('Gustave Dore - The Dumb Man Possessed.jpg', 'The Dumb Man Possessed', '耶穌勝過污鬼的權勢','related'),
    4: file(known.tempest, 'Jesus Stilling the Tempest', '耶穌平靜風浪'),
    5: file(known.jairus, 'Jesus Raising Up the Daughter of Jairus', '耶穌使睚魯的女兒復活'),
    6: file('Gustave Dore - Christ Feeding the Multitude.jpg', 'Christ Feeding the Multitude', '耶穌使眾人吃飽','related'),
    7: file('Gustave Dore - Jesus Healing the Sick.jpg', 'Jesus Healing the Sick', '耶穌醫治病人','related'),
    8: file('Gustave Dore - Jesus Healing the Lunatic.jpg', 'Jesus Healing the Lunatic', '耶穌醫治受苦的人','related'),
    9: file(known.transfiguration, 'The Transfiguration', '登山變像'),
    10: file('Gustave Dore - Jesus Blessing the Little Children.jpg', 'Jesus Blessing the Little Children', '耶穌為小孩子祝福'),
    11: file(known.entry, 'Entry of Jesus Into Jerusalem', '耶穌進入耶路撒冷'),
    12: file('Gustave Dore - The Widows Mite.jpg', "The Widow's Mite", '寡婦的兩個小錢'),
    13: file(known.prayerGarden, 'Jesus Praying in the Garden', '橄欖山上的耶穌','related'),
    14: file(known.lastSupper, 'The Last Supper', '耶穌與門徒最後的晚餐'),
    15: file('Gustave Dore - Jesus Falling Beneath the Cross.jpg', 'Jesus Falling Beneath the Cross', '耶穌背十字架走向各各他'),
    16: file(known.ascension, 'The Ascension', '復活的主升天')
  };

  const luke = {
    1: file(known.annunciation, 'The Annunciation', '天使向馬利亞報喜'),
    2: file('Gustave Dore - The Nativity.jpg', 'The Nativity', '耶穌降生'),
    3: file(known.baptism, 'The Baptism of Jesus', '耶穌受洗'),
    4: file('Gustave Dore - The Temptation of Jesus.jpg', 'The Temptation of Jesus', '耶穌在曠野受試探'),
    5: file(known.seaGalilee, 'Jesus Preaching at the Sea of Galilee', '耶穌在加利利海邊傳道'),
    6: file('Gustave Dore - The Sermon on the Mount.jpg', 'The Sermon on the Mount', '耶穌教導門徒與眾人','related'),
    7: file('Gustave Dore - Mary Magdalene Repentant.jpg', 'A Repentant Woman', '蒙赦免的女人以愛回應耶穌','related'),
    8: file(known.jairus, 'Jesus Raising Up the Daughter of Jairus', '耶穌使睚魯的女兒復活'),
    9: file(known.transfiguration, 'The Transfiguration', '登山變像','related'),
    10: file('The Bible panorama, or The Holy Scriptures in picture and story (1891) (14598361689).jpg', 'The Good Samaritan', '好撒瑪利亞人'),
    11: file(known.marthaMary, 'Jesus at the House of Martha and Mary', '耶穌在馬大和馬利亞家中','related'),
    12: file('Gustave Dore - Jesus Preaching to the Multitude.jpg', 'Jesus Preaching to the Multitude', '耶穌向眾人講論天國'),
    13: file('Gustave Dore - The Barren Fig Tree.jpg', 'The Barren Fig Tree', '不結果子的無花果樹','related'),
    14: file('Gustave Dore - The Great Supper.jpg', 'The Great Supper', '大筵席的比喻','related'),
    15: file(known.prodigal, 'The Return of the Prodigal Son', '浪子醒悟回家'),
    16: file(known.lazarus, "Lazarus at the Rich Man's House", '財主與拉撒路'),
    17: file('Gustave Dore - Jesus Healing the Sick.jpg', 'Jesus Healing the Sick', '耶穌醫治並呼召人以信心回應','related'),
    18: file(known.pharisee, 'The Pharisee and the Publican', '法利賽人和稅吏禱告'),
    19: file('Gustave Dore - The Buyers and Sellers Driven Out of the Temple.jpg', 'The Buyers and Sellers Driven Out of the Temple', '耶穌潔淨聖殿','related'),
    20: file(known.tribute, 'Christ and the Tribute Money', '耶穌回答納稅問題','related'),
    21: file('Gustave Dore - The Widows Mite.jpg', "The Widow's Mite", '寡婦的兩個小錢','related'),
    22: file(known.gethsemane, 'The Agony in the Garden', '耶穌在客西馬尼痛苦禱告'),
    23: file('Crucifixiondarkness.jpg', 'The Darkness at the Crucifixion', '十字架時遍地黑暗'),
    24: file(known.emmaus, 'Jesus and the Disciples Going to Emmaus', '復活的耶穌與門徒往以馬忤斯')
  };

  const apply = (book, mapping, expected, label) => {
    if (!book?.chapterStudies) {
      console.error(`ONE ${label} illustration map: chapterStudies unavailable`);
      return;
    }
    const keys = Object.keys(mapping);
    if (keys.length !== expected) console.error(`ONE ${label} illustration map expected ${expected}, got ${keys.length}`);
    const seen = new Set();
    for (let chapter=1; chapter<=expected; chapter++) {
      const illustration=mapping[chapter];
      const study=book.chapterStudies[String(chapter)];
      if(!illustration || !study){
        console.error(`ONE ${label} illustration missing chapter ${chapter}`);
        continue;
      }
      if (seen.has(illustration.src)) console.error(`ONE ${label} duplicate illustration: chapter ${chapter}`, illustration.src);
      seen.add(illustration.src);
      study.illustration=illustration;
    }
    document.documentElement.dataset[`${label}Illustrations`]=seen.size===expected?'complete':'partial';
  };

  apply(D.mark, mark, 16, 'mark');
  apply(D.luke, luke, 24, 'luke');
})();
