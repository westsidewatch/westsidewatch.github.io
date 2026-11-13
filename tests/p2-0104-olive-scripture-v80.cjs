'use strict';
// V80: one sourced scripture associated with each of twelve protected speakers.
// Editorial associations are not mislabeled as a statistically most-used verse.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const data=read('static/js/p2-0104-olive-scriptures-v80.js');
const sandbox={window:{}};vm.runInNewContext(data,sandbox);
const scriptures=sandbox.window.P2OliveScriptures;
const slugs=['watchman-nee','derek-prince','david-pawson','stephen-tong','huang-shuhua','kang-lai-chang','jerry-lai','tong-liu','jiang-xiuqin','rick-warren','yu-hong-jie','kou-shao-en'];
assert.equal(scriptures.cards.length,12);
assert.equal(new Set(scriptures.cards.map(c=>c.referenceEn)).size,12,'all 12 speakers have distinct verses');
assert.equal(scriptures.theme.referenceEn,'Romans 10:17');
assert.match(scriptures.theme.excerpt,/信道是從聽道來的/);
assert.equal(scriptures.theme.translationEn,'KJV');
assert.match(scriptures.theme.excerptEn,/faith cometh by hearing/);
scriptures.cards.forEach((c,i)=>{
 assert.equal(c.slug,slugs[i],`verse speaker order mismatch ${i+1}`);
 assert(c.excerpt.length>=12&&c.excerpt.length<110,'Chinese verse must remain legible');
 assert(c.excerptEn.length>=25&&c.excerptEn.length<180,'KJV editorial excerpt must remain readable');
 assert.equal(c.translationEn,'KJV','all twelve English verses must be labeled KJV');
 assert.match(c.referenceZh,/\d+:\d+/);
 assert.match(c.referenceEn,/\d+:\d+/);
 assert(['direct','editorial'].includes(c.evidence),'source confidence must be transparent');
});
const html=read('static/experiments/p2-0104-olive-continuation.html');
const js=read('static/js/p2-0104-olive-continuation.js');
const css=read('static/css/p2-0104-olive-continuation.css');
assert.match(html,/olive-stage__rubric-zh[^>]*lang="zh-Hant">橄欖山/);
assert.match(html,/olive-stage__rubric-scripture-zh" lang="zh-Hant">/);
assert.match(html,/olive-stage__rubric-scripture-en" lang="en">/);
assert.match(html,/So then faith cometh by hearing/);
assert.match(html,/ROMANS 10:17 · KJV/);
assert.match(html,/羅馬書 10:17/);
assert.equal((html.match(/class="olive-stage__companion-verse-en"/g)||[]).length,2,
  'two English KJV verse regions alongside speakers');
assert.equal((html.match(/class="olive-stage__companion-reference-en"/g)||[]).length,2,
  'both adjacent companion panels have bilingual verse references');
assert.equal((html.match(/class="olive-stage__companion"/g)||[]).length,2,
  'two independent scripture reading panels must be mounted beside facing posters');
assert.doesNotMatch(html,/class="olive-card__reverse-title"/,
  'no scripture on the physical reverse of any speaker card');
assert.doesNotMatch(html,/class="olive-card__reading-veil"/,
  'old verse-only reverse fields must be retired');
assert.match(html,/p2-0104-olive-scriptures-v80\.js/);
assert.match(js,/P2OliveScriptures\?\.cards\?\.\[speaker\]/);
assert.match(js,/position\(panel,card\.x,card\.y,card\.w,card\.h\)/);
assert.match(js,/stage\.dataset\.p2ScripturePlacement='adjacent-bilingual-cuv-kjv-v82'/);
assert.match(css,/\.olive-stage__companion-reading/);
assert.match(css,/\.olive-stage__rubric-zh/);
console.log("PASS / V82: 12 bilingual CUV-KJV passages, OS two-column chapter masthead and independent companion panels.");
