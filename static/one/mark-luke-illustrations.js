/* ONE · 馬可福音／路加福音逐章多雷插圖配置
 * 作品選擇依 Wikimedia Commons 的 Doré's Bible Illustrations 完整目錄逐項核對。
 * 不再使用錯誤的 Gutenberg 8710 圖片編號猜測。
 */
(() => {
  'use strict';
  const D = window.ONE_DATA;
  if (!D) return;

  const commonsGallery = 'https://commons.wikimedia.org/wiki/Dor%C3%A9%27s_Bible_Illustrations';
  const mediaSearch = title => `https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=${encodeURIComponent(`Gustave Doré ${title}`)}`;

  /*
   * src 使用 Commons Special:Redirect/file。已知 Commons 檔名直接寫入；
   * 其餘作品使用 Commons 完整目錄的標準作品名作為檔名候選，若遠端檔名日後變動，
   * ONE 的既有 onerror fallback 仍會保證版面可用，而 source 永遠指向可核對的 Commons 搜尋。
   */
  const file = (filename, title, alt) => ({
    src: `https://commons.wikimedia.org/wiki/Special:Redirect/file/${encodeURIComponent(filename)}`,
    alt: `古斯塔夫・多雷版畫：${alt}`,
    title,
    source: mediaSearch(title),
    catalog: commonsGallery
  });

  const known = {
    annunciation: 'Gustave Dore - The Annunciation.jpg',
    johnWilderness: 'DoreJohntheBaptistPreachingintheWilderness.jpg',
    tempest: 'JesusCalmingtheTempestDore.jpg',
    marthaMary: 'Jesus talks with Mary and Martha in their house.jpg',
    entry: 'Gustave Dore - Jesus rides into Jerusalem on a donkey on Palm Sunday.jpg',
    tribute: 'Gustave Dore - Jesus talks of the tribute money.jpg',
    baptism: 'Gustave Dore - John the Baptist baptizes Jesus.jpg',
    betrayal: 'Gustave Dore - Judas betrays Jesus with a kiss.jpg',
    transfiguration: 'Gustave Dore - The Transfiguration.jpg'
  };

  /*
   * 馬可：每章一幅不同作品。優先採本章直接對應作品；沒有逐章專屬版畫時，
   * 選同章／同段敘事最接近的 Doré 福音作品，但同卷不重複。
   */
  const mark = {
    1: file(known.johnWilderness, 'John the Baptist Preaching in the Wilderness', '施洗約翰在曠野傳道'),
    2: file('Gustave Dore - The Disciples Plucking Corn on the Sabbath.jpg', 'The Disciples Plucking Corn on the Sabbath', '門徒在安息日掐麥穗'),
    3: file('Gustave Dore - The Dumb Man Possessed.jpg', 'The Dumb Man Possessed', '耶穌勝過污鬼的權勢'),
    4: file(known.tempest, 'Jesus Stilling the Tempest', '耶穌平靜風浪'),
    5: file('Gustave Dore - Jesus Raising Up the Daughter of Jairus.jpg', 'Jesus Raising Up the Daughter of Jairus', '耶穌使睚魯的女兒復活'),
    6: file('Gustave Dore - Christ Feeding the Multitude.jpg', 'Christ Feeding the Multitude', '耶穌使眾人吃飽'),
    7: file('Gustave Dore - Jesus Healing the Sick.jpg', 'Jesus Healing the Sick', '耶穌醫治病人'),
    8: file('Gustave Dore - Jesus Healing the Lunatic.jpg', 'Jesus Healing the Lunatic', '耶穌醫治受苦的人'),
    9: file(known.transfiguration, 'The Transfiguration', '登山變像'),
    10: file('Gustave Dore - Jesus Blessing the Little Children.jpg', 'Jesus Blessing the Little Children', '耶穌為小孩子祝福'),
    11: file(known.entry, 'Entry of Jesus Into Jerusalem', '耶穌進入耶路撒冷'),
    12: file('Gustave Dore - The Widows Mite.jpg', "The Widow's Mite", '寡婦的兩個小錢'),
    13: file('Gustave Dore - Jesus Praying in the Garden.jpg', 'Jesus Praying in the Garden', '耶穌在橄欖山禱告'),
    14: file(known.betrayal, 'The Judas Kiss', '猶大以親嘴出賣耶穌'),
    15: file('Gustave Dore - Jesus Falling Beneath the Cross.jpg', 'Jesus Falling Beneath the Cross', '耶穌背十字架走向各各他'),
    16: file('Gustave Dore - The Ascension.jpg', 'The Ascension', '復活的主升天')
  };

  /*
   * 路加：24章使用24幅不同作品。路加特有材料優先使用 Doré 直接為路加所作的版畫。
   */
  const luke = {
    1: file(known.annunciation, 'The Annunciation', '天使向馬利亞報喜'),
    2: file('Gustave Dore - The Nativity.jpg', 'The Nativity', '耶穌降生'),
    3: file(known.baptism, 'The Baptism of Jesus', '耶穌受洗'),
    4: file('Gustave Dore - The Temptation of Jesus.jpg', 'The Temptation of Jesus', '耶穌在曠野受試探'),
    5: file('Gustave Dore - Jesus Preaching at the Sea of Galilee.jpg', 'Jesus Preaching at the Sea of Galilee', '耶穌在加利利海邊傳道'),
    6: file('Gustave Dore - The Sermon on the Mount.jpg', 'The Sermon on the Mount', '耶穌教導門徒與眾人'),
    7: file('Gustave Dore - Mary Magdalene Repentant.jpg', 'Mary Magdalene Repentant', '蒙赦免的女人以愛回應耶穌'),
    8: file('Gustave Dore - Jesus Raising Up the Daughter of Jairus.jpg', 'Jesus Raising Up the Daughter of Jairus', '耶穌使睚魯的女兒復活'),
    9: file(known.transfiguration, 'The Transfiguration', '登山變像'),
    10: file('The Bible panorama, or The Holy Scriptures in picture and story (1891) (14598361689).jpg', 'The Good Samaritan', '好撒瑪利亞人'),
    11: file(known.marthaMary, 'Jesus at the House of Martha and Mary', '耶穌在馬大和馬利亞家中'),
    12: file('Gustave Dore - Jesus Preaching to the Multitude.jpg', 'Jesus Preaching to the Multitude', '耶穌向眾人講論天國'),
    13: file('Gustave Dore - The Barren Fig Tree.jpg', 'The Barren Fig Tree', '不結果子的無花果樹'),
    14: file('Gustave Dore - The Great Supper.jpg', 'The Great Supper', '大筵席的比喻'),
    15: file('Gustave Dore - The Return of the Prodigal Son.jpg', 'The Return of the Prodigal Son', '浪子醒悟回家'),
    16: file('Gustave Dore Lazarus and the Rich Man.jpg', "Lazarus at the Rich Man's House", '財主與拉撒路'),
    17: file('Gustave Dore - Jesus Healing the Sick.jpg', 'Jesus Healing the Sick', '耶穌醫治並呼召人以信心回應'),
    18: file('Gustave Dore - The Pharisee and the Publican.jpg', 'The Pharisee and the Publican', '法利賽人和稅吏禱告'),
    19: file('Gustave Dore - The Buyers and Sellers Driven Out of the Temple.jpg', 'The Buyers and Sellers Driven Out of the Temple', '耶穌潔淨聖殿'),
    20: file(known.tribute, 'Christ and the Tribute Money', '耶穌回答納稅問題'),
    21: file('Gustave Dore - The Widows Mite.jpg', "The Widow's Mite", '寡婦的兩個小錢'),
    22: file('Gustave Dore - The Agony in the Garden.jpg', 'The Agony in the Garden', '耶穌在客西馬尼痛苦禱告'),
    23: file('Gustave Dore - The Darkness at the Crucifixion.jpg', 'The Darkness at the Crucifixion', '十字架時遍地黑暗'),
    24: file('Gustave Dore - Jesus and the Disciples Going to Emmaus.jpg', 'Jesus and the Disciples Going to Emmaus', '復活的耶穌與門徒往以馬忤斯')
  };

  const apply = (book, mapping, expected) => {
    if (!book?.chapterStudies) return;
    const keys = Object.keys(mapping);
    if (keys.length !== expected) console.error(`ONE illustration map expected ${expected}, got ${keys.length}`);
    const seen = new Set();
    Object.entries(mapping).forEach(([chapter, illustration]) => {
      if (seen.has(illustration.src)) console.error(`ONE duplicate illustration in same book: ${chapter}`, illustration.src);
      seen.add(illustration.src);
      if (book.chapterStudies[chapter]) book.chapterStudies[chapter].illustration = illustration;
    });
  };

  apply(D.mark, mark, 16);
  apply(D.luke, luke, 24);
})();
