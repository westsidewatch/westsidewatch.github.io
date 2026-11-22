#!/usr/bin/env node
'use strict';
const fs=require('node:fs');
const manifest=JSON.parse(fs.readFileSync('static/dawn-library/chinese-contemporary-discovery.json','utf8'));
const books=manifest.candidates.filter(x=>x.freeReading?.status?.startsWith('verified'));
const rows=[];
const check=async(url)=>{
 const abort=new AbortController(),timer=setTimeout(()=>abort.abort(),15000);
 try{return await fetch(url,{signal:abort.signal,headers:{'User-Agent':'Mozilla/5.0 (Dawn Library source audit)'}})}
 finally{clearTimeout(timer)}
};
const srcList=html=>[...html.matchAll(/(?:src|data-src|content)=["']([^"']+\.(?:png|jpe?g|webp)(?:\?[^"']*)?)["']/gi)].map(x=>x[1].replaceAll('&amp;','&')).slice(0,90);
(async()=>{
 for(const book of books){
  const row={title:book.title,workId:book.candidateId,sourceUrl:book.sourceUrl,configured:book.coverUrl||null,publisherHttp:null,pictureHttp:null,mime:null,pictureBytes:0,pageImageCandidates:[],errors:[]};
  try{const p=await check(book.sourceUrl);row.publisherHttp=p.status;
   if(p.ok){const html=await p.text();row.pageImageCandidates=srcList(html).slice(0,40);}
  }catch(e){row.errors.push('page '+String(e))}
  if(book.coverUrl)try{
   const p=await check(book.coverUrl);row.pictureHttp=p.status;row.mime=p.headers.get('content-type');
   if(p.ok)row.pictureBytes=(await p.arrayBuffer()).byteLength;
  }catch(e){row.errors.push('jacket '+String(e))}
  console.log('PUBLISHER_JACKET',JSON.stringify({title:row.title,pictureHttp:row.pictureHttp,bytes:row.pictureBytes,mime:row.mime,candidates:row.pageImageCandidates.slice(0,8),errors:row.errors}));
  rows.push(row);
 }
 fs.mkdirSync('artifacts/dawn-cover-audit',{recursive:true});
 fs.writeFileSync('artifacts/dawn-cover-audit/official-jackets.json',JSON.stringify(rows,null,2)+'\n');
 const ok=rows.filter(x=>x.pictureHttp===200&&x.mime?.startsWith('image/')&&x.pictureBytes>1000);
 console.log('JACKET_AUDIT_SUMMARY',JSON.stringify({freeWorks:books.length,workingImages:ok.length,missing:rows.filter(x=>!ok.includes(x)).map(x=>x.title)}));
})().catch(e=>{console.error(e);process.exitCode=1});