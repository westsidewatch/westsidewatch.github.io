/* Art-direction authority lives inside the EXISTING Westside Design OS:
   enforce source semantics before Chromium optical measurement. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
const css=fs.readFileSync('static/css/westside-editorial-grammar.css','utf8');
const page=fs.readFileSync('layouts/partials/editorial/grammar/cover.html','utf8');
const body=fs.readFileSync('layouts/partials/editorial/grammar/block.html','utf8');
const os=fs.readFileSync('static/css/westside-design-os.css','utf8');
const base=fs.readFileSync('layouts/_default/baseof.html','utf8');
const context=fs.readFileSync('docs/design/WESTSIDE-DESIGN-OS.md','utf8');
const grammar=fs.readFileSync('data/editorial/grammar/journal.json','utf8');
assert(context.includes('Westside Design OS')&&os.includes('westside-design-tokens.css'));
assert(base.includes('if .Params.os_editorial')&&base.includes('westside-editorial-grammar.css'));
assert(!/#[0-9a-f]{3,8}\b/i.test(css),'No literal competing palette outside OS');
assert(css.includes('--g-accent:var(--ws-water)')&&css.includes('--g-accent:var(--ws-olive)'));
assert(css.includes('--g-accent:var(--ws-harvest)')&&css.includes('--g-accent:var(--ws-crimson)'));
assert(css.includes('--g-label-ink:color-mix('),'Small editorial text must use readable neutral ink rather than decorative accent');
assert(css.includes('.ws-gram-cover__title-zh{')&&css.includes('font-size:var(--ws-type-scale-display-md)!important'));
assert(css.includes('font-family:var(--ws-type-display-en-sc)!important'));
assert(css.includes('font-family:var(--ws-type-display-zh)!important'));
assert(css.includes('font:var(--ws-weight-standard) var(--ws-type-scale-reading-lg)/2.06 var(--ws-type-reading-zh)'),
 'Long Chinese reading must use the shared OS reading role');
assert(!css.includes('font-family:Arial')&&!css.includes('font-family:Georgia'));
const cinema=css.split('.ws-gram-cover[data-mode="cinematic"]{')[1].split('}')[0];
assert(cinema.includes('background:var(--ws-ink)')&&!cinema.includes('var(--ws-night)'),
 'Cinema must not borrow Westside Journal blue');
assert(!cinema.includes('var(--ws-first-light)'));
assert(page.includes('ws-gram-cover__official-identity')&&page.includes('layout=sevenfold-vertical'),
 'The original church wordmark and the original V60 Scripture are preserved');
assert(body.includes('ws-gram-essay__text')&&body.includes('ws-gram-plate__image'));
const data=JSON.parse(grammar);
assert(data.cover.mode==='poster'&&data.blocks.some(b=>b.mode==='issue-toc'));
console.log('EDITORIAL_ART_DIRECTION_OS_PASS: original OS, Chinese-first optical role, genuine SC, sourced artwork, 7 realm colors and no cinema palette bleed');

const shell=fs.readFileSync('layouts/partials/editorial/grammar/page.html','utf8');
assert(!/[\u2190-\u21ff]/u.test(shell+page+body),'New editorial navigation must not reintroduce generic arrow glyphs');
