/* Scripture Studio / universal passage contract v1.
   Shared between home scripture, section theme scripture and tool scripture.
   The model has NO verse-specific layout coordinates or fixed number of strips.
   Validation of V18/USFM editorial break approval is intentionally independent.
*/
(function(root){
 'use strict';
 const text=v=>typeof v==='string'?v:'';
 const assert=(condition,message)=>{if(!condition)throw new Error(message)};
 function passage(spec){
  assert(spec&&typeof spec==='object','PASSAGE_OBJECT_REQUIRED');
  const zh=text(spec.zh),en=text(spec.en),ref=spec.reference||{};
  assert(zh.trim()&&en.trim(),'BILINGUAL_SCRIPTURE_REQUIRED');
  assert(text(ref.zh).trim()&&text(ref.en).trim()&&text(ref.chapterVerse).trim(),'BILINGUAL_REFERENCE_REQUIRED');
  const kind=['home','section','tool'].includes(spec.kind)?spec.kind:'section';
  const segments=spec.segments||{};
  const hard=spec.hardSpans||{};
  const normalized={id:text(spec.id)||'draft',kind,zh,en,
   reference:{zh:ref.zh,en:ref.en,chapterVerse:ref.chapterVerse},
   segments:{zh:Array.isArray(segments.zh)?[...segments.zh]:null,
             en:Array.isArray(segments.en)?[...segments.en]:null},
   hardSpans:{zh:Array.isArray(hard.zh)?[...hard.zh]:[],en:Array.isArray(hard.en)?[...hard.en]:[]},
   breakReview:spec.breakReview==='approved'?'approved':'unreviewed'};
  for(const lang of ['zh','en']){
   const units=normalized.segments[lang];
   if(units){assert(units.every(u=>typeof u==='string'&&u.length>0),'EMPTY_'+lang+'_UNIT');
    assert(units.join('')===normalized[lang],'SOURCE_MISMATCH_'+lang)}
   for(const locked of normalized.hardSpans[lang]){
    assert(typeof locked==='string'&&locked.length>0&&normalized[lang].includes(locked),'BAD_PROTECTED_SPAN_'+lang);
   }
  }
  return Object.freeze(normalized);
 }
 function referenceLabel(p){return p.reference.zh+' '+p.reference.en+' '+p.reference.chapterVerse}
 function tokenBoundaries(source,lang){
  let tokens;
  if(lang==='zh'){
   tokens=[...new Intl.Segmenter('zh-Hant',{granularity:'word'}).segment(source)].map(x=>x.segment);
  }else{tokens=source.match(/\\S+\\s*/g)||[]}
  assert(tokens.join('')===source,'TOKENIZER_SOURCE_LOSS_'+lang);
  const positions=[0],out=[];
  let offset=0;for(const unit of tokens){offset+=unit.length;positions.push(offset)}
  return positions;
 }
 function legalBreaks(p,lang){
  assert(lang==='zh'||lang==='en','LANGUAGE_REQUIRED');
  const source=p[lang],boundaries=new Set(tokenBoundaries(source,lang));
  const approved=p.segments[lang];
  const allowed=approved?approved.reduce((acc,u)=>{acc.pos+=u.length;acc.points.push(acc.pos);return acc},{pos:0,points:[0]}).points:[...boundaries];
  // Always protect supplied proper nouns, non-splittable expressions, and the
  // first/last codepoint. A candidate break is not an editorially approved break.
  const options=allowed.filter(pos=>pos>0&&pos<source.length&&boundaries.has(pos));
  const filtered=options.filter(pos=>{
   for(const span of p.hardSpans[lang]){
    let at=source.indexOf(span);
    while(at>=0){if(pos>at&&pos<at+span.length)return false;at=source.indexOf(span,at+span.length)}
   }
   const left=source.slice(0,pos),right=source.slice(pos);
   if(lang==='zh'){
    if(/[，。！？，、；：]$/.test(left)&&right.length<2)return false;
    if(/^[，。！？，、；：]/.test(right))return false;
    if(/[的了啊呢嗎吧]$/.test(left))return false;
   }else{
    if(/^[,.:;!?]/.test(right.trimStart()))return false;
   }
   return true;
  });
  return {points:filtered,source:approved?'reviewed-segments':'V18-lexical-candidates',reviewed:p.breakReview==='approved'&&!!approved};
 }
 function designParameters(p){
  // Optical direction is relative to passage length; no reference-specific
  // switch, no 4/6/7-column template, no 90%-fill hard gate.
  const zhChars=[...p.zh.replace(/\\s/g,'')].length;
  const enWords=(p.en.match(/\\S+/g)||[]).length;
  const total=zhChars+enWords;
  const density=total<=35?'airy':total<=95?'editorial':'extended';
  return {kind:p.kind, density, glyphPolicy:'one-size-bilingual',
   frame:'one-structural-frame',romanScriptStyle:'italic-if-verified-font',
   citation:referenceLabel(p),fixedStrips:null,hardFillTarget:null,
   semanticPriority:['source','natural-breaks','collision-free','two-way-readability','optical-balance','density']};
 }
 function audit(p){
  const z=legalBreaks(p,'zh'),e=legalBreaks(p,'en');
  return {validSource:!!p.zh&&!!p.en,reference:referenceLabel(p),kind:p.kind,
    layoutBreakCandidates:{zh:z.points.length,en:e.points.length},
    reviewed:z.reviewed&&e.reviewed,
    renderEligible:z.reviewed&&e.reviewed,
    reason:z.reviewed&&e.reviewed?'READY_FOR_VISUAL_QA':'BREAKPOINTS_REQUIRE_EDITORIAL_REVIEW'};
 }
 root.ScriptureStudioPassageModel=Object.freeze({passage,referenceLabel,tokenBoundaries,legalBreaks,designParameters,audit,version:'1.0.0'});
})(typeof window!=='undefined'?window:globalThis);
