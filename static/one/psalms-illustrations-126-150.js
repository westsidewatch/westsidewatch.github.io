/* Psalms ONE · 126–150.
 * Canonical policy: Songs of Ascents and praise Psalms must not be filled with
 * unrelated narrative engravings selected by loose themes (temple, family,
 * triumph, music, etc.). Keep the canonical no-image cover until reliable
 * Psalm-specific historical art or a chapter-specific generated engraving exists.
 */
(()=>{"use strict";const P=window.ONE_DATA?.psalms;if(!P?.chapterStudies)return;
for(let n=126;n<=150;n+=1){const s=P.chapterStudies[n];if(s)delete s.illustration;}
})();