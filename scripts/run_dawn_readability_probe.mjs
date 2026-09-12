import fs from 'node:fs/promises';
import path from 'node:path';
import { JSDOM } from 'jsdom';
import { Readability } from '@mozilla/readability';

const sourceUrl = process.env.DAWN_READABILITY_SOURCE || 'https://bibleproject.com/articles/did-god-or-people-write-bible/';
const response = await fetch(sourceUrl, { headers: { 'User-Agent': 'DawnLibrary/1.0 (+https://westsidewatch.github.io)' } });
if (!response.ok) throw new Error(`source HTTP ${response.status}`);
const html = await response.text();
const dom = new JSDOM(html, { url: sourceUrl });
const article = new Readability(dom.window.document).parse();
if (!article || !article.title || !article.textContent) throw new Error('Mozilla Readability returned no article');

const normalizedText = article.textContent.replace(/\s+/g, ' ').trim();
const excerpt = normalizedText.slice(0, 180);
const payload = {
  schema: 'dawn.readability.acceptance.v1',
  engine: '@mozilla/readability',
  sourceUrl,
  external: true,
  ownership: 'external',
  title: article.title,
  byline: article.byline || null,
  excerpt,
  textLength: normalizedText.length,
  contentLength: (article.content || '').length,
  admission: 'none; readability integration evidence only'
};

if (!/bible/i.test(payload.title)) throw new Error(`unexpected title: ${payload.title}`);
if (payload.textLength < 1500) throw new Error(`article body too short: ${payload.textLength}`);

await fs.mkdir('reports', { recursive: true });
await fs.mkdir('static/dawn-library/readability', { recursive: true });
await fs.writeFile('reports/DAWN-READABILITY.json', JSON.stringify(payload, null, 2) + '\n');
await fs.writeFile('static/dawn-library/readability/acceptance.json', JSON.stringify(payload, null, 2) + '\n');
console.log(JSON.stringify(payload, null, 2));
