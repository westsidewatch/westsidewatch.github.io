import test from 'node:test';
import assert from 'node:assert/strict';
import { generateUrbanBlocks, subdivideBlockToParcels, validateParcelGeometry } from './herodian-urban-blocks-core.js';

const rectangle=(x0,z0,x1,z1)=>[{x:x0,z:z0},{x:x1,z:z0},{x:x1,z:z1},{x:x0,z:z1}];
const parcel=(id,polygon)=>({id,geometry:{polygon}});

test('overlapping rectangles fail validation',()=>{
 const boundary=rectangle(0,0,100,100);
 const result=validateParcelGeometry([parcel('a',rectangle(5,5,30,30)),parcel('b',rectangle(20,20,40,40))],boundary);
 assert.equal(result.valid,false);
 assert.ok(result.errors.some(e=>e.kind==='overlapping-parcels'));
});

test('coincident rectangles fail validation',()=>{
 const boundary=rectangle(0,0,100,100);
 const result=validateParcelGeometry([parcel('a',rectangle(5,5,30,30)),parcel('b',rectangle(5,5,30,30))],boundary);
 assert.equal(result.valid,false);
});

test('disjoint parcels and boundary contact are valid',()=>{
 const boundary=rectangle(0,0,100,100);
 const result=validateParcelGeometry([parcel('a',rectangle(0,0,20,20)),parcel('b',rectangle(30,30,50,50))],boundary);
 assert.equal(result.valid,true,JSON.stringify(result.errors));
});

test('outside parcels are rejected',()=>{
 const boundary=rectangle(0,0,100,100);
 const result=validateParcelGeometry([parcel('a',rectangle(95,95,105,105))],boundary);
 assert.ok(result.errors.some(e=>e.kind==='outside-block'));
});

test('generated rectangular block parcels are nonoverlapping and within block',()=>{
 const polygon=rectangle(0,0,120,100);
 const block={id:'test:block',districtId:'test',geometry:{polygon},metadata:{}};
 const parcels=subdivideBlockToParcels(block);
 assert.ok(parcels.length>0,'expected generated parcels');
 const result=validateParcelGeometry(parcels,polygon);
 assert.equal(result.valid,true,JSON.stringify(result.errors.slice(0,8)));
 for(const p of parcels.filter(p=>p.metadata?.perimeterFabric)) assert.ok(p.metadata.frontage);
});

test('generated blocks publish a successful geometry audit',()=>{
 const polygon=rectangle(0,0,120,100);
 const block={id:'audit:block',districtId:'audit',geometry:{polygon},metadata:{}};
 const parcels=subdivideBlockToParcels(block);
 assert.ok(parcels.length>0);
 assert.equal(block.metadata.geometryAudit?.valid,true);
 assert.equal(block.metadata.geometryAudit.parcelCount,parcels.length);
});

test('T junction road endpoint is noded against crossing street',()=>{
 const district={id:'test-district',geometry:{polygon:rectangle(0,0,120,100)}};
 const road=(id,points)=>({id,geometry:{points}});
 const roads=[
  road('vertical',[{x:60,z:0},{x:60,z:100}]),
  road('branch',[{x:60,z:50},{x:120,z:50}])
 ];
 const result=generateUrbanBlocks({district,roads});
 assert.equal(result.withheld,false);
 assert.ok(result.graphNodes>=7,'T junction must create a graph node');
 assert.ok(result.graphEdges>=9,'T junction must split the vertical road');
});
