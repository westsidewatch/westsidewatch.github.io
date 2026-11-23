import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
const directory="static/dawn-library/reading-room/";
const pages=["index.html","gospel-essentials.html","inner-life.html","church-history.html","three-stars.html","spectrum-abiding.html","jerusalem-3000.html"];
const read=f=>fs.readFileSync(path.join(root,f),"utf8");
const html=Object.fromEntries(pages.map(p=>[p,read(directory+p)]));
const dossier=JSON.parse(read("docs/dawn-library/reading-lists/reading-list-dossiers-v1.json"));
const covers=JSON.parse(read("static/experiments/dawn-reading-lists/edition-cover-review.v1.json"));
const stars=JSON.parse(read("docs/dawn-library/first-issue-three-stars.v1.json"));
const exhibit=JSON.parse(read("static/experiments/dawn-reading-lists/jerusalem-3000-source.json"));
test("three genuine Chinese editorial lists with 22 work entries",()=>{
 assert.equal(dossier.lists.length,3);
 assert.deepEqual(Object.fromEntries(dossier.lists.map(x=>[x.slug,x.books.length])),{"inner-life":9,"church-history":7,"gospel-essentials":6});
 assert.equal(covers.works.length,22);
});
test("seven distinct readable pages use the same Design OS",()=>{
 for(const [name,text] of Object.entries(html)){assert.ok(text.includes("<main"),name+" lacks main");assert.ok(text.includes('href="/css/westside-design-os.css"'),name+" lacks Design OS");assert.ok(text.includes("</html>"),name+" does not close HTML");}
});
test("all local magazine links and within-page book anchors resolve",()=>{
 for(const [name,text] of Object.entries(html)) for(const [,raw] of text.matchAll(/href="([^"]+)"/g)){
   const link=raw.replaceAll("&amp;","&");
   if(!link.startsWith("./"))continue;
   const [target,anchor]=link.slice(2).split("#");
   assert.ok(!target||pages.includes(target)||["magazine.css","launch.css"].includes(target),name+" links to absent local resource "+link);
   if(anchor)assert.ok((target?html[target]:text)?.includes('id="'+anchor+'"'),name+" broken anchor "+link);
 }
});
test("every chosen work retains its editorial recommendation in the public article",()=>{
 for(const l of dossier.lists){const text=html[l.slug+".html"];
  for(const work of l.books){assert.ok(text.includes('id="'+work.id+'"'),work.id+" missing");assert.ok(text.includes(work.judgement),work.id+" lost recommendation");assert.ok(text.includes(work.counterpoint),work.id+" lost reading guide");}
 }
});
test("three stars are handpicked, cross three lists, and not a supplier ranking",()=>{
 assert.equal(stars.works.length,3);
 assert.deepEqual(stars.works.map(w=>w.id),["gospel-02","inner-05-chinese","history-01"]);
 for(const w of stars.works){assert.ok(w.main.length>=45,"recommendation too brief for "+w.id);assert.ok(html["three-stars.html"].includes(w.main));}
});
test("spectrum is substantive scripture study, not a tag directory",()=>{
 const s=html["spectrum-abiding.html"];
 for(const phrase of ["約翰福音15","希臘文","葡萄樹","舊約","彼此相愛","講道預備"])assert.ok(s.includes(phrase),phrase+" missing");
 assert.ok((s.match(/dl-research-chapter/g)||[]).length>=5);
});
test("Jerusalem exhibition preserves all eighteen distinct scenes",()=>{
 assert.equal(exhibit.items.length,18);
 const h=html["jerusalem-3000.html"];
 for(const x of exhibit.items)assert.ok(h.includes('id="'+x.id+'"'),"missing original curated scene "+x.id);
});
test("editorial reader pages omit internal engineering language",()=>{
 for(const [name,s] of Object.entries(html))for(const x of ["編輯試刊校樣","PENDING CI","Core Contract","PR #","校樣"])assert.equal(s.includes(x),false,name+" displays "+x);
});
test("access support follows editorial content",()=>{
 for(const n of ["gospel-essentials.html","inner-life.html","church-history.html"]){
  const s=html[n];assert.ok(s.indexOf('class="dl-support"')>s.indexOf('class="dl-end"'),"support precedes review "+n);
 }
});
