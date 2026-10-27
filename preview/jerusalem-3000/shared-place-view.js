import * as THREE from 'three';
// Persistent geographic references, not building meshes or historical footprints.
export function createSharedPlaceView(mount,places,{credit=true}={}){
 const layer=document.createElement('div');layer.className='j3k-place-references';layer.hidden=true;layer.setAttribute('aria-label','各時代共用地理參照（概略位置）');
 const svg=document.createElementNS('http://www.w3.org/2000/svg','svg');svg.setAttribute('aria-hidden','true');layer.append(svg);
 const entries=places.anchors().map((anchor,index)=>{
  const label=document.createElement('span');label.textContent=anchor.label;label.dataset.placeId=anchor.id;label.title='概略地理參照，不代表當期建築或古地表';
  const line=document.createElementNS(svg.namespaceURI,'line'),dot=document.createElementNS(svg.namespaceURI,'circle');dot.setAttribute('r','2.5');svg.append(line,dot);layer.append(label);return {anchor,label,line,dot,index};
 });if(credit){const note=document.createElement('small');note.className='j3k-place-credit';note.textContent='概略地理參照 · © OpenStreetMap contributors · ODbL';layer.append(note);}mount.append(layer);let visible=false;
 return {
  setVisible(value){visible=Boolean(value);layer.hidden=!visible;},
  project(camera,occupied=[]){if(!visible)return occupied;const w=mount.clientWidth,h=mount.clientHeight,boxes=[...occupied],bounds=mount.getBoundingClientRect(),caption=mount.parentElement.querySelector('.j3k-caption')?.getBoundingClientRect();svg.setAttribute('viewBox',`0 0 ${w} ${h}`);
   for(const {anchor,label,line,dot,index} of entries){
    const q=new THREE.Vector3(anchor.x,anchor.y+3,anchor.z).project(camera),clipped=q.z< -1||q.z>1||Math.abs(q.x)>.98||Math.abs(q.y)>.98;
    label.hidden=clipped;line.style.display=dot.style.display=clipped?'none':'';if(clipped)continue;
    const x=(q.x+1)*w/2,y=(1-q.y)*h/2,lw=label.offsetWidth,lh=label.offsetHeight;
    let left=Math.max(6,Math.min(w-lw-6,x+(index===1?-lw-30:30))),top=Math.max(55,Math.min(h-lh-8,y+(index===0?-38:index===1?20:30)));
    if(caption&&left<caption.right-bounds.left&&left+lw>caption.left-bounds.left)top=Math.max(55,Math.min(top,caption.top-bounds.top-lh-8));
    const overlaps=()=>boxes.some(b=>left<b.right+6&&left+lw>b.left-6&&top<b.bottom+5&&top+lh>b.top-5);
    for(let attempts=0;attempts<entries.length+occupied.length+2&&overlaps();attempts++)top=Math.max(55,top-lh-8);
    if(overlaps()){label.hidden=true;line.style.display='none';continue;}
    boxes.push({left,right:left+lw,top,bottom:top+lh});label.style.left=`${left}px`;label.style.top=`${top}px`;
    line.setAttribute('x1',x);line.setAttribute('y1',y);line.setAttribute('x2',Math.max(left,Math.min(left+lw,x)));line.setAttribute('y2',top+lh/2);dot.setAttribute('cx',x);dot.setAttribute('cy',y);
   }
   return boxes;
  },
  diagnostics(){return {enabled:visible,anchorIds:entries.map(e=>e.anchor.id),semanticCityObjects:false};},
  dispose(){layer.remove();}
 };
}
