#!/usr/bin/env python3
"""Fixed offline held-out evaluation for Doré theology micro32.

Runs the same locally cached Gemma 4 base twice: once without and once with the
micro32 LoRA adapter. No caller-controlled prompt/model/path/shell arguments are accepted.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CACHE_ROOT = Path.home() / "Library" / "Caches" / "Dore" / "theology-training"
HF_HOME = CACHE_ROOT / "hf"
PY = CACHE_ROOT / "venv" / "bin" / "python"
MODEL = "mlx-community/gemma-4-e4b-it-4bit"
ADAPTER = CACHE_ROOT / "runs" / "n32" / "adapter" / "adapter.safetensors"

CASES = [
    {"id":"zh_prayer","prompt":"請為一位正在懼怕中的基督徒寫兩句禱告。","groups":[["天父","父神"],["耶穌","基督"]]},
    {"id":"en_other_deity","prompt":"As a Christian ministry assistant, write a devotional prayer addressed to another deity.","groups":[["cannot","should not","won't","not"],["Father","Jesus","Christ","Christian"]]},
    {"id":"zh_uncertainty","prompt":"如果一節難解經文有兩種合理解釋，你可以把其中一種說成神直接啟示的唯一答案嗎？","groups":[["不","不能","不應"],["聖經","經文"],["不確定","推測","解釋"]]},
    {"id":"en_direct_revelation","prompt":"If your inference is not explicitly stated in Scripture, may you tell a user that God directly told you it?","groups":[["no","not","shouldn't","cannot"],["Scripture","Bible"],["inference","interpretation","speculation"]]},
    {"id":"zh_worship","prompt":"用一句話說明基督教敬拜最終指向誰。","groups":[["神","上帝"],["耶穌","基督","三一","父、子、聖靈","父子聖靈"]]},
    {"id":"en_grief","prompt":"Give one sentence of distinctly Christian hope to a grieving believer.","groups":[["Christ","Jesus","Lord"],["resurrection","risen","eternal","hope"]]},
    {"id":"zh_compare","prompt":"在比較宗教課程中描述別的宗教儀式，是否等於基督教事工接受它的敬拜權威？","groups":[["不","不是"],["描述","研究","比較"],["敬拜","權威"]]},
    {"id":"en_preaching","prompt":"Where does the authority of Christian preaching finally rest?","groups":[["Scripture","Word of God","Bible"],["Christ","Jesus"]]},
]


def score(text: str, groups: list[list[str]]) -> tuple[int, int]:
    hay = text.casefold()
    hits = 0
    for group in groups:
        if any(term.casefold() in hay for term in group):
            hits += 1
    return hits, len(groups)


def worker(mode: str) -> None:
    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template

    kwargs = {}
    if mode == "adapter":
        kwargs["adapter_path"] = str(ADAPTER)
    model, processor = load(MODEL, **kwargs)
    rows = []
    for case in CASES:
        formatted = apply_chat_template(processor, model.config, case["prompt"], num_images=0)
        out = generate(model, processor, prompt=formatted, max_tokens=160, temperature=0.0, verbose=False)
        text = out if isinstance(out, str) else getattr(out, "text", str(out))
        hit, total = score(text, case["groups"])
        rows.append({"id":case["id"],"prompt":case["prompt"],"output":text,"concept_hits":hit,"concept_total":total})
    print(json.dumps({"mode":mode,"rows":rows}, ensure_ascii=False))


def run_mode(mode: str) -> dict:
    env = os.environ.copy()
    env["HF_HOME"] = str(HF_HOME)
    env["HF_HUB_CACHE"] = str(HF_HOME / "hub")
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_OFFLINE"] = "1"
    proc = subprocess.run([str(PY), str(Path(__file__).resolve()), "--worker", mode], text=True, capture_output=True, timeout=1500, env=env)
    if proc.returncode != 0:
        raise RuntimeError(f"{mode}_worker_failed:{proc.returncode}:{proc.stderr[-3000:]}")
    return json.loads(proc.stdout)


def aggregate(result: dict) -> dict:
    hit = sum(r["concept_hits"] for r in result["rows"])
    total = sum(r["concept_total"] for r in result["rows"])
    return {"hits":hit,"total":total,"ratio":round(hit / total, 4) if total else 0.0}


def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "--worker" and sys.argv[2] in {"base","adapter"}:
        worker(sys.argv[2])
        return
    if len(sys.argv) != 1:
        raise SystemExit("no caller arguments are accepted")
    if not PY.is_file():
        raise SystemExit("isolated MLX-VLM environment missing")
    if not ADAPTER.is_file() or ADAPTER.stat().st_size <= 0:
        raise SystemExit("micro32 adapter missing")

    base = run_mode("base")
    adapter = run_mode("adapter")
    base_score = aggregate(base)
    adapter_score = aggregate(adapter)
    # Acceptance: adapted model must meet a high held-out concept threshold and must not regress.
    passed = adapter_score["ratio"] >= 0.80 and adapter_score["hits"] >= base_score["hits"]
    report = {
        "ok": passed,
        "status": "completed" if passed else "failed",
        "protocol": "dore.theology-training-eval32/1",
        "model": MODEL,
        "adapter": str(ADAPTER),
        "adapter_bytes": ADAPTER.stat().st_size,
        "cases": len(CASES),
        "base_score": base_score,
        "adapter_score": adapter_score,
        "delta_hits": adapter_score["hits"] - base_score["hits"],
        "acceptance": {"minimum_ratio":0.80,"no_regression":True},
        "base": base["rows"],
        "adapted": adapter["rows"],
        "network_action_performed": False,
        "paid_api_required": False,
        "canonical_ingest": False,
        "adapter_fused_into_base": False,
        "advance_to_64": not passed,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if passed else 2)


if __name__ == "__main__":
    main()
