#!/usr/bin/env python3
"""Bounded, failure-domain-specific repair planning for Doré Design.

Repairs are intentionally narrow: fix the proven failure domain without
re-generating the whole composition. Domains that cannot be safely repaired
with the current executable patch DSL fall back to regeneration.
"""
from __future__ import annotations

MAX_REPAIR_ATTEMPTS = 2

REPAIRABLE = {
    'vertical-gravity': ('move',),
    'focal-competition': ('move', 'resize', 'font_size'),
    'text-density': ('resize', 'font_size'),
    'alignment-drift': ('move', 'text_align'),
    'spacing-rhythm': ('move', 'resize'),
    'scale-hierarchy': ('resize', 'font_size'),
    'edge-crowding': ('move', 'resize'),
    'image-text-balance': ('move', 'resize'),
}

UNREPAIRABLE_WITH_CURRENT_DSL = {'contrast-hierarchy'}


def repair_contract(domains: list[str]) -> dict:
    normalized=[]
    for value in domains or []:
        domain=str(value or '').strip()
        if domain and domain not in normalized:
            normalized.append(domain)
    repairable={d:list(REPAIRABLE[d]) for d in normalized if d in REPAIRABLE}
    fallback=[d for d in normalized if d not in REPAIRABLE]
    return {
        'policy':'minimal-domain-repair-v1',
        'domains':normalized,
        'repairable':repairable,
        'fallback_regeneration_domains':fallback,
        'repair_possible':bool(repairable) and not bool(fallback),
        'max_repair_attempts':MAX_REPAIR_ATTEMPTS,
        'preserve_unaffected_structure':True,
        'production_mutation_allowed':False,
    }


def validate_repair_ops(domains: list[str], patch: dict) -> dict:
    contract=repair_contract(domains)
    if not contract['repair_possible']:
        return {**contract,'ok':False,'reason':'domain_requires_regeneration'}
    ops=(patch or {}).get('ops') or []
    if not isinstance(ops,list) or not ops:
        return {**contract,'ok':False,'reason':'repair_patch_ops_required'}
    allowed=set()
    for values in contract['repairable'].values():
        allowed.update(values)
    seen=[]
    for op in ops:
        name=str((op or {}).get('op') or '').strip()
        if name not in allowed:
            return {**contract,'ok':False,'reason':'repair_op_outside_failure_domain','invalid_op':name,'allowed_ops':sorted(allowed)}
        seen.append(name)
    return {**contract,'ok':True,'used_ops':seen,'allowed_ops':sorted(allowed)}
