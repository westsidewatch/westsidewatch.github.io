/* Psalms ONE · 101–125.
 * Canonical policy: do not recycle narrative engravings merely because their
 * theme resembles a Psalm. Preserve a historical image only when its relation
 * to that Psalm is defensible; otherwise leave illustration absent until the
 * canonical chapter-specific engraving is generated.
 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P?.chapterStudies)return;
for(let n=101;n<=125;n+=1){const s=P.chapterStudies[n];if(s)delete s.illustration;}
})();