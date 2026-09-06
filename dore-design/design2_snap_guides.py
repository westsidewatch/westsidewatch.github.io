#!/usr/bin/env python3
"""Dependency-free snap, guides and multi-select augmentation for Design 2.0 canvas."""

CSS='''<style id="d2-snap-guides-css">
.d2-multi-selected{outline:1px solid rgba(180,154,85,.68)!important;outline-offset:2px}
.d2-guide{position:absolute;z-index:9997;pointer-events:none;background:#b49a55;display:none}.d2-guide.v{top:0;bottom:0;width:1px}.d2-guide.h{left:0;right:0;height:1px}.d2-guide.show{display:block}
#d2-selection[data-count]:after{content:attr(data-count) " selected";position:absolute;left:0;top:-22px;background:#171814;color:#d8c27a;padding:3px 6px;border-radius:4px;font:9px ui-monospace,monospace;white-space:nowrap}
</style>'''

JS=r'''<script id="d2-snap-guides-js">(()=>{
const canvas=document.querySelector('.canvas');if(!canvas)return;
const SNAP=6;let selected=[],primary=null,gesture=null;
const gv=document.createElement('div'),gh=document.createElement('div');gv.className='d2-guide v';gh.className='d2-guide h';canvas.append(gv,gh);
const nodes=()=>[...canvas.querySelectorAll('[data-id]')];
function mark(){nodes().forEach(n=>n.classList.toggle('d2-multi-selected',selected.includes(n)));const b=document.querySelector('#d2-selection');if(b){if(selected.length>1)b.dataset.count=selected.length;else delete b.dataset.count}}
function setSelection(n,add){if(!add)selected=[n];else if(selected.includes(n))selected=selected.filter(x=>x!==n);else selected.push(n);if(!selected.length)selected=[n];primary=n;mark()}
function guidesOff(){gv.classList.remove('show');gh.classList.remove('show')}
function candidates(n){const outX=[0,600,1200],outY=[0,1140,2280];for(const o of nodes()){if(o===n||selected.includes(o))continue;outX.push(o.offsetLeft,o.offsetLeft+o.offsetWidth/2,o.offsetLeft+o.offsetWidth);outY.push(o.offsetTop,o.offsetTop+o.offsetHeight/2,o.offsetTop+o.offsetHeight)}return {x:outX,y:outY}}
function nearest(value,arr){let best=null,dist=Infinity;for(const a of arr){const d=Math.abs(a-value);if(d<dist){dist=d;best=a}}return dist<=SNAP?best:null}
function snapPrimary(n){const c=candidates(n),left=n.offsetLeft,top=n.offsetTop,w=n.offsetWidth,h=n.offsetHeight;const xs=[left,left+w/2,left+w],ys=[top,top+h/2,top+h];let sx=null,sy=null,dx=0,dy=0;for(const x of xs){const m=nearest(x,c.x);if(m!==null){sx=m;dx=m-x;break}}for(const y of ys){const m=nearest(y,c.y);if(m!==null){sy=m;dy=m-y;break}}if(sx!==null){n.style.left=Math.round(left+dx)+'px';gv.style.left=Math.round(sx)+'px';gv.classList.add('show')}else gv.classList.remove('show');if(sy!==null){n.style.top=Math.round(top+dy)+'px';gh.style.top=Math.round(sy)+'px';gh.classList.add('show')}else gh.classList.remove('show');return {dx,dy}}
canvas.addEventListener('pointerdown',e=>{const n=e.target.closest('[data-id]');if(!n)return;setSelection(n,e.shiftKey);gesture={x:e.clientX,y:e.clientY,starts:new Map(selected.map(x=>[x,{l:x.offsetLeft,t:x.offsetTop}]))};});
canvas.addEventListener('pointermove',e=>{if(!gesture||!primary)return;const st=gesture.starts.get(primary);if(!st)return;const moved=Math.abs(e.clientX-gesture.x)+Math.abs(e.clientY-gesture.y)>1;if(!moved)return;for(const n of selected){if(n===primary)continue;const s=gesture.starts.get(n);if(!s)continue;n.style.left=Math.round(s.l+(primary.offsetLeft-st.l))+'px';n.style.top=Math.round(s.t+(primary.offsetTop-st.t))+'px'}const beforeL=primary.offsetLeft,beforeT=primary.offsetTop,{dx,dy}=snapPrimary(primary);if(dx||dy){for(const n of selected){if(n===primary)continue;n.style.left=Math.round(n.offsetLeft+dx)+'px';n.style.top=Math.round(n.offsetTop+dy)+'px'}}mark();});
async function saveAll(){if(selected.length<2)return;for(const n of selected){await fetch('/api/workspace',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({op:'set_node',page_id:'multiwrite-home',id:n.dataset.id,patch:{x:n.offsetLeft,y:n.offsetTop,w:n.offsetWidth,h:n.offsetHeight}})})}parent.postMessage({type:'dore-saved',page_id:'multiwrite-home'},'*')}
canvas.addEventListener('pointerup',()=>{guidesOff();if(gesture&&selected.length>1)saveAll();gesture=null});
addEventListener('keydown',e=>{if(e.key==='Escape'){selected=[];primary=null;mark();guidesOff()}});
})()</script>'''

def augment(html):
    if 'class="canvas"' not in html or 'data-id=' not in html:return html
    return html.replace('</head>',CSS+'</head>',1).replace('</body>',JS+'</body>',1)
