"""Staging manifest and allowlisted publication targets for DORÉ DESIGN 2.0."""
import hashlib
import design2_checks

ALLOWED_TARGETS={
    'multiwrite-home':'multiwrite-home',
    'homepage':'homepage',
    'journal-vol-00':'journal-vol-00',
}


def resolve_target(page_id,target):
    expected=ALLOWED_TARGETS.get(page_id)
    if not expected or target!=expected: raise ValueError('publish_target_not_allowed')
    return expected


def build_manifest(candidate,target,rendered_html):
    snap=candidate.get('snapshot') or {}
    resolve_target(snap.get('page_id'),target)
    checks=design2_checks.require(snap,rendered_html)
    html_hash=hashlib.sha256(rendered_html.encode('utf-8')).hexdigest()
    return {
        'schema':'dore.design.staging-manifest.v1',
        'candidate_id':candidate.get('id'),
        'page_id':snap.get('page_id'),
        'revision':snap.get('revision'),
        'snapshot_sha256':snap.get('sha256'),
        'target':target,
        'render_sha256':html_hash,
        'checks':checks,
    }


def same_render(manifest,rendered_html):
    return manifest.get('render_sha256')==hashlib.sha256(rendered_html.encode('utf-8')).hexdigest()
