import React from 'react';
import church from '../../../../visual-workchain/runs/foundation-096-r05/church.html?raw';
import journal from '../../../../visual-workchain/runs/foundation-096-r05/journal.html?raw';
import dawn from '../../../../visual-workchain/runs/foundation-096-r05/dawn.html?raw';
import wall from '../../../../visual-workchain/runs/foundation-096-r05/wall.html?raw';
const base=new URLSearchParams(window.location.search).get('site')||'http://127.0.0.1:4173/experiments/foundation-096-r05/';
function Page({source}){return <iframe title="Westside Watch" srcDoc={source.replace('<head>','<head><base href="'+base+'">')} style={{display:'block',width:'100%',height:'100vh',border:0}}/>}
export default {title:'Westside/096/Foundation R05',component:Page,parameters:{layout:'fullscreen'}};
export const Church={args:{source:church}};export const Journal={args:{source:journal}};export const Dawn={args:{source:dawn}};export const Wall={args:{source:wall}};
