const ROOT='../cover-preview/root.json';
const WINDOW=72;
const BUFFER=24;

const json=async url=>{const r=await fetch(url,{cache:'force-cache'});if(!r.ok)throw new Error(`cover stream ${r.status}: ${url}`);return r.json()};
const esc=s=>String(s??'').replace(/[&<>\"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;'}[c]));

export async function createDawnCoverStream(host,{onSelect}={}){
  const root=await json(ROOT), cache=new Map();
  host.classList.add('dawn-cover-stream');
  host.innerHTML='<div class="dawn-cover-stream__status">Loading collection…</div><div class="dawn-cover-stream__rail"></div><div class="dawn-cover-stream__sentinel" aria-hidden="true"></div>';
  const rail=host.querySelector('.dawn-cover-stream__rail'),status=host.querySelector('.dawn-cover-stream__status'),sentinel=host.querySelector('.dawn-cover-stream__sentinel');
  let cursor=0, visible=[], loading=false;
  const shardFor=index=>root.shards.find(s=>index>=s.offset&&index<s.offset+s.count);
  async function shard(s){if(!s)return null;if(!cache.has(s.href))cache.set(s.href,json(`../cover-preview/${s.href}`));return cache.get(s.href)}
  async function slice(start,count){const end=Math.min(root.workCount,start+count),out=[];let p=start;while(p<end){const meta=shardFor(p);if(!meta)break;const data=await shard(meta),local=p-meta.offset,take=Math.min(end-p,meta.count-local);out.push(...data.items.slice(local,local+take));p+=take}return out}
  const card=(x,i)=>{const cover=x.cover?.src?`<img src="${esc(x.cover.src)}" alt="" loading="lazy" decoding="async">`:'<span class="dawn-cover-stream__fallback"></span>';return `<button class="dawn-cover-stream__work" data-i="${i}" data-work-id="${esc(x.workId)}">${cover}<span><strong>${esc(x.title)}</strong><small>${esc((x.authors||[]).join(' · '))}</small></span></button>`};
  function render(){rail.innerHTML=visible.map((x,i)=>card(x,i)).join('');rail.querySelectorAll('[data-i]').forEach(b=>b.onclick=()=>onSelect?.(visible[+b.dataset.i]));status.textContent=`${Math.min(cursor,root.workCount).toLocaleString()} / ${root.workCount.toLocaleString()} works · ${root.shardCount} shards`;}
  async function advance(){if(loading||cursor>=root.workCount)return;loading=true;try{const rows=await slice(cursor,WINDOW);cursor+=rows.length;visible.push(...rows);if(visible.length>WINDOW+BUFFER)visible=visible.slice(-(WINDOW+BUFFER));render()}finally{loading=false}}
  const io=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting))advance()},{root:host,rootMargin:'800px 0px'});io.observe(sentinel);await advance();
  return {root,advance,destroy(){io.disconnect();cache.clear()},get cursor(){return cursor}};
}
