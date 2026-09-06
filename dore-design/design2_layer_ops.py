#!/usr/bin/env python3
"""Small Design 2.0 workspace operations kept native to Doré."""

def install(base):
    original=base.mutate
    def mutate(w,payload):
        if payload.get('op')!='reorder_node':
            return original(w,payload)
        pid=payload.get('page_id');nid=payload.get('id');index=payload.get('index')
        pg=base.page(w,pid) if pid else None
        if not pg: raise ValueError('page_not_found')
        nodes=pg.get('nodes',[])
        old=next((i for i,n in enumerate(nodes) if n.get('id')==nid),None)
        if old is None: raise ValueError('node_not_found')
        if not isinstance(index,int): raise ValueError('invalid_index')
        node=nodes.pop(old);index=max(0,min(index,len(nodes)));nodes.insert(index,node)
        pg['nodes']=nodes
        return base.save(w)
    base.mutate=mutate
