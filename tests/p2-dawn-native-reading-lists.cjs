'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'../static');
const read=p=>fs.readFileSync(path.join(root,p),'utf8');
const json=JSON.parse(read('dawn-library/p2-reading-lists-issue-01.json'));
const html=read('experiments/p2-0105-dawn-preview.html');
const js=read('js/p2-0105-dawn-continuation.js');
const css=read('css/p2-0105-dawn-integrated.css');
const vm=require('node:vm');
new vm.Script(js,{filename:'p2-0105-dawn-continuation.js'});
assert.equal(json.schema,'dawn.p2.editorial-reading-issue.v1');
assert.deepEqual(json.lists.map(x=>x.id),['gospel-essentials','inner-life','church-history']);
assert.deepEqual(json.lists.map(x=>x.works.length),[6,9,7]);
const ids=new Set();
for(const list of json.lists){
 assert(list.question?.length>20,'Reader question missing '+list.id);
 assert(list.sequence?.includes('→'),'Curated reading sequence missing '+list.id);
 assert(html.includes('data-dawn-reading-list="'+list.id+'"'),'Native reading index missing '+list.id);
 for(const book of list.works){
  assert(!ids.has(book.editorialKey),'Duplicate editorial work '+book.editorialKey);
  ids.add(book.editorialKey);
  for(const k of ['title','creator','judgement','counterpoint','comparison'])assert(book[k]?.length>=(['title','creator'].includes(k)?2:4),'Missing editorial '+k+' '+book.editorialKey);
  if(book.libraryWorkId)assert(/^(OL\d+W|dawn:[\w:-]+)$/.test(book.libraryWorkId),'Unverified Work ID');
  if(book.image?.startsWith('/'))assert(fs.existsSync(path.join(root,book.image)),'Missing local cover '+book.image);
 }
}
assert.equal(ids.size,22);
assert.equal((html.match(/data-dawn-portal=/g)||[]).length,3,'Original three P2 portals must remain intact');
for(const key of ['dawn-second__motherform','dawn-wall-grid','dawn-department-grid','dawn-personal-dialog','dawn-book-detail','dawn-catalogue']){
 assert(html.includes(key),'Original P2-05 region removed '+key);
}
assert(!html.includes('dawn-curation-prologue'),'Parallel Dawn homepage must not be copied');
assert(js.includes("if(activePortal==='書單')void showReadingList(ticket)"),'Original catalogue does not own booklist route');
assert(js.includes("openCollection('書單')"),'Native catalogue navigation missing');
assert(js.includes("renderPortalWorks(items,'書單')"),'Native six-column book gallery not reused');
assert(js.includes("selectBookPreview(works,li,work)"),'Original cover-opening interaction removed');
assert(js.includes("detailSource.textContent=work.sourceLabel"),'Reading version must not be mislabeled as free full text');
assert(!html.includes('dawn-reading-room__reading-lists'),'Oversized parallel reading-list masthead must be physically removed');
assert(!html.includes('id="dawn-issue-contents"'),'Duplicate large reading masthead has reappeared');
assert.equal((html.match(/class="dawn-wall__tile dawn-reading-list__tile/g)||[]).length,3,'Three guided list sleeves must use existing wall tiles');
assert(html.indexOf('data-dawn-portal="光譜"')<html.indexOf('data-dawn-reading-list="gospel-essentials"'),'Booklists must follow the original three editorial portals');
assert(html.includes('class="dawn-reading-list__series" aria-labelledby="dawn-reading-list-heading"'),'Reading lists need an independent named chapter in the original vinyl wall');
assert(html.includes('<h2 id="dawn-reading-list-heading">書單</h2>'),'Visible Chinese 書單 wayfinding missing');
assert(!html.includes('dawn-reading-list__issue'),'Invisible tiny English-only strip must not return');
assert((html.match(/<span class="dawn-reading-list__serial">書單 /g)||[]).length===3,'Each list square must say 書單, not resemble an individual book');
assert(css.includes('.dawn-reading-list__series-grid')&&css.includes('grid-column:1 / -1!important'),'Guided group must occupy a whole record-wall row without mixing with original covers');
assert(html.includes('class="dawn-reading-room__departments" aria-labelledby="dawn-departments-heading" hidden'),'Seven subjects should not compete on editorial opening');
assert(js.includes("works.prepend(guide)"),'Guided question square must precede original books');
assert(js.includes("guide.className='dawn-reading-list__guide'"),'2x2 guide not rendered inside existing catalogue');
assert(css.includes('.dawn-reading-list__tile')&&css.includes('.dawn-reading-list__guide'),'One visual grammar for small square sleeves and large 2x2 reading guide is missing');
assert(css.includes('dawn-reading-room__departments[hidden]'),'Seven subjects may not be present on editorial landing');
console.log('PASS: P2-05 original 3 portals, 7 subjects, native book reader, 3 guided lists, 22 editorial works');
