/* Psalms ONE · 76–100.
 * Canonical policy: generic OT scenes selected by theme are not chapter art.
 * Historical art is allowed only with a defensible Psalm-specific relationship;
 * otherwise use the shared canonical no-image cover until a chapter-specific
 * generated engraving is available.
 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P?.chapterStudies)return;
for(let n=76;n<=100;n+=1){const s=P.chapterStudies[n];if(s)delete s.illustration;}
})();