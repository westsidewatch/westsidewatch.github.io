/* P2/04 · V60 / MERSI LETTERPRESS, NOT A RECTANGULAR REVEAL.
 * One continuous measured Olivet terrain SVG. Complete contour lines
 * are printed in six successive speaker-owned batches, inside-out.
 * No dashed drawing, no independent RAF, no invented topography.
 */
(()=>{'use strict';
 const stage=document.querySelector('#p2-olive-stage');
 const mount=document.querySelector('.olive-editorial-engraving__print--topography');
 if(!stage||!mount)return;
 const clamp=x=>Math.max(0,Math.min(1,Number(x)||0));
 // Rebalance against the much broader leaf shapes: measured terrain
 // deserves legible ink, alternating light and warm gold with one dark
 // line edition for depth. All colors come from the existing Design OS.
 const colors=['var(--ws-morning-gold)','var(--ws-pale-gold)','var(--ws-warm-gold)',
               'var(--ws-first-light)','var(--ws-morning-gold)','var(--ws-pale-gold)'];
 let batches=null,latest=Array(6).fill(0);
 function paint(_plants,terrain){
  latest=Array.isArray(terrain)?terrain.map(clamp):Array(6).fill(clamp(terrain));
  if(!batches)return;
  let count=0;
  for(let i=0;i<batches.length;i++){
   const alpha=latest[i]||0;
   for(const path of batches[i]){
    path.style.opacity=alpha.toFixed(3);
    if(alpha>.001)count++;
   }
  }
  stage.dataset.p2TerrainVisiblePaths=String(count);
  stage.dataset.p2TerrainCompleteRings=String(latest.filter(x=>x>.999).length);
 }
 window.P2OliveEngraving={paint};
 fetch('/images/p2-realms/v15/04-olive-terrain-continuous-mother-v74.svg')
 .then(r=>{if(!r.ok)throw Error('Olivet DEM SVG '+r.status);return r.text()})
 .then(source=>{
  const doc=new DOMParser().parseFromString(source,'image/svg+xml');
  if(doc.querySelector('parsererror')||doc.documentElement.localName!=='svg')
   throw Error('invalid geographic SVG');
  const svg=document.importNode(doc.documentElement,true);
  svg.removeAttribute('width');svg.removeAttribute('height');
  svg.setAttribute('preserveAspectRatio','xMidYMid meet');
  svg.setAttribute('aria-hidden','true');
  mount.append(svg);
  const paths=[...svg.querySelectorAll('#olivet-true-topography path')];
  if(paths.length<24)throw Error('too few measured contour paths');
  // Measured contour paths are already authentic geography. Print the
  // LARGE ridge contours first, then progressively smaller hill rings.
  // Sorting small-first left two tiny, disembodied shapes beside the
  // portraits until the last speakers appeared: unacceptable composition.
  // Every path is still painted whole, never unveiled by a rectangle.
  const ranked=paths.map(path=>{
   path.style.strokeDasharray='none';
   path.style.strokeDashoffset='0';
   path.setAttribute('stroke-dasharray','none');
   path.setAttribute('stroke-dashoffset','0');
   const b=path.getBBox();
   return {path,area:b.width*b.height,range:b.width+b.height};
  }).sort((a,b)=>b.area-a.area||b.range-a.range);
  batches=Array.from({length:6},()=>[]);
  ranked.forEach(({path},index)=>{
   const edition=Math.min(5,Math.floor(index*6/ranked.length));
   path.style.stroke=colors[edition];
   const original=Number(path.getAttribute('stroke-width'))||.65;
   // Maintain the major/minor engraving hierarchy while giving Olivet
   // enough weight to balance the botanical print at actual screen size.
   path.style.strokeWidth=(original*1.65).toFixed(2);
   path.style.opacity='0';
   path.dataset.p2ContourImpression=String(edition+1);
   batches[edition].push(path);
  });
  mount.classList.add('has-path-growth');
  stage.dataset.p2TerrainStrokeEngine='real-dem-one-continuous-mother-v74';
  stage.dataset.p2TerrainPathTotal=String(paths.length);
  paint(null,latest);
 })
 .catch(err=>{
  stage.dataset.p2TerrainStrokeEngine='static-fallback';
  console.warn('04 measured whole-contour fallback:',err.message);
 });
})();
