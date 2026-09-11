"""Westside Watch 8:5 motion stream using the verified local Codrops interaction."""
PAGE_ID='motion-codrops-site-8x5'

def _page():
    return {'id':PAGE_ID,'name':'Motion · Westside Watch 8:5','canvas':{'w':1440,'h':960},'nodes':[],'design_experiment':{'schema':'dore.design-experiment.v1','track':'motion-language','prototype':'westside-watch-8x5','status':'design-candidate','source':'local verified Codrops-motion reproduction','principles':['freeze-motion-engine','brand-content-only','eight-by-five','weighted-reading-stream','westside-watch','one-live-source-first-card','one-live-content-preview','one-signature-hold-slide-content']}}

def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        for p in w.get('pages',[]):
            if p.get('id')==PAGE_ID:p.update(_page());return base.save(w)
        w['pages'].append(_page());return base.save(w)
    base.workspace=workspace

def install_editor(html):return html

def render(edit=False):
    badge='<div class="dore-badge">DORÉ DESIGN · WESTSIDE WATCH · 8:5 MOTION</div>' if edit else ''
    base='https://tympanus.net/Tutorials/GridToFullPreview/assets/products/'
    items=[
      ('ONE','馬太福音第七章','讀取 ONE…','/one/?book=40&chapter=7'),
      ('JOURNAL','米斯巴','守望 · Journal','/journal/'),
      ('DAWN LIBRARY','黎明書局','Dawn Library','/website/dawn-library/'),
      ('FEATURE','看見','Feature · Journal','/journal/'),
      ('PRAYER','瑪拉拿','Prayer · Journal','/journal/'),
      ('WITNESS','見證人','Witness · Journal','/journal/'),
      ('DIALOGUE','守望者 · 對話','Dialogue · Journal','/journal/'),
      ('LIVING WATER','活水堂西區','Living Water Assembly West','/church/'),
    ]
    products=[];previews=[]
    for i,(kind,title,sub,href) in enumerate(items,1):
        idx=i-1
        one_attrs=' data-source="ONE" data-book="40" data-chapter="7"' if idx==0 else ''
        products.append(f'''<li class="product" data-name="{title}" data-kind="{kind}" data-sub="{sub}" data-href="{href}" data-index="{idx}"{one_attrs}><img src="{base}product-{i}.webp" alt=""><div class="brand-shade"></div><div class="brand-copy"><small>{kind}</small><strong>{title}</strong><span>{sub}</span></div></li>''')
        previews.append(''.join([f'<img data-id="{idx}" src="{base}product-{i}.webp" alt="">',f'<img data-id="{idx}" src="{base}product-{i}-detail-1.webp" alt="">',f'<img data-id="{idx}" src="{base}product-{i}-detail-2.webp" alt="">']))
    products=''.join(products);previews=''.join(previews)
    one_preview='''<article class="one-live-preview" hidden><div class="one-live-copy"><small>ONE · CHAPTER PREVIEW</small><h2 class="one-live-title"></h2><p class="one-live-passage"></p><p class="one-live-story"></p><ol class="one-live-route"></ol><span class="one-live-cta">進入 ONE 閱讀完整章節 →</span></div></article>'''
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Westside Watch · 8:5</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;min-height:100%;background:#eee8da;color:#252525;font-family:"Noto Serif TC",Georgia,serif}}body{{overflow-x:hidden}}.dore-badge{{position:fixed;z-index:99;top:8px;left:8px;background:#252525;color:#cebd74;padding:7px 9px;font:9px ui-monospace,monospace;letter-spacing:.12em}}.frame{{height:92px;display:grid;grid-template-columns:1fr auto auto;gap:30px;align-items:center;padding:0 4vw;border-bottom:1px solid rgba(37,37,37,.12)}}.frame h1{{font:26px "Cormorant Garamond",Georgia,serif;font-weight:400;margin:0;letter-spacing:.02em}}.frame span{{font:10px ui-monospace,monospace;letter-spacing:.13em;text-transform:uppercase}}.frame em{{font-style:normal;color:#8b8066}}.cats{{display:flex;justify-content:center;gap:25px;padding:14px 0 2px;font-size:13px}}.cats span:first-child{{color:#9b884c}}.products{{position:relative;min-height:calc(100vh - 108px);padding:48px}}.products__grid,.products__preview{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));grid-template-rows:repeat(2,auto);gap:5vw;align-content:center}}.products__grid{{list-style:none;margin:0;padding:0;min-height:calc(100vh - 204px)}}.product{{position:relative;aspect-ratio:8/5;overflow:hidden;background:#d7cfbd;transform:translate3d(0,0,0);will-change:transform,opacity;cursor:pointer}}.product>img{{width:100%;height:100%;display:block;object-fit:cover;filter:saturate(.58) contrast(.92)}}.brand-shade{{position:absolute;inset:0;background:linear-gradient(0deg,rgba(18,17,13,.78),rgba(18,17,13,.04) 70%)}}.brand-copy{{position:absolute;inset:0;padding:15px;display:flex;flex-direction:column;justify-content:flex-end;color:#f5f0e4;pointer-events:none}}.brand-copy small{{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#cebd74}}.brand-copy strong{{font:400 clamp(17px,1.55vw,27px) "Noto Serif TC",Georgia,serif;margin-top:4px}}.brand-copy span{{font:10px ui-monospace,monospace;opacity:.72;margin-top:5px}}.products__preview{{position:absolute;inset:48px;pointer-events:none;min-height:calc(100vh - 204px)}}.product-preview{{position:absolute;top:50%;width:calc(50% - 2.5vw);height:100%;transform:translateY(-50%);opacity:0;overflow:hidden;background:#171713;will-change:opacity,transform}}.product-preview.--left{{left:0}}.product-preview.--right{{right:0}}.product-preview__images{{position:absolute;inset:0;will-change:transform;z-index:1}}.product-preview__images img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;filter:saturate(.62)}}.product-preview__details{{position:absolute;z-index:4;left:22px;bottom:20px;color:#f4efe3;text-shadow:0 1px 8px #000}}.product-preview__details small{{font:9px ui-monospace,monospace;letter-spacing:.15em;color:#cebd74}}.product-preview__details p{{font-size:24px;margin:4px 0}}.product-preview__details span{{font:10px ui-monospace,monospace;opacity:.75}}.masked-preview{{position:absolute;inset:0;background:#eee8da;clip-path:polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%);will-change:clip-path;z-index:8}}
.one-live-preview{{position:absolute;top:0;right:0;bottom:0;width:54%;z-index:3;display:flex;padding:clamp(28px,3.2vw,54px);background:linear-gradient(90deg,rgba(238,232,218,.96),#eee8da 16%,#e8e0cf 100%);color:#252525;overflow:hidden;transform:translateX(102%);opacity:0;will-change:transform,opacity;box-shadow:-26px 0 58px rgba(24,21,15,.16)}}.one-live-preview[hidden]{{display:none}}.one-live-copy{{min-width:0;display:flex;flex-direction:column;justify-content:center}}.one-live-copy small{{font:9px ui-monospace,monospace;letter-spacing:.16em;color:#8d793f}}.one-live-copy h2{{font:400 clamp(27px,3vw,50px)/1 "Noto Serif TC",Georgia,serif;margin:12px 0 7px;max-width:10em}}.one-live-passage{{font:10px ui-monospace,monospace;letter-spacing:.07em;margin:0 0 19px;color:#6f654f}}.one-live-story{{font-size:clamp(12px,1vw,15px);line-height:1.75;max-width:38em;margin:0 0 16px}}.one-live-route{{list-style:none;margin:0;padding:0;border-top:1px solid rgba(37,37,37,.16)}}.one-live-route li{{display:grid;grid-template-columns:58px 1fr;gap:10px;padding:6px 0;border-bottom:1px solid rgba(37,37,37,.12);font-size:10px;line-height:1.4}}.one-live-route b{{font:9px ui-monospace,monospace;color:#8d793f}}.one-live-cta{{margin-top:16px;font:9px ui-monospace,monospace;letter-spacing:.08em;color:#5f543c}}.product-preview.is-one-live .product-preview__details{{transition:opacity .28s ease}}.product-preview.is-one-reading .product-preview__details{{opacity:0}}
@media(max-width:1100px){{.one-live-preview{{width:60%;padding:26px}}.one-live-copy h2{{font-size:34px}}.one-live-story{{font-size:12px}}}}@media(max-width:900px){{.products__grid{{grid-template-columns:repeat(2,1fr)}}.products__preview{{display:none}}.frame{{grid-template-columns:1fr}}.frame span,.frame em{{display:none}}}}
</style></head><body>{badge}<header class="frame"><h1>Westside Watch</h1><span>Watch for the Dawn</span><em>ONE · JOURNAL · DAWN LIBRARY · LIVING WATER</em></header><nav class="cats"><span>守望</span><span>查經</span><span>閱讀</span><span>見證</span><span>禱告</span><span>對話</span></nav><main class="products"><ul class="products__grid">{products}</ul><div class="products__preview"><div class="product-preview --left"><div class="product-preview__images">{previews}</div>{one_preview}<div class="product-preview__details"><small class="preview-kind"></small><p class="product-title"></p><span class="preview-sub"></span></div><div class="masked-preview"></div></div><div class="product-preview --right"><div class="product-preview__images">{previews}</div>{one_preview}<div class="product-preview__details"><small class="preview-kind"></small><p class="product-title"></p><span class="preview-sub"></span></div><div class="masked-preview"></div></div></div></main>
<script src="/one/one-data.js"></script><script src="/one/matthew-complete.js"></script>
<script>(()=>{{
 const card=document.querySelector('.product[data-source="ONE"][data-book="40"][data-chapter="7"]');
 const study=window.ONE_DATA?.matthew?.chapterStudies?.['7'];
 if(card&&study){{
   const title=study.title||window.ONE_DATA.matthew.chapters?.[6]||'馬太福音第七章';
   const passage=study.passage||'馬太福音 7';
   const sub=`${{passage}} · ${{study.movement||''}}`.replace(/ · $/,'');
   const href='/one/?book=40&chapter=7';
   const image=study.illustration?.src;
   card.dataset.name=title;card.dataset.kind='ONE · 馬太福音';card.dataset.sub=sub;card.dataset.href=href;
   card.querySelector('.brand-copy small').textContent='ONE · 馬太福音';card.querySelector('.brand-copy strong').textContent=title;card.querySelector('.brand-copy span').textContent=sub;
   if(image){{card.querySelector(':scope > img').src=image;card.querySelector(':scope > img').alt=study.illustration?.alt||title}}
   document.querySelectorAll('.product-preview').forEach(preview=>{{
     const pimgs=[...preview.querySelectorAll('.product-preview__images img[data-id="0"]')];
     pimgs.forEach(img=>{{if(image)img.src=image;img.alt=study.illustration?.alt||title}});
   }});
   document.querySelectorAll('.one-live-preview').forEach(panel=>{{
     panel.querySelector('.one-live-title').textContent=title;
     panel.querySelector('.one-live-passage').textContent=sub;
     panel.querySelector('.one-live-story').textContent=study.story||study.position||'';
     panel.querySelector('.one-live-route').innerHTML=(study.route||[]).slice(0,4).map(row=>`<li><b>${{row[0]||''}}</b><span>${{row[1]||''}}</span></li>`).join('');
   }});
   card.dataset.oneBound='true';document.documentElement.dataset.oneCard='matthew-7-live';
 }} else {{document.documentElement.dataset.oneCard='missing'}}
}})();</script>
<script>(()=>{{
 const products=[...document.querySelectorAll('.product')],left=document.querySelector('.product-preview.--left'),right=document.querySelector('.product-preview.--right');
 let timer=null,active=null,activeRect=null,gallery=null,phaseTimer=null,animations=[];
 const thick='polygon(45% 0,55% 0,55% 45%,100% 45%,100% 55%,55% 55%,55% 100%,45% 100%,45% 55%,0 55%,0 45%,45% 45%)',thin='polygon(50% 0,50% 0,50% 50%,100% 50%,100% 50%,50% 50%,50% 100%,50% 100%,50% 50%,0 50%,0 50%,50% 50%)';
 function stop(){{animations.forEach(a=>{{try{{a.cancel()}}catch(e){{}}}});animations=[]}}
 function pv(p){{let i=+p.dataset.index;return(i%4===0||i%4===1)?right:left}}
 function side(p){{return [p]}}
 function resetOne(preview){{clearTimeout(phaseTimer);phaseTimer=null;preview.classList.remove('is-one-live','is-one-reading');const panel=preview.querySelector('.one-live-preview'),images=preview.querySelector('.product-preview__images');if(panel){{panel.hidden=true;panel.style.transform='translateX(102%)';panel.style.opacity='0'}}if(images){{images.hidden=false;images.style.transform='translateX(0)'}}}}
 function setMode(preview,p){{resetOne(preview);const live=p.dataset.source==='ONE'&&p.dataset.oneBound==='true',panel=preview.querySelector('.one-live-preview');if(live){{preview.classList.add('is-one-live');panel.hidden=false;panel.style.transform='translateX(102%)';panel.style.opacity='0'}}return live}}
 function imgs(preview,id,cycle=true){{let all=[...preview.querySelectorAll('.product-preview__images img')];all.forEach(x=>x.style.opacity=0);let a=all.filter(x=>x.dataset.id==id),k=0;if(a.length)a[0].style.opacity=1;clearInterval(gallery);if(cycle)gallery=setInterval(()=>{{a.forEach(x=>x.style.opacity=0);if(a.length){{k=(k+1)%a.length;a[k].style.opacity=1}}}},500)}}
 function oneSecondAct(preview,p){{clearTimeout(phaseTimer);phaseTimer=setTimeout(()=>{{if(active!==p)return;const panel=preview.querySelector('.one-live-preview'),images=preview.querySelector('.product-preview__images');preview.classList.add('is-one-reading');animations.push(images.animate([{{transform:'translateX(0)'}},{{transform:'translateX(-38%)'}}],{{duration:760,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));animations.push(panel.animate([{{transform:'translateX(102%)',opacity:0}},{{transform:'translateX(0)',opacity:1}}],{{duration:760,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));document.documentElement.dataset.oneMotion='content'}} ,1650)}}
 function enter(p){{active=p;activeRect=p.getBoundingClientRect();stop();clearInterval(gallery);clearTimeout(phaseTimer);let preview=pv(p),s=side(p),id=+p.dataset.index,live=setMode(preview,p);preview.querySelector('.preview-kind').textContent=p.dataset.kind;preview.querySelector('.product-title').textContent=p.dataset.name;preview.querySelector('.preview-sub').textContent=p.dataset.sub;imgs(preview,id,!live);animations.push(preview.animate([{{opacity:0,transform:'translateY(-50%) scale(.94)'}},{{opacity:1,transform:'translateY(-50%) scale(1)'}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));let mask=preview.querySelector('.masked-preview');animations.push(mask.animate([{{clipPath:thick}},{{clipPath:thin}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));s.forEach(x=>{{let j=+x.dataset.index,col=j%4,row=j<4?0:1,dx=(col%2===0?1:-1)*2.5,dy=(row===0?1:-1)*2.5;animations.push(x.animate([{{opacity:1,transform:'translate(0,0)'}},{{opacity:0,transform:`translate(${{dx}}vw,${{dy}}vw)`}}],{{duration:650,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}))}});if(live){{document.documentElement.dataset.oneMotion='hold';oneSecondAct(preview,p)}}}}
 function leave(){{if(timer){{clearTimeout(timer);timer=null}}clearTimeout(phaseTimer);phaseTimer=null;if(!active){{activeRect=null;return}}stop();clearInterval(gallery);let p=active,preview=pv(p),s=side(p),mask=preview.querySelector('.masked-preview'),images=preview.querySelector('.product-preview__images'),panel=preview.querySelector('.one-live-preview');if(preview.classList.contains('is-one-reading')){{animations.push(images.animate([{{transform:getComputedStyle(images).transform==='none'?'translateX(-38%)':getComputedStyle(images).transform}},{{transform:'translateX(0)'}}],{{duration:420,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));animations.push(panel.animate([{{transform:'translateX(0)',opacity:1}},{{transform:'translateX(102%)',opacity:0}}],{{duration:420,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}))}}animations.push(preview.animate([{{opacity:1,transform:'translateY(-50%) scale(1)'}},{{opacity:0,transform:'translateY(-50%) scale(.94)'}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));animations.push(mask.animate([{{clipPath:thin}},{{clipPath:thick}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}));s.forEach(x=>{{let cs=getComputedStyle(x);animations.push(x.animate([{{opacity:cs.opacity,transform:cs.transform==='none'?'translate(0,0)':cs.transform}},{{opacity:1,transform:'translate(0,0)'}}],{{duration:520,easing:'cubic-bezier(.65,0,.2,1)',fill:'forwards'}}))}});setTimeout(()=>resetOne(preview),530);active=null;activeRect=null;document.documentElement.dataset.oneMotion='idle'}}
 function leaveOutsideActive(e){{if(!active||!activeRect)return;const x=e.clientX,y=e.clientY;if(x<activeRect.left||x>activeRect.right||y<activeRect.top||y>activeRect.bottom)leave()}}
 products.forEach(p=>{{p.addEventListener('mouseenter',()=>{{clearTimeout(timer);timer=setTimeout(()=>{{enter(p);timer=null}},100)}});p.addEventListener('mouseleave',leave);p.addEventListener('click',()=>{{location.href=p.dataset.href}})}});
 document.addEventListener('pointermove',leaveOutsideActive,{{passive:true}});document.documentElement.addEventListener('mouseleave',leave);window.addEventListener('blur',leave);document.documentElement.dataset.motion='ready';document.documentElement.dataset.oneMotion='idle'
}})();</script></body></html>'''