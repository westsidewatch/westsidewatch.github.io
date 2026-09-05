"""DORÉ DESIGN 2.0 validated document commands.

Pure document-coordinate operations. No DOM, shell, filesystem or publication side effects.
"""
import copy
import math

ALIGN = {'left', 'center', 'right'}
PATCH_KEYS = {'x', 'y', 'w', 'h', 'size', 'text_align'}


def _number(value, name, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f'invalid_number:{name}')
    if positive and value <= 0:
        raise ValueError(f'invalid_positive:{name}')
    return value


def _page(workspace, page_id):
    page = next((p for p in workspace.get('pages', []) if p.get('id') == page_id), None)
    if not page:
        raise ValueError('page_not_found')
    return page


def _node(page, node_id):
    node = next((n for n in page.get('nodes', []) if n.get('id') == node_id), None)
    if not node:
        raise ValueError('node_not_found')
    return node


def validate_patch(node, patch):
    if not isinstance(patch, dict) or not patch:
        raise ValueError('invalid_patch')
    unknown = set(patch) - PATCH_KEYS
    if unknown:
        raise ValueError('unsupported_patch:' + ','.join(sorted(unknown)))
    out = {}
    for key, value in patch.items():
        if key in {'x', 'y'}:
            out[key] = _number(value, key)
        elif key in {'w', 'h'}:
            out[key] = _number(value, key, positive=True)
        elif key == 'size':
            value = _number(value, key, positive=True)
            if value < 6 or value > 300:
                raise ValueError('font_size_out_of_range')
            out[key] = value
        elif key == 'text_align':
            if node.get('type') != 'text' or value not in ALIGN:
                raise ValueError('invalid_text_align')
            out[key] = value
    return out


def patch_node(workspace, page_id, node_id, patch):
    out = copy.deepcopy(workspace)
    page = _page(out, page_id)
    node = _node(page, node_id)
    node.update(validate_patch(node, patch))
    return out


def patch_many(workspace, page_id, patches):
    if not isinstance(patches, list) or not patches:
        raise ValueError('invalid_patches')
    out = copy.deepcopy(workspace)
    page = _page(out, page_id)
    # Validate all first so the operation is atomic.
    prepared = []
    seen = set()
    for item in patches:
        if not isinstance(item, dict) or not isinstance(item.get('id'), str) or item['id'] in seen:
            raise ValueError('invalid_patch_target')
        seen.add(item['id'])
        node = _node(page, item['id'])
        prepared.append((node, validate_patch(node, item.get('patch'))))
    for node, patch in prepared:
        node.update(patch)
    return out


def nudge(workspace, page_id, ids, dx, dy):
    dx = _number(dx, 'dx'); dy = _number(dy, 'dy')
    if not isinstance(ids, list) or not ids:
        raise ValueError('invalid_selection')
    return patch_many(workspace, page_id, [
        {'id': node_id, 'patch': {
            'x': _node(_page(workspace, page_id), node_id).get('x', 0) + dx,
            'y': _node(_page(workspace, page_id), node_id).get('y', 0) + dy,
        }} for node_id in ids
    ])


def apply(workspace, command):
    if not isinstance(command, dict):
        raise ValueError('invalid_command')
    op = command.get('op'); page_id = command.get('page_id')
    if op == 'node.patch':
        return patch_node(workspace, page_id, command.get('id'), command.get('patch'))
    if op == 'node.patch_many':
        return patch_many(workspace, page_id, command.get('patches'))
    if op == 'node.nudge':
        return nudge(workspace, page_id, command.get('ids'), command.get('dx', 0), command.get('dy', 0))
    raise ValueError('unsupported_design2_command')
