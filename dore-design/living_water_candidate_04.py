"""Living Water Candidate 04 — weighted Doré currents with verifiable light-engine trials."""
import html
import living_water_candidate as c01

PAGE_ID='living-water-candidate-04'
ITEMS=[
('a','SCRIPTURE','起初，光進入黑暗。',21,2,'center 42%','#'),('a','JOURNAL','守望',39,1,'center 35%','/journal/'),('a','PRAYER','儆醒',46,1,'center 55%','#'),('a','FEATURE','一座光明的城',75,2,'center 46%','/journal/'),
('b','ONE','查經',93,1,'center 38%','/one/'),('b','DAYLIGHT CAFE','共享',115,2,'center 42%','#'),('b','STUDY','同行',122,1,'center 35%','#'),('b','DAWN LIBRARY','黎明書局',127,3,'center 55%','#'),
('c','STORY','看見',164,1,'center 46%','/journal/'),('c','VIDEO','影像',170,1,'center 38%','#'),('c','JOURNAL','見證人',186,2,'center 42%','/journal/'),('c','DIALOGUE','對話',192,1,'center 35%','#'),
('d','PRAYER','你們要禱告',198,2,'center 55%','#'),('d','HYMN','頌讚',216,1,'center 46%','#'),('d','MARANATHA','主啊，我願你來。',224,3,'center 38%','#'),('d','CHURCH','Living Water',237,1,'center 42%','/church/')]
STREAM_META={'a':('.24','-.11'),'b':('.14','-.36'),'c':('.19','-.02'),'d':('.11','-.22')}

def page():
    return {'id':PAGE_ID,'name':'Living Water · Candidate 04','canvas':{'w':1440,'h':960},'nodes':[], 'design_experiment':{'schema':'dore.design-experiment.v1','track':'living-water-homepage','candidate':'04','status':'design-candidate','source':'user-direction-2026-09-09','principles':['inherit-c01-after-page2','four-horizontal-currents','journal-four-movements-internal-only','never-show-W-labels','8:5-weighted-rhythm','editorial-item-model','per-item-dore-original','D-react-bits-lightrays-classic-webgl','no-esm-runtime-dependency','runtime-fps-probe','C-unverified','light-over-content','no-third-party-demo-iframe','first-layer-only']}}

def install_workspace(base):
    original=base.workspace
    def workspace():
        w=original()
        if not any(p.get('id')==PAGE_ID for p in w.get('pages',[])): w['pages'].append(page());w=base.save(w)
        return w
    base.workspace=workspace

def install_editor(doc): return doc.replace("'living-water-candidate-03'])","'living-water-candidate-03','living-water-candidate-04'])")

def tile_markup(item):
    stream,kind,title,dore,weight,crop,href=item
    return '<a class="tile" href="%s" data-dore="%s" data-weight="%s" data-crop="%s"><div class="tcopy"><span class="index">%s</span><h3>%s</h3></div></a>'%(html.escape(href,quote=True),dore,weight,html.escape(crop,quote=True),html.escape(kind),html.escape(title))

def nav_markup():
    groups=[]
    for key in 'abcd':
        speed,origin=STREAM_META[key]
        body=''.join(tile_markup(x) for x in ITEMS if x[0]==key)
        groups.append('<div class="stream-wrap %s" data-speed="%s" data-origin="%s"><div class="stream %s">%s</div></div>'%(key,speed,origin,key,body))
    return '<section class="live-nav" id="liveNav"><div class="live-nav-stage"><div class="dore-river-bg" aria-hidden="true"><img id="riverPlateA" class="river-plate" alt=""><img id="riverPlateB" class="river-plate" alt=""></div><div class="dawn-horizon"></div><div class="live-water"><div class="current-line l1"></div><div class="current-line l2"></div><div class="current-line l3"></div><div class="current-line l4"></div>%s</div><div class="light-engine c off" id="lightC" aria-hidden="true"></div><div class="light-engine d" id="lightD" aria-hidden="true"><canvas id="lightRaysCanvas"></canvas></div><div class="light-switch"><span id="lightStatus">D STARTING</span><button type="button" data-light="c">C · God Rays</button><button type="button" class="on" data-light="d">D · LightRays</button><button type="button" data-light="off">Off</button></div></div></section>'%''.join(groups)

