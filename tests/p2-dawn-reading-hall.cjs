/* P2 05 Reading Room smoke/interaction gate. node tests/p2-dawn-reading-hall.cjs */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const ROOT=path.resolve(__dirname,'../static');
const js=fs.readFileSync(path.join(ROOT,'js/p2-0105-dawn-continuation.js'),'utf8');
const html=fs.readFileSync(path.join(ROOT,'experiments/p2-0105-dawn-preview.html'),'utf8');
const css=fs.readFileSync(path.join(ROOT,'css/p2-0105-dawn-integrated.css'),'utf8');
const living=JSON.parse(fs.readFileSync(path.join(ROOT,'dawn-library/living/root.json'),'utf8'));
assert.equal(living.classification.roots.length,7);
assert.equal(living.classification.roots.reduce((n,r)=>n+r.children.length,0),42);
for(const id of ['dawn-second__press--motherform','dawn-department-grid','dawn-open-catalogue','dawn-wall-grid']){
 assert(html.includes(id), 'Missing hall HTML '+id);
}
assert.equal((html.match(/data-dawn-portal=/g)||[]).length,3,'preserve original three portals');
assert(!html.includes('dawn-room-heading')&&!html.includes('dawn-reading-room__masthead'),'No duplicate L2 brand heading; scripture plates own section identity');
assert(js.includes("if(tile.dataset.dawnPortal)openCollection(tile.dataset.dawnPortal)"));
assert(js.includes('livingSubjectBooks(child.id'),'reuse verified canonical Living category leaves');
assert(css.includes('var(--ws-harvest)')&&css.includes('var(--ws-paper)'),'OS tokens must be used');
assert(js.includes("void mountReadingDepartments();"),'mount at current reader opening');
const start=js.indexOf(" // P2 Reading Room: original Living 7-root taxonomy");
const end=js.indexOf(" const ChineseCategoryLabel=",start);
assert(start>0&&end>start,'real production reader module location');
const source=js.slice(start,end);
class Element {
 constructor(tag){this.tagName=tag;this.children=[];this.handlers={};this.dataset={};this.attrs={};this.textContent='';this.className='';}
 append(...x){this.children.push(...x);}
 replaceChildren(...x){this.children=x.flatMap(y=>y.fragment?y.children:[y]);}
 addEventListener(k,cb){this.handlers[k]=cb;}
 setAttribute(k,v){this.attrs[k]=v;}
}
const grid=new Element('nav'),status=new Element('p'),workcount=new Element('strong');
const nodes={'#dawn-department-grid':grid,'#dawn-department-status':status,'#dawn-hall-workcount':workcount};
const $=key=>nodes[key]||null;
const calls={open:0,render:0,display:[]};
const openCollection=()=>{calls.open++};
const displayClassificationGroup=group=>calls.display.push(group.id);
const renderCatalogueClassification=async()=>{calls.render++};
const classificationTree={roots:living.classification.roots};
const document={createElement:tag=>new Element(tag),createDocumentFragment:()=>Object.assign(new Element('fragment'),{fragment:true})};
const fetch=async url=>{
 assert.equal(url,'/dawn-library/living/root.json');
 return {ok:true,json:async()=>living};
};
const load=new Function('$','document','fetch','openCollection','renderCatalogueClassification','classificationTree','displayClassificationGroup','console',source+"\nreturn mountReadingDepartments;");
(async()=>{
 const mount=load($,document,fetch,openCollection,renderCatalogueClassification,classificationTree,displayClassificationGroup,console);
 await mount();
 assert.equal(grid.children.length,7,'seven visible interactive departments');
 assert.equal(workcount.textContent,'203,448');
 assert.equal(status.textContent,'');
 for(let i=0;i<7;i++){
  const b=grid.children[i];
  assert.equal(b.dataset.subjectId,living.classification.roots[i].id);
  b.handlers.click();
 }
 await new Promise(resolve=>setImmediate(resolve));
 assert.equal(calls.open,7);
 assert.equal(calls.render,7);
 assert.deepEqual(calls.display,living.classification.roots.map(r=>r.id));
 await mount();
 assert.equal(grid.children.length,7,'mount idempotent');
 console.log('PASS: 7 original Living roots / 42 children; 3 channels preserved; all department clicks route to original classification');
})().catch(e=>{console.error(e);process.exitCode=1});
