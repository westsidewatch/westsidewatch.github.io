/* Dawn Living Wall runtime v1 — lazy shards + bounded DOM. */
export class DawnLivingWall {
  constructor(rootUrl='/static/dawn-library/living/root.json',{windowCards=84,prefetchAhead=1}={}){
    this.rootUrl=rootUrl;this.windowCards=windowCards;this.prefetchAhead=prefetchAhead;this.root=null;this.cache=new Map();this.loading=new Map();
  }
  async init(){
    const r=await fetch(this.rootUrl,{cache:'no-cache'});if(!r.ok)throw new Error(`Dawn root ${r.status}`);
    this.root=await r.json();
    if(this.root.admissionAuthority!==false||this.root.projectionOnly!==true)throw new Error('Dawn projection boundary violated');
    await this.loadShard(0);return this;
  }
  async loadShard(index){
    if(!this.root)throw new Error('Dawn root not initialized');
    if(index<0||index>=this.root.shards.length)return null;
    if(this.cache.has(index))return this.cache.get(index);
    if(this.loading.has(index))return this.loading.get(index);
    const p=(async()=>{const meta=this.root.shards[index],r=await fetch(meta.href);if(!r.ok)throw new Error(`Dawn shard ${index+1} ${r.status}`);const data=await r.json();if(data.admissionAuthority!==false||data.projectionOnly!==true||data.workCount!==data.workRefs.length)throw new Error('Dawn shard boundary violated');this.cache.set(index,data);this.loading.delete(index);return data})();
    this.loading.set(index,p);return p;
  }
  shardForOffset(offset){return Math.floor(Math.max(0,offset)/this.root.shardSize)}
  async window(offset=0,count=this.windowCards){
    if(!this.root)await this.init();count=Math.min(count,this.windowCards);const end=Math.min(this.root.canonicalWorkCount,offset+count),a=this.shardForOffset(offset),b=this.shardForOffset(Math.max(offset,end-1));let refs=[];
    for(let i=a;i<=b;i++){const s=await this.loadShard(i);refs.push(...s.workRefs)}
    const base=a*this.root.shardSize,visible=refs.slice(offset-base,offset-base+(end-offset));
    for(let i=1;i<=this.prefetchAhead;i++)this.loadShard(b+i).catch(()=>{});
    return {offset,count:visible.length,total:this.root.canonicalWorkCount,refs:visible};
  }
  async render(container,offset,renderCard){
    const w=await this.window(offset);const frag=document.createDocumentFragment();
    for(const ref of w.refs)frag.append(renderCard(ref));
    container.replaceChildren(frag);container.dataset.dawnOffset=String(w.offset);container.dataset.dawnVisible=String(w.count);container.dataset.dawnTotal=String(w.total);return w;
  }
  releaseFarFrom(offset){
    if(!this.root)return;const center=this.shardForOffset(offset);for(const key of this.cache.keys())if(Math.abs(key-center)>this.prefetchAhead+1)this.cache.delete(key);
  }
}
