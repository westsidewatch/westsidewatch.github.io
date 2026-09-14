#!/usr/bin/env python3
"""Immutable sandbox for executable Doré Design candidate patches."""
from __future__ import annotations
import copy, hashlib, json
import design2_renderer

ALLOWED_OPS={'move','resize','font_size','text_align','add_node','set_style'}
MAX_OPS=48
SAFE_NODE_TYPES={'text','panel','light','rule','portal'}
SAFE_STYLE_KEYS={'background','color','border','border_radius','opacity','letter_spacing','line_height','font_weight','font_family'}

def _num(value,name):
    if not isinstance(value,(int,float)): raise ValueError('invalid_numeric_'+name)
    value=float(value)
    if not -100000<=value<=100000: raise ValueError('numeric_out_of_range_'+name)
    return value

def _page(snapshot):
    if not isinstance(snapshot,dict) or snapshot.get('schema')!='dore.design.publish-snapshot.v1': raise ValueError('sandbox_snapshot_required')
    page=snapshot.get('page')
    if not isinstance(page,dict): raise ValueError('sandbox_page_required')
    return page

def _safe_style(style):
    if not isinstance(style,dict): raise ValueError('candidate_style_object_required')
    out={}
    for k,v in style.items():
        if k not in SAFE_STYLE_KEYS: raise ValueError('candidate_style_not_allowed:'+str(k))
        if not isinstance(v,(str,int,float)): raise ValueError('candidate_style_value_invalid:'+str(k))
        out[k]=v
    return out

def validate_patch(patch):
    if not isinstance(patch,dict) or patch.get('schema')!='dore.design.candidate-patch.v1': raise ValueError('invalid_candidate_patch_schema')
    ops=patch.get('ops')
    if not isinstance(ops,list) or not ops or len(ops)>MAX_OPS: raise ValueError('invalid_candidate_patch_ops')
    for op in ops:
        if not isinstance(op,dict) or op.get('op') not in ALLOWED_OPS: raise ValueError('candidate_patch_op_not_allowed')
        kind=op['op']
        if kind=='add_node':
            node=op.get('node')
            if not isinstance(node,dict) or not str(node.get('id') or '').strip(): raise ValueError('candidate_add_node_required')
            if node.get('type') not in SAFE_NODE_TYPES: raise ValueError('candidate_node_type_not_allowed')
            for key in ('x','y','w','h'): _num(node.get(key),key)
            if float(node['w'])<=0 or float(node['h'])<=0: raise ValueError('candidate_patch_size_must_be_positive')
            if node.get('style') is not None: _safe_style(node['style'])
            continue
        if not str(op.get('node_id') or '').strip(): raise ValueError('candidate_patch_node_required')
        if kind=='move': _num(op.get('x'),'x');_num(op.get('y'),'y')
        elif kind=='resize':
            w=_num(op.get('w'),'w');h=_num(op.get('h'),'h')
            if w<=0 or h<=0: raise ValueError('candidate_patch_size_must_be_positive')
        elif kind=='font_size':
            size=_num(op.get('size'),'size')
            if not 6<=size<=320: raise ValueError('candidate_patch_font_size_out_of_range')
        elif kind=='text_align' and op.get('value') not in {'left','center','right'}: raise ValueError('candidate_patch_text_align_invalid')
        elif kind=='set_style': _safe_style(op.get('style'))
    return True

def apply_patch(snapshot,patch):
    validate_patch(patch);out=copy.deepcopy(snapshot);page=_page(out);nodes={str(n.get('id')):n for n in page.get('nodes') or [] if isinstance(n,dict)}
    for op in patch['ops']:
        kind=op['op']
        if kind=='add_node':
            node=copy.deepcopy(op['node']);nid=str(node['id'])
            if nid in nodes: raise ValueError('candidate_add_node_duplicate:'+nid)
            page.setdefault('nodes',[]).append(node);nodes[nid]=node;continue
        node=nodes.get(str(op['node_id']))
        if node is None: raise ValueError('candidate_patch_node_not_found:'+str(op['node_id']))
        if kind=='move': node['x'],node['y']=float(op['x']),float(op['y'])
        elif kind=='resize': node['w'],node['h']=float(op['w']),float(op['h'])
        elif kind=='font_size': node['size']=float(op['size'])
        elif kind=='text_align': node['text_align']=op['value']
        elif kind=='set_style': node['style']={**(node.get('style') or {}),**_safe_style(op['style'])}
    material={k:v for k,v in out.items() if k not in {'sha256','created_at'}}
    out['sha256']=hashlib.sha256(json.dumps(material,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest();return out

def geometry_evidence(snapshot):
    page=_page(snapshot);canvas=page.get('canvas') or {};cw=float(canvas.get('width',canvas.get('w',page.get('width',1440))) or 1440);ch=float(canvas.get('height',canvas.get('h',page.get('height',900))) or 900);rows=[]
    for node in page.get('nodes') or []:
        if not isinstance(node,dict): continue
        x=float(node.get('x',0) or 0);y=float(node.get('y',0) or 0);w=float(node.get('w',node.get('width',0)) or 0);h=float(node.get('h',node.get('height',0)) or 0)
        rows.append({'id':str(node.get('id') or ''),'type':str(node.get('type') or 'node'),'x':x,'y':y,'w':w,'h':h,'center_x_ratio':round((x+w/2)/cw,6) if cw else 0,'center_y_ratio':round((y+h/2)/ch,6) if ch else 0,'font_size':node.get('size'),'text_align':node.get('text_align'),'inside_canvas':x>=0 and y>=0 and x+w<=cw and y+h<=ch})
    return {'canvas':{'w':cw,'h':ch},'node_count':len(rows),'nodes':rows,'all_inside_canvas':all(r['inside_canvas'] for r in rows)}

def materialize(snapshot,patch,candidate_id):
    candidate=apply_patch(snapshot,patch);html=design2_renderer.render_snapshot(candidate,edit=False);evidence=geometry_evidence(candidate)
    return {'schema':'dore.design.sandbox-candidate.v1','candidate_id':str(candidate_id),'patch':copy.deepcopy(patch),'snapshot':candidate,'rendered_html':html,'render_sha256':hashlib.sha256(html.encode()).hexdigest(),'geometry':evidence,'canonical_workspace_mutated':False}
