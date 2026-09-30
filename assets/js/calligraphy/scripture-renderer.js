import { scriptureJiziCells } from './scripture-jizi.js';

function esc(value='') { return String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

function imageHref(glyph) {
  return glyph?.regionUrl || glyph?.imageUrl || glyph?.src || glyph?.url || null;
}

export function renderScriptureSvg(result, options = {}) {
  const cells = scriptureJiziCells(result);
  const width = options.width || 720;
  const cellH = options.cellHeight || 150;
  const margin = options.margin || 72;
  const height = margin * 2 + cells.length * cellH;
  const center = width / 2;
  const paper = options.paper || '#f4efe3';
  const ink = options.ink || '#171512';

  const body = cells.map((cell, i) => {
    const y = margin + i * cellH + cellH / 2;
    const t = cell.transform || {};
    const scale = t.scale ?? 1;
    const rotate = t.rotate ?? 0;
    const x = center + (t.x || 0);
    const yy = y + (t.y || 0);
    const href = imageHref(cell.glyph);
    if (href) {
      const size = cellH * 0.9 * scale;
      return `<image href="${esc(href)}" x="${x-size/2}" y="${yy-size/2}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet" transform="rotate(${rotate} ${x} ${yy})"/>`;
    }
    return `<text x="${x}" y="${yy}" text-anchor="middle" dominant-baseline="central" font-size="${cellH*0.62*scale}" fill="${ink}" opacity="${cell.missing ? 0.22 : 0.72}" transform="rotate(${rotate} ${x} ${yy})">${esc(cell.literal)}</text>`;
  }).join('');

  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(result.text)}"><rect width="100%" height="100%" fill="${paper}"/>${body}</svg>`;
}
