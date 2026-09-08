import subprocess
from pathlib import Path

from dore_core.substrates.qmd import PRODUCTION_COLLECTION, production_config, search


def test_production_config_targets_admitted_collection_and_isolated_state():
    config = production_config()
    assert config.collection == PRODUCTION_COLLECTION == "dore-production"
    assert config.state_root is not None
    assert Path(config.state_root).name == "production"


def test_production_search_keeps_bm25_fast_path_and_collection_scope():
    seen = []

    def runner(argv):
        seen.append(argv)
        return subprocess.CompletedProcess(argv, 0, stdout='[{"title":"Matthew 6","uri":"docs/matthew.md"}]', stderr="")

    out = search("馬太福音", production_config(binary="/tmp/qmd"), runner=runner)
    assert out["ok"] is True
    assert out["lane"] == "bm25"
    assert out["collection"] == "dore-production"
    assert out["managed_state"] is True
    assert seen[0][1] == "search"
    assert "-c" in seen[0]
    assert seen[0][seen[0].index("-c") + 1] == "dore-production"
    assert "--no-rerank" not in seen[0]
