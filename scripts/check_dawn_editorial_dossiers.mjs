// Checks that a reader-centered editorial dossier is a substantive comparison,
// not a provider-sourced list or a claim of completed human editorial review.
// A passing run is NOT a literary/theological quality certification.
import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";
export function validateDossiers(d) {
 const errors=[], add=x=>errors.push(x);
 if(d?.schema!=="dawn.editorial-reading-dossiers.v1")add("invalid dossier schema");
 if(d?.stage!=="editorial_research_not_publication")add("only pre-publication dossier status permitted");
 if(!d?.basis?.includes("reader-question-first"))add("source-first instead of reader-first");
 if(!Array.isArray(d?.lists)||d.lists.length<2)add("two contrasting editorial lists required");
 const ids=new Set(), slugs=new Set();
 for(const l of d?.lists??[]){
  if(ids.has(l.id))add("duplicate list ID "+l.id);ids.add(l.id);
  if(slugs.has(l.slug))add("duplicate list slug "+l.slug);slugs.add(l.slug);
  for(const k of ["title","method","readerQuestion","thesis","audience","nonAudience","editorialSequence"])if(!l[k]||l[k].length<9)add("missing editorial "+k+" for "+l.id);
  if(l.reviewStatus!=="research_shortlist_with_primary_text_spotchecks")add("unapproved review status "+l.id);
  if(!Array.isArray(l.excluded)||l.excluded.length<2)add("no justified exclusions "+l.id);
  if(!Array.isArray(l.books)||l.books.length<6)add("books too few "+l.id);
  const bookIds=new Set(),works=new Set();
  for(const b of l.books??[]){
   if(bookIds.has(b.id))add("duplicate work in list "+b.id);bookIds.add(b.id);
   const sameWork=(b.workTitle||b.title).toLowerCase();
   if(works.has(sameWork))add("duplicate canonical work "+sameWork);works.add(sameWork);
   for(const k of ["title","workTitle","author","role","judgement","counterpoint","comparison","readerLevel","textReviewed"])if(typeof b[k]!=="string"||b[k].length<(k==="readerLevel"?2:5))add("missing "+k+" on "+b.id);
   if(!Array.isArray(b.evidence)||b.evidence.length<1)add("no bibliographic/research evidence "+b.id);
   else for(const u of b.evidence)if(!/^https:\/\//.test(u))add("evidence not official https URL "+b.id);
   for(const k of ["downloadUrl","readerUrl","freePdf","imageUrl","bookPrice","freeAccess","publicApproved","awardWinner"])if(Object.hasOwn(b,k))add("access/claim leaked into editorial stage "+b.id+" "+k);
  }
  for(const x of l.excluded??[])if((x.reason||"").length<20)add("exclusion without editorial reasoning "+l.id);
  if((l.readingQuestions?.length??0)<3)add("not enough reading questions "+l.id);
 }
 return errors;
}
const script=fileURLToPath(import.meta.url);
if(process.argv[1]&&path.resolve(process.argv[1])===script){
 const target=path.resolve(process.argv[2]??path.join(path.dirname(script),"..","docs","dawn-library","reading-lists","reading-list-dossiers-v1.json"));
 const failures=validateDossiers(JSON.parse(fs.readFileSync(target,"utf8")));
 if(failures.length){failures.forEach(x=>console.error("FAIL",x));process.exitCode=1;}
 else console.log("PASS: two research-stage editorial booklist dossiers, comparative reasons and evidence");
}
