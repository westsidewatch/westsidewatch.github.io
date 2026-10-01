import { scriptureJiziCells } from './scripture-jizi.js';

function esc(value='') { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
function imageHref(glyph) { return glyph?.regionUrl || glyph?.imageUrl || glyph?.src || glyph?.url || null; }

// Small deterministic rhythm: avoids typeset-like equal boxes without opening a research pipeline.
const RHYTHM = [
  {x:0, s:1.04, r:-1.2, gap:.96}, {x:7, s:.94, r:.8, gap:1.04},
  {x:-5, s:1.08, r:-.5, gap:.91}, {x:4, s:.98, r:1.1, gap:1.08},
  {x:-3, s:1.02, r:-.8, gap:.97}, {x:6, s:.92, r:.4, gap:1.03}
];

function layoutCells(cells, cellH, margin) {
  let cursor = margin + cellH / 2;
  return cells.map((cell, i) => {
    const p = RHYTHM[i % RHYTHM.length];
    const user = cell.transform || {};
    const out = {
      ...cell,
      layout: {
        x: p.x + (user.x || 0),
        y: cursor + (user.y || 0),
        scale: p.s * (user.scale ?? 1),
        rotate: p.r + (user.rotate || 0)
      }
    };
    cursor += cellH * p.gap;
    return out;
  });
}

export function renderScriptureSvg(result, options = {}) {
  const raw = scriptureJiziCells(result);
  const width = options.width || 720;
  const cellH = options.cellHeight || 150;
  const margin = options.margin || 72;
  const cells = layoutCells(raw, cellH, margin);
  const lastY = cells.at(-1)?.layout?.y || margin;
  const height = Math.ceil(lastY + cellH / 2 + margin);
  const center = width / 2;
  const paper = options.paper || '#f4efe3';
  const ink = options.ink || '#171512';

  const body = cells.map(cell => {
    const t = cell.layout;
    const x = center + t.x;
    const y = t.y;
    const href = imageHref(cell.glyph);
    if (href) {
      const size = cellH * .9 * t.scale;
      return `<image href="${esc(href)}" x="${x-size/2}" y="${y-size/2}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet" transform="rotate(${t.rotate} ${x} ${y})"/>`;
    }
    return `<text x="${x}" y="${y}" text-anchor="middle" dominant-baseline="central" font-size="${cellH*.62*t.scale}" fill="${ink}" opacity="${cell.missing ? .22 : .72}" transform="rotate(${t.rotate} ${x} ${y})">${esc(cell.literal)}</text>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(result.text)}"><rect width="100%" height="100%" fill="${paper}"/>${body}</svg>`;
}
