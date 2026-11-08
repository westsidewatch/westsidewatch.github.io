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
scriptures.cards.forEach((c,i)=>{
 assert.equal(c.slug,slugs[i],`verse speaker order mismatch ${i+1}`);
 assert(c.excerpt.length>=12&&c.excerpt.length<110,'card verse must be readable');
 assert.match(c.referenceZh,/\d+:\d+/);
 assert.match(c.referenceEn,/\d+:\d+/);
 assert(['direct','editorial'].includes(c.evidence),'source confidence must be transparent');
});
const html=read('static/experiments/p2-0104-olive-continuation.html');
const js=read('static/js/p2-0104-olive-continuation.js');
const css=read('static/css/p2-0104-olive-continuation.css');
assert.match(html,/olive-stage__rubric-zh[^>]*lang="zh-Hant">橄欖山/);
assert.match(html,/olive-stage__rubric-scripture[^>]*lang="zh-Hant">可見信道/);
assert.match(html,/羅馬書 10:17/);
assert.match(html,/olive-card__scripture-text/);
assert.match(html,/olive-card__scripture-cite/);
assert.match(html,/p2-0104-olive-scriptures-v80\.js/);
assert(!html.includes('THE FIRST BRANCH')&&!html.includes('KIDRON</span>'));
assert.match(js,/P2OliveScriptures\?\.cards\?\.\[id\]/);
assert.match(js,/sourcePassage\.slug!==roster\[id\]\[0\]/);
assert.match(js,/back\.dataset\.scriptureSpeaker=sourcePassage\.slug/);
assert.match(css,/\.olive-card__scripture-cite/);
assert.match(css,/\.olive-stage__rubric-zh/);
console.log('PASS / V80: bilingual Olive chapter + Romans 10:17, twelve sourced speaker verses and immutable originals.');
