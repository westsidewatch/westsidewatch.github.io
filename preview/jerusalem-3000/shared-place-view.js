import * as THREE from 'three';
// Persistent geographic references, not building meshes or historical footprints.
export function createSharedPlaceView(mount,places,{credit=true,ariaLabel='各時代共用地理參照（概略位置）',className='',maxLabels=null}={}){
 const layer=document.createElement('div');layer.className='j3k-place-references'+(className?' '+className:'');layer.hidden=true;layer.setAttribute('aria-label',ariaLabel);
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('aria-hidden','true');layer.append(svg);
 let entries=[];
 function setAnchors(anchors){
  const previous=new Map(entries.map(e=>[e.anchor.id,e]));
  entries=anchors.map((anchor,index)=>{
  const existing=previous.get(anchor.id);if(existing){previous.delete(anchor.id);existing.anchor=anchor;if(existing.label.textContent!==anchor.label)existing.label.textContent=anchor.label;if(anchor.description&&existing.label.title!==anchor.description)existing.label.title=anchor.description;return existing;}
  const label=document.createElement('span');label.textContent=anchor.label;label.dataset.placeId=anchor.id;label.title=anchor.description||'概略地理參照，不代表當期建築或古地表';
  const line=document.createElementNS(svg.namespaceURI,'line'),dot=document.createElementNS(svg.namespaceURI,'circle');dot.setAttribute('r','2.5');svg.append(line,dot);layer.append(label);return {anchor,label,line,dot,index};
 });
 for(const e of previous.values()){e.label.remove();e.line.remove();e.dot.remove();}
 }
 setAnchors(places.anchors());if(credit){const note=document.createElement('small');note.className='j3k-place-credit';note.textContent='概略地理參照 · © OpenStreetMap contributors · ODbL';layer.append(note);}mount.append(layer);let visible=false;
 return {
  setAnchors,
  setVisible(value){visible=Boolean(value);layer.hidden=!visible;},
  project(camera,occupied=[]){if(!visible)return occupied;const w=mount.clientWidth,h=mount.clientHeight,boxes=[...occupied],bounds=mount.getBoundingClientRect(),caption=mount.parentElement.querySelector('.j3k-caption')?.getBoundingClientRect();svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
   let painted=0;const limit=maxLabels?maxLabels(w):Infinity;
   for(const {anchor,label,line,dot,index} of entries){
    const q=new THREE.Vector3(anchor.x,anchor.y+3,anchor.z).project(camera),clipped=painted>=limit||q.z< -1||q.z>1||Math.abs(q.x)>.98||Math.abs(q.y)>.98;
    label.hidden=clipped;line.style.display=dot.style.display=clipped?'none':'';if(clipped)continue;
    const x=(q.x+1)*w/2,y=(1-q.y)*h/2,lw=label.offsetWidth,lh=label.offsetHeight;
    // Try both sides of the anchor and several rows; reserve the real controls
    // and caption instead of pushing later labels underneath mobile toolbars.
    const blocked=[...boxes];
    for(const el of [mount.parentElement.querySelector('.j3k-event-controls'),mount.parentElement.querySelector('.j3k-terrain-badge')]){if(!el||el.hidden)continue;const r=el.getBoundingClientRect();blocked.push({left:r.left-bounds.left,right:r.right-bounds.left,top:r.top-bounds.top,bottom:r.bottom-bounds.top});}
    if(caption)blocked.push({left:caption.left-bounds.left,right:caption.right-bounds.left,top:caption.top-bounds.top,bottom:caption.bottom-bounds.top});
    const candidates=[];
    for(const dx of [30,-lw-30,-lw/2])for(const dy of [-30,20,-60,50,-90,80,-120,110,-150,140,-180,170]){
     const left=Math.max(6,Math.min(w-lw-6,x+dx)),top=Math.max(55,Math.min(h-lh-8,y+dy)),overlap=blocked.some(b=>left<b.right+6&&left+lw>b.left-6&&top<b.bottom+5&&top+lh>b.top-5);
     if(!overlap)candidates.push({left,top,score:Math.hypot(left+lw/2-x,top+lh/2-y)});
    }
    candidates.sort((a,b)=>a.score-b.score);if(!candidates.length){label.hidden=true;line.style.display=dot.style.display='none';continue;}const {left,top}=candidates[0];
    painted++;boxes.push({left,right:left+lw,top,bottom:top+lh});label.style.left=`${left}px`;label.style.top=`${top}px`;
    line.setAttribute('x1',x);line.setAttribute('y1',y);line.setAttribute('x2',Math.max(left,Math.min(left+lw,x)));line.setAttribute('y2',top+lh/2);dot.setAttribute('cx',x);dot.setAttribute('cy',y);
   }
   return boxes;
  },
  diagnostics(){return {enabled:visible,anchorIds:entries.map(e=>e.anchor.id),labelledIds:visible?entries.filter(e=>!e.label.hidden).map(e=>e.anchor.id):[],semanticCityObjects:false};},
  dispose(){layer.remove();}
 };
}
