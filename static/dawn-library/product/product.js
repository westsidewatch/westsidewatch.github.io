const root = document.querySelector('[data-dawn-product]');
const shelvesHost = root.querySelector('[data-shelves]');
const search = root.querySelector('[data-search]');
const count = root.querySelector('[data-count]');

const [storefront, surface, manifest, featured] = await Promise.all([
  fetch('../storefront.json').then(r => r.json()),
  fetch('../surfaces/dawn-storefront.json').then(r => r.json()),
  fetch('../resource-fabric/manifest.json').then(r => r.json()),
  fetch('../resource-fabric/featured.json').then(r => r.json())
]);

const surfaceShelves = new Map((surface?.shelves || []).map(shelf => [shelf.id, shelf]));
const featuredWorks = new Map((featured?.rows || []).map(row => [row[0], row]));
const searchBucketCache = new Map();

function projectedRecord(row) {
  if (!row) return null;
  return {
    workId: row[0],
    title: row[1] || 'Untitled',
    author: row[2] || '',
    coverPointer: row[3] || null,
    readingPointer: row[4] || null,
    authorityBacked: Boolean(row[5])
  };
}

function canonicalRecord(workId) {
  return projectedRecord(featuredWorks.get(workId));
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
        author: work?.author || legacy.author || '',
        source: legacy.source || pointerSource(work?.readingPointer),
        coverPointer: work?.coverPointer || null,
        canonical: Boolean(work)
      };
    })
  };
}

const shelves = (storefront?.shelves || []).map(mergeShelf);
const curatedTotal = shelves.reduce((n, shelf) => n + shelf.items.length, 0);

function coverUrl(item) {
  const pointer = item?.coverPointer;
  if (typeof pointer === 'string' && pointer.startsWith('/dawn-library/covers/')) return pointer;
  return '';
}

function pointerSource(pointer) {
  if (typeof pointer === 'string' && /^https?:\/\//.test(pointer)) return { url: pointer };
  if (pointer && typeof pointer === 'object' && typeof pointer.url === 'string') return { url: pointer.url };
  return null;
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

function appendShelf(title, items) {
  if (!items.length) return 0;
  const section = document.createElement('section');
  section.className = 'shelf';
  const heading = document.createElement('h2');
  heading.textContent = title;
  const rail = document.createElement('div');
  rail.className = 'rail';
  items.forEach(item => rail.append(makeBook(item)));
  section.append(heading, rail);
  shelvesHost.append(section);
  return items.length;
}

function renderCurated() {
  shelvesHost.replaceChildren();
  let visible = 0;
  for (const shelf of shelves) visible += appendShelf(shelf.title, shelf.items);
  count.textContent = `${manifest?.workCount || curatedTotal} resources`;
}

function normalize(text) {
  return (text || '').toLocaleLowerCase().match(/[\p{L}\p{N}_]+/gu)?.join(' ') || '';
}

function tokenPrefix(token) {
  return Array.from(token).slice(0, 4).join('');
}

function fnv1a(text) {
  let h = 0x811c9dc5;
  for (const b of new TextEncoder().encode(text)) {
    h ^= b;
    h = Math.imul(h, 0x01000193) >>> 0;
  }
  return h >>> 0;
}

async function searchFabric(query) {
  const normalized = normalize(query);
  if (!normalized) return [];
  const tokens = normalized.split(' ').filter(Boolean);
  const prefix = tokenPrefix(tokens[0]);
  const bucket = fnv1a(prefix) % (manifest?.searchBucketCount || 64);
  if (!searchBucketCache.has(bucket)) {
    const id = bucket.toString(16).padStart(2, '0');
    searchBucketCache.set(bucket, fetch(`../resource-fabric/search-${id}.json`).then(r => r.json()));
  }
  const payload = await searchBucketCache.get(bucket);
  const seen = new Set();
  const results = [];
  for (const row of payload?.rows || []) {
    if (row[0] !== prefix) continue;
    const haystack = normalize(`${row[2]} ${row[3]}`);
    if (!tokens.every(token => haystack.includes(token))) continue;
    if (seen.has(row[1])) continue;
    seen.add(row[1]);
    results.push({
      workId: row[1],
      title: row[2] || 'Untitled',
      author: row[3] || '',
      source: null,
      coverPointer: null,
      canonical: true
    });
  }
  return results;
}

let searchGeneration = 0;
async function renderSearch(query) {
  const generation = ++searchGeneration;
  const results = await searchFabric(query);
  if (generation !== searchGeneration) return;
  shelvesHost.replaceChildren();
  const visible = appendShelf('All canonical resources', results);
  count.textContent = `${visible} / ${manifest?.workCount || 0}`;
  if (!visible) {
    const empty = document.createElement('p');
    empty.className = 'empty';
    empty.textContent = '沒有符合目前搜尋的館藏。';
    shelvesHost.append(empty);
  }
}

search.addEventListener('input', event => {
  const q = event.target.value.trim();
  if (!q) {
    searchGeneration += 1;
    renderCurated();
    return;
  }
  renderSearch(q).catch(error => {
    console.error('Resource Fabric search failed', error);
  });
});

renderCurated();
