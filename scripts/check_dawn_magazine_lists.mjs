// Dawn magazine booklists: structure gate, not browser/image-rights certification.
import fs from "node:fs"; import path from "node:path"; import { fileURLToPath } from "node:url";
const ROOT=path.resolve(path.dirname(fileURLToPath(import.meta.url)),"..");
export function checkReadingListProofs(dossiers,covers,pages){
 const errs=[], fail=s=>errs.push(s), registry=new Map(covers.works.map(x=>[x.workId,x]));
 if(dossiers.lists.length<2)fail("two independently readable magazine features required");
 if(covers.works.length!==dossiers.lists.flatMap(x=>x.books).length)fail("cover/access record cardinality mismatch");
 if(new Set(covers.works.map(x=>x.workId)).size!==covers.works.length)fail("duplicate work identity");
 if(covers.editorialIndependentOfLinks!==true)fail("editing must not depend on access inventory");
 for(const list of dossiers.lists){
  const page=pages[list.slug];
  if(!page){fail("missing magazine page "+list.slug);continue;}
  for(const phrase of ["dl-hero","dl-intro","dl-entry","dl-end","dl-support","為什麼推薦","怎樣閱讀","從書單走進書局"])if(!page.includes(phrase))fail("incomplete editorial structure "+list.slug+" "+phrase);
  if(page.indexOf('class="dl-support"')<page.indexOf('class="dl-end"'))fail("access must follow editorial publication "+list.slug);
  if(page.includes("純色封面")||page.includes("下載失敗")||page.includes("PENDING CI"))fail("engineering copy in reader page");
  for(const b of list.books){
    const r=registry.get(b.id);
    if(!r){fail("missing cover/access record "+b.id);continue;}
    if(!page.includes('id="'+b.id+'"'))fail("book absent from magazine page "+b.id);
    if(!b.judgement||!page.includes(b.judgement))fail("lost recommendation rationale "+b.id);
    if(!b.counterpoint||!page.includes(b.counterpoint))fail("lost reading guide "+b.id);
    if(r.cover.src&&!/^https:\/\//.test(r.cover.src))fail("invalid cover URL "+b.id);
    if(r.cover.src&&(!r.cover.credit||!r.cover.sourceStatus))fail("unattributed cover "+b.id);
    if(r.cover.src&&!page.includes(r.cover.src.replaceAll("&","&amp;")))fail("verified cover reference absent from HTML "+b.id);
    if(r.cover.reusePermission==="approved"&&r.cover.renderVerified!==true)fail("unearned publication clearance "+b.id);
    if(r.readingSupport.freeChineseTextUrl&&!r.readingSupport.freeChineseTextVerified)fail("unverified free reading claim "+b.id);
  }
 }
 return errs;
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const read=p=>fs.readFileSync(path.join(ROOT,p),"utf8"),d=JSON.parse(read("docs/dawn-library/reading-lists/reading-list-dossiers-v1.json"));
 const c=JSON.parse(read("static/experiments/dawn-reading-lists/edition-cover-review.v1.json"));
 const pages={};
 for(const l of d.lists)pages[l.slug]=read("static/experiments/dawn-reading-lists/"+l.slug+".html");
 const failures=checkReadingListProofs(d,c,pages);
 if(failures.length){failures.forEach(x=>console.error("FAIL",x));process.exitCode=1;}
 else console.log("PASS: two reader-facing editorial magazine proofs; cover references; independent access appendix");
}
