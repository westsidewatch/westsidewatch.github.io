import {SKELETON_WINDOW} from './spatial-skeleton.js';
const COLORS={districts:'#556e36',routes:'#ac4f29',waterDefense:'#237887',sacredCivic:'#704b88'};
export function createSpatialSkeletonView({parent,controls,terrain,getSnapshot,getPhaseLabel=id=>id}){
 const button=document.createElement('button');button.type='button';button.textContent='空間骨架對照';button.setAttribute('aria-pressed','false');controls.append(button);
 const panel=document.createElement('section');panel.className='j3k-skeleton-panel';panel.id='j3k-spatial-skeleton';panel.hidden=true;button.setAttribute('aria-controls',panel.id);
 const title=document.createElement('h3');title.textContent='同一地形 · 同一比例 · 時代骨架';
 const note=document.createElement('p');note.textContent='底圖為現代 DEM（深色低、淺色高）。綠：已登記地區；橘：路徑；藍：水防位置；紫：公共核心。點僅標示意模型中心或來源概略區位，非測繪平面。虛線為模型布局包絡，非古城界。';
 const canvas=document.createElement('canvas');canvas.width=660;canvas.height=690;canvas.setAttribute('role','img');canvas.setAttribute('aria-label','共同現代地形上的時代空間骨架');
 const summary=document.createElement('p');summary.setAttribute('aria-live','polite');panel.append(title,note,canvas,summary);parent.append(panel);
 const background=document.createElement('canvas');background.width=canvas.width;background.height=canvas.height;
 const frame=SKELETON_WINDOW,w=frame.maxX-frame.minX,h=frame.maxZ-frame.minZ,px=x=>(x-frame.minX)/w*canvas.width,pz=z=>(z-frame.minZ)/h*canvas.height;
 const ctx=background.getContext('2d'),g=terrain.mesh.geometry,p=g.attributes.position,index=g.index;ctx.fillStyle='#e6dfcd';ctx.fillRect(0,0,canvas.width,canvas.height);
 for(let i=0;i<index.count;i+=3){const ids=[index.getX(i),index.getX(i+1),index.getX(i+2)],xs=ids.map(j=>p.getX(j)),zs=ids.map(j=>p.getZ(j));if(Math.max(...xs)<frame.minX||Math.min(...xs)>frame.maxX||Math.max(...zs)<frame.minZ||Math.min(...zs)>frame.maxZ)continue;const y=ids.reduce((s,j)=>s+p.getY(j),0)/3,t=Math.max(0,Math.min(1,y/300));ctx.fillStyle=`rgb(${Math.round(100+t*115)},${Math.round(112+t*85)},${Math.round(90+t*71)})`;ctx.beginPath();ids.forEach((j,n)=>n?ctx.lineTo(px(p.getX(j)),pz(p.getZ(j))):ctx.moveTo(px(p.getX(j)),pz(p.getZ(j))));ctx.closePath();ctx.fill();ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=.6;ctx.stroke();}
 let enabled=false,last=null;
 function refresh(){if(!enabled)return;const data=getSnapshot();if(!data)return;last=data;panel.dataset.phase=data.phaseId;title.textContent=`${getPhaseLabel(data.phaseId)} · 同一地形／同一比例`;canvas.setAttribute('aria-label',`${getPhaseLabel(data.phaseId)}的空間骨架示意`);const draw=canvas.getContext('2d');draw.clearRect(0,0,canvas.width,canvas.height);draw.drawImage(background,0,0);
  const e=data.layoutEnvelope;if(e){draw.strokeStyle='#423d33';draw.setLineDash([6,5]);draw.strokeRect(px(e.minX),pz(e.minZ),px(e.maxX)-px(e.minX),pz(e.maxZ)-pz(e.minZ));draw.setLineDash([]);}
  for(const f of data.features){draw.strokeStyle=COLORS[f.domain];draw.fillStyle=COLORS[f.domain];draw.lineWidth=2;draw.beginPath();if(f.kind==='point'){draw.arc(px(f.points[0].x),pz(f.points[0].z),4,0,Math.PI*2);draw.fill();}else{f.points.forEach((p,n)=>n?draw.lineTo(px(p.x),pz(p.z)):draw.moveTo(px(p.x),pz(p.z)));if(f.kind==='polygon')draw.closePath();draw.stroke();}}
  draw.fillStyle='#282b22';draw.font='16px sans-serif';draw.fillText('N ↑',12,24);draw.fillText('500m',12,canvas.height-15);draw.fillRect(12,canvas.height-10,500/w*canvas.width,3);
  const labels={districts:'地區',routes:'路徑',waterDefense:'水防',sacredCivic:'公共核心'};summary.textContent=Object.entries(data.domains).map(([key,d])=>`${labels[key]}：${d.spatialObjects} 項可定位示意／${d.gapIds.length} 項缺少可畫幾何`).join('；')+'。零項不代表歷史不存在；本圖只反映目前登記範圍。';
 }
 button.addEventListener('click',()=>{enabled=!enabled;button.setAttribute('aria-pressed',String(enabled));panel.hidden=!enabled;refresh();});
 return {refresh,diagnostics:()=>last?structuredClone(last):null,dispose(){button.remove();panel.remove();}};
}
