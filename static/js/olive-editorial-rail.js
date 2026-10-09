/* Shared Olive editorial asset adapter. No duplicate speaker registry or poster typography. */
(() => {
  'use strict';
  const rail = document.querySelector('.olive-speaker-rail');
  if (!rail) return;
  const slugs = {
    '大衛鮑森':'david-pawson','江秀琴':'jiang-xiuqin','賴若瀚':'jerry-lai',
    '劉彤':'tong-liu','葉光明':'derek-prince','倪柝聲':'watchman-nee',
    '康來昌':'kang-lai-chang','唐崇榮':'stephen-tong','寇紹恩':'kou-shao-en',
    '華理克':'rick-warren','于宏潔':'yu-hong-jie','黃淑華':'huang-shuhua'
  };
  fetch('/dore-design/runtime/olive-editorial-covers.v1.json')
    .then(response => { if (!response.ok) throw new Error('editorial manifest unavailable'); return response.json(); })
    .then(data => {
      const covers = new Map((data.records || []).filter(record =>
        typeof record.speaker === 'string' &&
        /^\/images\/olive\/[a-z0-9-]+\.png$/.test(record.url)
      ).map(record => [record.speaker, record]));
      rail.querySelectorAll('.olive-speaker-card').forEach(card => {
        const record = covers.get(slugs[card.dataset.person]);
        if (!record || card.querySelector('.olive-speaker-card__editorial')) return;
        const image = document.createElement('img');
        image.className = 'olive-speaker-card__editorial';
        image.src = record.url;
        image.alt = '';
        image.loading = 'lazy';
        image.decoding = 'async';
        image.addEventListener('load', () => { card.dataset.editorialAsset = 'ready'; }, {once:true});
        image.addEventListener('error', () => { image.remove(); }, {once:true});
        card.prepend(image);
      });
    })
    .catch(() => { /* Preserve the existing accessible rail if assets are unavailable. */ });
})();
