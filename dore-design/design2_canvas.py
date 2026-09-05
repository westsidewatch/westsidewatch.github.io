"""DORÉ DESIGN 2.0 direct-manipulation canvas adapter.

Stage A deliberately uses pointer events with zero runtime dependency. It proves
our document-coordinate/command boundary before Moveable/Selecto are vendored.
The adapter contract can later be replaced without changing workspace data.
"""
from html import escape

CSS='''<style id="dore2-canvas-style">
[data-d2-node]{cursor:move;touch-action:none}[data-d2-node].d2-selected{outline:2px solid #8c6818!important;outline-offset:4px}.d2-handle{position:absolute;width:12px;height:12px;right:-8px;bottom:-8px;border:2px solid #fff;background:#8c6818;box-shadow:0 0 0 1px #5d4715;cursor:nwse-resize;z-index:9999}.d2-guide-x,.d2-guide-y{position:absolute;pointer-events:none;z-index:9998;background:rgba(140,104,24,.65);display:none}.d2-guide-x{top:0;bottom:0;width:1px}.d2-guide-y{left:0;right:0;height:1px}
</style>'''

JS=r'''<script id="dore2-canvas-js">(()=>{
const PAGE=document.body.dataset.d2Page,REV=()=>Number(document.body.dataset.d2Revision||0),canvas=document.querySelector('.canvas');if(!canvas||!PAGE)return;
let selected=null,gesture=null;const gx=document.createElement('i'),gy=document.createElement('i');gx.className='d2-guide-x';gy.className='d2-guide-y';canvas.append(gx,gy);
const num=(el,k)=>parseFloat(el.dataset[k]||0),scale=()=>{const r=canvas.getBoundingClientRect();return r.width/canvas.offsetWidth||1};
function select(el){document.querySelectorAll('.d2-selected').forEach(x=>x.classList.remove('d2-selected'));document.querySelectorAll('.d2-handle').forEach(x=>x.remove());selected=el;if(!el)return;el.classList.add('d2-selected');const h=document.createElement('b');h.className='d2-handle';el.appendChild(h);parent.postMessage({type:'dore-select',page_id:PAGE,id:el.dataset.id,field:'text',value:el.innerText},'*')}
function guides(x,y,w,h){const cx=x+w/2,cy=y+h/2,CW=canvas.offsetWidth,CH=canvas.offsetHeight;gx.style.display=Math.abs(cx-CW/2)<7?'block':'none';gx.style.left=(CW/2)+'px';gy.style.display=Math.abs(cy-CH/2)<7?'block':'none';gy.style.top=(CH/2)+'px';return {x:Math.abs(cx-CW/2)<7?CW/2-w/2:x,y:Math.abs(cy-CH/2)<7?CH/2-h/2:y}}
function hideGuides(){gx.style.display=gy.style.display='none'}
async function commit(patch){if(!selected)return;parent.postMessage({type:'dore2-command',expected_revision:REV(),command:{op:'node.patch',page_id:PAGE,id:selected.dataset.id,patch}},'*')}
canvas.addEventListener('pointerdown',e=>{const el=e.target.closest('[data-d2-node]');if(!el){select(null);return}e.preventDefault();select(el);const s=scale(),resize=e.target.classList.contains('d2-handle');gesture={id:e.pointerId,resize,sx:e.clientX,sy:e.clientY,x:num(el,'x'),y:num(el,'y'),w:num(el,'w'),h:num(el,'h')||el.offsetHeight,s};el.setPointerCapture(e.pointerId)});
canvas.addEventListener('pointermove',e=>{if(!gesture||!selected||e.pointerId!==gesture.id)return;const dx=(e.clientX-gesture.sx)/gesture.s,dy=(e.clientY-gesture.sy)/gesture.s;if(gesture.resize){const w=Math.max(12,gesture.w+dx),h=Math.max(12,gesture.h+dy);selected.style.width=w+'px';selected.style.height=h+'px';selected.dataset.previewW=w;selected.dataset.previewH=h}else{let x=gesture.x+dx,y=gesture.y+dy;const snapped=guides(x,y,gesture.w,gesture.h);x=snapped.x;y=snapped.y;selected.style.left=x+'px';selected.style.top=y+'px';selected.dataset.previewX=x;selected.dataset.previewY=y}});
canvas.addEventListener('pointerup',e=>{if(!gesture||!selected||e.pointerId!==gesture.id)return;const p=gesture.resize?{w:Number(selected.dataset.previewW||gesture.w),h:Number(selected.dataset.previewH||gesture.h)}:{x:Number(selected.dataset.previewX||gesture.x),y:Number(selected.dataset.previewY||gesture.y)};hideGuides();gesture=null;commit(p)});
parent.postMessage({type:'dore2-direct-ready',page_id:PAGE,revision:REV()},'*');
})()</script>'''


def augment(html,page_id,revision):
    """Mark rendered nodes and inject direct-manipulation behavior."""
    html=html.replace('</head>',CSS+'</head>',1)
    html=html.replace('<body ',f'<body data-d2-page="{escape(str(page_id))}" data-d2-revision="{int(revision)}" ',1)
    # Existing editable text nodes already carry data-id. Rules/blocks receive
    # data-id from the renderer in the next adapter phase; Stage A targets text.
    html=html.replace('data-id="','data-d2-node="1" data-x="0" data-y="0" data-w="0" data-id="')
    return html.replace('</body>',JS+'</body>',1)
