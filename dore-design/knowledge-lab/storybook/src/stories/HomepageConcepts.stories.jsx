import React from 'react';
const ids={atlas:'homepage-concept-index',current:'homepage-concept-dispatch',signal:'homepage-concept-folio'};
function HomepageConcept({concept='atlas'}){return <iframe title={concept} src={`http://localhost:4310/editor-canvas?page=${ids[concept]}`} style={{width:'100%',height:'100vh',border:0,display:'block'}}/>}
export default {title:'New Westside/Homepage Concepts',component:HomepageConcept,parameters:{layout:'fullscreen'}};
export const DawnAtlas={args:{concept:'atlas'}};
export const LivingCurrent={args:{concept:'current'}};
export const SignalNocturne={args:{concept:'signal'}};
