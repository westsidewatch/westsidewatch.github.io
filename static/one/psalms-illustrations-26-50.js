/* Psalms ONE · 26–50.
 * Canonical policy: do not assign generic OT engravings by mood/theme. A Psalm
 * receives historical art only when a defensible chapter-specific relationship
 * is documented. Otherwise it intentionally uses the shared canonical no-image
 * cover until a chapter-specific generated engraving is added.
 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P?.chapterStudies)return;
for(let n=26;n<=50;n+=1){const s=P.chapterStudies[n];if(s)delete s.illustration;}
})();