#!/usr/bin/env python3
"""Small Design 2.0 workspace operations kept native to Doré."""

def install(base):
    original=base.mutate
    def mutate(w,payload):
        op=payload.get('op')
        native=('reorder_node','reorder_nodes','batch_set_nodes','align_nodes','group_nodes','ungroup_nodes','distribute_nodes','stack_nodes','center_nodes','add_frame','set_asset')
        if op not in native:return original(w,payload)
        pid=payload.get('page_id');pg=base.page(w,pid) if pid else None
        if not pg:raise ValueError('page_not_found')
        nodes=pg.get('nodes',[])
        if op=='batch_set_nodes':
            patches=payload.get('patches') or []
            byid={n.get('id'):n for n in nodes}
            safe=('x','y','w','h','hidden','locked','group_id','fit','crop_x','crop_y','font_family','font_size','font_weight','color','line_height','letter_spacing','text_align')
            for item in patches:
                n=byid.get(item.get('id'));patch=item.get('patch') or {}
                if not n:raise ValueError('node_not_found')
                n.update({k:v for k,v in patch.items() if k in safe})
            return base.save(w)
        if op=='reorder_nodes':
            order=payload.get('order') or [];byid={n.get('id'):n for n in nodes}
            if set(order)!=set(byid):raise ValueError('invalid_node_order')
            pg['nodes']=[byid[i] for i in order];return base.save(w)
        if op=='add_frame':
            used={n.get('id') for n in nodes};base_id=str(payload.get('id') or 'frame');nid=base_id;i=1
            while nid in used:i+=1;nid=f'{base_id}-{i}'
            nodes.append({'id':nid,'type':'frame','role':'frame','x':float(payload.get('x',120)),'y':float(payload.get('y',180)),'w':float(payload.get('w',960)),'h':float(payload.get('h',540)),'frame_fill':'transparent','frame_stroke':'#b49a55'});return base.save(w)
        if op=='set_asset':
            aid=payload.get('asset_id');patch=payload.get('patch') or {};assets=w.setdefault('assets',{})
            if not aid or aid not in assets:raise ValueError('asset_not_found')
            assets[aid].update({k:v for k,v in patch.items() if k in ('uri','name','mime','sha256','path')});return base.save(w)
        if op=='reorder_node':
            nid=payload.get('id');index=payload.get('index');old=next((i for i,n in enumerate(nodes) if n.get('id')==nid),None)
            if old is None:raise ValueError('node_not_found')
            if not isinstance(index,int):raise ValueError('invalid_index')
            node=nodes.pop(old);nodes.insert(max(0,min(index,len(nodes))),node);return base.save(w)
        ids=[x for x in payload.get('ids',[]) if isinstance(x,str)];chosen=[n for n in nodes if n.get('id') in ids]
        if not chosen:raise ValueError('nodes_not_found')
        if op=='group_nodes':
            gid=payload.get('group_id') or 'group'
            for n in chosen:n['group_id']=gid
        elif op=='ungroup_nodes':
            for n in chosen:n.pop('group_id',None)
        elif op=='align_nodes':
            mode=payload.get('mode');xs=[float(n.get('x',0)) for n in chosen];ys=[float(n.get('y',0)) for n in chosen];rs=[float(n.get('x',0))+float(n.get('w',0)) for n in chosen];bs=[float(n.get('y',0))+float(n.get('h',0)) for n in chosen]
            for n in chosen:
                nw=float(n.get('w',0));nh=float(n.get('h',0))
                if mode=='left':n['x']=min(xs)
                elif mode=='center':n['x']=(min(xs)+max(rs)-nw)/2
                elif mode=='right':n['x']=max(rs)-nw
                elif mode=='top':n['y']=min(ys)
                elif mode=='middle':n['y']=(min(ys)+max(bs)-nh)/2
                elif mode=='bottom':n['y']=max(bs)-nh
                else:raise ValueError('invalid_alignment')
        elif op=='center_nodes':
            mode=payload.get('mode');cw=float(payload.get('canvas_w',1200));ch=float(payload.get('canvas_h',2280))
            for n in chosen:
                if mode in ('canvas-x','canvas-both'):n['x']=(cw-float(n.get('w',0)))/2
                if mode in ('canvas-y','canvas-both'):n['y']=(ch-float(n.get('h',0)))/2
        elif op=='distribute_nodes':
            mode=payload.get('mode')
            if len(chosen)<3:raise ValueError('distribution_requires_three_nodes')
            axis='x' if mode=='horizontal' else 'y' if mode=='vertical' else None;size='w' if axis=='x' else 'h'
            if not axis:raise ValueError('invalid_distribution')
            ordered=sorted(chosen,key=lambda n:float(n.get(axis,0)));start=float(ordered[0].get(axis,0));end=float(ordered[-1].get(axis,0))+float(ordered[-1].get(size,0));gap=(end-start-sum(float(n.get(size,0)) for n in ordered))/(len(ordered)-1);pos=start
            for n in ordered:n[axis]=pos;pos+=float(n.get(size,0))+gap
        elif op=='stack_nodes':
            mode=payload.get('mode');axis='x' if mode=='horizontal' else 'y' if mode=='vertical' else None;size='w' if axis=='x' else 'h';gap=float(payload.get('gap',24))
            if not axis:raise ValueError('invalid_stack')
            ordered=sorted(chosen,key=lambda n:float(n.get(axis,0)));pos=float(ordered[0].get(axis,0))
            for n in ordered:n[axis]=pos;pos+=float(n.get(size,0))+gap
        return base.save(w)
    base.mutate=mutate
