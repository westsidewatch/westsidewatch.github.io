"""Multi-selection geometry primitives for DORÉ DESIGN 2.0."""
import copy

def _nodes(workspace,page_id,ids):
    page=next((p for p in workspace.get('pages',[]) if p.get('id')==page_id),None)
    if page is None:raise ValueError('page_not_found')
    found=[]
    for node_id in ids:
        node=next((n for n in page.get('nodes',[]) if n.get('id')==node_id),None)
        if node is None:raise ValueError('node_not_found')
        found.append(node)
    return found

def align(workspace,page_id,ids,edge):
    if len(ids)<2 or edge not in {'left','center','right','top','middle','bottom'}:raise ValueError('invalid_alignment')
    out=copy.deepcopy(workspace);nodes=_nodes(out,page_id,ids)
    left=min(n.get('x',0) for n in nodes);top=min(n.get('y',0) for n in nodes)
    right=max(n.get('x',0)+n.get('w',0) for n in nodes);bottom=max(n.get('y',0)+n.get('h',0) for n in nodes)
    for node in nodes:
        if edge=='left':node['x']=left
        elif edge=='right':node['x']=right-node.get('w',0)
        elif edge=='center':node['x']=(left+right-node.get('w',0))/2
        elif edge=='top':node['y']=top
        elif edge=='bottom':node['y']=bottom-node.get('h',0)
        else:node['y']=(top+bottom-node.get('h',0))/2
    return out

def distribute(workspace,page_id,ids,axis):
    if len(ids)<3 or axis not in {'horizontal','vertical'}:raise ValueError('invalid_distribution')
    out=copy.deepcopy(workspace);nodes=_nodes(out,page_id,ids)
    key='x' if axis=='horizontal' else 'y';size='w' if axis=='horizontal' else 'h'
    nodes.sort(key=lambda n:n.get(key,0));start=nodes[0].get(key,0)
    end=nodes[-1].get(key,0)+nodes[-1].get(size,0)
    gap=(end-start-sum(n.get(size,0) for n in nodes))/(len(nodes)-1);cursor=start
    for node in nodes:
        node[key]=cursor;cursor+=node.get(size,0)+gap
    return out
