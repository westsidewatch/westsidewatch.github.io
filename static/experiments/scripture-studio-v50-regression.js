/* Scripture Studio V50 / reproducible no-font test fixtures.
 * These are SYNTHETIC texts, not Bible quotations. They test only the shared
 * compositional engine; real CUV/KJV editorial review and visual QA remain separate.
 * Run by loading scripture-studio-passage-model.js then this script.
 */
(function(root){
 'use strict';
 const model=root.ScriptureStudioPassageModel;
 if(!model)throw Error('PASSAGE_MODEL_MISSING');
 const tests=[
  {name:'SHORT',zh:'天地有光。',en:'Let there be light.',
   reference:{zh:'測試',en:'Test',chapterVerse:'0:1'},
   units:{zh:['天地','有光。'],en:['Let there ','be light.']}},
  {name:'MEDIUM',zh:'甲乙丙丁戊己庚辛壬癸子丑',en:'one two three four five six seven eight nine ten eleven twelve',
   reference:{zh:'測試',en:'Test',chapterVerse:'0:2'},
   units:{zh:['甲乙','丙丁','戊己','庚辛','壬癸','子丑'],
    en:['one ','two ','three ','four ','five ','six ','seven ','eight ','nine ','ten ','eleven ','twelve']}},
  {name:'LONG',
   zh:'甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉',
   en:'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty',
   reference:{zh:'測試',en:'Test',chapterVerse:'0:3'},
   units:{zh:['甲乙','丙丁','戊己','庚辛','壬癸','子丑','寅卯','辰巳','午未','申酉'],
    en:'one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty'.split(' ').map((w,i,a)=>w+(i<a.length-1?' ':''))}}
 ];
 const results=tests.map(t=>{
  const p=model.passage({id:t.name,kind:'section',zh:t.zh,en:t.en,
   reference:t.reference,segments:t.units,breakReview:'unreviewed'});
  const candidates=model.runSignatures(t.units.zh,t.units.en,14);
  const allValid=candidates.every(c=>model.verifyMixedRuns(t.units.zh,t.units.en,c.signatures).ok);
  const allBilingual=candidates.every(c=>c.signatures.every(sig=>sig.includes('Z')&&sig.includes('E')));
  const noModifiedSource=t.units.zh.join('')===p.zh&&t.units.en.join('')===p.en;
  const unreviewed=model.audit(p).renderEligible===false;
  return {name:t.name,candidates:candidates.length,maxBands:Math.max(0,...candidates.map(c=>c.count)),
    sourceExact:noModifiedSource,H4:allValid,bilingual:allBilingual,editorialBlocked:unreviewed,
    pass:noModifiedSource&&allValid&&allBilingual&&unreviewed&&candidates.length>0};
 });
 root.__scriptureStudioRegression=results;
 if(results.some(x=>!x.pass))throw Error('SCRIPTURE_V50_REGRESSION_FAILED: '+JSON.stringify(results));
})(typeof window!=='undefined'?window:globalThis);
