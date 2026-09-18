#!/usr/bin/env node
import fs from 'node:fs';
import crypto from 'node:crypto';
import { boundaryDecisionForText } from './content-boundary.mjs';
const input=process.argv[2]; const source=process.argv[3]||'authority';
if(!input) throw new Error('input required');
const text=fs.readFileSync(input,'utf8');
const rows=text.split(/\r?\n/).filter(Boolean);
const out=[];
for(const row of rows){
 const b=boundaryDecisionForText(row);
 if(b.decision==='exclude') continue;
 const id=crypto.createHash('sha1').update(source+'|'+row).digest('hex');
 out.push({id,source,boundary:'pass',raw:row});
}
fs.writeFileSync('dore-expedition-ingested.json',JSON.stringify({schema:'dore.expedition.ingest.v1',source,scanned:rows.length,retained:out.length,items:out},null,2));
console.log(JSON.stringify({source,scanned:rows.length,retained:out.length}));