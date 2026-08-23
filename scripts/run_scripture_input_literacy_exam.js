'use strict';
const fs=require('fs');
const path=require('path');
const parserApi=require('../static/dore/dore-scripture-reference-parser.js');
const corpus=JSON.parse(fs.readFileSync(path.join(__dirname,'../static/dore/scripture-input-literacy.json'),'utf8'));
const parser=parserApi.create(corpus);
const failures=[];
function expect(name,input,expected){const got=parser.parseQuery(input);const slim=got&&got.map(x=>x.kind==='chapter'?[x.book,x.chapter]:[x.book,x.chapter,x.start,x.end]);const pass=JSON.stringify(slim)===JSON.stringify(expected);if(!pass)failures.push({name,input,expected,got:slim});console.log(`${pass?'PASS':'FAIL'} ${name}: ${input}`)}
if((corpus.books||[]).length!==66)failures.push({name:'66-book-corpus',got:(corpus.books||[]).length,expected:66});else console.log('PASS 66-book-corpus');
// Training/self exam: these are known classroom stimuli.
expect('training-range-traditional','羅馬書3：12-16',[["ROM",3,12,16]]);
expect('training-abbrev','林前 8:9-15',[["1CO",8,9,15]]);
expect('training-chinese-chapter-verse','賽三第四節',[["ISA",3,4,4]]);
expect('training-spoken-range','帖後3章八節到十節',[["2TH",3,8,10]]);
expect('training-chapter-chinese','帖後三',[["2TH",3]]);
expect('training-chapter-arabic','帖後3',[["2TH",3]]);
expect('training-name-variant','創世紀2:5-9',[["GEN",2,5,9]]);
expect('training-multi','帖後3：15-19 創世紀2:5-9',[["2TH",3,15,19],["GEN",2,5,9]]);
// Blind/transfer exam: not copied from the lesson examples.
expect('blind-simplified-abbrev','帖后2：1-4',[["2TH",2,1,4]]);
expect('blind-other-epistle','林後十一：3-6',[["2CO",11,3,6]]);
expect('blind-english-abbrev','1 Thess 5:16-18',[["1TH",5,16,18]]);
expect('blind-chinese-chapter','詩二十三',[["PSA",23]]);
expect('blind-short-letter','約三 1:2',[["3JN",1,2,2]]);
expect('blind-three-references','太5:3-5 羅8:28 詩23:1',[["MAT",5,3,5],["ROM",8,28,28],["PSA",23,1,1]]);
expect('blind-punctuation-mix','彼前2．9－10；啟21：1-2',[["1PE",2,9,10],["REV",21,1,2]]);
const report={milestone:'SCRIPTURE_SEARCH_INPUT_LITERACY_1_COMPLETE',status:failures.length?'FAIL':'PASS',books:(corpus.books||[]).length,failures};
fs.mkdirSync(path.join(__dirname,'../reports'),{recursive:true});
fs.writeFileSync(path.join(__dirname,'../reports/DORÉ-SCRIPTURE-INPUT-LITERACY.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
process.exit(failures.length?1:0);
