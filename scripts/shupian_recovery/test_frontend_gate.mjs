#!/usr/bin/env node
/** Regression for public catalog admission (no network necessary). */
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const html=readFileSync('static/shupian/index.html','utf8');
const match=html.match(/function media\(ep\)\{[\s\S]*?\n\}/);
assert.ok(match,'Media gate must exist');
const factory=new Function('URL','Date','Set',
  'const EXPIRES_AFTER=24*60*60*1000; const sourceFailures=new Set();\n'+
  match[0]+'\nreturn {media,sourceFailures};');
const {media,sourceFailures}=factory(URL,Date,Set);
const valid={status:'passed',videoStarted:true,seekSucceeded:true,observedAt:new Date().toISOString()};
const make=(url,proof=valid)=>({sources:[{url,playbackVerification:proof}]});
assert.equal(media(make('https://test.example/video.m3u8')).length,1,'HLS must be accepted');
assert.equal(media(make('https://test.example/video.mp4')).length,1,'MP4 must be accepted');
assert.equal(media(make('https://test.example/video.webm')).length,1,'WebM must be accepted');
assert.equal(media(make('http://test.example/video.mp4')).length,0,'Insecure media refused');
assert.equal(media(make('https://test.example/video.mp4',{})).length,0,'Missing proof refused');
assert.equal(media(make('https://test.example/video.mp4',{...valid,seekSucceeded:false})).length,0,'Seek failure refused');
assert.equal(media(make('https://test.example/video.mp4',{...valid,observedAt:'2020-01-01T00:00:00Z'})).length,0,'Expired proof refused');
sourceFailures.add('https://test.example/video.mp4');
assert.equal(media(make('https://test.example/video.mp4')).length,0,'Playback failure removes source');
assert.deepEqual(JSON.parse(html.match(/<script id="catalog" type="application\/json">([\s\S]*?)<\/script>/)[1]),[],'No unreviewed inline titles');
assert.ok(html.includes("fetch('screenings.json'"),'Viewer must use approved-only screenings feed');
console.log('PASS: real video extensions accepted; unverified/expired/broken links blocked.');
