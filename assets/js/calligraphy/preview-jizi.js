// Lightweight first-production path.
// Remote glyph previews stay raster; SVG is only the composition container.

const esc = (s='') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

const RHYTHM = [
  [0,1.04,-1.2,.96],[7,.94,.8,1.04],[-5,1.08,-.5,.91],
  [4,.98,1.1,1.08],[-3,1.02,-.8,.97],[6,.92,.4,1.03]
];

export function renderPreviewJizi(glyphs, options={}) {
  const width = options.width || 720;
  const cell = options.cellHeight || 150;
  const margin = options.margin || 72;
  let cursor = margin + cell / 2;
  const placed = glyphs.map((g,i) => {
    const [dx,scale,rotate,gap] = RHYTHM[i % RHYTHM.length];
    const y = cursor; cursor += cell * gap;
    return {...g, x:width/2+dx, y, scale, rotate};
  });
  const height = Math.ceil((placed.at(-1)?.y || margin) + cell/2 + margin);
  const images = placed.map(g => {
    const size = cell * .92 * g.scale;
    return `<image href="${esc(g.previewUrl)}" x="${g.x-size/2}" y="${g.y-size/2}" width="${size}" height="${size}" preserveAspectRatio="xMidYMid meet" transform="rotate(${g.rotate} ${g.x} ${g.y})"/>`;
  }).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" role="img"><rect width="100%" height="100%" fill="${options.paper || '#f4efe3'}"/>${images}</svg>`;
}

export function glyphPreview(literal, previewUrl, teacher, sourceUrl) {
  return { literal, previewUrl, teacher: teacher || null, sourceUrl: sourceUrl || null };
}
