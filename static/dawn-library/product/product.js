const root = document.querySelector('[data-dawn-product]');
const shelvesHost = root.querySelector('[data-shelves]');
const search = root.querySelector('[data-search]');
const count = root.querySelector('[data-count]');

const [storefront, surface, canonical] = await Promise.all([
  fetch('../storefront.json').then(r => r.json()),
  fetch('../surfaces/dawn-storefront.json').then(r => r.json()),
  fetch('../canonical-index.json').then(r => r.json())
]);

const canonicalWorks = canonical?.works || {};
const surfaceShelves = new Map((surface?.shelves || []).map(shelf => [shelf.id, shelf]));

function canonicalRecord(workId) {
  return canonicalWorks[workId] || null;
}

function mergeShelf(storeShelf) {
  const canonicalShelf = surfaceShelves.get(storeShelf.id);
  const refs = canonicalShelf?.items || [];
  return {
    id: storeShelf.id,
    title: storeShelf.title,
    kind: storeShelf.kind,
    items: (storeShelf.items || []).map((legacy, index) => {
      const workId = refs[index]?.workId || legacy.workId || null;
      const work = canonicalRecord(workId);
      return {
        workId,
        title: work?.title || legacy.title || 'Untitled',
        author: work?.authors?.[0] || legacy.author || '',
        source: legacy.source || null,
        cover: legacy.cover || null,
        canonical: Boolean(work)
      };
    })
  };
}

const shelves = (storefront?.shelves || []).map(mergeShelf);
const total = shelves.reduce((n, shelf) => n + shelf.items.length, 0);

function coverUrl(item) {
  const url = item?.cover?.url;
  if (!url || typeof url !== 'string') return '';
  try {
    const parsed = new URL(url);
    return parsed.protocol === 'https:' ? parsed.href : '';
  } catch {
    return '';
  }
}

function makeBook(item) {
  const card = document.createElement('article');
  card.className = 'book';
  card.dataset.workId = item.workId || '';
  const coverWrap = document.createElement('div');
  coverWrap.className = 'cover-wrap';
  const fallback = document.createElement('div');
  fallback.className = 'fallback';
  fallback.innerHTML = `<small>Dawn Library</small><strong></strong><small>${item.author || 'Canonical Work'}</small>`;
  fallback.querySelector('strong').textContent = item.title;
  coverWrap.append(fallback);
  const url = coverUrl(item);
  if (url) {
    const img = document.createElement('img');
    img.alt = `${item.title} 封面`;
    img.loading = 'lazy';
    img.referrerPolicy = 'no-referrer';
    img.src = url;
    img.addEventListener('load', () => fallback.remove(), { once: true });
    img.addEventListener('error', () => img.remove(), { once: true });
    coverWrap.append(img);
  }
  if (item.canonical) {
    const badge = document.createElement('span');
    badge.className = 'badge';
    badge.textContent = 'DAWN';
    coverWrap.append(badge);
  }
  const title = document.createElement('h3');
  title.textContent = item.title;
  const author = document.createElement('p');
  author.textContent = item.author || '—';
  card.append(coverWrap, title, author);
  if (item.source?.url) {
    card.tabIndex = 0;
    card.setAttribute('role', 'link');
    card.addEventListener('click', () => window.open(item.source.url, '_blank', 'noopener,noreferrer'));
    card.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        window.open(item.source.url, '_blank', 'noopener,noreferrer');
      }
    });
  }
  return card;
}

function render(query = '') {
  const q = query.trim().toLocaleLowerCase();
  shelvesHost.replaceChildren();
  let visible = 0;
  for (const shelf of shelves) {
    const items = shelf.items.filter(item => !q || `${item.title} ${item.author}`.toLocaleLowerCase().includes(q));
    if (!items.length) continue;
    visible += items.length;
    const section = document.createElement('section');
    section.className = 'shelf';
    const heading = document.createElement('h2');
    heading.textContent = shelf.title;
    const rail = document.createElement('div');
    rail.className = 'rail';
    items.forEach(item => rail.append(makeBook(item)));
    section.append(heading, rail);
    shelvesHost.append(section);
  }
  count.textContent = q ? `${visible} / ${total}` : `${total} books`;
  if (!visible) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '沒有符合目前搜尋的館藏。';
    shelvesHost.append(empty);
  }
}

search.addEventListener('input', event => render(event.target.value));
render();
