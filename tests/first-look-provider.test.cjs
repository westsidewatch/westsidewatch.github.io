const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
function runtime(){
 const element=tag=>({tag,currentTime:0,dataset:{},children:[],events:{},replaceChildren(){this.children=[]},appendChild(n){this.children.push(n)},append(n){this.children.push(n)},setAttribute(){},addEventListener(name,fn){this.events[name]=fn},canPlayType(){return 'maybe'},play(){this.playCalls=(this.playCalls||0)+1;return Promise.resolve()}});
 const document={querySelector(){return null},createElement:element,head:element('head')},window={location:{href:'https://westsidewatch.github.io/cinema/'}};
 vm.runInNewContext(fs.readFileSync('cinema/provider-adapters.js','utf8'),{document,window,URL});
 return {provider:window.HolyLightProviders,target:element('div')};
}
test('First Look mounts a real official player without autoplay or an extra host play action',()=>{
 const {provider,target}=runtime();const item={title:'Film',providerSources:[{provider:'youtube',embed:true,official:true,embedUrl:'https://www.youtube-nocookie.com/embed/abcdefghijk'}]};
 const {frame}=provider.mount(target,item,0,{autoplay:false});
 assert.equal(target.children[0],frame);assert.equal(new URL(frame.src).searchParams.get('autoplay'),'0');assert.ok(frame.allow.includes('autoplay'));
 assert.equal(new URL(provider.mount(target,item).frame.src).searchParams.get('autoplay'),'1');
});
test('Official non-YouTube source pointers stay intact',()=>{
 const {provider,target}=runtime(),url='https://example.org/player?refId=canonical-film';
 const mounted=provider.mount(target,{title:'Film',providerSources:[{provider:'official',embed:true,embedUrl:url}]},0,{autoplay:false});
 assert.equal(mounted.frame.src,url);
});
test('Manual native playback preserves timing and caption tracks',()=>{
 const {provider,target}=runtime();const item={title:'Film',providerSources:[{provider:'hls',streamUrl:'https://example.org/film.m3u8',subtitleTracks:[{src:'/film.zh.vtt',srclang:'zh-Hant',label:'繁體中文',default:true}]}]};
 const {video}=provider.mount(target,item,42,{autoplay:false});
 assert.equal(video.autoplay,false);assert.equal(video.controls,true);assert.equal(video.children[0].srclang,'zh-Hant');
 video.events.loadedmetadata();assert.equal(video.currentTime,42);assert.equal(video.playCalls,undefined);
 assert.equal(provider.mount(target,item).video.autoplay,true);
});