CSS=r'''
.live-nav{height:280svh;position:relative;background:#1b1a16;color:#f5f0e3;isolation:isolate}.live-nav-stage{position:sticky;top:0;height:100svh;overflow:hidden;background:#1b1a16}.dore-river-bg{position:absolute;inset:-7%;z-index:0;overflow:hidden;pointer-events:none}.river-plate{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center top;filter:grayscale(1) contrast(1.02) brightness(.62);opacity:0;transform:translate3d(0,2%,0) scale(1.10);transition:opacity 2.2s ease,transform 22s linear}.river-plate.on{opacity:.27;transform:translate3d(0,-5%,0) scale(1.13)}.dore-river-bg:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(22,21,16,.58),rgba(22,21,16,.18) 35%,rgba(22,21,16,.24) 68%,rgba(22,21,16,.62)),linear-gradient(180deg,rgba(22,21,16,.38),rgba(22,21,16,.08) 44%,rgba(22,21,16,.50))}.dawn-horizon{position:absolute;z-index:2;left:-6vw;right:-6vw;top:0;height:1px;background:linear-gradient(90deg,transparent 2%,rgba(206,189,116,.22) 18%,rgba(255,239,177,.76) 50%,rgba(206,189,116,.28) 82%,transparent 98%);box-shadow:0 0 24px rgba(206,189,116,.28);pointer-events:none}.live-water{--tile-h:20vh;--unit:calc(var(--tile-h)*1.6);--gap:.9vw;height:100svh;position:relative;z-index:4;overflow:hidden}.stream-wrap{position:absolute;left:0;width:max-content;will-change:transform;transform:translate3d(var(--scroll-x,0px),0,0)}.stream-wrap.a{top:3vh}.stream-wrap.b{top:27vh}.stream-wrap.c{top:51vh}.stream-wrap.d{top:75vh}.stream{display:flex;gap:var(--gap);width:max-content;animation:ambient-a 38s linear infinite;animation-delay:-7s}.stream-wrap.b .stream{animation-name:ambient-b;animation-duration:50s;animation-delay:-23s}.stream-wrap.c .stream{animation-name:ambient-c;animation-duration:43s;animation-delay:-31s}.stream-wrap.d .stream{animation-name:ambient-d;animation-duration:58s;animation-delay:-17s}.tile{height:var(--tile-h);width:var(--unit);position:relative;overflow:hidden;flex:0 0 auto;border:1px solid rgba(242,231,190,.34);background:#25231d center/cover no-repeat;box-shadow:0 16px 55px rgba(0,0,0,.14);isolation:isolate;color:inherit;text-decoration:none;transition:transform .55s cubic-bezier(.2,.75,.2,1),border-color .55s}.tile[data-weight="2"]{width:calc(var(--unit)*2 + var(--gap))}.tile[data-weight="3"]{width:calc(var(--unit)*3 + var(--gap)*2)}.tile:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(110deg,rgba(255,242,190,.07),rgba(22,21,17,.18) 45%,rgba(238,225,177,.03));mix-blend-mode:screen}.tile:after{content:"";position:absolute;inset:0;z-index:2;background:linear-gradient(0deg,rgba(11,10,8,.80),rgba(12,11,9,.30) 50%,rgba(12,11,9,.08))}.tile .tcopy{position:absolute;z-index:3;left:1.25vw;right:1.25vw;bottom:1vw}.tile h3{font-size:clamp(21px,2vw,36px);font-weight:400;line-height:.92;margin:.12em 0;text-shadow:0 2px 18px rgba(0,0,0,.52)}.tile[data-weight="2"] h3{font-size:clamp(25px,2.5vw,44px)}.tile[data-weight="3"] h3{font-size:clamp(29px,3.15vw,56px);max-width:18ch}.tile .index{font-size:8px;letter-spacing:.18em;color:rgba(238,220,154,.88)}.tile:hover{transform:translateY(-7px) scale(1.012);border-color:rgba(226,207,126,.86)}.current-line{position:absolute;z-index:1;left:-10vw;right:-10vw;height:1px;background:linear-gradient(90deg,transparent,rgba(206,189,116,.10) 10%,rgba(255,236,169,.48) 46%,rgba(206,189,116,.17) 82%,transparent)}.current-line.l1{top:25vh}.current-line.l2{top:49vh;opacity:.78}.current-line.l3{top:73vh;opacity:.58}.current-line.l4{top:97vh;opacity:.40}.light-engine{position:absolute;inset:0;z-index:7;pointer-events:none;overflow:hidden;mix-blend-mode:screen}.light-engine canvas{position:absolute;inset:0;width:100%!important;height:100%!important;display:block}.light-engine.d{opacity:.72}.light-engine.off{display:none}.light-switch{position:fixed;right:24px;top:70px;z-index:2147483000;display:flex;align-items:center;gap:7px;padding:7px;background:rgba(18,17,13,.90);border:1px solid rgba(206,189,116,.62);backdrop-filter:blur(10px)}#lightStatus{min-width:118px;color:#cebd74;font:9px ui-monospace,monospace;letter-spacing:.08em;text-align:right}.light-switch button{border:1px solid rgba(206,189,116,.45);background:#171714;color:#e3dcc8;padding:8px 11px;font:10px ui-monospace,monospace;cursor:pointer}.light-switch button.on{background:#cebd74;color:#171714}@keyframes ambient-a{from{transform:translate3d(1vw,0,0)}to{transform:translate3d(-11vw,0,0)}}@keyframes ambient-b{from{transform:translate3d(-8vw,0,0)}to{transform:translate3d(5vw,0,0)}}@keyframes ambient-c{from{transform:translate3d(2vw,0,0)}to{transform:translate3d(-9vw,0,0)}}@keyframes ambient-d{from{transform:translate3d(-5vw,0,0)}to{transform:translate3d(7vw,0,0)}}@media(max-width:760px){.live-nav{height:260svh}.live-water{--tile-h:16.5vh;--gap:2.2vw}.tile[data-weight="3"]{width:calc(var(--unit)*2.25 + var(--gap)*1.25)}.stream-wrap.a{top:4vh}.stream-wrap.b{top:27vh}.stream-wrap.c{top:50vh}.stream-wrap.d{top:73vh}.light-switch{right:10px;top:58px;max-width:calc(100vw - 20px);flex-wrap:wrap}}@media(prefers-reduced-motion:reduce){.stream,.stream-wrap{animation:none!important;transform:none!important}.light-engine{display:none!important}}
'''

