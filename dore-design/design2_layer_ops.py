#!/usr/bin/env python3
"""Small Design 2.0 workspace operations kept native to Doré."""

def install(base):
    original=base.mutate
    def mutate(w,payload):
        op=payload.get('op')
        if op not in {'reorder_node','align_nodes','group_nodes','ungroup_nodes'}:
            return original(w,payload)
        pid=payload.get('page_id');pg=base.page(w,pid) if pid else None
        if not pg: raise ValueError('page_not_found')
        nodes=pg.get('nodes',[])
        if op=='reorder_node':
            nid=payload.get('id');index=payload.get('index')
            old=next((i for i,n in enumerate(nodes) if n.get('id')==nid),None)
            if old is None: raise ValueError('node_not_found')
            if not isinstance(index,int): raise ValueError('invalid_index')
            node=nodes.pop(old);index=max(0,min(index,len(nodes)));nodes.insert(index,node);pg['nodes']=nodes
            return base.save(w)
        ids=[x for x in (payload.get('ids') or []) if isinstance(x,str)]
        chosen=[n for n in nodes if n.get('id') in ids]
        if not chosen: raise ValueError('nodes_not_found')
        if op=='group_nodes':
            gid=str(payload.get('group_id') or ('group-'+chosen[0].get('id','selection')))[:80]
            for n in chosen:n['group_id']=gid
            return base.save(w)
        if op=='ungroup_nodes':
            for n in chosen:n.pop('group_id',None)
            return base.save(w)
        mode=payload.get('mode');cw=(pg.get('canvas') or {}).get('w',1200);ch=(pg.get('canvas') or {}).get('h',930)
        left=min(n.get('x',0) for n in chosen);right=max(n.get('x',0)+n.get('w',0) for n in chosen);top=min(n.get('y',0) for n in chosen);bottom=max(n.get('y',0)+n.get('h',0) for n in chosen)
        for n in chosen:
            if mode=='left':n['x']=left
            elif mode=='center':n['x']=(cw-n.get('w',0))/2
            elif mode=='right':n['x']=right-n.get('w',0)
            elif mode=='top':n['y']=top
            elif mode=='middle':n['y']=(ch-n.get('h',0))/2
            elif mode=='bottom':n['y']=bottom-n.get('h',0)
            else: raise ValueError('invalid_alignment')
        return base.save(w)
    base.mutate=mutate
