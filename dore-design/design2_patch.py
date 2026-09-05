"""Validated element patch primitive for DORÉ DESIGN 2.0."""
import copy
ALLOWED={'x','y','w','h','size','text_align'}
def apply(workspace,page_id,node_id,patch):
    if not isinstance(patch,dict) or not patch or set(patch)-ALLOWED:raise ValueError('invalid_patch')
    out=copy.deepcopy(workspace)
    page=next((p for p in out.get('pages',[]) if p.get('id')==page_id),None)
    if page is None:raise ValueError('page_not_found')
    node=next((n for n in page.get('nodes',[]) if n.get('id')==node_id),None)
    if node is None:raise ValueError('node_not_found')
    for key,value in patch.items():
        if key=='text_align':
            if node.get('type')!='text' or value not in {'left','center','right'}:raise ValueError('invalid_text_align')
        else:
            if isinstance(value,bool) or not isinstance(value,(int,float)):raise ValueError('invalid_number')
            if key in {'w','h','size'} and value<=0:raise ValueError('invalid_positive')
        node[key]=value
    return out
