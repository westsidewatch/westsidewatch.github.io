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
  // The editorial PNGs are portrait assets; their old typography metadata was
  // never rendered in the homepage rail. Restore names as live overlay text,
  // using the approved English spelling and Chinese display name.
  const englishNames={
    '大衛鮑森':'DAVID PAWSON','江秀琴':'GRACE CHIANG','賴若瀚':'JERRY LAI',
    '劉彤':'TONG LIU','葉光明':'DEREK PRINCE','倪柝聲':'WATCHMAN NEE',
    '康來昌':'KANG LAI CHANG','唐崇榮':'STEPHEN TONG','寇紹恩':'KOU SHAO EN',
    '華理克':'RICK WARREN','于宏潔':'YU HONG JIE','黃淑華':'HUANG SHUHUA'
  };
  const ensureName=card=>{
    const name=card.dataset.person;
    if(!englishNames[name]||card.querySelector('.olive-speaker-card__identity'))return;
    const label=document.createElement('span');
    label.className='olive-speaker-card__identity';
    const en=document.createElement('span');en.className='olive-speaker-card__identity-en';en.lang='en';en.textContent=englishNames[name];
    const zh=document.createElement('span');zh.className='olive-speaker-card__identity-zh';zh.lang='zh-Hant';zh.textContent=name;
    label.append(en,zh);card.append(label);
  };
  rail.querySelectorAll('.olive-speaker-card').forEach(ensureName);
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
