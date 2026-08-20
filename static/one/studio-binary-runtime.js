/* ONE Studio binary runtime — quarantine compatibility stub.
 * The first direct-binary Lamentations 3 AVIF proved the upload path, but is not production-safe.
 * Keep ONE stable by removing only that experimental 25:3 override.
 * No MutationObserver, timer, DOM writer loop, navigation listener, or typography injection.
 */
(()=>{
  "use strict";
  const BOOK=25, CHAPTER=3;
  const P=window.ONE_COVER_POLICY;
  if(P && !P.__lam03Quarantined){
    const original=P.getCover?.bind(P);
    P.getCover=(book,chapter)=>Number(book)===BOOK&&Number(chapter)===CHAPTER?null:(original?original(book,chapter):null);
    P.__lam03Quarantined=true;
  }
  const study=window.ONE_DATA?.studyBooks?.[BOOK]?.chapterStudies?.[CHAPTER];
  if(study){
    delete study.illustration;
    delete study.illustrations;
    delete study.coverIllustration;
    delete study.coverImage;
    delete study.doreCover;
    delete study.studioCover;
  }
  document.documentElement.dataset.oneStudioBinaryRuntime="lam03-quarantined";
})();
