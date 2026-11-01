import * as THREE from 'three';
import {HERODIAN_DIMENSIONS as D} from './herodian-dimensions.js';
import {sanctuaryAccessVertices} from './sanctuary-access-geometry.js';
// Relative illustrative placement, never surveyed ancient street vertices.
// Keep the source anchor intact; constrain only this display candidate to the
// inherited platform's exterior. The rounded platform itself is unverified.
export function westernPrecinctRoute(r){
 const width=8,clearance=.35,platformWest=r.platformEast-D.platform.eastWest/2;
 const x=platformWest-clearance-width/2,z=-r.north;
 return {points:[[x,z-178.5],[x,z+178.5]],width,clearance,sourceAnchor:{east:r.east,north:r.north},displayOffsetEast:x-r.east,platformWest,authority:'authored-exterior-route-relative-to-rounded-platform-not-surveyed-street',historicalGeometryAccepted:false};
}
export function westernRouteReservation(r,padding=1){
 const p=westernPrecinctRoute(r),[a,b]=p.points;
 return {objectId:'j3k:object:western-street',authority:p.authority,polygon:[{x:a[0]-p.width/2-padding,z:a[1]-padding},{x:a[0]+p.width/2+padding,z:a[1]-padding},{x:b[0]+p.width/2+padding,z:b[1]+padding},{x:b[0]-p.width/2-padding,z:b[1]+padding}]};
}
export function buildWesternPrecinctRoute(builder,r){
 const p=westernPrecinctRoute(r),surface=(x,z)=>r.terrain?.heightAtWorld?.(x,z)??r.up;
 // Thin, terrain-following paving replaces 50m-wide slabs and an invented24m wall.
 // No bridge, platform gate or underground passage is invented to close gaps.
 const v=sanctuaryAccessVertices(p.points,p.width,surface,(x,z)=>surface(x,z)+.16,r.terrain?{terrain:r.terrain,anchor:{x:0,z:0}}:null);
 const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(v,3));g.computeVertexNormals();
 builder.add(g,'inferred',.24,{duration:.12,lift:95,shade:.9});g.dispose();return p;
}
