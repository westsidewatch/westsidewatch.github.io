// Structure/provenance gate only: NEVER substitutes for human editorial review.
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
export function check(d) {
 const e=[],fail=s=>e.push(s), ids=new Set();
 if(d?.schema!=="dawn.editorial-reading-lists.v1")fail("invalid schema");
 if(d?.editorialFirst!==true)fail("editorial-first requirement");
 if(d?.publicationGate!=="human-review-only")fail("human publication gate");
 if(!Array.isArray(d?.archetypes)||d.archetypes.length<16)fail("insufficient editorial archetypes");
 for(const s of d?.archetypes??[]){
  if(ids.has(s.id))fail("duplicate archetype "+s.id);ids.add(s.id);
  for(const k of ["title","question","criteria","redFlag"])if(typeof s[k]!=="string"||s[k].length<3)fail("missing "+k+" on "+s.id);
  if(s.status!=="editorial-concept-only")fail("unapproved editorial status "+s.id);
 }
 const refs=new Set((d?.references??[]).map(r=>r.id));
 if((d?.pilots?.length??0)<3)fail("insufficient distinct pilots");
 for(const p of d?.pilots??[]){
  if(!ids.has(p.archetype))fail("unknown archetype "+p.id);
  for(const k of ["question","thesis","reader","notFor","tradeoff","rejectExample"])if(typeof p[k]!=="string"||p[k].length<3)fail("missing "+k+" on "+p.id);
  if((p.sample?.length??0)<2)fail("pilot lacks comparative works "+p.id);
  for(const ref of p.methodEvidence??[])if(!refs.has(ref))fail("unknown evidence "+ref);
  for(const w of p.sample??[]){
    for(const k of ["title","author","role","caution"])if(typeof w[k]!=="string"||!w[k])fail("incomplete work "+p.id+" "+k);
    for(const k of ["downloadUrl","accessUrl","price","free","publiclyRecommended"])if(Object.hasOwn(w,k))fail("source-driven/published field "+k);
    if(w.recommender&&!w.recommendationEvidence)fail("unattributed recommender");
    if(w.recommendationEvidence&&!refs.has(w.recommendationEvidence))fail("unverified attribution key");
  }
 }
 if(d?.sourcePolicy?.stage!=="after-editorial-judgement")fail("source-first policy disallowed");
 return e;
}
const self=fileURLToPath(import.meta.url);
if(process.argv[1]&&path.resolve(process.argv[1])===self){
 const p=path.resolve(process.argv[2]??path.join(path.dirname(self),"..","docs","dawn-library","editorial-booklist-studio.v1.json"));
 const errors=check(JSON.parse(fs.readFileSync(p,"utf8")));
 if(errors.length){errors.forEach(s=>console.error("FAIL",s));process.exitCode=1;}else console.log("PASS editorial-first structural gate");
}
