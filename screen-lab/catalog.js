/* Doré Screen Lab — isolated catalog, no main-site cinema dependencies. */
(() => {
  const demo = [
    ['經典電影選集','電影','#6d5146','#b3a28a'],['城市與記憶','紀錄片','#4b6061','#b8b4a3'],
    ['光影之間','電影','#3c4656','#a08b75'],['遠方的故事','劇集','#6a6053','#c4ad8b'],
    ['動畫短篇','動畫','#596e69','#c2a18b'],['歷史的現場','紀錄片','#6a493e','#a9a38a'],
    ['夜色與旅人','電影','#303f4d','#867f79'],['人間紀事','劇集','#64634b','#b2a183'],
    ['大地回聲','紀錄片','#53634e','#a3a38c'],['時間的邊界','電影','#554d66','#b5a6a0'],
    ['紙上的世界','動畫','#72594f','#b9ac98'],['第二幕','劇集','#4d555e','#c0ad91']
  ].map(([title,type,a,b]) => ({title,type,a,b,year:'概念示意',description:'設計佔位項目，並非實際電影或已驗證片源。',demo:true}));
  const categories=['全部','電影','劇集','紀錄片','動畫','短片'];
  const grid=document.getElementById('grid'),filters=document.getElementById('filters'),search=document.getElementById('search');
  const dialog=document.getElementById('detail'),status=document.getElementById('catalog-status');
  const urlInput=document.getElementById('stream-url'),playForm=document.getElementById('stream-form');
  let films=demo,active='全部';
  const https = v => {try {const u=new URL(v);return u.protocol==='https:'?u.href:null;}catch{return null;}};
  const mediaUrl=v=>{const u=https(v);return u && /\.(m3u8|mp4|m4v|webm|ogv|ogg)$/i.test(new URL(u).pathname)?u:null;};
  function youtubeId(value) {
    const url=https(value);if(!url)return null;
    const u=new URL(url),host=u.hostname.toLowerCase().replace(/^www\./,'');
    let id=null;
    if(host==='youtu.be')id=u.pathname.split('/')[1];
    if(host==='youtube.com'||host==='m.youtube.com'||host==='youtube-nocookie.com'){
      id=u.pathname==='/watch'?u.searchParams.get('v'):u.pathname.match(/^\/(?:embed|shorts|live)\/([^/]+)/)?.[1];
    }
    return /^[A-Za-z0-9_-]{11}$/.test(id||'')?id:null;
  }
  function normalize(raw) {
    if (!Array.isArray(raw)) throw Error('片庫必須是 JSON 陣列');
    if (raw.length>500) throw Error('一次最多載入 500 部作品');
    return raw.map((f,i)=>{
      if (!f || typeof f!=='object' || typeof f.title!=='string' || !f.title.trim()) throw Error('第 '+(i+1)+' 筆缺少片名');
      const type=categories.includes(f.type)&&f.type!=='全部'?f.type:'電影';
      return {title:f.title.trim().slice(0,160),type,year:String(f.year||'').slice(0,30),description:String(f.description||'').slice(0,1000),
        poster:https(f.poster)||(youtubeId(f.source)?'https://i.ytimg.com/vi/'+youtubeId(f.source)+'/hqdefault.jpg':null),stream:mediaUrl(f.stream),youtube:youtubeId(f.source),source:https(f.source),verified:false,a:'#4d555b',b:'#b6a58b',demo:false};
    });
  }
  function setFilter(v){active=v;render();}
  function render(){
    filters.replaceChildren();
    for(const c of categories){const b=document.createElement('button');b.type='button';b.textContent=c;b.setAttribute('aria-pressed',String(c===active));b.onclick=()=>setFilter(c);filters.append(b);}
    grid.replaceChildren();const q=search.value.trim().toLocaleLowerCase();
    const chosen=films.filter(f=>(active==='全部'||f.type===active)&&[f.title,f.type,f.year].join(' ').toLocaleLowerCase().includes(q));
    document.getElementById('count').textContent=chosen.length+' TITLES';
    if(!chosen.length){const p=document.createElement('p');p.textContent='沒有符合條件的影片。';grid.append(p);}
    for(const f of chosen){
      const b=document.createElement('button');b.type='button';b.className='tile';
      const poster=document.createElement('div');poster.className='poster';poster.style.setProperty('--a',f.a);poster.style.setProperty('--b',f.b);
      const label=document.createElement('span');label.textContent=f.title;
      if(f.poster){const img=document.createElement('img');img.src=f.poster;img.alt='';img.loading='lazy';img.referrerPolicy='no-referrer';img.className='poster-image';img.onerror=()=>img.remove();poster.append(img);}
      poster.append(label);
      const name=document.createElement('strong');name.textContent=f.title;
      const meta=document.createElement('small');meta.textContent=[f.year,f.type,f.stream?'待驗證片源':f.youtube?'YouTube 官方播放器':f.demo?'示意封面':'來源待驗證'].filter(Boolean).join(' · ');
      b.append(poster,name,meta);b.onclick=()=>openDetail(f);grid.append(b);
    }
  }
  function openDetail(f){
    document.getElementById('title').textContent=f.title;
    document.getElementById('meta').textContent=[f.year,f.type].filter(Boolean).join(' / ');
    document.getElementById('description').textContent=f.description||'尚無介紹';
    const host=document.getElementById('player');host.replaceChildren();
    const box=document.createElement('div');box.className='detail-actions';
    const info=document.createElement('p');info.textContent=f.stream?'已提供直接媒體連結，但尚未確認可播放。':'沒有可直接播放的媒體來源。';
    box.append(info);
    if(f.stream){const btn=document.createElement('button');btn.textContent='前往線上試映 ↗';btn.onclick=()=>{
      closeDetail();urlInput.value=f.stream;document.querySelector('#stream-title').scrollIntoView({behavior:'smooth'});
      playForm.requestSubmit();
    };box.append(btn);}
    if(f.youtube){
      const btn=document.createElement('button');btn.type='button';btn.textContent='使用 YouTube 官方播放器 ↗';
      btn.onclick=()=>{
        const frame=document.createElement('iframe');
        frame.src='https://www.youtube-nocookie.com/embed/'+f.youtube+'?autoplay=1';
        frame.title=f.title+' — YouTube 播放器';frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';
        frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';
        frame.style.cssText='width:100%;aspect-ratio:16/9;border:0';
        host.replaceChildren(frame);
      };box.append(btn);
    }
    if(f.source){const link=document.createElement('a');link.href=f.source;link.target='_blank';link.rel='noopener noreferrer';link.textContent='查看來源網站 ↗';box.append(link);}
    host.append(box);dialog.showModal();
  }
  function closeDetail(){dialog.close();document.getElementById('player').replaceChildren();}
  document.getElementById('detail-close').onclick=closeDetail;
  dialog.addEventListener('close',()=>document.getElementById('player').replaceChildren());
  document.querySelectorAll('[data-screen-filter]').forEach(button => button.addEventListener('click', () => setFilter(button.dataset.screenFilter)));
  search.addEventListener('input',render);
  document.getElementById('catalog-file').addEventListener('change',async e=>{
    const file=e.target.files?.[0];if(!file)return;
    if(file.size>1024*1024){status.textContent='檔案不可超過 1 MB';return;}
    try {films=normalize(JSON.parse(await file.text()));active='全部';search.value='';status.textContent='已載入 '+films.length+' 筆資料（僅本次頁面有效，不會上傳或儲存）。';render();}
    catch(err){status.textContent='片庫格式錯誤：'+err.message;}
    e.target.value='';
  });
  document.getElementById('film-add-form').addEventListener('submit', e => {
    e.preventDefault();
    const form=e.currentTarget, raw=Object.fromEntries(new FormData(form));
    if(!raw.title?.trim()){status.textContent='請輸入片名。';return;}
    for(const key of ['poster','stream','source']){
      if(raw[key]?.trim() && !https(raw[key].trim())){status.textContent=key+' 必須是 HTTPS 網址。';return;}
    }
    if(raw.stream?.trim() && !mediaUrl(raw.stream.trim())){status.textContent='影片來源須為直接 HTTPS 媒體網址（MP4、WebM、Ogg 或 HLS）。';return;}
    try {
      const film=normalize([raw])[0];
      if(films.length>=500)throw Error('片庫已達 500 筆上限');
      films=[film,...films];active='全部';search.value='';form.reset();render();
      status.textContent='已加入「'+film.title+'」，只保留在本次頁面。';
    }catch(err){status.textContent='無法加入：'+err.message;}
  });
  document.getElementById('catalog-export').addEventListener('click',()=>{
    const payload=films.filter(f=>!f.demo).map(({title,type,year,description,poster,stream,source})=>({title,type,year,description,poster,stream,source}));
    if(!payload.length){status.textContent='目前沒有可匯出的正式片庫項目；請先新增或匯入影片。';return;}
    const blob=new Blob([JSON.stringify(payload,null,2)],{type:'application/json'});
    const href=URL.createObjectURL(blob),a=document.createElement('a');a.href=href;a.download='screen-lab-catalog.json';
    document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(href),1000);
    status.textContent='已匯出 '+payload.length+' 筆片庫資料。這是 JSON 資料檔，不包含影片。';
  });
  async function loadCurated(){
    try {
      const response=await fetch('./curated.json',{cache:'no-store'});
      if(!response.ok)throw Error('HTTP '+response.status);
      const curated=normalize(await response.json());
      films=curated;active='全部';render();
      status.textContent='已載入 '+curated.length+' 部真實開放電影作品。未驗證的海報或播放來源不會標示為可播放。';
    }catch(err){
      status.textContent='真實片庫載入失敗；暫時顯示示意海報。'+err.message;
    }
  }
  document.getElementById('catalog-reset').onclick=()=>{search.value='';loadCurated();};
  render();loadCurated();
})();
