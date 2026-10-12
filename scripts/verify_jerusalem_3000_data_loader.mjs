import assert from 'node:assert/strict';
import {loadCityData,invalidateCityData} from '../preview/jerusalem-3000/city-data-loader.js';
const original=globalThis.fetch;let calls=0;
try {
 globalThis.fetch=async(url,options)=>{calls++;assert.equal(options.cache,'no-cache');return {ok:true,json:async()=>({objects:[{id:'stable',state:'standing'}]})};};
 const [a,b]=await Promise.all([loadCityData('./data/shared.json'),loadCityData('./data/../data/shared.json')]);
 assert.equal(calls,1,'concurrent equivalent URLs must share a request');
 a.objects[0].state='ruined';assert.equal(b.objects[0].state,'standing');
 assert.equal((await loadCityData('./data/shared.json')).objects[0].state,'standing');assert.equal(calls,1);
 invalidateCityData('./data/shared.json');await loadCityData('./data/shared.json');assert.equal(calls,2);
 invalidateCityData();
 globalThis.fetch=async()=>{calls++;return {ok:false,status:503};};
 await assert.rejects(loadCityData('./data/retry.json'),/503/);
 globalThis.fetch=async()=>{calls++;return {ok:true,json:async()=>({revision:2})};};
 assert.equal((await loadCityData('./data/retry.json')).revision,2);assert.equal(calls,4,'failed responses must not poison cache');
 globalThis.fetch=async()=>({ok:true,json:async()=>{throw new SyntaxError('bad JSON');}});
 await assert.rejects(loadCityData('./data/malformed.json'),/bad JSON/);
 globalThis.fetch=async()=>({ok:true,json:async()=>({ok:true})});assert.equal((await loadCityData('./data/malformed.json')).ok,true);
 console.log('PASS: request coalescing, URL identity, consumer isolation, invalidation and HTTP/JSON retry');
} finally {globalThis.fetch=original;invalidateCityData();}
