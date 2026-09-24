import {routeEvidenceClass,validateEventRoute} from './event-route-runtime.js';

const ROUTE_URL='./data/events/jesus-entry.json';
const fallback={
  'bethphage-zone':[93,30],
  'mount-of-olives-ridge':[70,43],
  'kidron-descent-zone':[56.5,65],
  'jerusalem-east-approach':[49,69],
  'temple-zone':[27.5,59]
};

export async function mountJesusEntryRoute(stage){
  const route=await fetch(ROUTE_URL).then(r=>{if(!r.ok)throw new Error('Jesus entry event unavailable');return r.json()});
  const errors=validateEventRoute(route);if(errors.length) throw new Error(errors.join('; '));
  const svg=stage.querySelector('.j3k-route'),labels=stage.querySelector('.j3k-route-labels');
  svg.replaceChildren();labels.replaceChildren();
  const NS='http://www.w3.org/2000/svg';
  const nodes=new Map(route.nodes.map(n=>[n.id,n]));
  const point=id=>fallback[id];
  for(const segment of route.segments){
    const a=point(segment.from),b=point(segment.to);if(!a||!b)continue;
    const path=document.createElementNS(NS,'path');
    path.setAttribute('d',`M ${a[0]*10} ${a[1]*5.6} L ${b[0]*10} ${b[1]*5.6}`);
    path.setAttribute('class',`route-${routeEvidenceClass(segment.status)}`);
    path.dataset.segmentId=segment.id;path.dataset.confidence=segment.confidence;svg.append(path);
  }
  for(const node of route.nodes){
    const p=point(node.id);if(!p)continue;
    const c=document.createElementNS(NS,'circle');c.setAttribute('cx',p[0]*10);c.setAttribute('cy',p[1]*5.6);c.setAttribute('r','7');c.setAttribute('class','route-node');c.dataset.evidence=node.evidence;svg.append(c);
    const label=document.createElement('span');label.style.setProperty('--x',p[0]+'%');label.style.setProperty('--y',p[1]+'%');label.textContent=node.label;label.dataset.evidence=node.evidence;labels.append(label);
  }
  stage.dataset.eventAuthority=route.id;
  return route;
}
