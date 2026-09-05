"""DORÉ DESIGN 2.0 validated document commands."""
import copy,math
ALIGN={'left','center','right'};PATCH_KEYS={'x','y','w','h','size','text_align'}
def _number(v,n,positive=False):
    if isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v):raise ValueError(f'invalid_number:{n}')
    if positive and v<=0:raise ValueError(f'invalid_positive:{n}')
    return v
def _page(w,pid):
    p=next((p for p in w.get('pages',[]) if p.get('id')==pid),None)
    if not p:raise ValueError('page_not_found')
    return p
def _node(p,nid):
    n=next((n for n in p.get('nodes',[]) if n.get('id')==nid),None)
    if not n:raise ValueError('node_not_found')
    return n
def _box(n):return(float(n.get('x',0)),float(n.get('y',0)),float(n.get('w',0)),float(n.get('h') or 0))
def validate_patch(n,p):
    if not isinstance(p,dict) or not p:raise ValueError('invalid_patch')
    u=set(p)-PATCH_KEYS
    if u:raise ValueError('unsupported_patch:'+','.join(sorted(u)))
    out={}
    for k,v in p.items():
        if k in {'x','y'}:out[k]=_number(v,k)
        elif k in {'w','h'}:out[k]=_number(v,k,True)
        elif k=='size':
            v=_number(v,k,True)
            if not 6<=v<=300:raise ValueError('font_size_out_of_range')
            out[k]=v
        elif k=='text_align':
            if n.get('type')!='text' or v not in ALIGN:raise ValueError('invalid_text_align')
            out[k]=v
    return out
def patch_node(w,pid,nid,p):
    out=copy.deepcopy(w);n=_node(_page(out,pid),nid);n.update(validate_patch(n,p));return out
def patch_many(w,pid,ps):
    if not isinstance(ps,list) or not ps:raise ValueError('invalid_patches')
    out=copy.deepcopy(w);page=_page(out,pid);prepared=[];seen=set()
    for item in ps:
        if not isinstance(item,dict) or not isinstance(item.get('id'),str) or item['id'] in seen:raise ValueError('invalid_patch_target')
        seen.add(item['id']);n=_node(page,item['id']);prepared.append((n,validate_patch(n,item.get('patch'))))
    for n,p in prepared:n.update(p)
    return out
def set_text(w,pid,nid,text):
    if not isinstance(text,str):raise ValueError('invalid_text')
    if len(text)>200000:raise ValueError('text_too_large')
    out=copy.deepcopy(w);n=_node(_page(out,pid),nid)
    if n.get('type')!='text':raise ValueError('not_text_node')
    n['text']=text
    return out
def nudge(w,pid,ids,dx,dy):
    dx=_number(dx,'dx');dy=_number(dy,'dy');page=_page(w,pid)
    if not isinstance(ids,list) or not ids:raise ValueError('invalid_selection')
    return patch_many(w,pid,[{'id':i,'patch':{'x':_node(page,i).get('x',0)+dx,'y':_node(page,i).get('y',0)+dy}} for i in ids])
def align_nodes(w,pid,ids,edge):
    if edge not in {'left','center','right','top','middle','bottom'}:raise ValueError('invalid_alignment')
    if not isinstance(ids,list) or len(ids)<2:raise ValueError('selection_requires_two')
    page=_page(w,pid);ns=[_node(page,i) for i in ids];bs=[_box(n) for n in ns];L=min(x for x,y,a,b in bs);R=max(x+a for x,y,a,b in bs);T=min(y for x,y,a,b in bs);B=max(y+b for x,y,a,b in bs);ps=[]
    for n,(x,y,a,b) in zip(ns,bs):
        p={'x':L} if edge=='left' else {'x':(L+R-a)/2} if edge=='center' else {'x':R-a} if edge=='right' else {'y':T} if edge=='top' else {'y':(T+B-b)/2} if edge=='middle' else {'y':B-b};ps.append({'id':n['id'],'patch':p})
    return patch_many(w,pid,ps)
def distribute(w,pid,ids,axis):
    if axis not in {'horizontal','vertical'}:raise ValueError('invalid_distribution')
    if not isinstance(ids,list) or len(ids)<3:raise ValueError('distribution_requires_three')
    page=_page(w,pid);ns=[_node(page,i) for i in ids];key=(lambda n:_box(n)[0]) if axis=='horizontal' else(lambda n:_box(n)[1]);ns.sort(key=key);boxes=[_box(n) for n in ns];ps=[]
    if axis=='horizontal':
        start=boxes[0][0];end=boxes[-1][0]+boxes[-1][2];gap=(end-start-sum(b[2] for b in boxes))/(len(ns)-1);cursor=start
        for n,b in zip(ns,boxes):ps.append({'id':n['id'],'patch':{'x':cursor}});cursor+=b[2]+gap
    else:
        start=boxes[0][1];end=boxes[-1][1]+boxes[-1][3];gap=(end-start-sum(b[3] for b in boxes))/(len(ns)-1);cursor=start
        for n,b in zip(ns,boxes):ps.append({'id':n['id'],'patch':{'y':cursor}});cursor+=b[3]+gap
    return patch_many(w,pid,ps)
def apply(w,c):
    if not isinstance(c,dict):raise ValueError('invalid_command')
    op=c.get('op');pid=c.get('page_id')
    if op=='node.patch':return patch_node(w,pid,c.get('id'),c.get('patch'))
    if op=='node.patch_many':return patch_many(w,pid,c.get('patches'))
    if op=='node.text':return set_text(w,pid,c.get('id'),c.get('text'))
    if op=='node.nudge':return nudge(w,pid,c.get('ids'),c.get('dx',0),c.get('dy',0))
    if op=='node.align':return align_nodes(w,pid,c.get('ids'),c.get('edge'))
    if op=='node.distribute':return distribute(w,pid,c.get('ids'),c.get('axis'))
    raise ValueError('unsupported_design2_command')