JS=r'''<script src="/one/one-dore-cover-registry.js"></script><script src="/one/one-dore-assets-241.js"></script><script>
(function(){
var s=document.getElementById('liveNav');if(!s)return;
var R=window.ONE_DORE_COVER_REGISTRY;
function src(id,w){return R&&R.files&&R.files[id]?'https://commons.wikimedia.org/wiki/Special:Redirect/file/'+encodeURIComponent(R.files[id])+'?width='+(w||1200):''}
s.querySelectorAll('.tile[data-dore]').forEach(function(t){var u=src(+t.dataset.dore,(+t.dataset.weight||1)>1?1800:1000);if(u){t.style.backgroundImage='url("'+u.replace(/"/g,'%22')+'")';t.style.backgroundPosition=t.dataset.crop||'center'}});
var ids=[1,7,21,39,46,75,93,115,122,127,164,170,186,192,198,216,224,237,240,241].filter(function(x){return R&&R.files&&R.files[x]}),a=document.getElementById('riverPlateA'),b=document.getElementById('riverPlateB'),front=a,back=b,n=0;
if(ids.length){function show(img,id,done){img.classList.remove('on');img.src=src(id,1920);img.onload=function(){requestAnimationFrame(done)};img.onerror=done}function next(){n=(n+1)%ids.length;show(back,ids[n],function(){front.classList.remove('on');back.classList.add('on');var t=front;front=back;back=t;setTimeout(next,18000)})}show(front,ids[0],function(){front.classList.add('on');setTimeout(next,18000)})}
var wraps=[].slice.call(s.querySelectorAll('.stream-wrap')),raf=0;
function update(){raf=0;var r=s.getBoundingClientRect(),range=Math.max(1,s.offsetHeight-innerHeight),p=Math.max(0,Math.min(1,-r.top/range));wraps.forEach(function(w){var sp=+w.dataset.speed||.15,o=+w.dataset.origin||0,dir=w.classList.contains('b')||w.classList.contains('d')?1:-1;w.style.setProperty('--scroll-x',((o+dir*p*sp)*innerWidth).toFixed(2)+'px')})}
function q(){if(!raf)raf=requestAnimationFrame(update)}addEventListener('scroll',q,{passive:true});addEventListener('resize',q);update();
var C=document.getElementById('lightC'),D=document.getElementById('lightD'),status=document.getElementById('lightStatus'),mode='d';
s.querySelectorAll('[data-light]').forEach(function(btn){btn.onclick=function(){mode=btn.dataset.light;C.classList.toggle('off',mode!=='c');D.classList.toggle('off',mode!=='d');s.querySelectorAll('[data-light]').forEach(function(x){x.classList.toggle('on',x===btn)});if(mode==='c')status.textContent='C NOT VERIFIED';else if(mode==='off')status.textContent='LIGHT OFF';else status.textContent='D STARTING'}});
var canvas=document.getElementById('lightRaysCanvas');
try{
  var gl=canvas.getContext('webgl',{alpha:true,antialias:false,premultipliedAlpha:false});if(!gl)throw new Error('WebGL unavailable');
  var vs='attribute vec2 p;void main(){gl_Position=vec4(p,0.0,1.0);}';
  var fs='precision highp float;uniform float iTime;uniform vec2 iResolution;uniform vec2 rayPos;uniform vec2 rayDir;uniform vec2 mousePos;uniform vec3 raysColor;uniform float raysSpeed;uniform float lightSpread;uniform float rayLength;uniform float mouseInfluence;uniform float distortion;uniform float pulsating;float strength(vec2 s,vec2 d,vec2 c,float a,float b,float sp){vec2 v=c-s;vec2 n=normalize(v);float ca=dot(n,d);float dc=ca+distortion*sin(iTime*2.0+length(v)*0.01)*0.2;float sf=pow(max(dc,0.0),1.0/max(lightSpread,0.001));float dist=length(v);float md=iResolution.x*rayLength;float lf=clamp((md-dist)/md,0.0,1.0);float pulse=pulsating>0.5?(0.8+0.2*sin(iTime*sp*3.0)):1.0;float base=clamp((0.45+0.15*sin(dc*a+iTime*sp))+(0.3+0.2*cos(-dc*b+iTime*sp)),0.0,1.0);return base*lf*sf*pulse;}void main(){vec2 c=vec2(gl_FragCoord.x,iResolution.y-gl_FragCoord.y);vec2 md=normalize(mousePos*iResolution.xy-rayPos);vec2 fd=normalize(mix(rayDir,md,mouseInfluence));float r1=strength(rayPos,fd,c,36.2214,21.11349,1.5*raysSpeed);float r2=strength(rayPos,fd,c,22.3991,18.0234,1.1*raysSpeed);float e=r1*0.5+r2*0.4;float br=1.0-c.y/iResolution.y;vec3 col=e*vec3(0.28+br*0.72,0.34+br*0.66,0.18+br*0.52)*raysColor;float alpha=clamp(e*0.72,0.0,0.68);gl_FragColor=vec4(col,alpha);}';
  function shader(type,txt){var sh=gl.createShader(type);gl.shaderSource(sh,txt);gl.compileShader(sh);if(!gl.getShaderParameter(sh,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(sh));return sh}
  var prog=gl.createProgram();gl.attachShader(prog,shader(gl.VERTEX_SHADER,vs));gl.attachShader(prog,shader(gl.FRAGMENT_SHADER,fs));gl.linkProgram(prog);if(!gl.getProgramParameter(prog,gl.LINK_STATUS))throw new Error(gl.getProgramInfoLog(prog));gl.useProgram(prog);
  var buf=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buf);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,3,-1,-1,3]),gl.STATIC_DRAW);var pl=gl.getAttribLocation(prog,'p');gl.enableVertexAttribArray(pl);gl.vertexAttribPointer(pl,2,gl.FLOAT,false,0,0);
  var U={time:gl.getUniformLocation(prog,'iTime'),res:gl.getUniformLocation(prog,'iResolution'),pos:gl.getUniformLocation(prog,'rayPos'),dir:gl.getUniformLocation(prog,'rayDir'),mouse:gl.getUniformLocation(prog,'mousePos'),color:gl.getUniformLocation(prog,'raysColor'),speed:gl.getUniformLocation(prog,'raysSpeed'),spread:gl.getUniformLocation(prog,'lightSpread'),len:gl.getUniformLocation(prog,'rayLength'),mi:gl.getUniformLocation(prog,'mouseInfluence'),dist:gl.getUniformLocation(prog,'distortion'),pulse:gl.getUniformLocation(prog,'pulsating')};
  var mouse=[.5,.5],smooth=[.5,.5],frames=0,lastFps=performance.now();
  function resize(){var r=D.getBoundingClientRect(),dpr=Math.min(devicePixelRatio||1,1.5),w=Math.max(2,Math.floor(r.width*dpr)),h=Math.max(2,Math.floor(r.height*dpr));if(canvas.width!==w||canvas.height!==h){canvas.width=w;canvas.height=h;gl.viewport(0,0,w,h)}}
  addEventListener('resize',resize);addEventListener('mousemove',function(e){var r=D.getBoundingClientRect();if(r.width&&r.height)mouse=[(e.clientX-r.left)/r.width,(e.clientY-r.top)/r.height]},{passive:true});resize();
  function draw(now){requestAnimationFrame(draw);if(mode!=='d')return;resize();smooth[0]=smooth[0]*.92+mouse[0]*.08;smooth[1]=smooth[1]*.92+mouse[1]*.08;var t=now*.001,w=canvas.width,h=canvas.height;gl.useProgram(prog);gl.uniform1f(U.time,t);gl.uniform2f(U.res,w,h);gl.uniform2f(U.pos,w*.50,-h*.20);gl.uniform2f(U.dir,0.0,1.0);gl.uniform2f(U.mouse,smooth[0],smooth[1]);gl.uniform3f(U.color,.88,.78,.42);gl.uniform1f(U.speed,1.25);gl.uniform1f(U.spread,.48);gl.uniform1f(U.len,2.1);gl.uniform1f(U.mi,.10);gl.uniform1f(U.dist,.26);gl.uniform1f(U.pulse,1.0);gl.drawArrays(gl.TRIANGLES,0,3);frames++;if(now-lastFps>600){var fps=Math.round(frames*1000/(now-lastFps));status.textContent='D RUNNING · '+fps+' FPS';frames=0;lastFps=now}}
  requestAnimationFrame(draw);
}catch(err){D.classList.add('off');status.textContent='D ERROR';console.warn('D LightRays runtime failed',err)}
})();
</script>'''

def render(edit=False):
    doc=c01.render(edit);marker='<section class="world dark">'
    if marker not in doc:return doc
    doc=doc.replace(marker,nav_markup()+marker,1)
    doc=doc.replace('</style>',CSS+'</style>',1)
    doc=doc.replace('</body>',JS+'</body>',1)
    return doc
