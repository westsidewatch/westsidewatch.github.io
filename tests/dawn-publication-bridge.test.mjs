import assert from 'node:assert/strict';
const {buildDawnPublicationAdmission}=await import('../static/multiwrite/dawn-publication-bridge.mjs');
const file=(name)=>({filename:name,blob:new Blob(['x'])});
const input={bookModel:{publicationMetadata:{title:'約伯的三個朋友',author:'Doré',language:'zh-Hant'}},bookBuild:{publishedAt:'2026-09-12T00:00:00Z',qaResult:{status:'pass'}},materialized:{status:'accepted',files:{cover:file('cover.png'),web:file('book.html'),epub:file('book.epub'),pdf:file('book.pdf')}},publicationAcceptance:{status:'pass'}};
const a=buildDawnPublicationAdmission(input),b=buildDawnPublicationAdmission(input);
assert.equal(a.work.workId,b.work.workId);assert.deepEqual(a.work.authors,['Doré']);assert.deepEqual(a.work.languages,['zh-Hant']);assert.equal(a.edition.artifacts.web,'book.html');assert.equal(a.surface.ref.workId,a.work.workId);assert.equal(a.policy.surfaceOwnsIdentity,false);assert.throws(()=>buildDawnPublicationAdmission({...input,publicationAcceptance:{status:'blocked'}}));
console.log('Dawn publication bridge PASS',a.work.workId);
