import React from 'react';
const base = new URLSearchParams(window.location.search).get('site') || 'http://127.0.0.1:4173';
const View=({route})=><iframe title="Westside Watch" src={base+route} style={{display:'block',width:'100%',height:'100vh',border:0}}/>;
export default {title:'Westside/096/Actual routes',component:View,parameters:{layout:'fullscreen'}};
export const Church={args:{route:'/church/'}};
export const Worship={args:{route:'/church/sunday-worship/'}};
export const Magazine={args:{route:'/journal/'}};
export const Volume={args:{route:'/vol-00/'}};
