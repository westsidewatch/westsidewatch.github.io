import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const layout = fs.readFileSync('layouts/website/dawn-library.html', 'utf8');
const runtime = fs.readFileSync('static/js/dawn-web-surface.js', 'utf8');
const catalog = JSON.parse(fs.readFileSync('static/dawn-library/biblical-world/catalog.json', 'utf8'));
const candidates = JSON.parse(fs.readFileSync('static/dawn-library/biblical-world/discovery-candidates.json', 'utf8'));

function gutenbergSources(items) {
  return items.flatMap((item) => (item.sources || []).filter((source) =>
    source.provider === 'Project Gutenberg' &&
    /^https:\/\/(www\.)?gutenberg\.org\/ebooks\//.test(source.url || '')
  ));
}

test('public Dawn surface reads approved catalog, never discovery candidates', () => {
  assert.match(runtime, /biblical-world\/catalog\.json/);
  assert.doesNotMatch(runtime, /discovery-candidates\.json/);
  assert.match(layout, /data-dawn-biblical-world/);
  assert.match(layout, /data-dawn-web-surface-frame/);
});

test('catalog contains real Gutenberg pointers for the mounted adapter', () => {
  const sources = gutenbergSources(catalog.items || []);
  assert.ok(sources.length > 0, 'expected approved Gutenberg catalog pointers');
  assert.ok(sources.every((source) => source.downloadOnCatalog === false));
});

test('candidate corpus remains the 900+ benchmark, not public content', () => {
  assert.ok((candidates.items || []).length >= 900);
  assert.match(runtime, /source\.provider === 'Project Gutenberg'/);
  assert.match(runtime, /url\.hostname === 'www\.gutenberg\.org'/);
});

test('web surface remains external and provides escape hatch', () => {
  assert.match(layout, /target="_blank" rel="noopener noreferrer" data-dawn-web-surface-open/);
  assert.match(layout, /referrerpolicy="strict-origin-when-cross-origin"/);
  assert.match(runtime, /FRAME\.removeAttribute\('src'\)/);
});
