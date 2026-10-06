(() => {
  'use strict';

  const speakers = [
    ['speaker:david-pawson', '大衛鮑森'],
    ['speaker:jiang-xiuqin', '江秀琴'],
    ['speaker:derek-prince', '葉光明'],
    ['speaker:watchman-nee', '倪柝聲'],
    ['speaker:kang-lai-chang', '康來昌'],
    ['speaker:stephen-tong', '唐崇榮'],
    ['speaker:kou-shao-en', '寇紹恩'],
    ['speaker:rick-warren', '華理克'],
    ['speaker:tong-liu', '劉彤'],
    ['speaker:jerry-lai', '賴若瀚'],
    ['speaker:yu-hong-jie', '于宏潔'],
    ['speaker:huang-shuhua', '黃淑華']
  ];

  const speakerStage = document.querySelector('#olive-speakers');
  const seriesStage = document.querySelector('#olive-series');

  const recordsOf = payload => {
    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload?.records)) return payload.records;
    if (Array.isArray(payload?.items)) return payload.items;
    if (Array.isArray(payload?.resources)) return payload.resources;
    return [];
  };

  const card = (name, count, state = '') => {
    const article = document.createElement('article');
    article.className = 'speaker-card';
    article.innerHTML = `<p class="eyebrow">SPEAKER</p><h3>${name}</h3><p>${count === null ? state : `${count} 項已索引內容`}</p>`;
    return article;
  };

  async function loadSpeakers() {
    if (!speakerStage || !window.WestsideResources) return;
    speakerStage.replaceChildren();
    for (const [id, name] of speakers) {
      try {
        const payload = await window.WestsideResources.index('by-speaker', id);
        speakerStage.append(card(name, recordsOf(payload).length));
      } catch (error) {
        speakerStage.append(card(name, null, '館藏索引建立中'));
      }
    }
  }

  async function loadSeries() {
    if (!seriesStage || !window.WestsideResources) return;
    try {
      const [innerLife, goodtv] = await Promise.allSettled([
        window.WestsideResources.index('by-series', 'series:jiang-xiuqin:inner-life-45'),
        window.WestsideResources.index('by-series', 'series:jiang-xiuqin:goodtv')
      ]);
      const innerRecords = innerLife.status === 'fulfilled' ? recordsOf(innerLife.value) : [];
      const goodtvRecords = goodtv.status === 'fulfilled' ? recordsOf(goodtv.value) : [];
      seriesStage.innerHTML = `<article class="series-card"><p class="eyebrow">SERIES</p><h3>江秀琴 · 內在生活</h3><p>${innerRecords.length || 45} 集系列</p></article><article class="series-card"><p class="eyebrow">GOOD TV</p><h3>江秀琴 · GOOD TV</h3><p>${goodtvRecords.length || 3} 項已索引內容</p></article>`;
    } catch (error) {
      seriesStage.innerHTML = '<article class="series-card"><p class="eyebrow">SERIES</p><h3>江秀琴 · 內在生活</h3><p>45 集系列 · 索引接入中</p></article>';
    }
  }

  Promise.allSettled([loadSpeakers(), loadSeries()]);
})();
