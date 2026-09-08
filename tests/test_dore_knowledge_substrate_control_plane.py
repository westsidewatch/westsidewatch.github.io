from __future__ import annotations
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/'local'/'dore-local'/'production_actions.py'
spec=importlib.util.spec_from_file_location('dore_production_actions',PATH)
assert spec and spec.loader
production=importlib.util.module_from_spec(spec);spec.loader.exec_module(production)


def test_native_control_plane_exposes_knowledge_substrate_install():
    assert 'knowledge.substrates.install' in production.CAPABILITIES


def test_knowledge_install_is_bounded_to_dore_owned_installer(monkeypatch,tmp_path):
    repo=tmp_path/'repo'; script=repo/'local'/'dore-local'/'install-knowledge-substrates-macos.sh'
    script.parent.mkdir(parents=True); script.write_text('#!/bin/bash\n',encoding='utf-8')
    monkeypatch.setattr(production,'_repo',lambda:repo)
    monkeypatch.setattr(production,'_sync',lambda _repo:None)
    def fake_run(argv,cwd=None,timeout=120,env=None):
        if argv[:2]==['git','rev-parse']:
            return {'argv':argv,'returncode':0,'stdout':'abc123\n','stderr':''}
        assert argv==['bash',str(script)]
        return {'argv':argv,'returncode':0,'stdout':'{"ok":true,"offline_core":true,"authority":false}\n','stderr':''}
    monkeypatch.setattr(production,'_run',fake_run)
    out=production.knowledge_substrates_install({})
    assert out['ok'] is True
    assert out['capability']=='knowledge.substrates.install'
    assert out['evidence']['authority'] is False
