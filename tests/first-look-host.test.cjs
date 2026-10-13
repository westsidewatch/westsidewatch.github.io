const {test}=require('node:test');const assert=require('node:assert/strict');const vm=require('node:vm');const fs=require('node:fs');
function runtime(){
 const state={top:0,alignments:0,heights:0},events={},queue=[];
 const anchor={getBoundingClientRect:()=>({top:state.top}),scrollIntoView(){state.top=0;state.alignments++}};
 const style={};Object.defineProperty(style,'height',{get(){return this.value},set(value){this.value=value;state.heights++;state.top+=50}});
 const frame={style,contentWindow:{postMessage(){}},getBoundingClientRect:()=>({top:0,height:900}),addEventListener(){}};
 const location={hash:'#first-look-life',origin:'https://westsidewatch.github.io'};
 const window={addEventListener(name,fn){(events[name]||=[]).push(fn)}};
 const document={querySelectorAll:()=>[frame],getElementById:()=>anchor};
 vm.runInNewContext(fs.readFileSync('static/js/first-look-host.js','utf8'),{window,document,location,requestAnimationFrame(fn){queue.push(fn);return queue.length}});
 const flush=()=>{while(queue.length)queue.shift()()},emit=(name,event)=>{for(const fn of events[name]||[])fn(event);flush()};flush();
 return {state,frame,emit,location};
}
test('Lazy frame resize keeps the requested realm at the viewport top',()=>{const {state,frame,emit,location}=runtime();emit('message',{origin:location.origin,source:frame.contentWindow,data:{type:'ws-first-look:height',height:1200}});assert.equal(state.top,0);assert.equal(state.alignments,2)});
test('Ordinary scrolling never pulls the user back to a realm anchor',()=>{const {state,frame,emit,location}=runtime();state.top=-360;emit('scroll');assert.equal(state.top,-360);assert.equal(state.alignments,1);emit('message',{origin:location.origin,source:frame.contentWindow,data:{type:'ws-first-look:height',height:1200}});assert.equal(state.alignments,1)});
test('Foreign frame messages cannot resize a First Look',()=>{const {state,frame,emit}=runtime();emit('message',{origin:'https://unrelated.example',source:frame.contentWindow,data:{type:'ws-first-look:height',height:1200}});assert.equal(state.heights,0)});
