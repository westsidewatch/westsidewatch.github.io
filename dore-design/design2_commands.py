"""Command dispatcher for DORÉ DESIGN 2.0."""
import copy
import design2_patch,design2_align

def _page(workspace,page_id):
    page=next((p for p in workspace.get('pages',[]) if p.get('id')==page_id),None)
    if page is None:raise ValueError('page_not_found')
    return page

def _node(page,node_id):
    node=next((n for n in page.get('nodes',[]) if n.get('id')==node_id),None)
    if node is None:raise ValueError('node_not_found')
    return node

def apply(workspace,command):
    if not isinstance(command,dict):raise ValueError('invalid_command')
    op=command.get('op');page_id=command.get('page_id')
    if op=='node.patch':return design2_patch.apply(workspace,page_id,command.get('id'),command.get('patch'))
    if op=='node.patch_many':
        out=workspace
        patches=command.get('patches') or []
        if not patches:raise ValueError('invalid_patches')
        for item in patches:out=design2_patch.apply(out,page_id,item.get('id'),item.get('patch'))
        return out
    if op=='node.align':return design2_align.align(workspace,page_id,command.get('ids') or [],command.get('edge'))
    if op=='node.distribute':return design2_align.distribute(workspace,page_id,command.get('ids') or [],command.get('axis'))
    out=copy.deepcopy(workspace);page=_page(out,page_id)
    if op=='node.text':
        node=_node(page,command.get('id'));text=command.get('text')
        if node.get('type')!='text' or not isinstance(text,str):raise ValueError('invalid_text')
        node['text']=text;return out
    if op=='node.nudge':
        ids=command.get('ids') or []
        if not ids:raise ValueError('invalid_selection')
        dx=command.get('dx',0);dy=command.get('dy',0)
        for node_id in ids:
            node=_node(page,node_id);node['x']=node.get('x',0)+dx;node['y']=node.get('y',0)+dy
        return out
    raise ValueError('unsupported_design2_command')
