#!/usr/bin/env python3
"""Small Design 2.0 workspace operations kept native to Doré."""

def install(base):
    original=base.mutate
    def mutate(w,payload):
        op=payload.get('op')
        if op not in ('reorder_node','align_nodes','group_nodes','ungroup_nodes','distribute_nodes','stack_nodes','center_nodes'):
            return original(w,payload)
        pid=payload.get('page_id');pg=base.page(w,pid) if pid else None
        if not pg: raise ValueError('page_not_found')
        nodes=pg.get('nodes',[])
        if op=='reorder_node':
            nid=payload.get('id');index=payload.get('index');old=next((i for i,n in enumerate(nodes) if n.get('id')==nid),None)
            if old is None: raise ValueError('node_not_found')
            if not isinstance(index,int): raise ValueError('invalid_index')
            node=nodes.pop(old);index=max(0,min(index,len(nodes)));nodes.insert(index,node);pg['nodes']=nodes;return base.save(w)
        ids=[x for x in payload.get('ids',[]) if isinstance(x,str)];chosen=[n for n in nodes if n.get('id') in ids]
        if not chosen: raise ValueError('nodes_not_found')
        if op=='group_nodes':
            gid=payload.get('group_id') or 'group';
            for n in chosen:n['group_id']=gid
        elif op=='ungroup_nodes':
            for n in chosen:n.pop('group_id',None)
        elif op=='align_nodes':
            mode=payload.get('mode');xs=[float(n.get('x',0)) for n in chosen];ys=[float(n.get('y',0)) for n in chosen];rights=[float(n.get('x',0))+float(n.get('w',0)) for n in chosen];bottoms=[float(n.get('y',0))+float(n.get('h',0)) for n in chosen]
            for n in chosen:
                w0=float(n.get('w',0));h0=float(n.get('h',0))
                if mode=='left':n['x']=min(xs)
                elif mode=='center':n['x']=(min(xs)+max(rights)-w0)/2
                elif mode=='right':n['x']=max(rights)-w0
                elif mode=='top':n['y']=min(ys)
                elif mode=='middle':n['y']=(min(ys)+max(bottoms)-h0)/2
                elif mode=='bottom':n['y']=max(bottoms)-h0
                else:raise ValueError('invalid_alignment')
        elif op=='center_nodes':
            mode=payload.get('mode');canvas_w=float(payload.get('canvas_w',1200));canvas_h=float(payload.get('canvas_h',2280))
            for n in chosen:
                if mode in ('canvas-x','canvas-both'):n['x']=(canvas_w-float(n.get('w',0)))/2
                if mode in ('canvas-y','canvas-both'):n['y']=(canvas_h-float(n.get('h',0)))/2
        elif op=='distribute_nodes':
            mode=payload.get('mode')
            if len(chosen)<3: raise ValueError('distribution_requires_three_nodes')
            if mode=='horizontal':
                ordered=sorted(chosen,key=lambda n:float(n.get('x',0)));start=float(ordered[0].get('x',0));end=float(ordered[-1].get('x',0))+float(ordered[-1].get('w',0));total=sum(float(n.get('w',0)) for n in ordered);gap=(end-start-total)/(len(ordered)-1);pos=start
                for n in ordered:n['x']=pos;pos+=float(n.get('w',0))+gap
            elif mode=='vertical':
                ordered=sorted(chosen,key=lambda n:float(n.get('y',0)));start=float(ordered[0].get('y',0));end=float(ordered[-1].get('y',0))+float(ordered[-1].get('h',0));total=sum(float(n.get('h',0)) for n in ordered);gap=(end-start-total)/(len(ordered)-1);pos=start
                for n in ordered:n['y']=pos;pos+=float(n.get('h',0))+gap
            else:raise ValueError('invalid_distribution')
        elif op=='stack_nodes':
            mode=payload.get('mode');gap=float(payload.get('gap',24));ordered=sorted(chosen,key=lambda n:float(n.get('x' if mode=='horizontal' else 'y',0)))
            if mode=='horizontal':
                pos=float(ordered[0].get('x',0))
                for n in ordered:n['x']=pos;pos+=float(n.get('w',0))+gap
            elif mode=='vertical':
                pos=float(ordered[0].get('y',0))
                for n in ordered:n['y']=pos;pos+=float(n.get('h',0))+gap
            else:raise ValueError('invalid_stack')
        return base.save(w)
    base.mutate=mutate
