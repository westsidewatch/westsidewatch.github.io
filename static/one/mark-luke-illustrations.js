/* ONE · 馬可福音／路加福音逐章多雷插圖配置 */
(() => {
  'use strict';
  const D = window.ONE_DATA;
  if (!D) return;

  const commons = title => `https://commons.wikimedia.org/wiki/Special:MediaSearch?type=image&search=${encodeURIComponent(`Gustave Doré ${title}`)}`;
  const img = (file, title, alt) => ({
    src: `https://www.gutenberg.org/files/8710/8710-h/images/${file}`,
    alt: `古斯塔夫・多雷版畫：${alt}`,
    title,
    source: commons(title)
  });

  /* 每卷內避免重複；若沒有完全同章作品，選本章最接近的多雷福音場景。 */
  const mark = {
    1: img('049.jpg','Jesus Preaching at the Sea of Galilee','耶穌在加利利海邊傳道'),
    2: img('050.jpg','Jesus Healing the Sick','耶穌醫治病人'),
    3: img('052.jpg','Jesus and the Tribute Money','耶穌與納稅的問題'),
    4: img('051.jpg','Jesus Stilling the Tempest','耶穌平靜風浪'),
    5: img('054.jpg','The Daughter of Jairus','睚魯的女兒'),
    6: img('053.jpg','Jesus Walking on the Sea','耶穌在海面行走'),
    7: img('055.jpg','Christ and the Woman of Canaan','耶穌與外邦婦人'),
    8: img('056.jpg','The Feeding of the Multitude','耶穌使眾人吃飽'),
    9: img('057.jpg','The Transfiguration','登山變像'),
    10: img('058.jpg','Jesus Blessing the Children','耶穌為小孩子祝福'),
    11: img('059.jpg','The Entry into Jerusalem','耶穌進入耶路撒冷'),
    12: img('060.jpg','The Widow’s Mite','寡婦的兩個小錢'),
    13: img('061.jpg','Jesus on the Mount of Olives','耶穌在橄欖山教導'),
    14: img('071.jpg','The Last Supper','最後晚餐'),
    15: img('076.jpg','The Crucifixion','耶穌被釘十字架'),
    16: img('079.jpg','The Angel at the Sepulchre','天使在空墳墓宣告復活')
  };

  const luke = {
    1: img('044.jpg','The Annunciation','天使向馬利亞報喜'),
    2: img('045.jpg','The Nativity','耶穌降生'),
    3: img('047.jpg','The Baptism of Jesus','耶穌受洗'),
    4: img('048.jpg','The Temptation of Jesus','耶穌在曠野受試探'),
    5: img('049.jpg','Jesus Preaching at the Sea of Galilee','耶穌在加利利海邊傳道'),
    6: img('050.jpg','Jesus Healing the Sick','耶穌醫治病人'),
    7: img('062.jpg','Jesus and the Centurion','耶穌與百夫長'),
    8: img('051.jpg','Jesus Stilling the Tempest','耶穌平靜風浪'),
    9: img('057.jpg','The Transfiguration','登山變像'),
    10: img('063.jpg','The Good Samaritan','好撒瑪利亞人'),
    11: img('064.jpg','Jesus at the House of Martha and Mary','耶穌在馬大和馬利亞家中'),
    12: img('065.jpg','The Rich Fool','無知的財主'),
    13: img('066.jpg','The Barren Fig Tree','不結果子的無花果樹'),
    14: img('067.jpg','The Great Supper','大筵席'),
    15: img('068.jpg','The Prodigal Son','浪子回家'),
    16: img('069.jpg','The Rich Man and Lazarus','財主與拉撒路'),
    17: img('070.jpg','The Ten Lepers','十個痲瘋病人'),
    18: img('058.jpg','Jesus Blessing the Children','耶穌為小孩子祝福'),
    19: img('059.jpg','The Entry into Jerusalem','耶穌進入耶路撒冷'),
    20: img('052.jpg','Jesus and the Tribute Money','耶穌回答納稅問題'),
    21: img('061.jpg','Jesus on the Mount of Olives','耶穌在橄欖山教導'),
    22: img('071.jpg','The Last Supper','最後晚餐'),
    23: img('076.jpg','The Crucifixion','耶穌被釘十字架'),
    24: img('081.jpg','The Ascension','耶穌升天')
  };

  const apply = (book, mapping) => {
    if (!book?.chapterStudies) return;
    Object.entries(mapping).forEach(([chapter, illustration]) => {
      if (book.chapterStudies[chapter]) book.chapterStudies[chapter].illustration = illustration;
    });
  };

  apply(D.mark, mark);
  apply(D.luke, luke);
})();
